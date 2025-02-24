#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Manabu TERADA.
# Distributed under the terms of the Modified BSD License.

"""
This module defines the NetVis widget.
"""

from ipywidgets import DOMWidget
from traitlets import Unicode
from ._frontend import module_name, module_version


class NetVis(DOMWidget):
    """NetVis widget.
    This widget show Network Visualization.
    """

    _model_name = Unicode("NetVisModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("NetVisView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode("Hello World").tag(sync=True)
