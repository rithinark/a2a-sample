"""In-memory graph store that mirrors the intended Neo4j contract."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from financial_ai.domains.models import ExtractedEvent, Relationship


@dataclass
class KnowledgeGraph:
    """Stores typed relationships and supports exposure traversal."""

    adjacency: dict[str, list[Relationship]] = field(default_factory=lambda: defaultdict(list))
    events: list[ExtractedEvent] = field(default_factory=list)

    def apply_event(self, event: ExtractedEvent) -> None:
        self.events.append(event)
        for relationship in event.relationships:
            self.add_relationship(relationship)

    def add_relationship(self, relationship: Relationship) -> None:
        self.adjacency[relationship.subject].append(relationship)

    def related(self, subject: str, predicate: str | None = None) -> list[Relationship]:
        relationships = self.adjacency.get(subject, [])
        if predicate is None:
            return list(relationships)
        return [edge for edge in relationships if edge.predicate == predicate]

    def exposed_entities(self, theme: str) -> set[str]:
        theme_key = theme.casefold()
        exposed: set[str] = set()
        for subject, relationships in self.adjacency.items():
            for relationship in relationships:
                if theme_key in relationship.object.casefold() or theme_key in relationship.predicate.casefold():
                    exposed.add(subject)
        return exposed
