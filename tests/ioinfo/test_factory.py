#
# Copyright (C) 2018 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.ioinfo.factory."""
from __future__ import annotations

import pytest

import anyconfig.ioinfo.factory as TT

from anyconfig.ioinfo.datatypes import (
    IOInfo, IOI_PATH_OBJ, IOI_STREAM
)

from .constants import TEST_PY


TEST_IOI_PATH_OBJ = IOInfo(
    src=TEST_PY, type=IOI_PATH_OBJ, path=str(TEST_PY), extension="py"
)
TEST_IOI_STREAM = IOInfo(
    src=TEST_PY.open(), type=IOI_STREAM, path=str(TEST_PY), extension="py"
)


@pytest.mark.parametrize(
    ("obj", "exp"),
    (pytest.param(TEST_IOI_PATH_OBJ, TEST_IOI_PATH_OBJ, id="pathlib.Path"),
     pytest.param(TEST_IOI_STREAM, TEST_IOI_STREAM, id="IO stream"),
     pytest.param(str(TEST_PY), TEST_IOI_PATH_OBJ, id="path (str)"),
     ),
)
def test_make(obj, exp):
    assert TT.make(obj) == exp


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    ("obj", ),
    ((None, ),
     ),
)
def test_make_failiures(obj):
    with pytest.raises(ValueError):
        TT.make(obj)
