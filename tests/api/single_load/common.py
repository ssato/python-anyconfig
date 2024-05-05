#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
""""Common functions of test cases for anyconfig.api.single_load."""
from __future__ import annotations

import pathlib
import re
import typing

import anyconfig.api

from ...common import tdc


LOADER_TYPES = frozenset(anyconfig.api.list_types())

MOD: str = pathlib.Path(__file__).parent.name

TESTFILE_RE: re.Pattern = re.compile(r"^test_(.+).py$")

VALUES: tuple[tuple[str, typing.Optional[dict], ...], ...] = (
    ("c", {}), ("e", None), ("o", {})
)

if typing.TYPE_CHECKING:
    DataType = list[tuple[pathlib.Path, typing.Optional[dict], ...]]


def get_test_ids(data: DataType) -> list[str]:
    return [
        f"{p.parent.parent.name}/{p.parent.name}/{p.name}"
        for p, *_ in data
    ]


def get_mod_target_by_test_filepath(
    fpath: str, pattern: re.pattern = TESTFILE_RE
) -> tuple[str, ...]:
    """Get module name and target name by test file's path.

    :return: (module_name, target_name) or ()
    """
    path = pathlib.Path(fpath)
    match = pattern.match(path.name)
    if match:
        return (path.parent.name, match.groups()[0])

    return ()


def load_datasets(
    target: str, mod: str = MOD, values: tuple = VALUES,
) -> DataType:
    return [
        (ipath, *[data.get(k, v) for k, v in values])
        for ipath, data
        in tdc.collect_for(mod, target, subdir="api", load=False)
    ]


def load_datasets_by_test_filepath(
    path: str, values: tuple = VALUES,
) -> DataType:
    mod_target = get_mod_target_by_test_filepath(path)
    if not mod_target:
        return []

    return [
        (ipath, *[data.get(k, v) for k, v in values])
        for ipath, data
        in tdc.collect_for(*mod_target, subdir="api", load=False)
    ]
