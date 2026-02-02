#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.load with query options."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT
import anyconfig.query

from .common import (
    load_data_for_testfile, get_test_ids,
)

if typing.TYPE_CHECKING:
    import pathlib


if not anyconfig.query.SUPPORTED:
    pytest.skip(
        "jmespath lib to neede for query is not available.",
        allow_module_level=True,
    )

NAMES: tuple[str, ...] = ("inputs", "query", "exp")
DATA = load_data_for_testfile(__file__, values=(("q", ""), ("e", None)))
DATA_IDS: list[str] = get_test_ids(DATA)


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_load(
    inputs: list[pathlib.Path], query: str, exp,
) -> None:
    assert TT.load(inputs, ac_query=query) == exp


@pytest.mark.parametrize(NAMES, DATA[:1], ids=DATA_IDS[:1])
def test_load_with_invalid_query(
    inputs: list[pathlib.Path], query: str, exp,
) -> None:
    assert query or exp  # To avoid an error not using them.
    assert TT.load(
        inputs, ac_query="",
    ) == TT.load(inputs)
