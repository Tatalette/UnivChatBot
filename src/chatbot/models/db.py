from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

from chatbot.config import settings

Base = declarative_base()


class Qa(Base):
    __tablename__ = "qa"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    source = Column(String(20), default="manual")
    embedding = Column(Vector(settings.embeddings_dim), nullable=False)
    validated_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Integer, primary_key=True)
    glpi_user_id = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    answer_proposed = Column(Text)
    source = Column(String(20))
    status = Column(String(20), default="proposed")
    glpi_ticket_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())