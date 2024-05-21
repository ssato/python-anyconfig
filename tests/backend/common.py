#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Common functions for test cases of loaders and dumpers."""
from __future__ import annotations

import importlib
import pathlib
import re
import typing

import anyconfig.ioinfo
import pytest

from .. import common


NAMES: tuple[str, ...] = ("ipath", "opts", "exp")
PATH_PATTERN: re.Pattern = re.compile(
    r".+[/\\:\.]test_([^_]+)_([^_]+).py"
)


def get_name(testfile: str, pattern: re.Pattern = PATH_PATTERN) -> str:
    """Get the name of backend module.

    ex. tests/backend/loaders/json/test_json_stdlib.py
    -> "json.stdlib"
    """
    match = pattern.match(testfile)
    if not match:
        raise NameError(
            f"Filename does not match expected pattern: {testfile}"
        )

    return ".".join(match.groups())


def get_mod(testfile: str, pattern: re.Pattern = PATH_PATTERN):
    """Get the module to test."""
    name = get_name(testfile, pattern=pattern)
    mname = f"anyconfig.backend.{name}"
    try:
        return importlib.import_module(mname)
    except ImportError:
        pytest.skip(
            f"Skip becuase it failed to import: {mname}",
            allow_module_level=True
        )

    return None  # To suppress inconsistent-return-statements.


def get_test_ids(*args, **opts):
    return common.get_test_ids(*args, **opts)


def get_test_resdir(
    testfile: str,
    pattern: re.Pattern = PATH_PATTERN
) -> pathlib.Path:
    """Get test resource dir for given test file path.

    ex. tests/backend/loaders/json/test_json_stdlib.py
    -> tests/res/1/loaders/json.stdlib/
    """
    subdir = pathlib.Path(testfile).parent.parent.name
    name = get_name(testfile, pattern=pattern)

    return common.RESOURCE_DIR / subdir / name


def load_data_for_testfile(
    testfile: str,
    **opts
) -> list[tuple[pathlib.Path, dict[str, typing.Any], ...]]:
    datadir = get_test_resdir(testfile)
    return common.load_data_for_testfile(
        testfile, datadir=datadir, **opts
    )


def ioinfo_from_path(path: pathlib.Path) -> anyconfig.ioinfo.IOInfo:
    return anyconfig.ioinfo.make(path)
