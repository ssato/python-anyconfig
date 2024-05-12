#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"tests.common - common global variables and functions."""
from .globals_ import TESTDIR, RESOURCE_DIR
from .tdc import (
    get_test_ids, load_data_for_testfile
)

__all__ = [
    "TESTDIR", "RESOURCE_DIR",
    "get_test_ids", "load_data_for_testfile",
]
