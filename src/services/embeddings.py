import httpx

from chatbot.config import settings


def embed(text: str) -> list[float]:
    payload = {"model": settings.embeddings_model, "input": text}
    with httpx.Client(timeout=settings.http_timeout) as client:
        r = client.post(settings.embeddings_url, json=payload)
        r.raise_for_status()
        data = r.json()

    emb = data["data"][0]["embedding"]
    if len(emb) != settings.embeddings_dim:
        raise ValueError(
            f"Dimension embedding inattendue : {len(emb)} "
            f"(attendu {settings.embeddings_dim}). "
            f"Ajuste EMBEDDINGS_DIM et le vector(N) dans 001_init.sql."
        )
    return emb