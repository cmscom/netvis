"""NetworkX graph adapter for converting to netvis data structures."""

import warnings
from collections.abc import Callable
from typing import Any

import networkx as nx

from ..models import Edge, GraphLayer, Node


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

        if "multidigraph" in class_name:
            return "multidigraph"
        elif "multigraph" in class_name:
            return "multigraph"
        elif "digraph" in class_name:
            return "digraph"
        else:
            return "graph"

    @staticmethod
    def _extract_nodes(
        graph: Any,
        positions: dict[Any, Any],
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
                metadata=node_attrs,
            )

            nodes.append(node)

        return nodes

    @staticmethod
    def _extract_edges(
        graph: Any,
        edge_label: str | Callable | None = None,
    ) -> list[Edge]:
        """Extract edges from NetworkX graph with automatic type dispatch.

        Args:
            graph: NetworkX graph object
            edge_label: Attribute name or function for label mapping

        Returns:
            List of Edge objects with metadata
        """
        # Detect graph type and dispatch to appropriate extractor
        graph_type = NetworkXAdapter._detect_graph_type(graph)

        if graph_type in ("multigraph", "multidigraph"):
            return NetworkXAdapter._expand_multigraph_edges(graph, edge_label)
        elif graph_type == "digraph":
            return NetworkXAdapter._extract_edges_digraph(graph, edge_label)
        else:
            # Basic Graph type
            return NetworkXAdapter._extract_edges_simple(graph, edge_label)

    @staticmethod
    def _extract_edges_simple(
        graph: Any,
        edge_label: str | Callable | None = None,
    ) -> list[Edge]:
        """Extract edges from NetworkX Graph (undirected, simple).

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
            edge = Edge(source=source_str, target=target_str, label=label, metadata=edge_attrs)

            edges.append(edge)

        return edges

    @staticmethod
    def _extract_edges_digraph(
        graph: Any,
        edge_label: str | Callable | None = None,
    ) -> list[Edge]:
        """Extract edges from NetworkX DiGraph (directed).

        Args:
            graph: NetworkX DiGraph object
            edge_label: Attribute name or function for label mapping

        Returns:
            List of Edge objects with direction preserved in metadata
        """
        edges = []

        for source, target in graph.edges():
            # Convert node IDs to strings
            source_str = str(source)
            target_str = str(target)

            # Get edge attributes and preserve them in metadata
            edge_attrs = dict(graph[source][target]) if graph[source][target] else {}

            # Add direction indicator to metadata for DiGraph
            edge_attrs["directed"] = True

            # Apply label mapping
            label = NetworkXAdapter._map_edge_label(edge_attrs, edge_label)

            # Create Edge object
            edge = Edge(source=source_str, target=target_str, label=label, metadata=edge_attrs)

            edges.append(edge)

        return edges

    @staticmethod
    def _expand_multigraph_edges(
        graph: Any,
        edge_label: str | Callable | None = None,
    ) -> list[Edge]:
        """Extract and expand edges from NetworkX MultiGraph/MultiDiGraph.

        Multiple edges between the same pair of nodes are expanded into
        independent Edge objects, with edge keys preserved in metadata.

        Args:
            graph: NetworkX MultiGraph or MultiDiGraph object
            edge_label: Attribute name or function for label mapping

        Returns:
            List of Edge objects with edge keys preserved in metadata
        """
        edges = []

        # Check if this is a directed multigraph
        graph_type = NetworkXAdapter._detect_graph_type(graph)
        is_directed = graph_type == "multidigraph"

        # MultiGraph.edges() returns (source, target, key) tuples
        for source, target, key in graph.edges(keys=True):
            # Convert node IDs to strings
            source_str = str(source)
            target_str = str(target)

            # Get edge attributes for this specific edge key
            edge_attrs = dict(graph[source][target][key]) if graph[source][target][key] else {}

            # Preserve edge key in metadata
            edge_attrs["edge_key"] = key

            # Add direction indicator for MultiDiGraph
            if is_directed:
                edge_attrs["directed"] = True

            # Apply label mapping
            label = NetworkXAdapter._map_edge_label(edge_attrs, edge_label)

            # Create Edge object
            edge = Edge(source=source_str, target=target_str, label=label, metadata=edge_attrs)

            edges.append(edge)

        return edges

    @staticmethod
    def _get_existing_positions(graph: Any) -> dict[Any, Any] | None:
        """Extract existing 'pos' attribute from nodes.

        Args:
            graph: NetworkX graph object

        Returns:
            Dictionary mapping node IDs to (x, y) positions, or None if not available
        """
        positions = {}
        has_positions = False

        for node_id in graph.nodes():
            node_data = graph.nodes[node_id]
            if "pos" in node_data:
                positions[node_id] = node_data["pos"]
                has_positions = True

        return positions if has_positions else None

    @staticmethod
    def _apply_spring_layout(graph: Any) -> dict[Any, Any]:
        """Apply spring (force-directed) layout.

        Args:
            graph: NetworkX graph object

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        return nx.spring_layout(graph)

    @staticmethod
    def _apply_kamada_kawai_layout(graph: Any) -> dict[Any, Any]:
        """Apply Kamada-Kawai layout.

        Args:
            graph: NetworkX graph object

        Returns:
            Dictionary mapping node IDs to (x, y) positions

        Raises:
            ImportError: If scipy is not installed
        """
        try:
            import scipy  # type: ignore[import-not-found]  # noqa: F401
        except ImportError:
            raise ImportError(
                "Layout 'kamada_kawai' requires scipy. Install with: pip install net_vis[full]"
            )

        return nx.kamada_kawai_layout(graph)

    @staticmethod
    def _apply_spectral_layout(graph: Any) -> dict[Any, Any]:
        """Apply spectral layout.

        Args:
            graph: NetworkX graph object

        Returns:
            Dictionary mapping node IDs to (x, y) positions

        Raises:
            ImportError: If scipy is not installed
        """
        try:
            import scipy  # type: ignore[import-not-found]  # noqa: F401
        except ImportError:
            raise ImportError(
                "Layout 'spectral' requires scipy. Install with: pip install net_vis[full]"
            )

        return nx.spectral_layout(graph)

    @staticmethod
    def _apply_circular_layout(graph: Any) -> dict[Any, Any]:
        """Apply circular layout.

        Args:
            graph: NetworkX graph object

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        return nx.circular_layout(graph)

    @staticmethod
    def _apply_random_layout(graph: Any) -> dict[Any, Any]:
        """Apply random layout.

        Args:
            graph: NetworkX graph object

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        return nx.random_layout(graph)

    @staticmethod
    def _apply_custom_layout(graph: Any, layout_func: Callable) -> dict[Any, Any]:
        """Apply custom layout function.

        Args:
            graph: NetworkX graph object
            layout_func: Custom function that takes graph and returns position dict

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        return layout_func(graph)

    @staticmethod
    def _validate_positions(positions: dict[Any, Any]) -> bool:
        """Validate that positions don't contain NaN or inf values.

        Args:
            positions: Dictionary mapping node IDs to (x, y) positions

        Returns:
            True if valid, False otherwise
        """
        import math

        for node_id, (x, y) in positions.items():
            if math.isnan(x) or math.isnan(y) or math.isinf(x) or math.isinf(y):
                return False
        return True

    @staticmethod
    def _compute_layout(graph: Any, layout: str | Callable | None = None) -> dict[Any, Any]:
        """Compute node positions using specified layout algorithm.

        Args:
            graph: NetworkX graph object
            layout: Layout algorithm name, custom function, or None

        Returns:
            Dictionary mapping node IDs to (x, y) positions
        """
        # Handle empty graphs
        if len(graph.nodes()) == 0:
            return {}

        # Determine which layout to use
        positions = None

        if layout is None:
            # Try to use existing 'pos' attribute, fall back to spring
            positions = NetworkXAdapter._get_existing_positions(graph)
            if positions is None:
                try:
                    positions = NetworkXAdapter._apply_spring_layout(graph)
                except Exception as e:
                    warnings.warn(f"Spring layout failed: {e}, falling back to random layout")
                    positions = NetworkXAdapter._apply_random_layout(graph)
        elif callable(layout):
            # Custom layout function
            try:
                positions = NetworkXAdapter._apply_custom_layout(graph, layout)
            except Exception as e:
                warnings.warn(f"Custom layout failed: {e}, falling back to random layout")
                positions = NetworkXAdapter._apply_random_layout(graph)
        else:
            # Named layout algorithm
            layout_str = str(layout).lower()
            try:
                if layout_str == "spring":
                    positions = NetworkXAdapter._apply_spring_layout(graph)
                elif layout_str == "kamada_kawai":
                    positions = NetworkXAdapter._apply_kamada_kawai_layout(graph)
                elif layout_str == "spectral":
                    positions = NetworkXAdapter._apply_spectral_layout(graph)
                elif layout_str == "circular":
                    positions = NetworkXAdapter._apply_circular_layout(graph)
                elif layout_str == "random":
                    positions = NetworkXAdapter._apply_random_layout(graph)
                else:
                    warnings.warn(f"Unknown layout '{layout}', using spring layout")
                    positions = NetworkXAdapter._apply_spring_layout(graph)
            except Exception as e:
                warnings.warn(f"Layout '{layout}' failed: {e}, falling back to random layout")
                positions = NetworkXAdapter._apply_random_layout(graph)

        # Validate positions
        if not NetworkXAdapter._validate_positions(positions):
            warnings.warn(
                "Layout produced invalid positions (NaN/inf), falling back to random layout"
            )
            positions = NetworkXAdapter._apply_random_layout(graph)

        return positions

    @staticmethod
    def convert_graph(
        graph: Any,
        layout: str | Callable | None = None,
        node_color: str | Callable | None = None,
        node_label: str | Callable | None = None,
        edge_label: str | Callable | None = None,
    ) -> GraphLayer:
        """Convert NetworkX graph to GraphLayer with layout and styling.

        Args:
            graph: NetworkX graph object
            layout: Layout algorithm name, custom function, or None
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
        positions = NetworkXAdapter._compute_layout(graph, layout=layout)

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
            metadata={"graph_type": graph_type},
        )

        return layer

    @staticmethod
    def _map_node_color(
        node_id: Any, node_data: dict, mapping: str | Callable | None
    ) -> str | None:
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
    def _map_node_label(
        node_id: Any, node_data: dict, mapping: str | Callable | None
    ) -> str | None:
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
            return "numeric"
        return "categorical"

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
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]

        # Use hash of category string to select color
        category_hash = hash(category)
        color_index = category_hash % len(palette)

        return palette[color_index]
