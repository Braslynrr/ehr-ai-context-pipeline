import os

def _get_required_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value

class Config:
    same_site:str

    provider:str
    model:str
    max_tokens:int
    
    JWT_SECRET_KEY:str
    JWT_ALGORITHM:str


    def __init__(self, max_tokens = 4000):

        self.provider = _get_required_env("MEDICAL_LLM_PROVIDER")
        self.model = _get_required_env("MEDICAL_LLM_MODEL")
        self.max_tokens = max_tokens

        if self.provider == "gemini":
            _get_required_env("GOOGLE_API_KEY")

        if self.provider == "openai":
            _get_required_env("OPENAI_API_KEY")

        self.JWT_ALGORITHM = _get_required_env("JWT_ALGORITHM")
        self.JWT_SECRET_KEY = _get_required_env("JWT_SECRET_KEY")

        self.same_site = _get_required_env("SAME_SITE")