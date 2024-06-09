#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Test cases for Test Data Collecor."""
from __future__ import annotations

import pytest

import anyconfig.backend.json.stdlib as MOD

from . import common as TT
from .constants import (
    MOD_BACKEND, MOD_TYPE, TEST_FILE, TEST_DATADIR
)


@pytest.mark.parametrize(
    ("testfile", "exp"),
    ((str(TEST_FILE), f"{MOD_TYPE}.{MOD_BACKEND}"),
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
    ((str(TEST_FILE), MOD),
     ),
)
def test_get_mod(testfile, exp):
    assert TT.get_mod(testfile) == exp


@pytest.mark.parametrize(
    ("path", "exp"),
    ((str(TEST_FILE), TEST_DATADIR),
     ),
)
def test_get_test_resdir(path, exp):
    assert TT.get_test_resdir(path) == exp
