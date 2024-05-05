#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.single_load with ac_parser argument."""
from __future__ import annotations

import pathlib

import pytest

from . import common as TT


@pytest.mark.parametrize(
    ("data", "exp"),
    (([], []),
     ([(pathlib.Path("foo/bar/test_bar.py"), 1, 2, 3)],
      ["foo/bar/test_bar.py"]),
     ),
)
def test_get_test_ids(data, exp):
    assert TT.get_test_ids(data) == exp


def test_get_mod_target_by_test_filepath():
    mod_target = TT.get_mod_target_by_test_filepath(__file__)
    assert mod_target

    (mod, target) = mod_target
    assert mod == "single_load"
    assert target == "common"
