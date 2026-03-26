import traceback

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from backend.api.routes import auth, ehr
from backend.configuration import Config
from ehr_ai_core.aiagent.agent import EHRAgent
from ehr_ai_core.retrieval.IVector_db import IVector
from ehr_ai_core.retrieval.embedding import Embedder
from ehr_ai_core.retrieval.postgress_vector_db import Postgress_db
from services.ehr_service import EHRService
from services.rag_service import RagService
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        
        load_dotenv()
        config = Config()

        embedder = Embedder()
        db: IVector = Postgress_db()

        rag = RagService(db, embedder)
        agent = EHRAgent(config.provider,config.model, config.max_tokens)

        medical_service = EHRService(rag, agent)

        app.state.medical_service = medical_service
        app.state.config = config

        print("[STARTUP] Application initialized")

        yield

    except Exception as e:
        print("[FATAL ERROR] Startup failed")
        traceback.print_exc()
        raise e

    finally:
        print("[SHUTDOWN] Cleaning up resources")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ehr.router)