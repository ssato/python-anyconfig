#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Test cases for Test Data Collecor."""
from __future__ import annotations

import pathlib

import pytest

import anyconfig.backend.json.stdlib as MOD

from . import common as TT


CURDIR: pathlib.Path = pathlib.Path(__file__).parent
TESTFILE = CURDIR / "loaders" / "json" / "test_json_stdlib.py"

TEST_DATADIR = TT.common.RESOURCE_DIR / "loaders" / "json.stdlib"


@pytest.mark.parametrize(
    ("testfile", "exp"),
    ((str(TESTFILE), "json.stdlib"),
     (__file__, NameError),
     ),
)
def test_get_name(testfile, exp):
    if isinstance(exp, str):
        assert TT.get_name(testfile) == exp
    else:
        with pytest.raises(exp):
            TT.get_name(testfile)


@pytest.mark.parametrize(
    ("testfile", "exp"),
    ((str(TESTFILE), MOD),
     ),
)
def test_get_mod(testfile, exp):
    assert TT.get_mod(testfile) == exp


@pytest.mark.parametrize(
    ("path", "is_loader", "exp"),
    ((str(TESTFILE), True, TEST_DATADIR),
     ),
)
def test_get_test_resdir(path, is_loader, exp):
    assert TT.get_test_resdir(path, is_loader) == exp
