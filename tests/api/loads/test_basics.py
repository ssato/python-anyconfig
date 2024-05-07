#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Basic test cases for anyconfig.api.loads."""
from __future__ import annotations

import typing
import warnings

import pytest

import anyconfig.api._load as TT

from anyconfig.api import UnknownProcessorTypeError

from ... import common

if typing.TYPE_CHECKING:
    import pathlib


NAMES: tuple[str, ...] = ("content", "opts", "exp")

# .. seealso:: tests.common.tdc
DATA_0: list[
    tuple[pathlib.Path, dict, typing.Any]
] = common.load_data_for_testfile(__file__)

DATA: list[tuple[str, dict, typing.Any]] = [
    (i.read_text(), o, e) for i, o, e in DATA_0
]
DATA_IDS: list[str] = common.get_test_ids(DATA_0)


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_loads(content: str, opts: dict, exp) -> None:
    assert TT.loads(content, **opts) == exp


@pytest.mark.parametrize(NAMES, DATA[:1], ids=DATA_IDS[:1])
def test_loads_withou_ac_parser_option(content: str, opts: dict, exp):
    assert opts or exp
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter('always')
        assert TT.loads(content) is None
        assert len(warns) == 1
        assert issubclass(warns[-1].category, UserWarning)
        assert "ac_parser was not given but" in str(warns[-1].message)


@pytest.mark.parametrize(NAMES, DATA[:1], ids=DATA_IDS[:1])
def test_loads_with_invalid_ac_parser_option(content: str, opts: dict, exp):
    assert opts or exp
    with pytest.raises(UnknownProcessorTypeError):
        assert TT.loads(content, ac_parser="invalid_parser") is None
