from typing import Literal
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str

class BookingExtraction(BaseModel):
    intent: Literal["general_chat", "book_interview"]
    name: str | None = None
    email: str | None = None
    date: str | None = None
    time: str | None = None