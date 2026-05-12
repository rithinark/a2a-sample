"""In-memory graph model mirroring the future Neo4j intelligence layer."""

from __future__ import annotations

from collections import defaultdict
from uuid import UUID

from financial_ai.shared.models import ExtractedEvent, GraphRelationship, RelationshipType, Sentiment


class RelationshipGraph:
    """Small graph store for local reasoning and adapter tests."""

    def __init__(self):
        self._edges: dict[str, list[GraphRelationship]] = defaultdict(list)

    def apply_event(self, event: ExtractedEvent) -> list[GraphRelationship]:
        """Convert an extracted event into graph relationships."""

        relationships: list[GraphRelationship] = []
        theme = event.event_type.value
        for entity in event.entities:
            relationship_type = self._relationship_for_sentiment(event.sentiment)
            relationships.append(
                GraphRelationship(
                    source=entity,
                    target=theme,
                    relationship=relationship_type,
                    confidence=event.confidence,
                    evidence_document_id=event.document_id,
                )
            )
            relationships.append(
                GraphRelationship(
                    source=entity,
                    target=theme,
                    relationship=RelationshipType.MENTIONS,
                    confidence=event.confidence,
                    evidence_document_id=event.document_id,
                )
            )
        for relationship in relationships:
            self.add_relationship(relationship)
        return relationships

    def add_relationship(self, relationship: GraphRelationship) -> None:
        self._edges[relationship.source].append(relationship)

    def neighbors(self, node: str, relationship: RelationshipType | None = None) -> tuple[GraphRelationship, ...]:
        edges = self._edges.get(node, [])
        if relationship is None:
            return tuple(edges)
        return tuple(edge for edge in edges if edge.relationship is relationship)

    def exposed_entities(self, theme: str) -> tuple[str, ...]:
        """Return entities connected to a risk theme."""

        return tuple(
            source
            for source, edges in self._edges.items()
            if any(edge.target == theme and edge.relationship in {RelationshipType.EXPOSED_TO, RelationshipType.HURT_BY} for edge in edges)
        )

    def evidence_for_document(self, document_id: UUID) -> tuple[GraphRelationship, ...]:
        return tuple(
            edge
            for edges in self._edges.values()
            for edge in edges
            if edge.evidence_document_id == document_id
        )

    def _relationship_for_sentiment(self, sentiment: Sentiment) -> RelationshipType:
        if sentiment is Sentiment.POSITIVE:
            return RelationshipType.BENEFITS_FROM
        if sentiment is Sentiment.NEGATIVE:
            return RelationshipType.HURT_BY
        return RelationshipType.AFFECTS
