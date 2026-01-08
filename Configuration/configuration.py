import os
from dotenv import load_dotenv
import dspy

class Config:
    llm:dspy.LM = None
    __ehr_location:str

    def __init__(self, max_tokens = 4000, streaming = False):
        _ehr_location = "./data/"
        provider = "ollama"
        model = "qwen3:4b"
        load_dotenv()

        _ehr_location = os.getenv("MEDICAL_EHR_LOCATION")
        provider = os.getenv("MEDICAL_LLM_PROVIDER")
        model = os.getenv("MEDICAL_LLM_MODEL")


        self.__ehr_location = _ehr_location
        
        self.llm = dspy.LM(
            model= f"{provider}/{model}",
            max_tokens=max_tokens,
            num_retries=15,
            temperature=0.2
            #streaming = streaming
        )

        dspy.configure(lm=self.llm, async_max_workers=1, adapter=dspy.JSONAdapter())
    
    def get_ehr_location(self) -> str:
        return self.__ehr_location