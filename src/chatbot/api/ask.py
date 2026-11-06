from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chatbot.db.session import get_db
from chatbot.models.schemas import AskIn, AskOut
from chatbot.services import pipeline

router = APIRouter()


@router.post("/ask", response_model=AskOut)
def ask(payload: AskIn, db: Session = Depends(get_db)) -> AskOut:
    return pipeline.ask(db, payload.question, payload.glpi_user_id)