#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.parser.parse_single."""
from __future__ import annotations

import typing

import pytest

import anyconfig.parser as TT

from . import common


DATASETS: list[tuple[typing.Any, dict[str, typing.Any]]] = [
    (obj, data.get("e")) for _, obj, data in common.collect_data("single")
]


@pytest.mark.parametrize(("obj", "exp"), DATASETS)
def test_parse_single(obj, exp) -> None:
    assert TT.parse_single(obj) == exp
