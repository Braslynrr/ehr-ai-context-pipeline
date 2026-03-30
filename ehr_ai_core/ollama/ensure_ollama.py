import requests
import os

def ensure_model(name:str):
    try:
        ollama_url = os.getenv('OLLAMA_URL', 'http://ehr_ollama:11434')
        requests.post(f"{ollama_url}/api/pull", json={"name": name})
    except Exception as e:
        raise RuntimeError(f"Ollama ensuring failed: {e.args}")


def ensure_Ollama():
    ensure_model("bge-m3")
    ensure_model("nomic-embed-text")

    ensure_model("llama3")
    ensure_model("qwen3:4b")
    ensure_model("phi3:mini")
    