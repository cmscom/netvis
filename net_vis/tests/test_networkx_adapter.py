"""Tests for NetworkXAdapter conversion functionality."""

import pytest

# Skip all tests if networkx is not installed
pytest.importorskip("networkx")

import networkx as nx
from net_vis.adapters.networkx import NetworkXAdapter


class TestNetworkXAdapterConversion:
    """Tests for basic graph conversion."""

    def test_convert_graph_with_simple_graph(self):
        """Test NetworkXAdapter.convert_graph with simple nx.Graph."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G)

        assert layer is not None
        assert len(layer.nodes) == 3
        assert len(layer.edges) == 2
        assert layer.metadata["graph_type"] == "graph"

    def test_convert_graph_empty_graph(self):
        """Test NetworkXAdapter handles empty graph (0 nodes)."""
        G = nx.Graph()

        layer = NetworkXAdapter.convert_graph(G)

        assert layer is not None
        assert len(layer.nodes) == 0
        assert len(layer.edges) == 0


class TestNetworkXAdapterAttributes:
    """Tests for attribute preservation."""

    def test_preserves_node_attributes_in_metadata(self):
        """Test NetworkXAdapter preserves all node attributes in metadata."""
        G = nx.Graph()
        G.add_node(1, name="Node 1", value=10, category="A")
        G.add_node(2, name="Node 2", value=20, category="B")

        layer = NetworkXAdapter.convert_graph(G)

        node1 = next(n for n in layer.nodes if n.id == "1")
        assert node1.metadata == {"name": "Node 1", "value": 10, "category": "A"}

        node2 = next(n for n in layer.nodes if n.id == "2")
        assert node2.metadata == {"name": "Node 2", "value": 20, "category": "B"}

    def test_preserves_edge_attributes_in_metadata(self):
        """Test NetworkXAdapter preserves all edge attributes in metadata."""
        G = nx.Graph()
        G.add_edge(1, 2, weight=5.0, label="connects", type="strong")
        G.add_edge(2, 3, weight=3.0, label="links")

        layer = NetworkXAdapter.convert_graph(G)

        edge1 = next(e for e in layer.edges if e.source == "1" and e.target == "2")
        assert edge1.metadata == {"weight": 5.0, "label": "connects", "type": "strong"}

        edge2 = next(e for e in layer.edges if e.source == "2" and e.target == "3")
        assert edge2.metadata == {"weight": 3.0, "label": "links"}


class TestNetworkXAdapterLayout:
    """Tests for layout computation."""

    def test_applies_spring_layout_by_default(self):
        """Test NetworkXAdapter applies spring layout by default."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G)

        # Verify all nodes have non-zero positions (spring layout computed)
        for node in layer.nodes:
            # Positions should exist and be floats
            assert isinstance(node.x, float)
            assert isinstance(node.y, float)
            # At least some nodes should have non-zero positions
            # (spring layout spreads nodes out)

        # Verify at least one node has non-zero position
        has_nonzero = any(node.x != 0.0 or node.y != 0.0 for node in layer.nodes)
        assert has_nonzero


class TestNetworkXAdapterGraphTypes:
    """Tests for different NetworkX graph types."""

    def test_detect_graph_type_graph(self):
        """Test _detect_graph_type identifies Graph."""
        G = nx.Graph()
        graph_type = NetworkXAdapter._detect_graph_type(G)
        assert graph_type == "graph"

    def test_detect_graph_type_digraph(self):
        """Test _detect_graph_type identifies DiGraph."""
        G = nx.DiGraph()
        graph_type = NetworkXAdapter._detect_graph_type(G)
        assert graph_type == "digraph"

    def test_detect_graph_type_multigraph(self):
        """Test _detect_graph_type identifies MultiGraph."""
        G = nx.MultiGraph()
        graph_type = NetworkXAdapter._detect_graph_type(G)
        assert graph_type == "multigraph"

    def test_detect_graph_type_multidigraph(self):
        """Test _detect_graph_type identifies MultiDiGraph."""
        G = nx.MultiDiGraph()
        graph_type = NetworkXAdapter._detect_graph_type(G)
        assert graph_type == "multidigraph"


class TestNetworkXAdapterStyling:
    """Tests for node and edge styling."""

    def test_node_color_with_attribute_name(self):
        """Test node_color with attribute name (string)."""
        G = nx.Graph()
        G.add_node(1, color="red")
        G.add_node(2, color="blue")
        G.add_edge(1, 2)

        layer = NetworkXAdapter.convert_graph(G, node_color="color")

        node1 = next(n for n in layer.nodes if n.id == "1")
        assert node1.color == "red"

        node2 = next(n for n in layer.nodes if n.id == "2")
        assert node2.color == "blue"

    def test_node_color_with_callable_function(self):
        """Test node_color with callable function."""
        G = nx.Graph()
        G.add_node(1, value=10)
        G.add_node(2, value=20)
        G.add_edge(1, 2)

        def color_fn(node_data):
            return f"value_{node_data.get('value', 0)}"

        layer = NetworkXAdapter.convert_graph(G, node_color=color_fn)

        node1 = next(n for n in layer.nodes if n.id == "1")
        assert node1.color == "value_10"

        node2 = next(n for n in layer.nodes if n.id == "2")
        assert node2.color == "value_20"

    def test_node_label_with_attribute_name(self):
        """Test node_label with attribute name (string)."""
        G = nx.Graph()
        G.add_node(1, name="Alice")
        G.add_node(2, name="Bob")
        G.add_edge(1, 2)

        layer = NetworkXAdapter.convert_graph(G, node_label="name")

        node1 = next(n for n in layer.nodes if n.id == "1")
        assert node1.label == "Alice"

        node2 = next(n for n in layer.nodes if n.id == "2")
        assert node2.label == "Bob"

    def test_node_label_with_callable_function(self):
        """Test node_label with callable function."""
        G = nx.Graph()
        G.add_node(1, value=10)
        G.add_node(2, value=20)
        G.add_edge(1, 2)

        def label_fn(node_data):
            return f"Node {node_data.get('value', 0)}"

        layer = NetworkXAdapter.convert_graph(G, node_label=label_fn)

        node1 = next(n for n in layer.nodes if n.id == "1")
        assert node1.label == "Node 10"

    def test_edge_label_with_attribute_name(self):
        """Test edge_label with attribute name (string)."""
        G = nx.Graph()
        G.add_edge(1, 2, relation="friend")
        G.add_edge(2, 3, relation="colleague")

        layer = NetworkXAdapter.convert_graph(G, edge_label="relation")

        edge1 = next(e for e in layer.edges if e.source == "1" and e.target == "2")
        assert edge1.label == "friend"

        edge2 = next(e for e in layer.edges if e.source == "2" and e.target == "3")
        assert edge2.label == "colleague"

    def test_edge_label_with_callable_function(self):
        """Test edge_label with callable function."""
        G = nx.Graph()
        G.add_edge(1, 2, weight=5.0)
        G.add_edge(2, 3, weight=3.0)

        def label_fn(edge_data):
            return f"w={edge_data.get('weight', 0)}"

        layer = NetworkXAdapter.convert_graph(G, edge_label=label_fn)

        edge1 = next(e for e in layer.edges if e.source == "1" and e.target == "2")
        assert edge1.label == "w=5.0"

    def test_numeric_color_values_trigger_continuous_scale(self):
        """Test numeric color values trigger continuous scale."""
        values = [1.0, 2.0, 3.0, 4.0]
        color_type = NetworkXAdapter._detect_color_type(values)
        assert color_type == "numeric"

    def test_string_color_values_trigger_categorical_palette(self):
        """Test string color values trigger categorical palette."""
        values = ["red", "blue", "green"]
        color_type = NetworkXAdapter._detect_color_type(values)
        assert color_type == "categorical"

    def test_missing_attribute_uses_default_none(self):
        """Test missing attribute uses default (None) without error."""
        G = nx.Graph()
        G.add_node(1)  # No color attribute
        G.add_node(2, color="red")
        G.add_edge(1, 2)

        layer = NetworkXAdapter.convert_graph(G, node_color="color")

        node1 = next(n for n in layer.nodes if n.id == "1")
        assert node1.color is None  # Missing attribute

        node2 = next(n for n in layer.nodes if n.id == "2")
        assert node2.color == "red"
