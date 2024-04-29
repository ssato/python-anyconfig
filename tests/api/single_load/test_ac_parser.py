#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.single_load with ac_parser argument."""
from __future__ import annotations

import pathlib

import pytest

import anyconfig.api._load as TT

from . import common


@pytest.mark.parametrize(
    ("ipath", "opts", "exp"),
    [
        (ipath, opts, exp) for ipath, _, exp, opts
        in common.load_datasets("ac_parser")
    ],
)
def test_single_load(
    ipath: pathlib.Path, opts: dict, exp
):
    assert TT.single_load(ipath, **opts) == exp
