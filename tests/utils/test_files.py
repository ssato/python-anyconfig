#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for anyconfig.utils.files."""
from __future__ import annotations

import pathlib
import typing

import pytest

import anyconfig.utils.files as TT


@pytest.mark.parametrize(
    ("obj", "exp"),
    ((open(__file__, encoding="utf-8"), True),
     (__file__, False),
     ([__file__], False),
     (pathlib.Path(__file__), False),
     ([pathlib.Path(__file__)], False),
     ),
)
def test_is_io_stream(obj: typing.Any, exp: bool) -> None:
    res = TT.is_io_stream(obj)
    assert res if exp else not res


def test_get_path_from_stream() -> None:
    this = __file__

    with pathlib.Path(this).open(encoding="utf-8") as strm:
        assert TT.get_path_from_stream(strm) == this

    with pytest.raises(ValueError):
        TT.get_path_from_stream(this)

    assert TT.get_path_from_stream(this, safe=True) == ""
