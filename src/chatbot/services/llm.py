import httpx

from chatbot.config import settings

SYSTEM_PROMPT = """Tu es TARS, assistant de support de l'Université de Corse.
Réponds de manière concise, en français, en te basant UNIQUEMENT sur le contexte fourni.
Si le contexte ne suffit pas, dis-le clairement sans inventer.
Ne donne pas de procédures que tu ne connais pas."""


def generate(question: str, context: str) -> str:
    user_msg = (
        f"Contexte :\n{context}\n\n"
        f"Question de l'utilisateur :\n{question}"
    )
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        "max_tokens": 1000,
        "temperature": 0.3,
        "top_p": 0.95,
        "stream": False,
    }
    with httpx.Client(timeout=settings.llm_timeout) as client:
        r = client.post(settings.llm_url, json=payload)
        r.raise_for_status()
        data = r.json()
    return data["choices"][0]["message"]["content"].strip()