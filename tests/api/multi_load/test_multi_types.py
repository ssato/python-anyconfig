#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.multi_load with multi type inputs."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT

from .common import (
    NAMES, load_data_for_testfile, get_test_ids
)

if typing.TYPE_CHECKING:
    import pathlib


DATA = load_data_for_testfile(__file__)
DATA_IDS: list[str] = get_test_ids(DATA)


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_multi_load(
    inputs: list[pathlib.Path], opts: dict, exp
) -> None:
    assert TT.multi_load(inputs, **opts) == exp
