import requests

def ensure_model(name:str):
    requests.post("http://localhost:11434/api/pull", json={"name": name})

ensure_model("qwen3:4b")
ensure_model("phi3:mini")
ensure_model("nomic-embed-text")