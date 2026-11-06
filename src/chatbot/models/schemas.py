from typing import Literal, Optional

from pydantic import BaseModel, Field


class AskIn(BaseModel):
    question: str = Field(..., min_length=1)
    glpi_user_id: int


class AskOut(BaseModel):
    status: Literal["found_in_kb", "proposed"]
    answer: str
    source: Literal["kb", "web+llm"]
    conversation_id: Optional[int] = None


class ActionIn(BaseModel):
    conversation_id: int


class ActionOut(BaseModel):
    ok: bool
    ticket_id: Optional[int] = None
    message: Optional[str] = None