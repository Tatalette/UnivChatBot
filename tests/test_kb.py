from unittest.mock import patch

from chatbot.services import kb


def test_kb_insert_calls_embeddings(db):
    with patch("chatbot.services.kb.embed", return_value=[0.1] * 3584):
        qa = kb.insert(db, question="Q", answer="A", source="manual")
    assert qa.id is not None
    assert qa.question == "Q"
    assert qa.source == "manual"