#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Some global variables for test cases.
"""
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
