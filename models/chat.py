from typing import List
from pydantic import BaseModel

class ChatMessage(BaseModel):
    question: str
    response: str

class ChatHistory(BaseModel):
    messages: List[ChatMessage]
