"""Search the saved fictional passage embeddings using pgvector."""

import json

from sqlalchemy import text

from app.db.session import engine
from app.services.document_embeddings import EMBEDDING_MODEL, SemanticPassage
from app.services.document_rag import PASSAGE_LIMIT


def rank_saved_passages(vector: list[float]) -> list[SemanticPassage]:
    with engine.connect() as db:
        rows = db.execute(
            text("""
                SELECT id, document, section, text,
                       1 - (embedding <=> CAST(:query_vector AS vector)) AS score
                FROM document_embeddings
                WHERE model = :model
                ORDER BY embedding <=> CAST(:query_vector AS vector), id
                LIMIT :limit
            """),
            {"query_vector": json.dumps(vector), "model": EMBEDDING_MODEL, "limit": PASSAGE_LIMIT},
        ).mappings()
        return [SemanticPassage.model_validate(row) for row in rows]
