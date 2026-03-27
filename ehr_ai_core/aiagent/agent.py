import json

import requests

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
                    - Answer only using provided context
                    - If not in context, say you don't know
                    - Mention source polite and briefly
                    - Match language of the question
                    - if possible use markdown style

                    Question: {question}
                    Context: {context}
                   """

    def __init__(self, provider:str, model:str, max_tokens:str, url:str):
        if(provider=="ollama"):
            self.__ollama = createOllamaStreaming(model, url)
        else:
            self.__llm = createLLm(provider, model, max_tokens)

    def Predict(self, question: str, context: str) -> str:

        result = self.__llm(self.__build_prompt(question, context))
        
        return "".join(result)


    def Streaming_Prediction(self, question: str, context: str):
        prompt = self.__build_prompt(question, context)

        response = requests.post(
        self.__ollama['url'],
        json={
            "model": self.__ollama["model"],
            "prompt": prompt,
            "stream": True
        },
        stream=True)

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                yield data.get("response", "")