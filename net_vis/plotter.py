"""High-level API for plotting NetworkX graphs in JupyterLab."""

import json
from typing import Any, Callable
from net_vis.models import Scene, GraphLayer
from net_vis.adapters.networkx import NetworkXAdapter


class Plotter:
    """Main API for visualizing NetworkX graphs in JupyterLab.

    Provides a simple interface to convert NetworkX graph objects into
    interactive visualizations using the netvis MIME renderer. Supports
    all NetworkX graph types (Graph, DiGraph, MultiGraph, MultiDiGraph)
    with automatic attribute preservation and customizable styling.

    Examples:
        Basic visualization:
            >>> from net_vis import Plotter
            >>> import networkx as nx
            >>> G = nx.karate_club_graph()
            >>> plotter = Plotter(title="Karate Club")
            >>> plotter.add_networkx(G)

        Custom styling with attribute mapping:
            >>> plotter = Plotter()
            >>> plotter.add_networkx(
            ...     G,
            ...     node_color="club",
            ...     node_label="name",
            ...     layout='kamada_kawai'
            ... )

        Custom styling with functions:
            >>> plotter.add_networkx(
            ...     G,
            ...     node_color=lambda d: f"group_{d.get('club', 0)}",
            ...     node_label=lambda d: f"Node {d.get('id', '')}",
            ...     edge_label=lambda d: f"w={d.get('weight', 1.0)}"
            ... )

    Attributes:
        _scene: Internal Scene object containing all visualization layers
        _layer_counter: Counter for auto-generating unique layer IDs
    """

    def __init__(self, title: str | None = None) -> None:
        """Initialize plotter with optional scene title.

        Args:
            title: Optional title for the visualization scene
        """
        self._scene = Scene(title=title)
        self._layer_counter = 0

    def _generate_layer_id(self) -> str:
        """Generate unique layer ID.

        Returns:
            Unique layer identifier string
        """
        layer_id = f"layer_{self._layer_counter}"
        self._layer_counter += 1
        return layer_id

    def add_networkx(
        self,
        graph: Any,
        *,
        layer_id: str | None = None,
        layout: str | Callable | None = None,
        node_color: str | Callable | None = None,
        node_label: str | Callable | None = None,
        edge_label: str | Callable | None = None,
    ) -> str:
        """Add NetworkX graph as visualization layer.

        Converts a NetworkX graph to a visualization layer with automatic
        node/edge extraction, layout computation, and styling. Supports all
        NetworkX graph types with automatic type detection.

        Args:
            graph: NetworkX graph object (Graph/DiGraph/MultiGraph/MultiDiGraph).
                All node and edge attributes are preserved in metadata.
            layer_id: Custom layer ID (auto-generated if None).
            layout: Layout algorithm or custom function:
                - 'spring': Force-directed layout (default)
                - 'kamada_kawai': Kamada-Kawai path-length cost minimization
                - 'spectral': Spectral layout using graph Laplacian
                - 'circular': Nodes arranged in a circle
                - 'random': Random node positions
                - callable: Custom function(graph) -> dict[node_id, (x, y)]
                - None: Use existing 'pos' attribute or fall back to spring
            node_color: Node color mapping:
                - str: Attribute name to use for color values
                - callable: Function(node_data) -> color_value
                - None: No color mapping (default)
            node_label: Node label mapping:
                - str: Attribute name to use for labels
                - callable: Function(node_data) -> label_string
                - None: No label mapping (default)
            edge_label: Edge label mapping:
                - str: Attribute name to use for labels
                - callable: Function(edge_data) -> label_string
                - None: No label mapping (default)

        Returns:
            str: ID of the added layer (auto-generated or custom)

        Raises:
            TypeError: If graph is not a NetworkX graph object
            ValueError: If layout computation fails

        Examples:
            Basic usage:
                >>> plotter = Plotter()
                >>> G = nx.karate_club_graph()
                >>> layer_id = plotter.add_networkx(G)

            With layout control:
                >>> plotter.add_networkx(G, layout='kamada_kawai')

            With attribute-based styling:
                >>> G.nodes[0]['color'] = 'red'
                >>> plotter.add_networkx(G, node_color='color')

            With function-based styling:
                >>> plotter.add_networkx(
                ...     G,
                ...     node_color=lambda d: 'red' if d.get('club') == 0 else 'blue',
                ...     node_label=lambda d: f"Node {d.get('id', '')}"
                ... )

        Notes:
            - All graph types (Graph, DiGraph, MultiGraph, MultiDiGraph) are supported
            - DiGraph edges include 'directed': True in metadata
            - MultiGraph edges include 'edge_key' in metadata
            - Multiple edges are expanded to independent Edge objects
            - NaN/inf positions trigger automatic fallback to random layout
        """
        # Validate input is a NetworkX graph
        if not hasattr(graph, 'nodes') or not hasattr(graph, 'edges'):
            raise TypeError(
                f"Expected NetworkX graph object, got {type(graph).__name__}"
            )

        # Generate layer ID if not provided
        if layer_id is None:
            layer_id = self._generate_layer_id()

        # Convert NetworkX graph to GraphLayer using adapter
        graph_layer = NetworkXAdapter.convert_graph(
            graph,
            layout=layout,
            node_color=node_color,
            node_label=node_label,
            edge_label=edge_label,
        )
        graph_layer.layer_id = layer_id

        # Add layer to scene
        self._scene.layers.append(graph_layer)

        return layer_id

    def to_json(self) -> str:
        """Export scene structure as JSON string.

        Returns:
            JSON string representation of the scene
        """
        scene_dict = self._scene.to_dict()
        return json.dumps(scene_dict, indent=2)

    def _repr_mimebundle_(self, include=None, exclude=None) -> dict:
        """Return MIME bundle for IPython/JupyterLab display.

        Args:
            include: Optional list of MIME types to include
            exclude: Optional list of MIME types to exclude

        Returns:
            Dictionary mapping MIME types to content
        """
        scene_dict = self._scene.to_dict()

        return {
            "application/vnd.netvis+json": scene_dict,
            "text/plain": f"<Plotter with {len(self._scene.layers)} layer(s)>"
        }
