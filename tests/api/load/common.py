#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
# pylint: disable=unused-import
"""Common module for tests.api.load."""
from __future__ import annotations

import anyconfig.api._load as TT

from ...common import (  # noqa: F401
    get_test_ids, load_data_for_testfile
)
from ..single_load.constants import LOADER_TYPES  # noqa: F401


class Basa:
    @staticmethod
    def target_fn(*args, **kwargs):
        return TT.load(*args, **kwargs)


class MultiBase:
    target: str = 'load/multi'


class SingleBase:
    target: str = 'load/single'
