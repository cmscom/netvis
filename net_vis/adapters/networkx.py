"""NetworkX graph adapter for converting to netvis data structures."""

from typing import Any
from net_vis.models import Node, Edge, GraphLayer


class NetworkXAdapter:
    """Converts NetworkX graph objects to netvis GraphLayer format.

    Handles node/edge extraction, attribute preservation, layout computation,
    and visual property mapping for all NetworkX graph types (Graph, DiGraph,
    MultiGraph, MultiDiGraph).
    """

    @staticmethod
    def _detect_graph_type(graph: Any) -> str:
        """Detect NetworkX graph type.

        Args:
            graph: NetworkX graph object

        Returns:
            Graph type string: 'graph', 'digraph', 'multigraph', 'multidigraph'
        """
        # Check class name to determine type
        class_name = type(graph).__name__.lower()

        if 'multidigraph' in class_name:
            return 'multidigraph'
        elif 'multigraph' in class_name:
            return 'multigraph'
        elif 'digraph' in class_name:
            return 'digraph'
        else:
            return 'graph'

    @staticmethod
    def _extract_nodes(graph: Any, positions: dict[Any, tuple[float, float]]) -> list[Node]:
        """Extract nodes from NetworkX graph with ID conversion to string.

        Args:
            graph: NetworkX graph object
            positions: Dictionary mapping node IDs to (x, y) positions

        Returns:
            List of Node objects with positions and metadata
        """
        nodes = []

        for node_id in graph.nodes():
            # Convert node ID to string
            node_id_str = str(node_id)

            # Get position from layout (default to (0, 0) if missing)
            x, y = positions.get(node_id, (0.0, 0.0))

            # Get node attributes and preserve them in metadata
            node_attrs = dict(graph.nodes[node_id]) if graph.nodes[node_id] else {}

            # Create Node object
            node = Node(
                id=node_id_str,
                x=float(x),
                y=float(y),
                metadata=node_attrs
            )

            nodes.append(node)

        return nodes

    @staticmethod
    def _extract_edges(graph: Any) -> list[Edge]:
        """Extract edges from NetworkX graph for basic Graph type.

        Args:
            graph: NetworkX graph object

        Returns:
            List of Edge objects with metadata
        """
        edges = []

        for source, target in graph.edges():
            # Convert node IDs to strings
            source_str = str(source)
            target_str = str(target)

            # Get edge attributes and preserve them in metadata
            edge_attrs = dict(graph[source][target]) if graph[source][target] else {}

            # Create Edge object
            edge = Edge(
                source=source_str,
                target=target_str,
                metadata=edge_attrs
            )

            edges.append(edge)

        return edges

    @staticmethod
    def _compute_layout(graph: Any) -> dict[Any, tuple[float, float]]:
        """Compute node positions using spring layout by default.

        Args:
            graph: NetworkX graph object

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        # Import networkx here to avoid import errors if not installed
        try:
            import networkx as nx
        except ImportError:
            raise ImportError(
                "NetworkX is required for graph layout computation. "
                "Install it with: pip install networkx"
            )

        # Handle empty graphs
        if len(graph.nodes()) == 0:
            return {}

        # Use spring layout as default
        try:
            positions = nx.spring_layout(graph)
            return positions
        except Exception as e:
            # If spring layout fails, raise ValueError
            raise ValueError(f"Layout computation failed: {e}") from e

    @staticmethod
    def convert_graph(graph: Any) -> GraphLayer:
        """Convert NetworkX graph to GraphLayer with layout and styling.

        Args:
            graph: NetworkX graph object

        Returns:
            GraphLayer object with nodes, edges, and metadata

        Raises:
            ValueError: If layout computation fails
        """
        # Detect graph type
        graph_type = NetworkXAdapter._detect_graph_type(graph)

        # Compute layout positions
        positions = NetworkXAdapter._compute_layout(graph)

        # Extract nodes with positions
        nodes = NetworkXAdapter._extract_nodes(graph, positions)

        # Extract edges
        edges = NetworkXAdapter._extract_edges(graph)

        # Create GraphLayer with metadata
        layer = GraphLayer(
            layer_id="",  # Will be set by Plotter
            nodes=nodes,
            edges=edges,
            metadata={"graph_type": graph_type}
        )

        return layer
