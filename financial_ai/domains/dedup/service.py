"""Exact and semantic document deduplication."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from financial_ai.domains.models import NormalizedDocument, cosine_similarity


Embedding = list[float]


@dataclass
class DeduplicationService:
    """Tracks seen documents using checksums and embedding similarity."""

    semantic_threshold: float = 0.95
    checksums: dict[str, UUID] = field(default_factory=dict)
    embeddings: dict[UUID, Embedding] = field(default_factory=dict)

    def classify(self, document: NormalizedDocument, embedding: Embedding | None = None) -> NormalizedDocument:
        duplicate_id = self.checksums.get(document.checksum)
        if duplicate_id is None and embedding is not None:
            duplicate_id = self._semantic_duplicate(embedding)

        if duplicate_id is not None:
            return NormalizedDocument(**{**document.__dict__, "duplicate_of": duplicate_id})

        self.checksums[document.checksum] = document.raw_article_id
        if embedding is not None:
            self.embeddings[document.raw_article_id] = embedding
        return document

    def _semantic_duplicate(self, embedding: Embedding) -> UUID | None:
        for document_id, existing in self.embeddings.items():
            if cosine_similarity(embedding, existing) >= self.semantic_threshold:
                return document_id
        return None
