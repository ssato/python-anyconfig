#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.single_load to load primitive types."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT

from . import common

if typing.TYPE_CHECKING:
    import pathlib


@pytest.mark.parametrize(
    ("ipath", "opts", "exp"),
    [
        (ipath, opts, exp) for ipath, _, exp, opts
        in common.load_datasets("primitives")
    ],
)
def test_single_load(ipath: pathlib.Path, opts: dict, exp) -> None:
    assert TT.single_load(ipath, **opts) == exp
