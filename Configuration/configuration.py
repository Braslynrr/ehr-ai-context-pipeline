import os
from dotenv import load_dotenv
import dspy

def _get_required_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value

class Config:
    llm:dspy.LM = None
    __ehr_location:str

    def __init__(self, max_tokens = 4000, streaming = False):
        load_dotenv()

        _ehr_location = _get_required_env("MEDICAL_EHR_LOCATION")
        provider = _get_required_env("MEDICAL_LLM_PROVIDER")
        model = _get_required_env("MEDICAL_LLM_MODEL")


        if provider == "gemini":
            _get_required_env("GOOGLE_API_KEY")

        if provider == "openai":
            _get_required_env("OPENAI_API_KEY")


        self.__ehr_location = _ehr_location
        
        self.llm = dspy.LM(
            model= f"{provider}/{model}",
            max_tokens=max_tokens,
            num_retries=15,
            temperature=0.2
        )

        dspy.configure(lm=self.llm, async_max_workers=1, adapter=dspy.JSONAdapter())
    
    def get_ehr_location(self) -> str:
        return self.__ehr_location