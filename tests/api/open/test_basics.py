#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, no-member
"""Test cases for api.open."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._open as TT
import anyconfig.api._load as LD

from ... import common

if typing.TYPE_CHECKING:
    import pathlib


NAMES: tuple[str, ...] = ("ipath", "exp", "opts")
DATA: list[
    tuple[pathlib.Path, typing.Optional[dict], dict]
] = common.load_data_for_testfile(__file__, values=(("e", None), ("o", {})))

DATA_IDS: list[str] = common.get_test_ids(DATA)


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_open_text_io(ipath, exp, opts):
    with TT.open(ipath, **opts) as inp:
        assert LD.load(inp, **opts) == exp
