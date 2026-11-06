from unittest.mock import patch

from chatbot.models.db import Qa
from chatbot.services import pipeline


def test_ask_returns_kb_when_match(db):
    fake = Qa(id=1, question="Q", answer="A", source="manual", embedding=[0.0] * 3584)
    with patch("chatbot.services.kb.search", return_value=[(fake, 0.95)]):
        out = pipeline.ask(db, "Q", glpi_user_id=1)
    assert out.status == "found_in_kb"
    assert out.answer == "A"
    assert out.source == "kb"
    assert out.conversation_id is None