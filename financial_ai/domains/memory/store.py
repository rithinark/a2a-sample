"""Multi-layer memory store for raw, vector, graph, and episodic memory."""

from __future__ import annotations

from dataclasses import dataclass, field

from financial_ai.domains.graph.store import KnowledgeGraph
from financial_ai.domains.models import NormalizedDocument, cosine_similarity


@dataclass
class MemoryStore:
    """Coordinates archive, vector retrieval, graph memory, and summaries."""

    graph: KnowledgeGraph = field(default_factory=KnowledgeGraph)
    raw_archive: dict[str, NormalizedDocument] = field(default_factory=dict)
    vectors: dict[str, list[float]] = field(default_factory=dict)
    episodic_summaries: list[str] = field(default_factory=list)

    def archive(self, document: NormalizedDocument, embedding: list[float] | None = None) -> None:
        key = str(document.raw_article_id)
        self.raw_archive[key] = document
        if embedding is not None:
            self.vectors[key] = embedding

    def semantic_search(self, query_embedding: list[float], limit: int = 5) -> list[NormalizedDocument]:
        ranked = sorted(
            ((cosine_similarity(query_embedding, embedding), document_id) for document_id, embedding in self.vectors.items()),
            reverse=True,
        )
        return [self.raw_archive[document_id] for _, document_id in ranked[:limit]]

    def remember_summary(self, summary: str) -> None:
        if summary.strip():
            self.episodic_summaries.append(summary.strip())
