#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.load with template options."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT
import anyconfig.template

from . import common

if typing.TYPE_CHECKING:
    import pathlib

if not anyconfig.template.SUPPORTED:
    pytest.skip(
        "jinja2 lib neede for template option is not available",
        allow_module_level=True,
    )


NAMES: tuple[str, ...] = (*common.NAMES, "ctx")
DATA: list = common.load_data_for_testfile(
    __file__, values=(("o", {}), ("e", None), ("c", {})),
)
DATA_IDS: list[str] = common.get_test_ids(DATA)


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_load(
    inputs: list[pathlib.Path], opts: dict, exp, ctx: dict,
) -> None:
    assert TT.load(inputs, ac_context=ctx, **opts) == exp
