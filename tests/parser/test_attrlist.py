#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.parser.parse_attrlist."""
from __future__ import annotations

import typing

import pytest

import anyconfig.parser as TT

from . import common


DATASETS: list[tuple[typing.Any, dict[str, typing.Any]]] = [
    (obj, data.get("e"), data.get("o", {}))
    for _, obj, data in common.collect_data("attrlist")
]


@pytest.mark.parametrize(("obj", "exp", "opts"), DATASETS)
def test_parse_attrlist(obj, exp, opts) -> None:
    assert TT.parse_attrlist(obj, **opts) == exp
