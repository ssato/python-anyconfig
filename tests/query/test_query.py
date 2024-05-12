#
# Copyright (C) 2017 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases for anyconfig.query.query."""
from __future__ import annotations

import pytest

try:
    import anyconfig.query.query as TT
except ImportError as exc:
    raise pytest.skip(
        "Needed library to query was not found",
        allow_module_leve=True
    ) from exc


@pytest.mark.parametrize(
    ("data", "query", "exp"),
    (({"a": 1}, "a", 1),
     ({"a": {"b": 2}}, "a.b", 2),
     ({"a": 1}, "b.", {"a": 1}),
     ({"a": 1}, None, {"a": 1}),
     ({"a": 1}, "", {"a": 1}),
     ),
)
def test_query(data, query: str, exp):
    (res, _exc) = TT.query(data, query)
    assert res == exp
