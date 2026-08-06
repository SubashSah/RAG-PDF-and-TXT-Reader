from fastapi import APIRouter

from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat_endpoint(request: ChatRequest):
    answer = chat(session_id=request.session_id, question=request.question)

    return ChatResponse(
        answer=answer,
    )
