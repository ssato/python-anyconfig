#
# Copyright (C) 2015 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name, protected-access
# pylint: disable=bare-except
from __future__ import annotations

import copy


OBJ_10: dict = {"a": 1}
SCM_10: dict = {
    "properties": {"a": {"type": "integer"}},
    "type": "object"
}
STRICT_SCM_10 = copy.deepcopy(SCM_10)
STRICT_SCM_10["required"] = ["a"]

OBJ_20: dict = {"a": 1, "b": [1, 2], "c": {"d": "aaa", "e": 0.1}}
SCM_20: dict = {
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
STRICT_SCM_20 = copy.deepcopy(SCM_20)
STRICT_SCM_20["properties"]["b"]["minItems"] = 2
STRICT_SCM_20["properties"]["b"]["uniqueItems"] = True
STRICT_SCM_20["properties"]["c"]["required"] = ["d", "e"]
STRICT_SCM_20["required"] = ["a", "b", "c"]

NG_OBJ_10: dict = {"a": "aaa"}
