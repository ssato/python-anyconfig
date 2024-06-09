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

TEST_FILES: list[pathlib.Path] = list(
    (CURDIR / "loaders").glob("*/test_*.py")
)

assert TEST_FILES

MOD_TYPE_DEFAULT: str = "json"

if any(f for f in TEST_FILES if f.parent.name == MOD_TYPE_DEFAULT):
    MOD_TYPE = MOD_TYPE_DEFAULT
    MOD_BACKEND: str = "stdlib"
else:
    MOD_TYPE: str = TEST_FILES[0].parent.name
    MOD_BACKEND: str = TEST_FILES[0].stem.split("_")[-1]

TEST_FILE = (
    CURDIR / "loaders" / MOD_TYPE / f"test_{MOD_TYPE}_{MOD_BACKEND}.py"
)
TEST_DATADIR = TT.common.RESOURCE_DIR / "loaders" / f"{MOD_TYPE}.{MOD_BACKEND}"
