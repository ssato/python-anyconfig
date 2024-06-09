#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Constants for tests.backend.*."""
from __future__ import annotations

import pathlib

from . import common as TT


CURDIR: pathlib.Path = pathlib.Path(__file__).parent

MOD_TYPE: str = "json"
MOD_BACKEND: str = "stdlib"

TEST_FILE = (
    CURDIR / "loaders" / MOD_TYPE / f"test_{MOD_TYPE}_{MOD_BACKEND}.py"
)
TEST_DATADIR = TT.common.RESOURCE_DIR / "loaders" / "json.stdlib"
