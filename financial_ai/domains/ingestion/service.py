"""News ingestion and document normalization services."""

from __future__ import annotations

import hashlib
import re
from typing import Iterable

from financial_ai.shared.models import NormalizedDocument, RawArticle

_WHITESPACE = re.compile(r"\s+")


class IngestionService:
    """Converts raw source payloads into canonical documents."""

    def normalize(self, article: RawArticle) -> NormalizedDocument:
        title = self._clean(article.title)
        content = self._clean(article.content)
        checksum = article.checksum or self.content_checksum(content)
        return NormalizedDocument(
            raw_article_id=article.id,
            source=article.source.strip().lower(),
            title=title,
            content=content,
            url=article.url.strip(),
            checksum=checksum,
            published_at=article.published_at,
            metadata={"ingested_at": article.ingested_at.isoformat()},
        )

    def normalize_many(
        self, articles: Iterable[RawArticle]
    ) -> list[NormalizedDocument]:
        return [self.normalize(article) for article in articles]

    @staticmethod
    def content_checksum(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def _clean(value: str) -> str:
        return _WHITESPACE.sub(" ", value).strip()
