"""High-level API for plotting NetworkX graphs in JupyterLab."""

import json
from typing import Any
from net_vis.models import Scene, GraphLayer
from net_vis.adapters.networkx import NetworkXAdapter


class Plotter:
    """Main API for visualizing NetworkX graphs in JupyterLab.

    Provides a simple interface to convert NetworkX graph objects into
    interactive visualizations using the netvis MIME renderer.
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
    ) -> str:
        """Add NetworkX graph as visualization layer.

        Args:
            graph: NetworkX graph object (Graph/DiGraph/MultiGraph/MultiDiGraph)
            layer_id: Custom layer ID (auto-generated if None)

        Returns:
            layer_id: ID of the added layer

        Raises:
            ValueError: If graph is invalid or layout computation fails
            TypeError: If graph is not a NetworkX graph type
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
        graph_layer = NetworkXAdapter.convert_graph(graph)
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
