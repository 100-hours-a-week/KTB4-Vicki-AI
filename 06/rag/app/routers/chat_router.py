from fastapi import APIRouter, Request, HTTPException
from app.models.chat_model import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/v1", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(chat_data: ChatRequest, request: Request):
    query = chat_data.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="질문 내용을 입력해주세요.")

    rag_service = request.app.state.rag_service

    try:
        answer = rag_service.answer(query, n_results=3)
        return ChatResponse(query=query, answer=answer)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"서버 내부 처리 중 오류가 발생했습니다: {str(e)}"
        )
