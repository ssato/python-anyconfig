#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Basic test cases for anyconfig.api.loads."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT
import anyconfig.query

from ... import common


if not anyconfig.query.SUPPORTED:
    pytest.skip(
        "Required query module is not available",
        allow_module_level=True
    )


NAMES: tuple[str, ...] = ("content", "exp", "query", "opts")

# .. seealso:: tests.common.tdc
DATA_0: list = common.load_data_for_testfile(
    __file__, (("e", None), ("q", ""), ("o", {}))
)
DATA_IDS: list[str] = common.get_test_ids(DATA_0)
DATA: list[tuple[str, dict, typing.Any]] = [
    (i.read_text(), e, q.strip(), o) for i, e, q, o in DATA_0
]


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_loads(content: str, exp, query: str, opts: dict):
    assert TT.loads(content, ac_query=query, **opts) == exp


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_loads_with_invalid_query_option(
    content: str, exp, query: str, opts: dict
):
    assert exp or query
    assert TT.loads(
        content, ac_query=None, **opts
    ) == TT.loads(content, **opts)
