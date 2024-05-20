#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Test cases for Test Data Collecor."""
from __future__ import annotations

import pathlib

import pytest

from . import common as TT


CURDIR: pathlib.Path = pathlib.Path(__file__).parent
TESTFILE = CURDIR / "loaders" / "json" / "test_json_stdlib.py"

TEST_DATADIR = TT.common.RESOURCE_DIR / "loaders" / "json.stdlib"


@pytest.mark.parametrize(
    ("path", "is_loader", "exp"),
    ((str(TESTFILE), True, TEST_DATADIR),
     ),
)
def test_get_test_resdir(path, is_loader, exp):
    assert TT.get_test_resdir(path, is_loader) == exp
