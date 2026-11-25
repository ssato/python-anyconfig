#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2024 Satoru SATOH <satoru.satoh gmail.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import annotations

import pytest

import anyconfig.dicts as TT

from .. import common


NAMES: list[str] = ("obj", "query", "exp", "emsg")
DATA_0: list[tuple] = common.load_data_for_testfile(
    __file__, (("q", ""), ("e", None), ("s", "")),
    load_idata=True
)
DATA: list[tuple] = [(d, *rest) for _, d, *rest in DATA_0]
DATA_IDS: list[str] = common.get_test_ids(DATA_0)


def test_data():
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_get(obj, query, exp, emsg):
    (res, err) = TT.get(obj, query)

    assert bool(err) if emsg else err == ""
    assert res == exp


@pytest.mark.parametrize(
    ("query", "expected"),
    (
        ("services/0/host", "database"),
        ("services.1.host", "api"),
        ("services/0\n/host", "database"),
        ("matrix/1/0", 3),
        ("numeric/01", "mapping key"),
        ("escaped/0/a~1b/~0key", 42),
    ),
)
def test_get_through_nested_arrays(query, expected):
    obj = {
        "services": [{"host": "database"}, {"host": "api"}],
        "matrix": [[1, 2], [3, 4]],
        "numeric": {"01": "mapping key"},
        "escaped": [{"a/b": {"~key": 42}}],
    }

    assert TT.get(obj, query) == (expected, "")


@pytest.mark.parametrize("index", ("01", "1junk", "-1", "2"))
def test_get_invalid_array_index(index):
    value, error = TT.get({"values": [10, 20]}, "values/" + index)

    assert value is None
    assert error
