
import os
from pathlib import Path
from typing import List, Dict, Any

from ehr_ai_core.retrieval.embedding import Embedder
from ehr_ai_core.retrieval.postgress_vector_db import Postgress_db
from services.ehr_service import RagService


INPUT_DIR = os.getenv("INPUT_DIR", "/app/input")
EMBBEDER_MODEL = os.getenv("INPUT_DIR", "nomic-embed-text")

def load_json_files(input_dir: str) -> List[Dict[str, Any]]:
    documents = []
    for path in Path(input_dir).glob("*.json"):
        with open(path, "r", encoding="utf-8") as f:
            documents.append(path)
    return documents


if __name__ == "__main__":
    print("Ingestion Process Started!")
    
    files = load_json_files("E:/Projects/ehr-ai-context-pipeline/data")

    db = Postgress_db()
    embbeder = Embedder(EMBBEDER_MODEL)
    rag = RagService(db, embbeder)

    total = len(files)
    print(f"Ingesting {total} Files...")
    for i ,path in enumerate(files):
        rag.ingestion(path)
        print(f"{( (i+1) / total ) * 100}%")

    print("Process ended!")