from duckduckgo_search import DDGS

from chatbot.config import settings


def search(query: str, n: int | None = None) -> list[dict]:
    n = n or settings.web_top_n
    results: list[dict] = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=n):
                results.append(
                    {
                        "title": r.get("title", ""),
                        "snippet": r.get("body", ""),
                        "url": r.get("href", ""),
                    }
                )
    except Exception as e:
        # La recherche web est optionnelle : on continue avec ce qu'on a
        print(f"[web_search] erreur : {e}")
    return results