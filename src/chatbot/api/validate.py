from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from chatbot.db.session import get_db
from chatbot.models.db import Conversation
from chatbot.models.schemas import ActionIn, ActionOut
from chatbot.services import kb

router = APIRouter()


@router.post("/validate", response_model=ActionOut)
def validate(payload: ActionIn, db: Session = Depends(get_db)) -> ActionOut:
    conv = db.get(Conversation, payload.conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation introuvable")
    if conv.status != "proposed":
        raise HTTPException(400, f"Statut invalide : {conv.status}")

    kb.insert(
        db,
        question=conv.question,
        answer=conv.answer_proposed or "",
        source="web+llm",
    )
    conv.status = "validated"
    db.commit()
    return ActionOut(ok=True, message="Q/R ajoutée à la base de connaissances")