#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.load (multi_load)."""
from __future__ import annotations

import collections
import typing

import pytest

import anyconfig.api._load as TT

from .common import (
    NAMES, GLOB_PATTERN, load_data_for_testfile, get_test_ids,
)

if typing.TYPE_CHECKING:
    import pathlib


DATA = load_data_for_testfile(__file__)
DATA_IDS: list[str] = get_test_ids(DATA)

DATA_W_GLOB = [
    (inputs[0].parent / GLOB_PATTERN, opts, exp)
    for inputs, opts, exp in DATA
]


def test_data() -> None:
    assert DATA


def test_load_with_empty_list() -> None:
    with pytest.raises(ValueError, match="Maybe invalid input"):
        TT.load([])


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_load_for_a_list_of_path_objects(
    inputs: list[pathlib.Path], opts: dict, exp,
) -> None:
    assert TT.load(inputs, **opts) == exp
    assert TT.load((i for i in inputs), **opts) == exp


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_load_for_a_list_of_path_strings(
    inputs: list[pathlib.Path], opts: dict, exp,
) -> None:
    assert TT.load([str(i) for i in inputs], **opts) == exp
    assert TT.load((str(i) for i in inputs), **opts) == exp


@pytest.mark.parametrize(
    NAMES, DATA_W_GLOB, ids=get_test_ids(DATA_W_GLOB),
)
def test_load_for_glob_patterns(
    inputs: list[pathlib.Path], opts: dict, exp,
) -> None:
    assert TT.load(inputs, **opts) == exp


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_load_for_a_list_of_streams(
    inputs: list[pathlib.Path], opts: dict, exp,
) -> None:
    assert TT.load([i.open() for i in inputs], **opts) == exp


class MyDict(collections.OrderedDict):
    """Custom dict-like object."""


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_load_with_ac_dict_option(
    inputs: list[pathlib.Path], opts: dict, exp,
) -> None:
    res = TT.load(inputs, ac_dict=MyDict, **opts)
    assert res == exp
    assert isinstance(res, MyDict)


@pytest.mark.parametrize(NAMES, DATA[:1], ids=DATA_IDS[:1])
def test_load_with_wrong_merge_strategy(
    inputs: list[pathlib.Path], opts: dict, exp,
) -> None:
    assert exp  # dummy to avoid an error of unused argument.
    with pytest.raises(ValueError, match="Wrong merge strategy"):
        TT.load(inputs, ac_merge="wrong_merge_strategy", **opts)


def test_load_with_ignore_missing_option() -> None:
    paths = [
        "/path/to/file_not_exist_0.json",
        "/path/to/file_not_exist_1.json",
        "/path/to/file_not_exist_2.json",
    ]
    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        TT.load(paths)

    assert TT.load(paths, ac_ignore_missing=True) == {}
