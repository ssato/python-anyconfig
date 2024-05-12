#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.loads with schema validation option."""
from __future__ import annotations

import typing
import warnings

import pytest

import anyconfig.api._load as TT
import anyconfig.schema

from anyconfig.api import ValidationError

from ... import common


if "jsonschema" not in anyconfig.schema.VALIDATORS:
    pytest.skip(
        "Required schema module 'jsonschema' is not available",
        allow_module_level=True
    )


NAMES: tuple[str, ...] = ("content", "exp", "scm", "opts")

# .. seealso:: tests.common.tdc
DATA_0: list = common.load_data_for_testfile(
    __file__, (("e", None), ("s", ""), ("o", {}))
)
DATA_IDS: list[str] = common.get_test_ids(DATA_0)
DATA: list[tuple[str, dict, typing.Any]] = [
    (i.read_text(), e, s.strip(), o) for i, e, s, o in DATA_0
]


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_loads(content: str, exp, scm: str, opts: dict):
    assert TT.loads(content, ac_schema=scm, **opts) == exp


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@pytest.mark.parametrize(NAMES, DATA[:1], ids=DATA_IDS[:1])
def test_loads_without_schema(content: str, exp, scm: str, opts: dict):
    assert scm or exp

    with pytest.raises(ValidationError):
        TT.loads(content, ac_schema=SCM_NG_0, ac_schema_safe=False, **opts)

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        assert TT.loads(content, ac_schema=SCM_NG_0, **opts) is None
        assert len(warns) > 0
        assert issubclass(warns[-1].category, UserWarning)
