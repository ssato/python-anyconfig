#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.parser.parse."""
from __future__ import annotations

import typing

import pytest

import anyconfig.parser as TT

from . import common


DATASETS: list[tuple[typing.Any, dict[str, typing.Any]]] = [
    (obj, data.get("e"), data.get("o", {}))
    for _, obj, data in common.collect_data("parse")
]


@pytest.mark.parametrize(("obj", "exp", "opts"), DATASETS)
def test_parse(obj, exp, opts) -> None:
    assert TT.parse(obj, **opts) == exp
