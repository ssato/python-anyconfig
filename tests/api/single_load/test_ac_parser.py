#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.single_load with ac_parser argument."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT

from ... import common

if typing.TYPE_CHECKING:
    import pathlib


NAMES: tuple[str, ...] = ("ipath", "opts", "exp")
DATA: list = common.load_data_for_testfile(
    __file__, (("o", {}), ("e", None))
)
DATA_IDS: list[str] = common.get_test_ids(DATA)


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_single_load(ipath: pathlib.Path, opts: dict, exp) -> None:
    assert TT.single_load(ipath, **opts) == exp
