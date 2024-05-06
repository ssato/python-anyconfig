#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.parser.parse_attrlist."""
from __future__ import annotations

import pytest

import anyconfig.parser as TT

from .. import common


NAMES: list[str] = ("obj", "exp", "opts")
DATA_0: list[tuple] = common.load_data_for_testfile(
    __file__, (("e", None), ("o", {})),
    load_idata=True
)
DATA: list[tuple] = [(d, *rest) for _, d, *rest in DATA_0]
DATA_IDS: list[str] = common.get_test_ids(DATA_0)


def test_data():
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_parse_attrlist(obj, exp, opts) -> None:
    assert TT.parse_attrlist(obj, **opts) == exp
