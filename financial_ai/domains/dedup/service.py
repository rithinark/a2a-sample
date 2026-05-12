"""Exact and semantic deduplication services."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

from financial_ai.shared.models import NormalizedDocument


def semantic_fingerprint(text: str) -> dict[str, float]:
    """A lightweight token-frequency fingerprint used until embeddings are wired in."""

    tokens = [token.lower() for token in text.split() if token.strip()]
    counts = Counter(tokens)
    total = sum(counts.values()) or 1
    return {token: count / total for token, count in counts.items()}


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    """Compute cosine similarity between sparse semantic fingerprints."""

    common = set(left).intersection(right)
    numerator = sum(left[token] * right[token] for token in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


@dataclass(frozen=True)
class DedupDecision:
    """Deduplication decision with explainable reason."""

    is_duplicate: bool
    reason: str
    similarity: float = 0.0


class DeduplicationService:
    """Track seen articles by checksum and semantic similarity."""

    def __init__(self, semantic_threshold: float = 0.95):
        self.semantic_threshold = semantic_threshold
        self._checksums: set[str] = set()
        self._fingerprints: list[dict[str, float]] = []

    def evaluate(self, document: NormalizedDocument) -> DedupDecision:
        """Return whether the document should be marked duplicate."""

        if document.checksum in self._checksums:
            return DedupDecision(is_duplicate=True, reason="exact_checksum", similarity=1.0)

        fingerprint = semantic_fingerprint(f"{document.title} {document.content}")
        best_similarity = max(
            (cosine_similarity(fingerprint, existing) for existing in self._fingerprints),
            default=0.0,
        )
        if best_similarity >= self.semantic_threshold:
            return DedupDecision(
                is_duplicate=True,
                reason="semantic_similarity",
                similarity=best_similarity,
            )

        self._checksums.add(document.checksum)
        self._fingerprints.append(fingerprint)
        return DedupDecision(is_duplicate=False, reason="new_document", similarity=best_similarity)
