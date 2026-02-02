#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.load to load primitive types."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT

from .. import common

if typing.TYPE_CHECKING:
    import pathlib


NAMES: tuple[str, ...] = ("ipath", "opts", "exp")
DATA: list = common.load_data_for_testfile(__file__)
DATA_IDS: list[str] = common.get_test_ids(DATA)


def test_data_is_non_empty() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_load(ipath: pathlib.Path, opts: dict, exp) -> None:
    assert TT.load(ipath, **opts) == exp
