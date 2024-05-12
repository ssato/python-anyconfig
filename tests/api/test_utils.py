#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for anyconfig.utils.files."""
import pathlib

import pytest

import anyconfig.api.utils as TT

from anyconfig.ioinfo import make as ioinfo_make


THIS_PY = pathlib.Path(__file__)
THIS = ioinfo_make(THIS_PY)
OTHER = ioinfo_make(THIS_PY.parent / "pyproject.toml")


@pytest.mark.parametrize(
    ("obj", "exp"),
    (([], False),
     ([THIS], True),
     ([THIS, THIS], True),
     ([THIS, OTHER], False),
     ([THIS, OTHER], False),
     )
)
def test_are_same_file_types(obj, exp):
    assert TT.are_same_file_types(obj) == exp
