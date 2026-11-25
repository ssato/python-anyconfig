#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2024 Satoru SATOH <satoru.satoh gmail.com>
#
# pylint: disable=missing-docstring
from __future__ import annotations

import pytest

import anyconfig.dicts as TT

from .. import common


NAMES: list[str] = ("obj", "exp", "upd", "opts")
DATA_0: list[tuple] = common.load_data_for_testfile(
    __file__, (("e", None), ("s", {}), ("o", {})),
    load_idata=True
)
DATA: list[tuple] = [(d, *rest) for _, d, *rest in DATA_0]
DATA_IDS: list[str] = common.get_test_ids(DATA_0)


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_merge(obj, exp, upd, opts):
    TT.merge(obj, upd, **opts)
    assert obj == exp


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_merge_with_a_dict(obj, exp, upd, opts):
    TT.merge(obj, upd, **opts)
    assert obj == exp


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_merge_with_an_iterable(obj, exp, upd, opts):
    TT.merge(obj, upd.items(), **opts)
    assert obj == exp


def test_merge_with_invalid_data():
    with pytest.raises((ValueError, TypeError)):
        TT.merge({"a": 1}, 1)


@pytest.mark.parametrize(
    ("strategy", "expected"),
    (
        (TT.MS_REPLACE, {"nested": {"b": 2}, "items": [2], "new": 3}),
        (TT.MS_NO_REPLACE, {"nested": {"a": 1}, "items": [1], "new": 3}),
        (TT.MS_DICTS, {"nested": {"a": 1, "b": 2}, "items": [2], "new": 3}),
        (TT.MS_DICTS_AND_LISTS,
         {"nested": {"a": 1, "b": 2}, "items": [1, 2], "new": 3}),
    ),
)
def test_merge_with_a_one_shot_iterator(strategy, expected):
    obj = {"nested": {"a": 1}, "items": [1]}
    updates = ((key, value) for key, value in (
        ("nested", {"b": 2}), ("items", [2]), ("new", 3),
    ))

    TT.merge(obj, updates, ac_merge=strategy)

    assert obj == expected


def test_merge_iterator_retains_repeated_keys():
    obj = {"nested": {"original": 0}}
    updates = iter((("nested", {"a": 1}), ("nested", {"b": 2})))

    TT.merge(obj, updates, ac_merge=TT.MS_DICTS)

    assert obj == {"nested": {"original": 0, "a": 1, "b": 2}}
