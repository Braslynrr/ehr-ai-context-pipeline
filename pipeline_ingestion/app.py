
import os
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

from ehr_ai_core.error.app_error import AppError
from ehr_ai_core.retrieval.embedding import Embedder
from ehr_ai_core.retrieval.postgress_vector_db import Postgress_db
from ehr_ai_core.ollama.ensure_ollama import ensure_Ollama
from services.ehr_service import RagService

def load_json_files(input_dir: str) -> List[Dict[str, Any]]:
    documents = []
    for path in Path(input_dir).glob("*.json"):
        with open(path, "r", encoding="utf-8") as f:
            documents.append(path)
    return documents


if __name__ == "__main__":

    try:
        load_dotenv()
        ensure_Ollama()
        
        INPUT_DIR = os.getenv("MEDICAL_EHR_LOCATION", "/app/input")
        EMBBEDER_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

        print("Ingestion Process Started!")
        
        print("Dir:", INPUT_DIR)
        files = load_json_files(INPUT_DIR)

        db = Postgress_db()
        embbeder = Embedder(EMBBEDER_MODEL)
        rag = RagService(db, embbeder)

        total = len(files)
        print(f"Ingesting {total} Files...")
        for i ,path in enumerate(files):
            rag.ingestion(path)
            print(f"{( (i+1) / total ) * 100}%")

        print("Process ended!")

    except AppError as e: 
        print(f"Something went wrong: {e.message}")