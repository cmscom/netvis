#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Manabu TERADA.
# Distributed under the terms of the Modified BSD License.

"""
This module defines the NetVis widget.
"""

import json

from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, validate, TraitError
from ._frontend import module_name, module_version


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
