"""News ingestion pipeline abstractions."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from financial_ai.domains.models import NormalizedDocument, RawArticle


class NewsSource(Protocol):
    """Adapter contract for RSS, API, SEC, social, and calendar sources."""

    name: str

    def fetch(self) -> Iterable[RawArticle]:
        """Fetch newly available articles from the source."""


@dataclass
class IngestionPipeline:
    """Pulls raw articles and converts them into normalized documents."""

    sources: Sequence[NewsSource]

    def collect(self) -> list[NormalizedDocument]:
        documents: list[NormalizedDocument] = []
        for source in self.sources:
            for article in source.fetch():
                documents.append(self.normalize(article))
        return documents

    def normalize(self, article: RawArticle) -> NormalizedDocument:
        content = " ".join(article.content.split())
        published_at = article.published_at
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        return NormalizedDocument(
            raw_article_id=article.id,
            source=article.source,
            title=article.title.strip(),
            content=content,
            url=article.url,
            published_at=published_at,
            checksum=article.checksum,
        )


@dataclass(frozen=True)
class StaticNewsSource:
    """Deterministic source useful for local tests, replays, and demos."""

    name: str
    articles: Sequence[RawArticle]

    def fetch(self) -> Iterable[RawArticle]:
        yield from self.articles
