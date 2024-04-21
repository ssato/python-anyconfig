#
# Copyright (C) 2015 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name, protected-access
# pylint: disable=bare-except
from __future__ import annotations

import pytest

from .constants import (
    OBJ_10, OBJ_20,
    SCM_10, SCM_20,
    STRICT_SCM_10, STRICT_SCM_20,
    NG_OBJ_10
)
try:
    import anyconfig.schema.jsonschema.validator as TT
except ImportError:
    pytest.skip(
        "Required jsonschema lib is not available.",
        allow_module_level=True
    )


@pytest.mark.parametrize(
    ("obj", "scm"),
    ((OBJ_10, SCM_10),
     (OBJ_20, SCM_20),
     (OBJ_10, STRICT_SCM_10),
     (OBJ_20, STRICT_SCM_20),
     ),
)
def test_validate(obj, scm):
    (ret, msg) = TT.validate(obj, scm)
    assert not msg
    assert ret


@pytest.mark.parametrize(
    ("obj", "scm"),
    ((NG_OBJ_10, SCM_10),
     (NG_OBJ_10, SCM_20),
     ),
)
def test_validate__an_error(obj, scm):
    (ret, msg) = TT.validate(obj, scm, ac_schema_safe=True)
    assert msg
    assert not ret

    with pytest.raises(Exception):  # noqa: B017
        TT.validate(obj, scm, ac_schema_safe=False)


def test_validate__errors():
    obj: dict = {"a": 1, "b": 2.0}
    scm: dict = {
        "type": "object",
        "properties": {"a": {"type": "integer"}, "b": {"type": "string"}}
    }

    (ret, msg) = TT.validate(obj, scm, ac_schema_errors=True)
    assert msg  # ["'a' is not of type ...", "'b' is not ..."]
    assert not ret


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    ("obj", "scm", "success"),
    ((OBJ_10, SCM_10, True),
     (NG_OBJ_10, SCM_10, False),
     (NG_OBJ_10, SCM_20, False),
     ),
)
def test_is_valid(obj, scm, success):
    assert TT.is_valid(obj, scm) == success

    if not success:
        with pytest.raises(TT.ValidationError):
            TT.is_valid(obj, scm, ac_schema_safe=False)
