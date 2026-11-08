from sqlalchemy.orm import Session

from chatbot.config import settings
from chatbot.models.db import Conversation
from chatbot.models.schemas import AskOut
from chatbot.services import kb, llm, reranker, web_search


def ask(db: Session, question: str, glpi_user_id: int) -> AskOut:
    # 1. Recherche dans la base de connaissances
    candidates = kb.search(db, question, top_k=settings.kb_top_k)
    if candidates:
        top_qa, top_score = candidates[0]
        if top_score >= settings.similarity_threshold:
            return AskOut(
                status="found_in_kb",
                answer=top_qa.answer,
                source="kb",
                conversation_id=None,
            )

    # 2. Recherche web + rerank
    web_results = web_search.search(question, n=settings.web_top_n)
    snippets = [f"{r['title']}\n{r['snippet']}" for r in web_results]

    if snippets:
        ranked = reranker.rerank(question, snippets, top_k=settings.rerank_top_k)
        context_parts = [snippets[i] for i, _ in ranked]
    else:
        context_parts = []

    # 3. Appel LLM
    context = (
        "\n\n---\n\n".join(context_parts)
        if context_parts
        else "(aucun contexte trouvé)"
    )
    answer = llm.generate(question, context)

    # 4. Persistance (pour /validate et /reject)
    conv = Conversation(
        glpi_user_id=glpi_user_id,
        question=question,
        answer_proposed=answer,
        source="web+llm",
        status="proposed",
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)

    return AskOut(
        status="proposed",
        answer=answer,
        source="web+llm",
        conversation_id=conv.id,
    )