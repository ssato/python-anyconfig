#
# Copyright (C) 2015 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name, protected-access
# pylint: disable=bare-except
from __future__ import annotations

import copy
import pytest

try:
    import anyconfig.schema.jsonschema as TT
    SUPPORTED: bool = True
except ImportError:
    SUPPORTED: bool = False  # type: ignore


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


_OBJ_10: dict = {"a": 1}
_SCM_10: dict = {
    "properties": {"a": {"type": "integer"}},
    "type": "object"
}
_STRICT_SCM_10 = copy.deepcopy(_SCM_10)
_STRICT_SCM_10["required"] = ["a"]

_OBJ_20: dict = {"a": 1, "b": [1, 2], "c": {"d": "aaa", "e": 0.1}}
_SCM_20: dict = {
    "properties": {
        "a": {"type": "integer"},
        "b": {"items": {"type": "integer"}, "type": "array"},
        "c": {
            "properties": {"d": {"type": "string"}, "e": {"type": "number"}},
            "type": "object"
        }
    },
    "type": "object"
}
_STRICT_SCM_20 = copy.deepcopy(_SCM_20)
_STRICT_SCM_20["properties"]["b"]["minItems"] = 2
_STRICT_SCM_20["properties"]["b"]["uniqueItems"] = True
_STRICT_SCM_20["properties"]["c"]["required"] = ["d", "e"]
_STRICT_SCM_20["required"] = ["a", "b", "c"]


@pytest.mark.parametrize(
    ("obj", "exp_scm"),
    ((None, {"type": "null"}),
     (0, {"type": "integer"}),
     ("aaa", {"type": "string"}),
     ([1], {"items": {"type": "integer"}, "type": "array"}),
     (_OBJ_10, _SCM_10),
     (_OBJ_20, _SCM_20),
     ),
)
def test_gen_schema_validate(obj, exp_scm):
    assert TT.gen_schema(obj) == exp_scm

    if SUPPORTED:
        assert TT.validate(obj, exp_scm)


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
     (_OBJ_10, _STRICT_SCM_10),
     (_OBJ_20, _STRICT_SCM_20),
     ),
)
def test_gen_strict_schema_validate(obj, exp_scm):
    assert TT.gen_schema(obj, ac_schema_strict=True) == exp_scm

    if SUPPORTED:
        assert TT.validate(obj, exp_scm)


_SKIP_MSG: str = "json schema lib is not available"


@pytest.mark.skipif(not SUPPORTED, reason=_SKIP_MSG)
@pytest.mark.parametrize(
    ("obj", "scm"),
    ((_OBJ_10, _SCM_10),
     (_OBJ_20, _SCM_20),
     (_OBJ_10, _STRICT_SCM_10),
     (_OBJ_20, _STRICT_SCM_20),
     ),
)
def test_validate(obj, scm):
    (ret, msg) = TT.validate(obj, scm)
    assert not msg
    assert ret


_NG_OBJ_10: dict = {"a": "aaa"}


@pytest.mark.skipif(not SUPPORTED, reason=_SKIP_MSG)
@pytest.mark.parametrize(
    ("obj", "scm"),
    ((_NG_OBJ_10, _SCM_10),
     (_NG_OBJ_10, _SCM_20),
     ),
)
def test_validate__an_error(obj, scm):
    (ret, msg) = TT.validate(obj, scm, ac_schema_safe=True)
    assert msg
    assert not ret

    with pytest.raises(Exception):
        _rm = TT.validate(obj, scm, ac_schema_safe=False)


@pytest.mark.skipif(not SUPPORTED, reason=_SKIP_MSG)
def test_validate__errors():
    obj: dict = {"a": 1, "b": 2.0}
    scm: dict = {
        "type": "object",
        "properties": {"a": {"type": "integer"}, "b": {"type": "string"}}
    }

    (ret, msg) = TT.validate(obj, scm, ac_schema_errors=True)
    assert msg  # ["'a' is not of type ...", "'b' is not ..."]
    assert not ret


@pytest.mark.skipif(not SUPPORTED, reason=_SKIP_MSG)
@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    ("obj", "scm", "success"),
    ((_OBJ_10, _SCM_10, True),
     (_NG_OBJ_10, _SCM_10, False),
     (_NG_OBJ_10, _SCM_20, False),
     ),
)
def test_is_valid(obj, scm, success):
    assert TT.is_valid(obj, scm) == success

    if not success:
        with pytest.raises(TT.ValidationError):
            _rm = TT.is_valid(obj, scm, ac_schema_safe=False)
