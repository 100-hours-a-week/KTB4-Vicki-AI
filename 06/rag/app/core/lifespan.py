from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.utils.logging import logger
from app.services.vector_store_service import VectorStoreManager
from app.services.llm_service import LLMManager
from app.services.embedding_service import EmbeddingService
from app.services.rag_service import RAGService


@asynccontextmanager
async def lifespan(app: FastAPI):
    embedding_service = EmbeddingService()
    vector_store = VectorStoreManager(embedding_service)
    llm = LLMManager()
    rag_service = RAGService(vector_store, llm)

    app.state.vector_store = vector_store
    app.state.llm = llm
    app.state.rag_service = rag_service

    yield
