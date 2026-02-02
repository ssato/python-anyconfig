#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.parsers.
"""
from __future__ import annotations

import pathlib

import pytest

import anyconfig.backend.json
import anyconfig.backend.json.stdlib as JSONStdlib
try:
    import anyconfig.backend.yaml.pyyaml as PYYAML
except ImportError:
    PYYAML = None

import anyconfig.parsers.parsers as TT
import anyconfig.ioinfo

from anyconfig.common import (
    UnknownProcessorTypeError, UnknownFileTypeError
)

from ..common import RESOURCE_DIR


CNF_PATH: pathlib.Path = (
    RESOURCE_DIR / "loaders/json.stdlib/10/360_a_nested_map.json"
)


@pytest.fixture(name="parsers")
def found_parsers():
    return TT.Parsers()


def test_json_parsers(parsers):
    psrs = parsers.findall(None, forced_type="json")
    assert psrs
    assert JSONStdlib.Parser in psrs
    assert psrs[0] == JSONStdlib.Parser


@pytest.mark.skipif(PYYAML is None, reason="PyYAML is not available.")
def test_yaml_parsers(parsers):
    psrs = parsers.findall(None, forced_type="yaml")
    assert psrs
    assert PYYAML.Parser in psrs
    assert psrs[0] == PYYAML.Parser


@pytest.mark.parametrize(
    ("exc", "arg0", "kwargs"),
    ((ValueError, None, {}),
     (UnknownProcessorTypeError, None, {"forced_type": "_unkonw_type_"}),
     (UnknownFileTypeError, "cnf.unknown_ext", {}),
     ),
)
def test_find__failures(exc, arg0, kwargs, parsers):
    with pytest.raises(exc):
        parsers.find(arg0, **kwargs)


def test_find(parsers):
    pcls = anyconfig.backend.json.Parser
    assert isinstance(parsers.find("x.conf", forced_type="json"), pcls)
    assert isinstance(parsers.find("x.json"), pcls)

    with open(CNF_PATH, encoding="utf-8") as inp:
        assert isinstance(parsers.find(inp), pcls)

    inp = pathlib.Path("x.json")
    assert isinstance(parsers.find(inp), pcls)


def test_find__input_object(parsers):
    inp = anyconfig.ioinfo.make(CNF_PATH)
    psr = parsers.find(inp)
    assert isinstance(psr, anyconfig.backend.json.Parser)
