import os

def _get_required_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value

class Config:
    __ehr_location:str
    provider:str
    model:str
    max_tokens:int

    def __init__(self, max_tokens = 4000):

        self._ehr_location = _get_required_env("MEDICAL_EHR_LOCATION")
        self.provider = _get_required_env("MEDICAL_LLM_PROVIDER")
        self.model = _get_required_env("MEDICAL_LLM_MODEL")
        self.max_tokens = max_tokens

        if self.provider == "gemini":
            _get_required_env("GOOGLE_API_KEY")

        if self.provider == "openai":
            _get_required_env("OPENAI_API_KEY")

    
    def get_ehr_location(self) -> str:
        return self.__ehr_location

