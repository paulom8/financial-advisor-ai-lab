"""Refresh the fictional document passages and their pgvector embeddings."""

import asyncio
import json

from openai import AsyncOpenAI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import OPENAI_API_KEY
from app.db.session import engine
from app.services.document_embeddings import (
    EMBEDDING_DIMENSIONS,
    EMBEDDING_MODEL,
    embed_texts,
    section_embedding_text,
)
from app.services.document_rag import load_sections
from app.services.openai_service import OpenAIServiceError


async def fetch_vectors(inputs: list[str]) -> list[list[float]]:
    async with AsyncOpenAI(api_key=OPENAI_API_KEY, timeout=30.0, max_retries=0) as client:
        return await embed_texts(inputs, client)


def main() -> None:
    sections = load_sections()
    if not sections:
        raise SystemExit("No fictional document sections found.")
    if not OPENAI_API_KEY:
        raise SystemExit("Set OPENAI_API_KEY in backend/.env before seeding document vectors.")

    try:
        with engine.begin() as db:
            enabled = db.scalar(text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector')"))
            if not enabled:
                raise SystemExit("Enable the vector extension in financial_advisor_lab first.")

        vectors = asyncio.run(fetch_vectors([section_embedding_text(section) for section in sections]))
        if any(len(vector) != EMBEDDING_DIMENSIONS for vector in vectors):
            raise SystemExit("The embedding model returned an unexpected vector dimension.")
        rows = [
            {**section.model_dump(), "model": EMBEDDING_MODEL, "embedding": json.dumps(vector)}
            for section, vector in zip(sections, vectors, strict=True)
        ]

        with engine.begin() as db:
            # Serialise refreshes, including the first table creation.
            db.execute(text("SELECT pg_advisory_xact_lock(18467, 31208)"))
            db.execute(text(f"""
                CREATE TABLE IF NOT EXISTS document_embeddings (
                    id text PRIMARY KEY,
                    document text NOT NULL,
                    section text NOT NULL,
                    text text NOT NULL,
                    model text NOT NULL,
                    embedding vector({EMBEDDING_DIMENSIONS}) NOT NULL
                )
            """))
            db.execute(text("DELETE FROM document_embeddings"))
            db.execute(text("""
                INSERT INTO document_embeddings (id, document, section, text, model, embedding)
                VALUES (:id, :document, :section, :text, :model, CAST(:embedding AS vector))
            """), rows)
    except OpenAIServiceError as exc:
        raise SystemExit(str(exc)) from None
    except SQLAlchemyError as exc:
        sqlstate = getattr(exc.orig, "sqlstate", None) if hasattr(exc, "orig") else None
        suffix = f" (SQLSTATE {sqlstate})" if sqlstate else ""
        raise SystemExit(f"Could not seed document vectors in the lab database{suffix}.") from None
    finally:
        engine.dispose()

    print(f"Saved {len(rows)} fictional passages with {EMBEDDING_DIMENSIONS}-dimension embeddings.")


if __name__ == "__main__":
    main()
