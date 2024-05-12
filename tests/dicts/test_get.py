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
