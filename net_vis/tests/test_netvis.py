import pytest

from ..netvis import NetVis


def test_netvis_creation_blank():
    w = NetVis()
    assert w.value == ""


def test_netvis_creation_with_dict():
    # 0.4.0: ValueError (not TraitError) because __init__ validates before super().__init__
    with pytest.raises(ValueError, match="Value must be a string"):
        NetVis(value={"a": 1})


def test_netvis_creation_with_list():
    # 0.4.0: ValueError (not TraitError) because __init__ validates before super().__init__
    with pytest.raises(ValueError, match="Value must be a string"):
        NetVis(value=[1, 2, 3])


def test_netvis_creation_with_str():
    # 0.4.0: Must be valid GraphData with nodes and links
    data = '{"nodes": [{"id": "A"}], "links": []}'
    w = NetVis(value=data)
    assert isinstance(w.value, str)
    assert w.value == data


def test_netvis_mimebundle():
    """Test that NetVis returns correct MIME bundle for JupyterLab."""
    data = '{"nodes": [{"id": "A"}], "links": []}'
    w = NetVis(value=data)

    bundle = w._repr_mimebundle_()

    # Check that the bundle contains the custom MIME type
    assert "application/vnd.netvis+json" in bundle

    # Check the structure of the custom MIME type data
    mime_data = bundle["application/vnd.netvis+json"]
    assert "data" in mime_data
    assert "version" in mime_data

    # Check that data matches the input
    assert mime_data["data"] == data

    # Check that version is present
    assert isinstance(mime_data["version"], str)
    assert len(mime_data["version"]) > 0

    # Check fallback text/plain
    assert "text/plain" in bundle
    assert isinstance(bundle["text/plain"], str)


def test_netvis_invalid_json():
    """Test that invalid JSON raises ValueError."""
    with pytest.raises(ValueError, match="Invalid JSON format"):
        NetVis(value="invalid json")


def test_netvis_duplicate_node_id():
    """Test that duplicate node IDs raise ValueError."""
    data = '{"nodes": [{"id": "A"}, {"id": "A"}], "links": []}'
    with pytest.raises(ValueError, match="Duplicate node ID"):
        NetVis(value=data)


def test_netvis_invalid_link():
    """Test that links referencing non-existent nodes raise ValueError."""
    data = '{"nodes": [{"id": "A"}], "links": [{"source": "A", "target": "B"}]}'
    with pytest.raises(ValueError, match="does not exist in nodes"):
        NetVis(value=data)


def test_netvis_missing_nodes():
    """Test that missing 'nodes' field raises ValueError."""
    data = '{"links": []}'
    with pytest.raises(ValueError, match="must contain 'nodes' array"):
        NetVis(value=data)


def test_netvis_missing_links():
    """Test that missing 'links' field raises ValueError."""
    data = '{"nodes": [{"id": "A"}]}'
    with pytest.raises(ValueError, match="must contain 'links' array"):
        NetVis(value=data)


def test_empty_data_handling():
    """Test that NetVis can be created with empty string and returns correct MIME bundle."""
    # Create NetVis with empty string
    w = NetVis(value="")
    assert w.value == ""

    # Check that MIME bundle is still generated correctly
    bundle = w._repr_mimebundle_()
    assert "application/vnd.netvis+json" in bundle

    mime_data = bundle["application/vnd.netvis+json"]
    assert "data" in mime_data
    assert mime_data["data"] == ""
    assert "version" in mime_data


def test_repr_mimebundle_structure():
    """Test that _repr_mimebundle_() returns correct structure with all required fields."""
    data = '{"nodes": [{"id": "A"}, {"id": "B"}], "links": [{"source": "A", "target": "B"}]}'
    w = NetVis(value=data)

    bundle = w._repr_mimebundle_()

    # Verify MIME bundle keys
    assert "application/vnd.netvis+json" in bundle
    assert "text/plain" in bundle

    # Verify custom MIME type structure
    mime_data = bundle["application/vnd.netvis+json"]
    assert isinstance(mime_data, dict)
    assert "data" in mime_data
    assert "version" in mime_data
    assert mime_data["data"] == data

    # Verify version is a valid string
    from ..netvis import __version__

    assert mime_data["version"] == __version__


def test_plain_text_fallback():
    """Test that MIME bundle includes text/plain fallback for environments without custom renderer."""
    data = '{"nodes": [{"id": "A"}], "links": []}'
    w = NetVis(value=data)

    bundle = w._repr_mimebundle_()

    # Verify text/plain fallback exists
    assert "text/plain" in bundle
    assert isinstance(bundle["text/plain"], str)
    assert len(bundle["text/plain"]) > 0

    # Should contain meaningful text
    assert "NetVis" in bundle["text/plain"]


def test_multiple_instances():
    """Test that multiple NetVis instances maintain independent state."""
    data1 = '{"nodes": [{"id": "A"}], "links": []}'
    data2 = '{"nodes": [{"id": "B"}, {"id": "C"}], "links": [{"source": "B", "target": "C"}]}'

    # Create two separate instances
    w1 = NetVis(value=data1)
    w2 = NetVis(value=data2)

    # Verify they have different data
    assert w1.value == data1
    assert w2.value == data2
    assert w1.value != w2.value

    # Verify their MIME bundles are independent
    bundle1 = w1._repr_mimebundle_()
    bundle2 = w2._repr_mimebundle_()

    assert bundle1["application/vnd.netvis+json"]["data"] == data1
    assert bundle2["application/vnd.netvis+json"]["data"] == data2

    # Modifying one should not affect the other
    NetVis(value="")
    assert w1.value == data1  # w1 unchanged
    assert w2.value == data2  # w2 unchanged


def test_large_graph():
    """Test that NetVis can handle large graphs without crashing (1000 nodes, 2000 links)."""
    # Generate large graph data
    nodes = [{"id": f"node_{i}"} for i in range(1000)]

    # Create 2000 links (each node connects to ~2 others on average)
    links = []
    for i in range(1000):
        # Connect to next two nodes (circular)
        target1 = (i + 1) % 1000
        target2 = (i + 2) % 1000
        links.append({"source": f"node_{i}", "target": f"node_{target1}"})
        if len(links) < 2000:
            links.append({"source": f"node_{i}", "target": f"node_{target2}"})

    import json

    data = json.dumps({"nodes": nodes, "links": links[:2000]})

    # Should create without error
    w = NetVis(value=data)
    assert w.value == data

    # Should generate MIME bundle
    bundle = w._repr_mimebundle_()
    assert "application/vnd.netvis+json" in bundle

    # Verify data integrity
    mime_data = bundle["application/vnd.netvis+json"]
    parsed_data = json.loads(mime_data["data"])
    assert len(parsed_data["nodes"]) == 1000
    assert len(parsed_data["links"]) == 2000


def test_special_characters_in_node_id():
    """Test that NetVis handles special characters and Unicode in node IDs."""
    # Test various special characters and Unicode
    test_cases = [
        # Special characters
        '{"nodes": [{"id": "node-with-dash"}, {"id": "node_with_underscore"}], "links": [{"source": "node-with-dash", "target": "node_with_underscore"}]}',
        # Unicode characters (non-ASCII)
        '{"nodes": [{"id": "Nöde_Ä"}, {"id": "Nöde_Ö"}], "links": [{"source": "Nöde_Ä", "target": "Nöde_Ö"}]}',
        # Unicode characters (Emoji)
        '{"nodes": [{"id": "🔴"}, {"id": "🔵"}], "links": [{"source": "🔴", "target": "🔵"}]}',
        # Mixed alphanumeric and symbols
        '{"nodes": [{"id": "Node@123"}, {"id": "Node#456"}], "links": [{"source": "Node@123", "target": "Node#456"}]}',
        # Spaces in IDs
        '{"nodes": [{"id": "Node A"}, {"id": "Node B"}], "links": [{"source": "Node A", "target": "Node B"}]}',
    ]

    for data in test_cases:
        # Should create without error
        w = NetVis(value=data)
        assert w.value == data

        # Should generate valid MIME bundle
        bundle = w._repr_mimebundle_()
        assert "application/vnd.netvis+json" in bundle
        assert bundle["application/vnd.netvis+json"]["data"] == data
