CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS qa (
  id              SERIAL PRIMARY KEY,
  question        TEXT NOT NULL,
  answer          TEXT NOT NULL,
  source          VARCHAR(20) DEFAULT 'manual',
  embedding       vector(3584),
  validated_count INT DEFAULT 0,
  created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS qa_embedding_idx
  ON qa USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE TABLE IF NOT EXISTS conversation (
  id              SERIAL PRIMARY KEY,
  glpi_user_id    INT NOT NULL,
  question        TEXT NOT NULL,
  answer_proposed TEXT,
  source          VARCHAR(20),
  status          VARCHAR(20) DEFAULT 'proposed',
  glpi_ticket_id  INT,
  created_at      TIMESTAMP DEFAULT NOW()
);