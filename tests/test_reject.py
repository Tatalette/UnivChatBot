from unittest.mock import patch

from chatbot.models.db import Conversation
from chatbot.models.schemas import ActionIn


def test_reject_creates_glpi_ticket(db):
    conv = Conversation(
        glpi_user_id=1, question="Q?", answer_proposed="A.", source="web+llm",
        status="proposed",
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)

    from chatbot.api.reject import reject

    with patch("chatbot.services.glpi.create_ticket", return_value=42):
        out = reject(ActionIn(conversation_id=conv.id), db=db)

    assert out.ok is True
    assert out.ticket_id == 42
    db.refresh(conv)
    assert conv.status == "rejected"
    assert conv.glpi_ticket_id == 42