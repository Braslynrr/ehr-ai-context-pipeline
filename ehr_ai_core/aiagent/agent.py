import json

import requests

from .llm_factory import createLLm

class EHRAgent:
    """
    Handles clinicians questions through use of context and llm response 
    """

    __llm = None

    def __build_prompt(self, question: str, context: str):
        return f"""
                            Act as a doctor assistant. 
                            Each answer should have the context from which was taken, if the question is out of context the references can be omitted; So,
                            *Any question out the context should be decline due to it's not in the EHR*.
                            Ensure you are mention the source/reference and refactor it to be read by the user,
                            however don't show the content of the EHR like a json or any similar structure.
                            
                            [Ensure to identify the question language to answer correctly.]

                            Question: {question}
                            context: {context}
                   """

    def __init__(self, provider:str, model:str, max_tokens:str):
        self.__llm = createLLm(provider, model, max_tokens)

    def Predict(self, question: str, context: str) -> str:

        result = self.__llm(self.__build_prompt(question, context))
        
        return "".join(result)


    def Streaming_Prediction(self, question: str, context: str):
        prompt = self.__build_prompt(question, context)

        response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:4b",
            "prompt": prompt,
            "stream": True
        },
        stream=True)

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                yield data.get("response", "")