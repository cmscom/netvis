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
