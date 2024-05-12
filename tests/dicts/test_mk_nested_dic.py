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


NAMES: list[str] = ("obj", "val", "exp", "opts")
DATA_0: list[tuple] = common.load_data_for_testfile(
    __file__, (("q", ""), ("e", None), ("o", {})),
    load_idata=True
)
DATA: list[tuple] = [(d, *rest) for _, d, *rest in DATA_0]
DATA_IDS: list[str] = common.get_test_ids(DATA_0)


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_mk_nested_dic(obj, val, exp, opts):
    assert TT.mk_nested_dic(obj, val, **opts) == exp
