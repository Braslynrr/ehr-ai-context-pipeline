import traceback
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from backend.api.routes import auth, ehr
from backend.configuration import Config
from ehr_ai_core.redis.redis import RedisManager
from services.agent import EHRAgent
from ehr_ai_core.error.app_error import AppError
from ehr_ai_core.retrieval.IVector_db import IVector
from ehr_ai_core.retrieval.embedding import Embedder
from ehr_ai_core.retrieval.postgress_vector_db import Postgress_db
from services.ehr_service import EHRService
from services.rag_service import RagService
from fastapi.middleware.cors import CORSMiddleware
from ehr_ai_core.ollama.ensure_ollama import ensure_Ollama
from services.tools.ehr_json_ingestion import ehr_json_ingestion
from services.tools.ehr_db_loader import ehr_db_loader
from services.tools.ehr_redis_get import ehr_redis_get
from services.tools.ehr_redis_save import ehr_redis_save
from services.tools.ehr_retriever import ehr_retriever
from services.tools.ehr_patients import ehr_patient

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        ensure_Ollama()

        config = Config()

        embedder = Embedder(config.embedding_model)
        db: IVector = Postgress_db()
        redis = RedisManager()
        rag = RagService(db, embedder)
        agent = EHRAgent(config.provider,config.model, config.max_tokens, config.ollama_url)

        medical_service = EHRService(rag=rag, redis=redis)

        agent.add_tool(ehr_retriever(medical_service))
        agent.add_tool(ehr_patient(medical_service))
        agent.add_tool(ehr_db_loader(rag))
        agent.add_tool(ehr_json_ingestion(rag))
        agent.add_tool(ehr_redis_save(redis))
        agent.add_tool(ehr_redis_get(redis))


        app.state.medical_service = medical_service
        app.state.agent = agent
        app.state.config = config


        print("[STARTUP] Application initialized")

        yield

    except Exception as e:
        print("[FATAL ERROR] Startup failed")
        traceback.print_exc()
        raise e

    finally:
        print("[SHUTDOWN] Cleaning up resources")

load_dotenv()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN","http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: BaseException):
    # todo: logger
    print(exc)

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

app.include_router(auth.router)
app.include_router(ehr.router)
