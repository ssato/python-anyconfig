#
# Copyright (C) 2015 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name, protected-access
# pylint: disable=bare-except
from __future__ import annotations

import pytest

import anyconfig.schema.jsonschema.generator as TT

from .constants import (
    OBJ_10, OBJ_20,
    SCM_10, SCM_20,
    STRICT_SCM_10, STRICT_SCM_20,
)


@pytest.mark.parametrize(
    ("arr", "ops", "exp"),
    (([], {}, {"items": {"type": "string"}, "type": "array"}),
     ([1], {}, {"items": {"type": "integer"}, "type": "array"}),
     ),
)
def test_array_to_schema(arr, ops, exp):
    assert TT.array_to_schema(arr, **ops) == exp


@pytest.mark.parametrize(
    ("obj", "ops", "exp"),
    (({"a": 1}, {},
      {"type": "object", "properties": {"a": {"type": "integer"}}}),
     ),
)
def test_object_to_schema(obj, ops, exp):
    assert TT.object_to_schema(obj, **ops) == exp


@pytest.mark.parametrize(
    ("obj", "exp_scm"),
    ((None, {"type": "null"}),
     (0, {"type": "integer"}),
     ("aaa", {"type": "string"}),
     ([1], {"items": {"type": "integer"}, "type": "array"}),
     (OBJ_10, SCM_10),
     (OBJ_20, SCM_20),
     ),
)
def test_gen_schema_validate(obj, exp_scm):
    assert TT.gen_schema(obj) == exp_scm


@pytest.mark.parametrize(
    ("obj", "exp_scm"),
    ((None, {"type": "null"}),
     (0, {"type": "integer"}),
     ("aaa", {"type": "string"}),
     ([1],
      {"items": {"type": "integer"}, "type": "array",
       "minItems": 1, "uniqueItems": True}),
     (["aaa", "bbb", "aaa"],
      {"items": {"type": "string"}, "type": "array",
       "minItems": 3, "uniqueItems": False}),
     (OBJ_10, STRICT_SCM_10),
     (OBJ_20, STRICT_SCM_20),
     ),
)
def test_gen_strict_schema_validate(obj, exp_scm):
    assert TT.gen_schema(obj, ac_schema_strict=True) == exp_scm
