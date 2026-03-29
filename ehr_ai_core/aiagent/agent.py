import json

import requests

from ehr_ai_core.error.app_error import AppError

from .llm_factory import createLLm, createOllamaStreaming

class EHRAgent:
    """
    Handles clinicians questions through use of context and llm response 
    """

    __llm = None
    __ollama = None

    def __build_prompt(self, question: str, context: str):
        return f"""
                    You are a medical assistant.
                    Task list, order by priority:
                    - Ensure to match the question language
                    - If not in context, say you don't know
                    - Answer only using provided context
                    - Mention source polite and briefly
                    - if possible use markdown style
                    
                    Context: {context}

                    Question: {question}
                   """

    def __init__(self, provider:str, model:str, max_tokens:str, url:str):
        if(provider=="ollama"):
            self.__ollama = createOllamaStreaming(model, url)
        else:
            self.__llm = createLLm(provider, model, max_tokens)

    def Predict(self, question: str, context: str) -> str:

        if not self.__llm:
            raise AppError("LLM not initialized", 409)

        try:
            result = self.__llm(self.__build_prompt(question, context))
            return "".join(result)

        except Exception as e:
            raise AppError(f"LLM prediction failed: {e}", 500)


    def Streaming_Prediction(self, question: str, context: str):

        if not self.__ollama:
            raise AppError("Ollama not initialized", 409)
        
        prompt = self.__build_prompt(question, context)
        
        try:
            response = requests.post(
                self.__ollama['url'],
                json={
                    "model": self.__ollama["model"],
                    "prompt": prompt,
                    "stream": True
                },
                stream=True,
                timeout=30
            )

            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        yield data.get("response", "")
                    except json.JSONDecodeError:
                        continue  # línea corrupta, ignoras

        except requests.RequestException as e:
            raise AppError(f"Streaming request failed: {e}", 500)