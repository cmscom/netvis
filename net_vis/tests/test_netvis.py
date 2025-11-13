#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Manabu TERADA.
# Distributed under the terms of the Modified BSD License.

import pytest
from traitlets.traitlets import TraitError
from ..netvis import NetVis


def test_netvis_creation_blank():
    w = NetVis()
    assert w.value == ""


def test_netvis_creation_with_dict():
    with pytest.raises(TraitError):
        w = NetVis(value={"a": 1})
    # assert isinstance(w.value, str)
    # assert w.value == '{"a": 1}'


def test_netvis_creation_with_list():
    with pytest.raises(TraitError):
        w = NetVis(value=[1, 2, 3])
    # assert isinstance(w.value, str)
    # assert w.value == "[1, 2, 3]"


def test_netvis_creation_with_str():
    w = NetVis(value='{"a": 1}')
    assert isinstance(w.value, str)
    assert w.value == '{"a": 1}'


# T010: MIME bundle tests
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


# T011: Error handling tests
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
