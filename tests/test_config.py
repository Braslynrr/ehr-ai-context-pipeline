import pytest
from configuration import Config

def test_missing_env_raises_location(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("MEDICAL_EHR_LOCATION", raising=False)
    monkeypatch.setenv("MEDICAL_LLM_PROVIDER", "ollama")
    monkeypatch.setenv("MEDICAL_LLM_MODEL", "qwen3:4b")    

    with pytest.raises(RuntimeError):
        Config()

def test_missing_env_raises_provider(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MEDICAL_EHR_LOCATION","C:/")   
    monkeypatch.delenv("MEDICAL_LLM_PROVIDER", raising=False)
    monkeypatch.setenv("MEDICAL_LLM_MODEL", "qwen3:4b")   

    with pytest.raises(RuntimeError):
        Config()

def test_missing_env_raises_model(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MEDICAL_EHR_LOCATION", "C:/")
    monkeypatch.setenv("MEDICAL_LLM_PROVIDER", "ollama")
    monkeypatch.delenv("MEDICAL_LLM_MODEL", raising=False)

    with pytest.raises(RuntimeError):
        Config()

def test_missing_env_raises_gemini(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MEDICAL_EHR_LOCATION", "C:/")
    monkeypatch.setenv("MEDICAL_LLM_PROVIDER", "gemini")
    monkeypatch.setenv("MEDICAL_LLM_MODEL", "qwen3:4b")
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        Config()

def test_missing_env_raises_openai(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MEDICAL_EHR_LOCATION", "C:/")
    monkeypatch.setenv("MEDICAL_LLM_PROVIDER", "openai")
    monkeypatch.setenv("MEDICAL_LLM_MODEL", "qwen3:4b")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        Config()

