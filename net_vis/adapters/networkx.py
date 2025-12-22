"""NetworkX graph adapter for converting to netvis data structures."""

from typing import Any, Callable
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
    def _extract_nodes(
        graph: Any,
        positions: dict[Any, tuple[float, float]],
        node_color: str | Callable | None = None,
        node_label: str | Callable | None = None,
    ) -> list[Node]:
        """Extract nodes from NetworkX graph with ID conversion to string.

        Args:
            graph: NetworkX graph object
            positions: Dictionary mapping node IDs to (x, y) positions
            node_color: Attribute name or function for color mapping
            node_label: Attribute name or function for label mapping

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

            # Apply color mapping
            color = NetworkXAdapter._map_node_color(node_id, node_attrs, node_color)

            # Apply label mapping
            label = NetworkXAdapter._map_node_label(node_id, node_attrs, node_label)

            # Create Node object
            node = Node(
                id=node_id_str,
                x=float(x),
                y=float(y),
                color=color,
                label=label,
                metadata=node_attrs
            )

            nodes.append(node)

        return nodes

    @staticmethod
    def _extract_edges(
        graph: Any,
        edge_label: str | Callable | None = None,
    ) -> list[Edge]:
        """Extract edges from NetworkX graph for basic Graph type.

        Args:
            graph: NetworkX graph object
            edge_label: Attribute name or function for label mapping

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

            # Apply label mapping
            label = NetworkXAdapter._map_edge_label(edge_attrs, edge_label)

            # Create Edge object
            edge = Edge(
                source=source_str,
                target=target_str,
                label=label,
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
    def convert_graph(
        graph: Any,
        node_color: str | Callable | None = None,
        node_label: str | Callable | None = None,
        edge_label: str | Callable | None = None,
    ) -> GraphLayer:
        """Convert NetworkX graph to GraphLayer with layout and styling.

        Args:
            graph: NetworkX graph object
            node_color: Attribute name or function for node color mapping
            node_label: Attribute name or function for node label mapping
            edge_label: Attribute name or function for edge label mapping

        Returns:
            GraphLayer object with nodes, edges, and metadata

        Raises:
            ValueError: If layout computation fails
        """
        # Detect graph type
        graph_type = NetworkXAdapter._detect_graph_type(graph)

        # Compute layout positions
        positions = NetworkXAdapter._compute_layout(graph)

        # Extract nodes with positions and styling
        nodes = NetworkXAdapter._extract_nodes(
            graph,
            positions,
            node_color=node_color,
            node_label=node_label,
        )

        # Extract edges with styling
        edges = NetworkXAdapter._extract_edges(
            graph,
            edge_label=edge_label,
        )

        # Create GraphLayer with metadata
        layer = GraphLayer(
            layer_id="",  # Will be set by Plotter
            nodes=nodes,
            edges=edges,
            metadata={"graph_type": graph_type}
        )

        return layer

    @staticmethod
    def _map_node_color(node_id: Any, node_data: dict, mapping: str | Callable | None) -> str | None:
        """Map node attribute to color value.

        Args:
            node_id: Node identifier
            node_data: Node attributes dictionary
            mapping: Attribute name (str) or function (node_data -> color_value)

        Returns:
            Color value (string) or None if not mapped
        """
        if mapping is None:
            return None

        if callable(mapping):
            # Call function with node_data
            try:
                result = mapping(node_data)
                return str(result) if result is not None else None
            except Exception:
                return None
        else:
            # mapping is attribute name (str)
            value = node_data.get(mapping)
            return str(value) if value is not None else None

    @staticmethod
    def _map_node_label(node_id: Any, node_data: dict, mapping: str | Callable | None) -> str | None:
        """Map node attribute to label value.

        Args:
            node_id: Node identifier
            node_data: Node attributes dictionary
            mapping: Attribute name (str) or function (node_data -> label_str)

        Returns:
            Label string or None if not mapped
        """
        if mapping is None:
            return None

        if callable(mapping):
            # Call function with node_data
            try:
                result = mapping(node_data)
                return str(result) if result is not None else None
            except Exception:
                return None
        else:
            # mapping is attribute name (str)
            value = node_data.get(mapping)
            return str(value) if value is not None else None

    @staticmethod
    def _map_edge_label(edge_data: dict, mapping: str | Callable | None) -> str | None:
        """Map edge attribute to label value.

        Args:
            edge_data: Edge attributes dictionary
            mapping: Attribute name (str) or function (edge_data -> label_str)

        Returns:
            Label string or None if not mapped
        """
        if mapping is None:
            return None

        if callable(mapping):
            # Call function with edge_data
            try:
                result = mapping(edge_data)
                return str(result) if result is not None else None
            except Exception:
                return None
        else:
            # mapping is attribute name (str)
            value = edge_data.get(mapping)
            return str(value) if value is not None else None

    @staticmethod
    def _detect_color_type(values: list) -> str:
        """Detect if color values are numeric or categorical.

        Args:
            values: List of color values

        Returns:
            'numeric' or 'categorical'
        """
        # Check if all non-None values are numeric
        numeric_count = 0
        total_count = 0

        for val in values:
            if val is not None:
                total_count += 1
                if isinstance(val, (int, float)):
                    numeric_count += 1

        # If majority are numeric, treat as numeric
        if total_count > 0 and numeric_count / total_count > 0.5:
            return 'numeric'
        return 'categorical'

    @staticmethod
    def _apply_continuous_color_scale(value: float, min_val: float, max_val: float) -> str:
        """Apply continuous color scale to numeric value.

        Args:
            value: Numeric value to map
            min_val: Minimum value in dataset
            max_val: Maximum value in dataset

        Returns:
            Hex color string
        """
        # Simple linear interpolation from blue to red
        if max_val == min_val:
            ratio = 0.5
        else:
            ratio = (value - min_val) / (max_val - min_val)

        # Clamp ratio to [0, 1]
        ratio = max(0.0, min(1.0, ratio))

        # Blue (0) to Red (1)
        red = int(255 * ratio)
        blue = int(255 * (1 - ratio))
        green = 0

        return f"#{red:02x}{green:02x}{blue:02x}"

    @staticmethod
    def _apply_categorical_color_palette(category: str) -> str:
        """Apply categorical color palette.

        Args:
            category: Category value

        Returns:
            Hex color string from palette
        """
        # D3.js Category10 palette
        palette = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ]

        # Use hash of category string to select color
        category_hash = hash(category)
        color_index = category_hash % len(palette)

        return palette[color_index]
