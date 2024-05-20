#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Common functions for test cases of loaders and dumpers."""
from __future__ import annotations

import pathlib
import re
import typing

from .. import common


PATH_PATTERN: re.Pattern = re.compile(
    r".+[/\\:\.]test_([^_]+)_([^_]+).py"
)


def get_test_resdir(
    testfile: str,
    is_loader: bool = True,
    pattern: re.Pattern = PATH_PATTERN
) -> pathlib.Path:
    """Get test resource dir for given test file path.

    ex. tests/backend/loaders/json/test_json_stdlib.py
    -> tests/res/1/loaders/json.stdlib/
    """
    match = pattern.match(testfile)
    if not match:
        raise NameError(
            f"Filename does not match expected pattern: {testfile}"
        )

    name = ".".join(match.groups())
    subdir = "loaders" if is_loader else "dumpers"

    return common.RESOURCE_DIR / subdir / name


def load_data_for_testfile(
    testfile: str,
    is_loader: bool = True,
    **opts
) -> list[tuple[pathlib.Path, dict[str, typing.Any], ...]]:
    datadir = get_test_resdir(testfile, is_loader=is_loader)
    return common.load_data_for_testfile(
        testfile, datadir=datadir, **opts
    )
