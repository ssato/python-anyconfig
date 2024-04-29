#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, unused-import
"""Test cases for anyconfig.api.single_load to load primitive types."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT

try:
    import anyconfig.query.query  # noqa: F401
except ImportError:
    pytest.skip(
        "Required query module is not available",
        allow_module_level=True
    )

from . import common

if typing.TYPE_CHECKING:
    import pathlib


def load_datasets() -> list[tuple[pathlib.Path, typing.Any, str]]:
    return [
        (ipath, data.get("e"), data.get("q", ""), data.get("o", {}))
        for ipath, data
        in common.tdc.collect_for(
            "single_load", "query", subdir="api", load=False
        )
    ]


@pytest.mark.parametrize(
    ("ipath", "exp", "query", "opts"),
    load_datasets()
)
def test_single_load(ipath: pathlib.Path, exp, query, opts):
    assert TT.single_load(
        ipath, ac_query=query.strip(), **opts
    ) == exp


@pytest.mark.parametrize(
    ("ipath", "opts"),
    [(ipath, opts) for ipath, _, _, opts in load_datasets()]
)
def test_single_load_with_invalid_query_string(
    ipath: pathlib.Path, opts
):
    assert TT.single_load(
        ipath, ac_query=None, **opts
    ) == TT.single_load(ipath, **opts)
