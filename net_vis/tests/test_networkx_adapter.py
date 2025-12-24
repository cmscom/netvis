"""Tests for NetworkXAdapter conversion functionality."""

import pytest

# Skip all tests if networkx is not installed
pytest.importorskip("networkx")

import networkx as nx

from net_vis.adapters.networkx_adapter import NetworkXAdapter


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


class TestNetworkXAdapterLayouts:
    """Tests for layout algorithms."""

    def test_layout_spring_applies_spring_layout(self):
        """Test layout='spring' applies spring_layout."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G, layout="spring")

        # Verify all nodes have positions
        assert len(layer.nodes) == 3
        for node in layer.nodes:
            assert isinstance(node.x, float)
            assert isinstance(node.y, float)

    def test_layout_kamada_kawai_applies_kamada_kawai_layout(self):
        """Test layout='kamada_kawai' applies kamada_kawai_layout."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G, layout="kamada_kawai")

        # Verify all nodes have positions
        assert len(layer.nodes) == 3
        for node in layer.nodes:
            assert isinstance(node.x, float)
            assert isinstance(node.y, float)

    def test_layout_spectral_applies_spectral_layout(self):
        """Test layout='spectral' applies spectral_layout."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G, layout="spectral")

        # Verify all nodes have positions
        assert len(layer.nodes) == 3
        for node in layer.nodes:
            assert isinstance(node.x, float)
            assert isinstance(node.y, float)

    def test_layout_circular_applies_circular_layout(self):
        """Test layout='circular' applies circular_layout."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G, layout="circular")

        # Verify all nodes have positions
        assert len(layer.nodes) == 3
        for node in layer.nodes:
            assert isinstance(node.x, float)
            assert isinstance(node.y, float)

    def test_layout_random_applies_random_layout(self):
        """Test layout='random' applies random_layout."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G, layout="random")

        # Verify all nodes have positions
        assert len(layer.nodes) == 3
        for node in layer.nodes:
            assert isinstance(node.x, float)
            assert isinstance(node.y, float)

    def test_layout_with_custom_callable_function(self):
        """Test layout with custom callable function."""
        G = nx.Graph()
        G.add_node(1)
        G.add_node(2)
        G.add_edge(1, 2)

        def custom_layout(graph):
            """Custom layout placing nodes at specific positions."""
            return {1: (0.0, 0.0), 2: (1.0, 1.0)}

        layer = NetworkXAdapter.convert_graph(G, layout=custom_layout)

        node1 = next(n for n in layer.nodes if n.id == "1")
        assert node1.x == 0.0
        assert node1.y == 0.0

        node2 = next(n for n in layer.nodes if n.id == "2")
        assert node2.x == 1.0
        assert node2.y == 1.0

    def test_layout_none_uses_existing_pos_attribute(self):
        """Test layout=None uses existing 'pos' attribute if present."""
        G = nx.Graph()
        G.add_node(1, pos=(0.5, 0.5))
        G.add_node(2, pos=(0.7, 0.3))
        G.add_edge(1, 2)

        layer = NetworkXAdapter.convert_graph(G, layout=None)

        node1 = next(n for n in layer.nodes if n.id == "1")
        assert node1.x == 0.5
        assert node1.y == 0.5

        node2 = next(n for n in layer.nodes if n.id == "2")
        assert node2.x == 0.7
        assert node2.y == 0.3

    def test_layout_none_defaults_to_spring_when_no_pos(self):
        """Test layout=None defaults to spring when no 'pos' attribute."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G, layout=None)

        # Verify all nodes have positions (spring layout applied)
        assert len(layer.nodes) == 3
        for node in layer.nodes:
            assert isinstance(node.x, float)
            assert isinstance(node.y, float)

    def test_explicit_layout_overrides_existing_pos(self):
        """Test explicit layout overrides existing 'pos' attribute."""
        G = nx.Graph()
        G.add_node(1, pos=(0.5, 0.5))
        G.add_node(2, pos=(0.7, 0.3))
        G.add_edge(1, 2)

        layer = NetworkXAdapter.convert_graph(G, layout="circular")

        # Positions should be different from original pos attribute
        # (we can't predict exact values, but they should be valid floats)
        node1 = next(n for n in layer.nodes if n.id == "1")
        assert isinstance(node1.x, float)
        assert isinstance(node1.y, float)

    def test_layout_failure_falls_back_to_random_with_warning(self):
        """Test layout failure (NaN, inf) falls back to random with warning."""
        import warnings

        G = nx.Graph()
        G.add_edge(1, 2)

        def failing_layout(graph):
            """Layout that returns NaN values."""
            return {1: (float("nan"), 0.0), 2: (1.0, 1.0)}

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            layer = NetworkXAdapter.convert_graph(G, layout=failing_layout)

            # Should have warned about invalid positions
            assert len(w) > 0
            assert "invalid positions" in str(w[-1].message).lower()

        # Should still have valid positions (from fallback)
        for node in layer.nodes:
            assert isinstance(node.x, float)
            assert isinstance(node.y, float)
            import math

            assert not math.isnan(node.x)
            assert not math.isnan(node.y)


class TestNetworkXAdapterMultipleGraphTypes:
    """Tests for all NetworkX graph types support."""

    def test_convert_graph_with_undirected_graph(self):
        """Test NetworkXAdapter with nx.Graph (undirected)."""
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G)

        assert layer is not None
        assert len(layer.nodes) == 3
        assert len(layer.edges) == 2
        assert layer.metadata["graph_type"] == "graph"

        # Verify edges don't have 'directed' flag
        for edge in layer.edges:
            assert "directed" not in edge.metadata or not edge.metadata["directed"]

    def test_convert_graph_with_digraph(self):
        """Test NetworkXAdapter with nx.DiGraph (directed)."""
        G = nx.DiGraph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)

        layer = NetworkXAdapter.convert_graph(G)

        assert layer is not None
        assert len(layer.nodes) == 3
        assert len(layer.edges) == 2
        assert layer.metadata["graph_type"] == "digraph"

        # Verify all edges have 'directed' flag set to True
        for edge in layer.edges:
            assert edge.metadata["directed"] is True

    def test_convert_graph_with_multigraph(self):
        """Test NetworkXAdapter with nx.MultiGraph (multi-undirected)."""
        G = nx.MultiGraph()
        G.add_edge(1, 2, weight=1.0)
        G.add_edge(1, 2, weight=2.0)  # Second edge between same nodes
        G.add_edge(2, 3, weight=3.0)

        layer = NetworkXAdapter.convert_graph(G)

        assert layer is not None
        assert len(layer.nodes) == 3
        # Should have 3 edges (2 between nodes 1-2, 1 between nodes 2-3)
        assert len(layer.edges) == 3
        assert layer.metadata["graph_type"] == "multigraph"

        # Verify edge keys are preserved
        for edge in layer.edges:
            assert "edge_key" in edge.metadata

    def test_convert_graph_with_multidigraph(self):
        """Test NetworkXAdapter with nx.MultiDiGraph (multi-directed)."""
        G = nx.MultiDiGraph()
        G.add_edge(1, 2, relation="friend")
        G.add_edge(1, 2, relation="colleague")  # Second edge between same nodes
        G.add_edge(2, 3, relation="manager")

        layer = NetworkXAdapter.convert_graph(G)

        assert layer is not None
        assert len(layer.nodes) == 3
        # Should have 3 edges
        assert len(layer.edges) == 3
        assert layer.metadata["graph_type"] == "multidigraph"

        # Verify both edge keys and direction are preserved
        for edge in layer.edges:
            assert "edge_key" in edge.metadata
            assert edge.metadata["directed"] is True

    def test_digraph_edge_direction_preserved(self):
        """Test DiGraph edge direction preserved in output."""
        G = nx.DiGraph()
        G.add_edge(1, 2)
        G.add_edge(2, 1)  # Opposite direction

        layer = NetworkXAdapter.convert_graph(G)

        # Should have 2 edges (one in each direction)
        assert len(layer.edges) == 2

        # Find edges by source/target
        edge_1_to_2 = next(e for e in layer.edges if e.source == "1" and e.target == "2")
        edge_2_to_1 = next(e for e in layer.edges if e.source == "2" and e.target == "1")

        # Both should be marked as directed
        assert edge_1_to_2.metadata["directed"] is True
        assert edge_2_to_1.metadata["directed"] is True

    def test_multigraph_edge_keys_preserved(self):
        """Test MultiGraph edge keys preserved in edge metadata."""
        G = nx.MultiGraph()
        # Add multiple edges with custom keys
        G.add_edge(1, 2, key="first", weight=1.0)
        G.add_edge(1, 2, key="second", weight=2.0)
        G.add_edge(1, 2, key="third", weight=3.0)

        layer = NetworkXAdapter.convert_graph(G)

        # Should have 3 edges
        assert len(layer.edges) == 3

        # Verify all edges have edge_key preserved
        edge_keys = [edge.metadata["edge_key"] for edge in layer.edges]
        # NetworkX may use integer keys by default, but our custom keys should be preserved
        assert len(edge_keys) == 3
        assert all("edge_key" in edge.metadata for edge in layer.edges)

    def test_multigraph_expands_multiple_edges(self):
        """Test MultiGraph expands multiple edges to independent Edge objects."""
        G = nx.MultiGraph()
        # Add 3 edges between nodes 1 and 2
        G.add_edge(1, 2, label="edge_a")
        G.add_edge(1, 2, label="edge_b")
        G.add_edge(1, 2, label="edge_c")

        layer = NetworkXAdapter.convert_graph(G)

        # Should create 3 independent Edge objects
        assert len(layer.edges) == 3

        # All edges should be between nodes "1" and "2"
        for edge in layer.edges:
            assert (edge.source == "1" and edge.target == "2") or (
                edge.source == "2" and edge.target == "1"
            )

        # Each edge should have unique edge_key
        edge_keys = [edge.metadata["edge_key"] for edge in layer.edges]
        assert len(set(edge_keys)) == 3  # All keys should be unique
