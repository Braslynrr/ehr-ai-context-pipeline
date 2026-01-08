import os
from dotenv import load_dotenv
import dspy

class Config:
    __apiKey = None
    llm = None

    def __init__(self, model = "qwen3:4b", max_tokens = 4000, streaming = False):
        load_dotenv()
        self.__apiKey = os.getenv("API_KEY")

        if not self.__apiKey:
            raise ValueError("API_KEY environment variable is required")
        
        
        self.llm = dspy.LM(
            model= f"ollama/{model}",
            max_tokens=max_tokens,
            num_retries=15,
            temperature=0.2
            #streaming = streaming
        )

        dspy.configure(lm=self.llm, async_max_workers=1, adapter=dspy.JSONAdapter())