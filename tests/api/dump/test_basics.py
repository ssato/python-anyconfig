#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Basic test cases for anyconfig.api.dump."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._dump as TT

from anyconfig.api import (
    UnknownFileTypeError, UnknownProcessorTypeError,
)

from ... import common

if typing.TYPE_CHECKING:
    import pathlib


NAMES: tuple[str, ...] = ("obj", "opts", "exp")

# .. seealso:: tests.common.tdc
DATA_0: list = common.load_data_for_testfile(__file__, load_idata=True)
DATA_IDS: list[str] = common.get_test_ids(DATA_0)
DATA: list[tuple[typing.Any, dict, str]] = [
    (i, o, e.strip()) for _, i, o, e in DATA_0
]


def test_data_is_defined_and_not_empty() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_dump(
    obj, opts: dict, exp, tmp_path: pathlib.Path,
) -> None:
    out = tmp_path / "out.json"
    TT.dump(obj, out, **opts)
    assert out.read_text() == exp


@pytest.mark.parametrize(NAMES, DATA[:1], ids=DATA_IDS[:1])
def test_dump_without_ac_parser_option(
    obj, opts: dict, exp,
) -> None:
    assert opts or exp
    with pytest.raises(UnknownFileTypeError):
        TT.dump(obj, "out.txt")


@pytest.mark.parametrize(NAMES, DATA[:1], ids=DATA_IDS[:1])
def test_dump_with_invalid_ac_parser_option(
    obj, opts: dict, exp,
) -> None:
    assert opts or exp
    with pytest.raises(UnknownProcessorTypeError):
        TT.dump(obj, "out.json", ac_parser="invalid_id")
