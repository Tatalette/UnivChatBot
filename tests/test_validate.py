from unittest.mock import patch

from chatbot.models.db import Conversation
from chatbot.services.pipeline import ask as run_ask


def test_validate_inserts_into_kb(db):
    conv = Conversation(
        glpi_user_id=1, question="Q?", answer_proposed="A.", source="web+llm",
        status="proposed",
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)

    from chatbot.api.validate import validate
    from chatbot.models.schemas import ActionIn

    with patch("chatbot.services.kb.insert") as mock_insert:
        out = validate(ActionIn(conversation_id=conv.id), db=db)

    assert out.ok is True
    mock_insert.assert_called_once()
    db.refresh(conv)
    assert conv.status == "validated"