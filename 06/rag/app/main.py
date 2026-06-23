from fastapi import FastAPI

from app.routers import chat_router
from app.routers import file_router
from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router.router)
app.include_router(file_router.router)


@app.get("/")
def root():
    return {"message": "RAG Project"}
