#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.single_load with multi-type inputs."""
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
        in common.load_datasets("multi_types")
    ],
)
def test_single_load(
    ipath: pathlib.Path, opts: dict, exp
):
    assert TT.single_load(ipath, **opts) == exp
