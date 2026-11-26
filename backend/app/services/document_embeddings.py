"""Rank fictional document sections by embedding cosine similarity."""

from math import hypot, isfinite

from openai import AsyncOpenAI, OpenAIError

from app.services.document_rag import PASSAGE_LIMIT, DocumentSection
from app.services.openai_service import OpenAIServiceError

EMBEDDING_MODEL = "text-embedding-3-small"


class SemanticPassage(DocumentSection):
    score: float


async def semantic_rank(
    question: str, sections: list[DocumentSection], client: AsyncOpenAI | None,
) -> list[SemanticPassage]:
    if not sections:
        return []
    if client is None:
        raise OpenAIServiceError("Set OPENAI_API_KEY in backend/.env and restart the backend.", 503)

    inputs = [question, *(f"{s.document}\n{s.section}\n{s.text}" for s in sections)]
    try:
        response = await client.embeddings.create(
            model=EMBEDDING_MODEL, input=inputs, encoding_format="float",
        )
    except OpenAIError as exc:
        raise OpenAIServiceError("OpenAI could not generate embeddings. Check the API configuration and try again.") from exc

    ordered = sorted(response.data, key=lambda item: item.index)
    if [item.index for item in ordered] != list(range(len(inputs))):
        raise OpenAIServiceError("OpenAI returned an incomplete embedding batch.")

    normalized = []
    dimensions = len(ordered[0].embedding)
    for item in ordered:
        norm = hypot(*item.embedding)
        if len(item.embedding) != dimensions or not isfinite(norm) or norm == 0:
            raise OpenAIServiceError("OpenAI returned an invalid embedding vector.")
        normalized.append([value / norm for value in item.embedding])

    query, *passage_vectors = normalized
    ranked = []
    for section, vector in zip(sections, passage_vectors, strict=True):
        score = sum(left * right for left, right in zip(query, vector, strict=True))
        ranked.append(SemanticPassage(**section.model_dump(), score=max(-1.0, min(1.0, score))))
    return sorted(ranked, key=lambda passage: (-passage.score, passage.id))[:PASSAGE_LIMIT]
