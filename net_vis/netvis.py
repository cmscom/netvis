#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Manabu TERADA.
# Distributed under the terms of the Modified BSD License.

"""
This module defines the NetVis widget.
"""

import json
from typing import Dict, Any, Optional, Sequence

from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, validate, TraitError
from ._frontend import module_name, module_version
from ._version import __version__


def is_invalid_json(data):
    try:
        json.loads(data)
        return False
    except json.JSONDecodeError:
        return True


@register
class NetVis(DOMWidget, ValueWidget):
    """NetVis widget.
    This widget show Network Visualization.
    """

    _model_name = Unicode("NetVisModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("NetVisView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode().tag(sync=True)

    def __init__(self, value: str = None, **kwargs):
        """
        Initialize NetVis object with graph data validation.

        Args:
            value (str): JSON string containing graph data with 'nodes' and 'links'

        Raises:
            ValueError: If JSON is invalid, nodes/links are missing, or data is inconsistent
        """
        if value is not None:
            self._validate_graph_data(value)
        super().__init__(value=value, **kwargs)

    def _validate_graph_data(self, data: str) -> None:
        """
        Validate GraphData structure.

        Args:
            data (str): JSON string to validate

        Raises:
            ValueError: If validation fails
        """
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

        if not isinstance(parsed, dict):
            raise ValueError("GraphData must be a JSON object")

        if "nodes" not in parsed:
            raise ValueError("GraphData must contain 'nodes' array")

        if "links" not in parsed:
            raise ValueError("GraphData must contain 'links' array")

        nodes = parsed["nodes"]
        links = parsed["links"]

        if not isinstance(nodes, list):
            raise ValueError("'nodes' must be an array")

        if not isinstance(links, list):
            raise ValueError("'links' must be an array")

        # Check for duplicate node IDs
        node_ids = set()
        for node in nodes:
            if not isinstance(node, dict):
                raise ValueError("Each node must be an object")
            if "id" not in node:
                raise ValueError("Each node must have an 'id' field")

            node_id = node["id"]
            if node_id in node_ids:
                raise ValueError(f"Duplicate node ID: {node_id}")
            node_ids.add(node_id)

        # Check link references
        for link in links:
            if not isinstance(link, dict):
                raise ValueError("Each link must be an object")

            if "source" not in link:
                raise ValueError("Each link must have a 'source' field")
            if "target" not in link:
                raise ValueError("Each link must have a 'target' field")

            source = link["source"]
            target = link["target"]

            if source not in node_ids:
                raise ValueError(f"Link source '{source}' does not exist in nodes")
            if target not in node_ids:
                raise ValueError(f"Link target '{target}' does not exist in nodes")

    def _repr_mimebundle_(
        self,
        include: Optional[Sequence[str]] = None,
        exclude: Optional[Sequence[str]] = None
    ) -> Dict[str, Any]:
        """
        Return MIME bundle for JupyterLab rendering.

        This method is automatically called by IPython/JupyterLab to display
        the NetVis object. It returns a custom MIME type that will be handled
        by the NetVisRenderer TypeScript extension.

        Args:
            include: Optional list of MIME types to include (not used)
            exclude: Optional list of MIME types to exclude (not used)

        Returns:
            Dict containing MIME bundle with 'application/vnd.netvis+json' and 'text/plain'
        """
        return {
            'application/vnd.netvis+json': {
                'data': self.value,
                'version': __version__
            },
            'text/plain': 'NetVis Graph'
        }

    @validate("value")
    def _valid_value(self, proposal):
        # if isinstance(proposal["value"], str):
        #     _data = proposal["value"]
        # elif isinstance(proposal["value"], (dict, list)):
        #     _data = json.dumps(proposal["value"])
        # else:
        #     raise TraitError("Invalid data type: it must be JSON string or dict / list")
        _data = proposal["value"]
        if is_invalid_json(_data):
            raise TraitError("Invalid JSON value: it must be JSON string")
        return _data
