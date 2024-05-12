#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""test cases for anyconfig.utils.lists."""
from __future__ import annotations

import pytest

import anyconfig.utils.utils as TT


@pytest.mark.parametrize(
    ("keys", "opts", "exp"),
    ((('aaa', ), {"aaa": 1, "bbb": 2}, {"aaa": 1}),
     (('aaa', ), {"bbb": 2}, {}),
     )
)
def test_filter_options(keys, opts, exp) -> None:
    assert TT.filter_options(keys, opts) == exp
