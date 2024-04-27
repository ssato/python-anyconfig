#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2024 Satoru SATOH <satoru.satoh gmail.com>
#
# pylint: disable=missing-docstring
from __future__ import annotations

import typing

import pytest

import anyconfig.dicts as TT

from . import common


DATASETS: list[tuple[typing.Any, dict[str, typing.Any]]] = [
    (obj, data) for _, obj, data in common.collect_data("merge")
]


@pytest.mark.parametrize(("obj", "data"), DATASETS)
def test_merge(obj, data):
    exp = data.get("e")
    upd = data.get("s")
    opts = data.get("o")

    TT.merge(obj, upd, **opts)
    assert obj == exp


@pytest.mark.parametrize(("obj", "data"), DATASETS)
def test_merge_with_a_dict(obj, data):
    exp = data.get("e")
    upd = data.get("s")
    opts = data.get("o")

    TT.merge(obj, upd, **opts)
    assert obj == exp


@pytest.mark.parametrize(("obj", "data"), DATASETS)
def test_merge_with_an_iterable(obj, data):
    exp = data.get("e")
    upd = data.get("s").items()
    opts = data.get("o")

    TT.merge(obj, upd, **opts)
    assert obj == exp


def test_merge_with_invalid_data():
    with pytest.raises((ValueError, TypeError)):
        TT.merge({"a": 1}, 1)
