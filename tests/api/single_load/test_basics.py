#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
from __future__ import annotations

import collections
import pathlib

import pytest

import anyconfig.api._load as TT
import anyconfig.parsers

from anyconfig.api import (
    UnknownFileTypeError, UnknownProcessorTypeError
)
from ... import common


JSON_PARSER = anyconfig.parsers.find(None, 'json')

NAMES: tuple[str, ...] = ("ipath", "opts", "exp")
DATA: list = common.load_data_for_testfile(
    __file__, (("o", {}), ("e", None))
)
DATA_IDS: list[str] = common.get_test_ids(DATA)

NAMES_2: tuple[str, ...] = ("ipath", "exp")
DATA_2: list = [(ipath, exp) for ipath, _, exp in DATA]


def test_data() -> None:
    assert DATA


class MyDict(collections.OrderedDict):
    """My original dict class keep key orders."""


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_single_load_from_stream(ipath, opts, exp):
    assert TT.single_load(ipath.open(), **opts) == exp


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_single_load_from_path_str(ipath, opts, exp):
    assert TT.single_load(str(ipath), **opts) == exp


@pytest.mark.parametrize(NAMES_2, DATA_2, ids=DATA_IDS)
def test_single_load_with_ac_parser_by_instance(ipath, exp):
    assert TT.single_load(ipath, ac_parser=JSON_PARSER) == exp


@pytest.mark.parametrize(NAMES_2, DATA_2, ids=DATA_IDS)
def test_single_load_with_ac_parser_by_id(ipath, exp):
    assert TT.single_load(ipath, ac_parser=JSON_PARSER.cid()) == exp


@pytest.mark.parametrize(NAMES_2, DATA_2, ids=DATA_IDS)
def test_single_load_with_ac_ordered(ipath, exp):
    assert TT.single_load(
        ipath, ac_ordered=True
    ) == collections.OrderedDict(exp)


@pytest.mark.parametrize(NAMES_2, DATA_2, ids=DATA_IDS)
def test_single_load_with_ac_dict(ipath, exp):
    res = TT.single_load(ipath, ac_dict=MyDict)
    assert isinstance(res, MyDict)
    assert res == MyDict(**exp)


def test_single_load_missing_file_failures():
    with pytest.raises(FileNotFoundError):
        TT.single_load("not_exist.json")


def test_single_load_unknown_file_type_failures():
    with pytest.raises(UnknownFileTypeError):
        TT.single_load("dummy.txt")


def test_single_load_invalid_parser_object_failures():
    with pytest.raises(ValueError):
        TT.single_load("dummy.txt", ac_parser=object())


@pytest.mark.parametrize(
    ("ipath", ), [(ipath, ) for ipath, _, _ in DATA], ids=DATA_IDS
)
def test_single_load_unknown_processor_type_failures(ipath):
    with pytest.raises(UnknownProcessorTypeError):
        TT.single_load(ipath, ac_parser="proc_does_not_exist")


def test_single_load_ignore_missing():
    ipath = pathlib.Path() / 'conf_file_not_exist.json'
    assert not ipath.exists()

    assert TT.single_load(
        ipath, ac_parser='json', ac_ignore_missing=True
    ) == {}
