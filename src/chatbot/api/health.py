import socket
from urllib.parse import urlparse

from fastapi import APIRouter
from sqlalchemy import text

from chatbot.config import settings
from chatbot.db.session import SessionLocal

router = APIRouter()


def _tcp_check(url: str, timeout: float = 3.0) -> bool:
    p = urlparse(url)
    host = p.hostname
    port = p.port or (443 if p.scheme == "https" else 80)
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


@router.get("/health")
def health() -> dict:
    checks: dict[str, str] = {}

    # DB
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        checks["db"] = "ok"
    except Exception as e:
        checks["db"] = f"fail: {e}"

    # Endpoints IA (TCP uniquement : les endpoints attendent du POST)
    for name, url in [
        ("embeddings", settings.embeddings_url),
        ("llm", settings.llm_url),
        ("rerank", settings.rerank_url),
    ]:
        checks[name] = "reachable" if _tcp_check(url) else "unreachable"

    # GLPI
    try:
        p = urlparse(settings.glpi_url)
        with socket.create_connection(
            (p.hostname, p.port or 80), timeout=3
        ):
            checks["glpi"] = "reachable"
    except Exception:
        checks["glpi"] = "unreachable"

    return checks