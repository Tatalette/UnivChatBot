import httpx

from chatbot.config import settings


def rerank(
    question: str, candidates: list[str], top_k: int | None = None
) -> list[tuple[int, float]]:
    """Retourne [(index_candidat, score), ...] triés par score décroissant.

    Le format de réponse du serveur peut varier. On gère les plus courants :
      - [{"index": 0, "score": 0.9}, ...]
      - [{"index": 0, "relevance_score": 0.9}, ...]
      - {"results": [...]}
    """
    if not candidates:
        return []

    pairs = [[question, c] for c in candidates]
    with httpx.Client(timeout=settings.http_timeout) as client:
        r = client.post(settings.rerank_url, json={"pairs": pairs})
        r.raise_for_status()
        data = r.json()

    if isinstance(data, dict):
        data = data.get("results", data.get("scores", []))

    scored: list[tuple[int, float]] = []
    for item in data:
        if isinstance(item, dict):
            idx = item.get("index", item.get("idx", 0))
            score = item.get(
                "score", item.get("relevance_score", item.get("relevance", 0.0))
            )
            scored.append((int(idx), float(score)))
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            scored.append((int(item[0]), float(item[1])))

    scored.sort(key=lambda x: x[1], reverse=True)
    if top_k:
        scored = scored[:top_k]
    return scored