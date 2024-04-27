#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2024 Satoru SATOH <satoru.satoh gmail.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import annotations

import typing

import pytest

import anyconfig.dicts as TT

from . import common


DATASETS: list[tuple[typing.Any, dict[str, typing.Any]]] = [
    (obj, data) for _, obj, data in common.collect_data("get")
]


@pytest.mark.parametrize(("obj", "data"), DATASETS)
def test_get(obj, data):
    query = data.get("q")
    exp = data.get("e")
    emsg = data.get("s")

    (res, err) = TT.get(obj, query)

    assert bool(err) if emsg else err == ""
    assert res == exp
