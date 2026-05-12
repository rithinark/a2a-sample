"""In-memory graph abstraction mirroring the Neo4j knowledge model."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from financial_ai.shared.models import ExtractedEvent, Relationship


@dataclass
class KnowledgeGraph:
    """Small graph facade for local reasoning and testability."""

    nodes: dict[str, dict[str, str]] = field(default_factory=dict)
    edges: dict[str, list[Relationship]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def apply_event(self, event: ExtractedEvent) -> None:
        event_node = f"event:{event.document_id}"
        self.nodes[event_node] = {"kind": "event", "event_type": event.event_type.value}
        for entity in event.entities:
            self.nodes[entity.name] = {
                "kind": entity.kind,
                "ticker": entity.ticker or "",
            }
            self.edges[entity.name].append(
                Relationship(entity.name, "MENTIONS", event_node, event.confidence)
            )
        for relationship in event.relationships:
            self.edges[relationship.source].append(relationship)

    def related(self, node: str, relation: str | None = None) -> list[Relationship]:
        relationships = self.edges.get(node, [])
        if relation is None:
            return list(relationships)
        return [edge for edge in relationships if edge.relation == relation]
