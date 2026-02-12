#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
# pylint: disable=unused-import
"""Common module for tests.api.load."""
from __future__ import annotations

from ...multi_load.common import (  # noqa: F401
    NAMES, GLOB_PATTERN,
    load_data_for_testfile, get_test_ids,
)
