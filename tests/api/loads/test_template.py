#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.single_load with schema options."""
from __future__ import annotations

import typing
import warnings

import pytest

import anyconfig.api._load as TT
import anyconfig.template

from ... import common


if not anyconfig.template.SUPPORTED:
    pytest.skip(
        "jinja2 template lib is not available",
        allow_module_level=True
    )


NAMES: tuple[str, ...] = ("content", "exp", "ctx", "opts")

# .. seealso:: tests.common.tdc
DATA_0: list = common.load_data_for_testfile(
    __file__, (("e", None), ("c", {}), ("o", {}))
)
DATA_IDS: list[str] = common.get_test_ids(DATA_0)
DATA: list[tuple[str, dict, typing.Any]] = [
    (i.read_text(), *eco) for i, *eco in DATA_0
]


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_loads(content: str, exp, ctx: dict, opts: dict):
    assert TT.loads(content, ac_context=ctx, **opts) == exp


def test_loads_failures():
    content = '{"a": "{{ a"}'
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        res = TT.loads(content, ac_parser="json", ac_template=True)
        assert res == {"a": "{{ a"}
        # self.assertEqual(len(warns), 1)  # Needs to fix plugins
        assert issubclass(warns[-1].category, UserWarning)
