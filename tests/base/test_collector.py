#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-docstring
"""Test cases for tests.base.collector."""
from __future__ import annotations

import pathlib

from . import collector as TT


CUR_DIR = pathlib.Path(__file__).parent


class Collector(TT.TDataCollector):
    # To avoid error because there are no files with '.json' file extension in
    # tests/res/base/basics/20/.
    pattern = "*.*"
    should_exist = ()  # Likewise.


def test_members():
    obj = Collector()
    obj.init()

    assert obj.target
    assert obj.target != TT.TDataCollector.target
    assert obj.target == CUR_DIR.name

    assert obj.root is not None
    assert obj.root == CUR_DIR.parent / "res" / obj.target / obj.kind

    assert obj.datasets
