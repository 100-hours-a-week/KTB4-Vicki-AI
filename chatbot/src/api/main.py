from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, field_validator

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.graph import search_agent

    app.state.graph = search_agent
    yield


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def strip_and_check(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("question은 공백일 수 없습니다.")
        return v


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return "Hello"


@app.post("/chat")
def answer(request: ChatRequest):
    config = {"configurable": {"thread_id": "1111"}}
    response = app.state.graph.invoke({"messages": request.question}, config=config)
    answer = response["messages"][-1].content
    return ChatResponse(answer=answer)
