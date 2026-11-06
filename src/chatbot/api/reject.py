from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from chatbot.db.session import get_db
from chatbot.models.db import Conversation
from chatbot.models.schemas import ActionIn, ActionOut
from chatbot.services import glpi

router = APIRouter()


@router.post("/reject", response_model=ActionOut)
def reject(payload: ActionIn, db: Session = Depends(get_db)) -> ActionOut:
    conv = db.get(Conversation, payload.conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation introuvable")
    if conv.status != "proposed":
        raise HTTPException(400, f"Statut invalide : {conv.status}")

    ticket_id = glpi.create_ticket(
        question=conv.question,
        proposed_answer=conv.answer_proposed or "",
        user_id=conv.glpi_user_id,
    )
    conv.status = "rejected"
    conv.glpi_ticket_id = ticket_id
    db.commit()
    return ActionOut(ok=True, ticket_id=ticket_id, message="Ticket GLPI créé")