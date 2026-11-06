"""Tests : nécessitent un PostgreSQL + pgvector accessible via DATABASE_URL.
On n'utilise pas SQLite (incompatible avec le type Vector).
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chatbot.config import settings
from chatbot.models.db import Base


@pytest.fixture(scope="function")
def db():
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()