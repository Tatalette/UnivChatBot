from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # IA
    llm_url: str
    llm_model: str
    embeddings_url: str
    embeddings_model: str
    embeddings_dim: int = 3584
    rerank_url: str
    rerank_model: str

    # DB
    database_url: str

    # GLPI
    glpi_url: str
    glpi_app_token: str
    glpi_user_token: str

    # Pipeline
    similarity_threshold: float = 0.80
    kb_top_k: int = 5
    web_top_n: int = 5
    rerank_top_k: int = 3
    llm_timeout: float = 120.0
    http_timeout: float = 60.0


settings = Settings()