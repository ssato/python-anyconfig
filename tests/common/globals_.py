#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Some global variables for test cases.
"""
import pathlib


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

TEST_DATA_MAJOR_VERSION: int = 1

TESTDIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
RESOURCE_DIR: pathlib.Path = TESTDIR / "res" / str(TEST_DATA_MAJOR_VERSION)
