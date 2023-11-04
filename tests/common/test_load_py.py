#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Testcases for tests.common.load_py.
"""
import pathlib
import typing

import pytest

from . import load_py as TT


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
    filepath = tmp_path / TEST_DATA_FILENAME
    filepath.write_text(inp)

    assert TT.load_literal_data_from_path(filepath) == exp


@pytest.mark.parametrize(
    ('inp', 'exp'),
    DATA_PAIRS
)
def test_load_data_from_py(
    inp: str, exp: typing.Any, tmp_path: pathlib.Path
):
    filepath = tmp_path / TEST_DATA_FILENAME
    filepath.write_text(f"{TT.DATA_VAR_NAME} = {inp}")

    assert TT.load_data_from_py(filepath) == exp
