"""News ingestion primitives for source pollers and parser workers."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable
from datetime import datetime

from financial_ai.shared.models import NormalizedDocument, RawArticle

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    """Collapse whitespace and strip noisy source text."""

    return _WHITESPACE_RE.sub(" ", value).strip()


def content_checksum(title: str, content: str) -> str:
    """Create the exact-deduplication hash for a document."""

    normalized = f"{normalize_text(title)}\n{normalize_text(content)}".encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


class NewsIngestionPipeline:
    """Normalize raw source payloads into canonical documents."""

    def normalize_article(
        self,
        *,
        source: str,
        title: str,
        content: str,
        url: str,
        published_at: datetime | None = None,
        metadata: dict | None = None,
    ) -> RawArticle:
        clean_title = normalize_text(title)
        clean_content = normalize_text(content)
        return RawArticle(
            source=source,
            title=clean_title,
            content=clean_content,
            url=url,
            published_at=published_at,
            checksum=content_checksum(clean_title, clean_content),
            metadata=metadata or {},
        )

    def parse(self, article: RawArticle) -> NormalizedDocument:
        """Convert a raw article into the parser-worker output contract."""

        return NormalizedDocument(
            article_id=article.id,
            source=article.source,
            title=article.title,
            content=article.content,
            url=article.url,
            checksum=article.checksum,
            published_at=article.published_at,
            ingested_at=article.ingested_at,
            metadata=article.metadata,
        )

    def ingest_batch(self, payloads: Iterable[dict]) -> list[NormalizedDocument]:
        """Normalize and parse a batch of source payload dictionaries."""

        documents: list[NormalizedDocument] = []
        for payload in payloads:
            article = self.normalize_article(
                source=payload["source"],
                title=payload["title"],
                content=payload["content"],
                url=payload["url"],
                published_at=payload.get("published_at"),
                metadata=payload.get("metadata"),
            )
            documents.append(self.parse(article))
        return documents
