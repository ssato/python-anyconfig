#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.load with input of other file types."""
from __future__ import annotations

import pytest

import anyconfig.api

import anyconfig.api._load as TT

from . import common


LOADER_TYPES = frozenset(anyconfig.api.list_types())


@pytest.mark.skipif(
    "yaml" not in LOADER_TYPES,
    reason="yaml loader is not availabla."
)
@pytest.mark.parametrize(
    ("ipath", "exp"),
    [(ipath, exp) for ipath, _, exp, _ in common.load_datasets("yaml")],
)
def test_single_load_for_yaml_files(ipath, exp):
    assert TT.single_load(ipath) == exp


@pytest.mark.skipif(
    "toml" not in LOADER_TYPES,
    reason="toml loader is not availabla."
)
@pytest.mark.parametrize(
    ("ipath", "exp"),
    [(ipath, exp) for ipath, _, exp, _ in common.load_datasets("toml")],
)
def test_single_load_for_toml_files(ipath, exp):
    assert TT.single_load(ipath) == exp
