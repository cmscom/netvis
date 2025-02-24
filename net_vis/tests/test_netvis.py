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
