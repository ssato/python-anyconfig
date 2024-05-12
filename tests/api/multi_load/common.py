#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Common constants and utility functions for test cases of
anyconfig.api.multi_load.
"""
from __future__ import annotations

import anyconfig.api.utils

from ... import common


NAMES: tuple[str, ...] = ("inputs", "opts", "exp")
GLOB_PATTERN: str = "*.*"


def load_data_for_testfile(testfile: str, **kwargs):
    return [
        (sorted(i.parent.glob(GLOB_PATTERN)), opts, exp, *rest)
        for i, opts, exp, *rest
        in common.load_data_for_testfile(testfile, **kwargs)
        if exp is not None
    ]


def get_test_ids(data: list) -> list[str]:
    return common.get_test_ids(
        [(mis[0] if anyconfig.utils.is_iterable(mis) else mis, *rest)
         for mis, *rest in data]
    )
