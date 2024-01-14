#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Testcases for tests.common.load_py.
"""
import collections
import pathlib
import typing

import pytest

import anyconfig.backend.python.utils as TT


DATA_PAIRS = (
    ('None', None),
    ('1', 1),
    ('"1"', '1'),
    ('[]', []),
    ('[1, 2]', [1, 2]),
    ('{}', {}),
    ('{"a": 1}', {'a': 1}),
    ('{"a": [1, 2, 3]}', {'a': [1, 2, 3]}),
)

TEST_DATA_FILENAME: str = "test_data.py"


@pytest.mark.parametrize(
    ('inp', 'exp'),
    DATA_PAIRS
)
def test_load_literal_data_from_string(inp: str, exp: typing.Any):
    assert TT.load_literal_data_from_string(inp) == exp


@pytest.mark.parametrize(
    ('inp', 'exp'),
    DATA_PAIRS
)
def test_load_literal_data_from_path(
    inp: str, exp: typing.Any, tmp_path: pathlib.Path
):
    ipath = tmp_path / TEST_DATA_FILENAME
    ipath.write_text(inp)

    assert TT.load_literal_data_from_path(ipath) == exp


def test_load_data_from_py_errors(tmp_path: pathlib.Path):
    ipath = tmp_path / TEST_DATA_FILENAME
    ipath.touch()  # empty.

    with pytest.raises(ValueError):
        with pytest.warns(UserWarning):
            TT.load_data_from_py(ipath)


@pytest.mark.parametrize(
    ('inp', 'exp'),
    DATA_PAIRS
)
def test_load_data_from_py_safely(
    inp: str, exp: typing.Any, tmp_path: pathlib.Path
):
    ipath = tmp_path / TEST_DATA_FILENAME
    ipath.write_text(f"{TT.DATA_VAR_NAME} = {inp}")

    assert TT.load_data_from_py(ipath, fallback=True) == exp


PY_DATA_0 = {"a": 1, "b": "B", "c": [1, 2, 3], "d": {"d": {"d2": True}}}
PY_SCRIPT_0: str = f"""
import collections

{TT.DATA_VAR_NAME} = collections.OrderedDict({list(PY_DATA_0.items())})
"""


@pytest.mark.parametrize(
    ('inp', 'exp'),
    ((PY_SCRIPT_0, collections.OrderedDict(PY_DATA_0.items())),
     ),
)
def test_load_data_from_py_complex_cases(
    inp: str, exp: typing.Any, tmp_path: pathlib.Path
):
    ipath = tmp_path / TEST_DATA_FILENAME
    ipath.write_text(inp)

    assert TT.load_data_from_py(ipath) == exp


@pytest.mark.parametrize(
    ('inp', 'exp'),
    DATA_PAIRS
)
def test_load_from_path(
    inp: str, exp: typing.Any, tmp_path: pathlib.Path
):
    ipath = tmp_path / TEST_DATA_FILENAME

    ipath.write_text(inp)
    assert TT.load_from_path(ipath) == exp

    ipath.write_text(f"{TT.DATA_VAR_NAME} = {inp}")
    assert TT.load_from_path(ipath, allow_exec=True, fallback=True) == exp
