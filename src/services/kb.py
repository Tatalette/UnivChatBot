from sqlalchemy import select
from sqlalchemy.orm import Session

from chatbot.models.db import Qa
from chatbot.services.embeddings import embed


def search(
    db: Session, question: str, top_k: int = 5
) -> list[tuple[Qa, float]]:
    """Retourne [(Qa, score_cosinus)] triés par similarité décroissante."""
    qvec = embed(question)
    distance = Qa.embedding.cosine_distance(qvec)
    stmt = (
        select(Qa, distance.label("distance"))
        .order_by(distance)
        .limit(top_k)
    )
    rows = db.execute(stmt).all()
    return [(row[0], 1.0 - float(row[1])) for row in rows]


def insert(
    db: Session, question: str, answer: str, source: str
) -> Qa:
    qvec = embed(question)
    qa = Qa(question=question, answer=answer, source=source, embedding=qvec)
    db.add(qa)
    db.commit()
    db.refresh(qa)
    return qa