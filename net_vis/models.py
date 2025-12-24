"""Data models for graph visualization."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    """Represents a graph vertex with position and visual properties.

    Attributes:
        id: Unique node identifier (converted to string)
        label: Optional display label
        x: X-coordinate position
        y: Y-coordinate position
        color: Optional color value (hex string or color name)
        metadata: Additional node attributes from source graph
    """

    id: str
    label: str | None = None
    x: float = 0.0
    y: float = 0.0
    color: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    """Represents a graph edge with optional visual properties.

    Attributes:
        source: Source node ID
        target: Target node ID
        label: Optional display label
        weight: Optional edge weight
        metadata: Additional edge attributes from source graph
    """

    source: str
    target: str
    label: str | None = None
    weight: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphLayer:
    """Represents a single network visualization layer.

    Corresponds to one NetworkX graph object in a scene.

    Attributes:
        layer_id: Unique layer identifier
        nodes: List of nodes in this layer
        edges: List of edges in this layer
        metadata: Additional layer metadata
    """

    layer_id: str
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Scene:
    """Represents a complete visualization container.

    Top-level structure for JSON/HTML export, containing one or more graph layers.

    Attributes:
        layers: List of graph layers to visualize
        title: Optional scene title
        metadata: Additional scene metadata
    """

    layers: list[GraphLayer] = field(default_factory=list)
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert scene to dictionary format for MIME renderer.

        Returns:
            Dictionary representation compatible with netvis MIME renderer format.
        """
        # Combine all nodes and links from all layers
        all_nodes = []
        all_links = []

        for layer in self.layers:
            # Convert nodes to netvis format
            for node in layer.nodes:
                node_dict: dict[str, Any] = {
                    "id": node.id,
                    "x": node.x,
                    "y": node.y,
                }
                if node.label is not None:
                    node_dict["name"] = node.label
                if node.color is not None:
                    node_dict["category"] = node.color
                # Add metadata as additional fields
                node_dict.update(node.metadata)
                all_nodes.append(node_dict)

            # Convert edges to netvis format (links)
            for edge in layer.edges:
                link_dict: dict[str, Any] = {
                    "source": edge.source,
                    "target": edge.target,
                }
                if edge.label is not None:
                    link_dict["label"] = edge.label
                if edge.weight is not None:
                    link_dict["value"] = edge.weight
                # Add metadata as additional fields
                link_dict.update(edge.metadata)
                all_links.append(link_dict)

        result: dict[str, Any] = {
            "nodes": all_nodes,
            "links": all_links,
        }

        if self.title:
            result["title"] = self.title

        return result
