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
