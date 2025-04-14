from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agent: str
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chat.id")
    query: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
