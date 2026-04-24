import json

from fastapi import Response
import requests

from ehr_ai_core.chunkers.chunk_formats import check_chunk_format, get_chunk_prompt
from ehr_ai_core.context import context_builder, join_object
from ehr_ai_core.error.app_error import AppError
from services.tools.Itool import ITool
from services.utils.utils import dict_diff, format_changes

from .llm_factory import createLLm, createOllamaStreaming

class EHRAgent:
    """
    Handles clinicians questions through use of context and llm response 
    """
    __tools:dict[str, ITool] = {}
    __llm = None
    __ollama = None

    def __build_prompt(self, data:dict , context: str):

        if 'pending_action_id' in data:
            return f"""
                - Your only task is convert the following into ONE short confirmation request sentence.
                - Ensure response in {data['language']}
                - Avoid genering extra tokens
                

                modification context:
                {context}

                Output:
                Doctor {data['doctor']}, this action needs your confirmation fist.
                """
        elif 'action_done' in data:
            return f"""
                Notify changes where successfully done. 
                - Ensure response in {data['language']}
                Query: {data['query']}
                Changes: {context}
            """
        else: 
             return f"""
                    You are a medical assistant.
                    - Ensure response in {data['language']}
                    - If not in context, say you don't know
                    - Answer only using provided context
                    - Mention source polite and briefly
                    - if possible use markdown style
                    
                    Context: {context}

                    Query: {data['query']}
                   """
            

    def __init__(self, provider:str, model:str, max_tokens:str, url:str):
        if(provider=="ollama"):
            self.__ollama = createOllamaStreaming(model, url)
        else:
            self.__llm = createLLm(provider, model, max_tokens)

    def __ollama_call(self, prompt: str) -> str:
        try:
            response = requests.post(
                self.__ollama['url'],
                json={
                    "model": self.__ollama["model"],
                    "prompt": prompt,
                    "stream": False,

                },
                timeout=60
            )

            response.raise_for_status()
            return response.json()["response"]

        except requests.RequestException as e:
            raise AppError(f"Request failed: {e}", 500)
        

    def __ollama_stream(self, prompt: str, strict:bool = False):
        try:
            options = {
                "temperature": 0.1,
                "top_p": 0.6,
                "repeat_penalty": 1.1,
            }

            if strict:
                options["stop"]: ["\n"] 

            response = requests.post(
                self.__ollama['url'],
                json={
                    "model": self.__ollama["model"],
                    "prompt": prompt,
                    "stream": True,
                    "options": options
                },
                stream=True,
                timeout=60
            )

            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        yield data.get("response", "")
                    except json.JSONDecodeError:
                        continue

        except requests.RequestException as e:
            raise AppError(f"Streaming request failed: {e}", 500)
        

    def __llm_json_call(self,prompt:str, chunk_type:str, max_retries:int = 3):
        for _ in range(max_retries):
            raw = self.__ollama_call(prompt)

            data = self.safe_parse_json(raw)

            if data is None:
                to = raw.find('{')
                deleting_text = raw[to:]
                data = self.safe_parse_json(deleting_text)
                if data is None:
                    continue

            check = check_chunk_format(data, chunk_type)

            if check["valid"]:
                return data
            else:
                return check
            

        raise AppError("Failed to generate valid structured output", 500)
        
    def safe_parse_json(self, text: str):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    def classify(self, query:str):
        prompt = f"""
        Classify the medical query into one intent:
        - get_info → retrieving existing patient data
        - update_info → modifying or adding patient data
        - execute_action -> afirmative or positive permision query 
        - OOC answer → out of context query

        Return ONLY JSON:
        {get_chunk_prompt("intent")}

        Query: {query}
        """
        return self.__llm_json_call(prompt=prompt, chunk_type="intent")
        

    def add_tool(self, tool:ITool):
        self.__tools[tool.name] = tool

    def call_tool(self, name:str) -> ITool:
        if name in self.__tools:
            return self.__tools[name]
        raise AppError("Undefined Tool", 500)

    def Streaming_Prediction(self, data: dict, context: str, strict:bool = False):

        if not self.__ollama:
            raise AppError("Ollama not initialized", 409)
        
        prompt = self.__build_prompt(data=data,context= context)
        
        return self.__ollama_stream(prompt = prompt, strict = strict)


    def todo_feature_streaming(self, feature_name:str):
        prompt = f"Notify that {feature_name} action can be perform, due to it isn't implemented"
        return self.__ollama_stream(prompt=prompt)
    
    def guide_modification(self, query:str):
        schema = "guide_modification"
        structure = get_chunk_prompt(schema)

        prompt = f"""
            Extract structured update instructions from the query.
            - Avoid explanations
            Return ONLY JSON:

            {structure}

            Query: {query}
            """
        return self.__llm_json_call(prompt=prompt, chunk_type=schema)
    

    def extract_information(self, query:str, schema:str, current:str|None):
        structure = get_chunk_prompt(schema)
        prompt = f"""You are a JSON generator.
        
                Return ONLY valid JSON. Do NOT include:
                - explanations
                - text
                - comments
                - markdown

                Output must start with '{{' or '[' and end with '}}' or ']'.

                Structure:
            {structure}

        query: {query}
        """
        if current:
            prompt += f"\nCurrent info: {current}"

        return self.__llm_json_call(prompt=prompt, chunk_type=schema)


    def information_response(self, data:dict):
        patientId = data["patientId"]
        context = f"[User: {data['doctor']}]\n"

        yield { "chunk": "Collecting information", "thinking": True}
        relevant_chunks = self.call_tool("ehr_retriever").run(data)

        if patientId:
            data["patients"] = [patientId]
            patient = self.__tools["ehr_patient"].run(data)[0]
            context += f"Patient: {join_object(patient)}\n" 
            context += context_builder(relevant_chunks)
        else:
            id_list = set(chunk["patient_id"] for chunk in relevant_chunks)
            data["patients"] = [id for id in id_list]
            
            patients =  self.call_tool("ehr_patient").run(data)

            context += f"[General Query]\n\n"
            for patient in patients:
                context+= f"Patient: {patient['name']} ({patient['patient_id']})\n"
                patient_chunks = filter( lambda c : c["patient_id"] == patient['patient_id'], relevant_chunks)
                context += context_builder(patient_chunks)
                context += "\n\n"

        yield from self.Streaming_Prediction(data, context)

    def define_pending_action(self, data:dict):
        query = data["query"]

        yield { "chunk": "Collecting information", "thinking": True}
        direction = self.guide_modification(query = query)
        if direction["action"].lower() in ["update","remove"]:
            entity = direction["entity"]
            data["entity"] = entity                

            chunks = self.call_tool("ehr_db_loader").run(data)
            
            chunk:dict = [c for c in chunks if c["type"] == entity].pop()

            copied_chunk = dict(chunk)

            yield { "chunk": "Parsing information", "thinking": True}
            json_data = self.extract_information(query=query, schema=entity, current = join_object(chunk["content"])) 
            copied_chunk["content"] = json_data
            data["json_data"] = copied_chunk

            if isinstance(json_data, dict) and "valid" in json_data.keys():
                missing_fields = join_object(json_data['missing'])
                yield from self.Streaming_Prediction(data, f"you need to provide the next information to proced:\n {missing_fields}")
            else: 
                self.call_tool("ehr_redis_save").run(data)

                if isinstance(chunk["content"], dict):
                    diff = dict_diff(chunk["content"], copied_chunk["content"])
                    diff_text = format_changes(diff)
                    yield from self.Streaming_Prediction(data, diff_text)
                else: 
                    to_str_obj = join_object(chunk)
                    from_str_obj = join_object(copied_chunk)
                    yield from self.Streaming_Prediction(data, f"from:\n{to_str_obj} to:\n {from_str_obj}")
        else:
            yield from self.todo_feature_streaming("Create a new information")

    def plan_update(self, data:dict):
        patientId = data["patientId"]
        if patientId:
            yield from self.define_pending_action(data)
        else:
            yield from self.todo_feature_streaming("perform general update queries")
        

    def  execute_pending_action(self, data:dict):
            data["pending_action_id"] = f"{data['doctor']}:action"

            data = self.call_tool("ehr_redis_get").run(data)
            
            yield { "chunk": "Collecting action information", "thinking": True}
            
            entity = data["entity"] 
            
            chunks = self.call_tool("ehr_db_loader").run(data)

            chunk = data["json_data"]
            
            new_chunks = [
                chunk if c["type"] == entity else c
                for c in chunks
            ]

            data["chunks"] = new_chunks
            
            yield { "chunk": "Trying to apply new updates", "thinking": True}

            self.call_tool("ehr_json_ingestion").run(data)
            
            data['action_done'] = True
            
            yield from self.Streaming_Prediction(data, join_object(chunk))

    def perform_intent(self, data:dict):
        try:
            generator = []
            intent:str = data["intent"].lower()
            
            if intent == "get_info":
                generator = self.information_response(data=data)
            elif intent == "update_info":
                generator = self.plan_update(data=data)
            elif intent == "execute_action":
                generator = self.execute_pending_action(data=data)
            elif intent == "occ answer":
                generator = self.Streaming_Prediction(data, "It's not a medical query")
            else:
                raise AppError("The sistem can't perform the requested action", 500)
                    

            for chunk in generator:
                    if isinstance(chunk, dict):
                        yield chunk
                    else:
                        yield {"chunk": chunk}
        except BaseException as e:
            raise AppError(f"Streaming request failed: {e}", 500)
        
