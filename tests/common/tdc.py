#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test Data Collecor."""
from __future__ import annotations

import itertools
import os.path
import pathlib
import re
import typing

from . import paths, globals_


TEST_FILE_RE: re.Pattern = re.compile(r"test_(.+).py")

VALUES: tuple[tuple[str, typing.Optional[dict], ...], ...] = (
    ("o", {}), ("e", None)
)

LVL_DEFAULT: int = 3


def get_test_id(path: pathlib.Path, level: int = LVL_DEFAULT) -> str:
    return os.path.join(*path.parts[-level:])


def get_test_ids(
    data: list[tuple[pathlib.Path, typing.Any, ...]],
    level: int = LVL_DEFAULT
) -> list[str]:
    return [get_test_id(p, level=level) for p, *_ in data]


def get_test_resdir(
    testfile: str,
    topdir: pathlib.Path = globals_.TESTDIR,
    resdir: pathlib.Path = globals_.RESOURCE_DIR,
    pattern: re.Pattern = TEST_FILE_RE
) -> pathlib.Path:
    """Get test resource dir for given test file path.

    ex. tests/api/single_load/test_query.py
     -> /path/to/tests/res/1/api/single_load/query/
    """
    path = pathlib.Path(testfile).resolve()
    subdir = pattern.match(path.name).groups()[0]
    relpath = os.path.join(
        *[x for x, y in itertools.zip_longest(path.parent.parts, topdir.parts)
          if y is None]
    )

    return resdir / relpath / subdir


def load_data_for_testfile(
    testfile: str,
    values: tuple[tuple[str, typing.Optional[dict], ...], ...] = VALUES,
    load_idata: bool = False,
    datadir: typing.Optional[pathlib.Path] = None,
    **opts
) -> list[tuple[pathlib.Path, dict[str, typing.Any], ...]]:
    """Collct test data for test file, ``testfile``.

    :param testfile: a str represents test file path
    :param opts: keyword options for `get_test_resdir`
    """
    if datadir is None:
        datadir = get_test_resdir(testfile, **opts)

    if load_idata:
        return [
            (ipath, idata, *[aux.get(k, v) for k, v in values])
            for ipath, idata, aux
            in paths.load_data(datadir, load_idata=True)
        ]

    return [
        (ipath, *[aux.get(k, v) for k, v in values])
        for ipath, aux in paths.load_data(datadir)
    ]
