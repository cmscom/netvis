"""Tests for Plotter class public API."""

import pytest

# Skip all tests if networkx is not installed
pytest.importorskip("networkx")

import networkx as nx
from net_vis import Plotter


class TestPlotterInit:
    """Tests for Plotter initialization."""

    def test_init_without_title(self):
        """Test Plotter.__init__ without title."""
        plotter = Plotter()
        assert plotter._scene is not None
        assert plotter._scene.title is None
        assert plotter._layer_counter == 0

    def test_init_with_title(self):
        """Test Plotter.__init__ with optional title."""
        plotter = Plotter(title="Test Graph")
        assert plotter._scene is not None
        assert plotter._scene.title == "Test Graph"
        assert plotter._layer_counter == 0


class TestPlotterAddNetworkX:
    """Tests for Plotter.add_networkx method."""

    def test_add_networkx_accepts_graph(self):
        """Test Plotter.add_networkx accepts nx.Graph."""
        plotter = Plotter()
        G = nx.Graph()
        G.add_edge(1, 2)

        layer_id = plotter.add_networkx(G)
        assert layer_id is not None
        assert isinstance(layer_id, str)

    def test_add_networkx_returns_layer_id(self):
        """Test Plotter.add_networkx returns layer_id."""
        plotter = Plotter()
        G = nx.Graph()
        G.add_edge(1, 2)

        layer_id = plotter.add_networkx(G)
        assert layer_id == "layer_0"

        # Add another graph
        layer_id2 = plotter.add_networkx(G)
        assert layer_id2 == "layer_1"

    def test_add_networkx_with_custom_layer_id(self):
        """Test Plotter.add_networkx with custom layer_id."""
        plotter = Plotter()
        G = nx.Graph()
        G.add_edge(1, 2)

        layer_id = plotter.add_networkx(G, layer_id="custom_layer")
        assert layer_id == "custom_layer"

    def test_add_networkx_invalid_type_raises_typeerror(self):
        """Test Plotter.add_networkx raises TypeError for non-NetworkX objects."""
        plotter = Plotter()

        with pytest.raises(TypeError, match="Expected NetworkX graph object"):
            plotter.add_networkx("not a graph")

        with pytest.raises(TypeError, match="Expected NetworkX graph object"):
            plotter.add_networkx({"nodes": [], "edges": []})


class TestPlotterReprMimeBundle:
    """Tests for Plotter._repr_mimebundle_ method."""

    def test_repr_mimebundle_returns_dict(self):
        """Test Plotter._repr_mimebundle_ returns dict with application/vnd.netvis+json."""
        plotter = Plotter()
        G = nx.Graph()
        G.add_edge(1, 2)
        plotter.add_networkx(G)

        bundle = plotter._repr_mimebundle_()
        assert isinstance(bundle, dict)
        assert "application/vnd.netvis+json" in bundle
        assert "text/plain" in bundle

    def test_repr_mimebundle_contains_valid_data(self):
        """Test _repr_mimebundle_ contains valid netvis JSON data."""
        plotter = Plotter()
        G = nx.Graph()
        G.add_edge(1, 2)
        plotter.add_networkx(G)

        bundle = plotter._repr_mimebundle_()
        data = bundle["application/vnd.netvis+json"]

        assert "nodes" in data
        assert "links" in data
        assert len(data["nodes"]) == 2  # Nodes 1 and 2
        assert len(data["links"]) == 1  # Edge 1-2


class TestPlotterIntegration:
    """Integration tests for Plotter with real NetworkX graphs."""

    def test_plotter_with_karate_club_graph(self):
        """Test Plotter with nx.karate_club_graph integration."""
        plotter = Plotter(title="Karate Club")
        G = nx.karate_club_graph()

        layer_id = plotter.add_networkx(G)

        assert layer_id == "layer_0"
        assert len(plotter._scene.layers) == 1

        bundle = plotter._repr_mimebundle_()
        data = bundle["application/vnd.netvis+json"]

        # Karate club has 34 nodes and 78 edges
        assert len(data["nodes"]) == 34
        assert len(data["links"]) == 78

    def test_plotter_to_json(self):
        """Test Plotter.to_json returns valid JSON string."""
        plotter = Plotter()
        G = nx.Graph()
        G.add_edge(1, 2)
        plotter.add_networkx(G)

        json_str = plotter.to_json()
        assert isinstance(json_str, str)
        assert "nodes" in json_str
        assert "links" in json_str

        # Verify it's valid JSON
        import json
        data = json.loads(json_str)
        assert "nodes" in data
        assert "links" in data


class TestPlotterStyling:
    """Tests for Plotter styling parameters."""

    def test_add_networkx_with_all_styling_parameters(self):
        """Test Plotter.add_networkx with all styling parameters."""
        plotter = Plotter()
        G = nx.Graph()
        G.add_node(1, color="red", name="Node A")
        G.add_node(2, color="blue", name="Node B")
        G.add_edge(1, 2, relation="connects")

        layer_id = plotter.add_networkx(
            G,
            node_color="color",
            node_label="name",
            edge_label="relation",
        )

        assert layer_id == "layer_0"
        bundle = plotter._repr_mimebundle_()
        data = bundle["application/vnd.netvis+json"]

        # Verify nodes have colors and labels
        assert len(data["nodes"]) == 2
        node1 = next(n for n in data["nodes"] if n["id"] == "1")
        assert node1["category"] == "red"
        assert node1["name"] == "Node A"

        # Verify edges have labels
        assert len(data["links"]) == 1
        assert data["links"][0]["label"] == "connects"
