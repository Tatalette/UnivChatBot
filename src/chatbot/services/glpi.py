import httpx

from chatbot.config import settings


class GlpiClient:
    def __init__(self) -> None:
        self.base = settings.glpi_url.rstrip("/")
        self.app_token = settings.glpi_app_token
        self.user_token = settings.glpi_user_token
        self._session_token: str | None = None

    def _headers(self, with_session: bool = True) -> dict:
        h = {"App-Token": self.app_token, "Content-Type": "application/json"}
        if with_session and self._session_token:
            h["Session-Token"] = self._session_token
        else:
            h["Authorization"] = f"user_token {self.user_token}"
        return h

    def init_session(self) -> str:
        url = f"{self.base}/apirest.php/initSession"
        with httpx.Client(timeout=settings.http_timeout) as client:
            r = client.get(url, headers=self._headers(with_session=False))
            r.raise_for_status()
            self._session_token = r.json()["session_token"]
        return self._session_token

    def create_ticket(self, name: str, content: str) -> int:
        if not self._session_token:
            self.init_session()
        url = f"{self.base}/apirest.php/Ticket"
        payload = {
            "input": {
                "name": name[:255],
                "content": content,
                "type": 1,   # 1 = incident
                "status": 1, # 1 = nouveau
            }
        }
        with httpx.Client(timeout=settings.http_timeout) as client:
            r = client.post(url, headers=self._headers(), json=payload)
            r.raise_for_status()
            return int(r.json()["id"])


_glpi = GlpiClient()


def create_ticket(question: str, proposed_answer: str, user_id: int) -> int:
    content = (
        f"Question posée au chatbot par l'utilisateur GLPI #{user_id} :\n"
        f"{question}\n\n"
        f"Réponse proposée par l'IA (refusée par l'utilisateur) :\n"
        f"{proposed_answer}"
    )
    return _glpi.create_ticket(
        name=f"[Chatbot] {question[:100]}",
        content=content,
    )