"""Exact and semantic deduplication utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from financial_ai.shared.models import NormalizedDocument


class SemanticIndex(Protocol):
    """Minimal vector index contract for semantic duplicate checks."""

    def max_similarity(self, text: str) -> float:
        """Return the highest cosine similarity to indexed documents."""


@dataclass(frozen=True)
class DedupDecision:
    """Result of a deduplication decision."""

    is_duplicate: bool
    reason: str
    similarity: float | None = None


class DeduplicationService:
    """Deduplicates normalized documents before expensive LLM processing."""

    def __init__(self, semantic_threshold: float = 0.95):
        self.semantic_threshold = semantic_threshold
        self._checksums: set[str] = set()

    def check(
        self, document: NormalizedDocument, index: SemanticIndex | None = None
    ) -> DedupDecision:
        if document.checksum in self._checksums:
            return DedupDecision(is_duplicate=True, reason="exact_checksum")

        if index is not None:
            similarity = index.max_similarity(document.content)
            if similarity >= self.semantic_threshold:
                return DedupDecision(
                    is_duplicate=True,
                    reason="semantic_similarity",
                    similarity=similarity,
                )

        return DedupDecision(is_duplicate=False, reason="unique")

    def remember(self, document: NormalizedDocument) -> None:
        self._checksums.add(document.checksum)
