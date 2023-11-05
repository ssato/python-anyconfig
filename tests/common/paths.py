#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Compute paths.
"""
import pathlib


TEST_DATA_MAJOR_VERSION: int = 1

TESTDIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
RESOURCE_DIR: pathlib.Path = TESTDIR / "res" / str(TEST_DATA_MAJOR_VERSION)


def loader_resdir(loader: str) -> pathlib.Path:
    """Top dir to provide test resource data for the loader ``loader``.
    """
    return RESOURCE_DIR / "loaders" / loader


def dumper_resdir(dumper: str) -> pathlib.Path:
    """Top dir to provide test resource data for the dumper ``dumper``.
    """
    return RESOURCE_DIR / "dumpers" / dumper


def get_expected_data_path(
    ipath: pathlib.Path, file_ext: str = "json"
) -> pathlib.Path:
    """Get a path to expected data for input, `ipath`.
    """
    return ipath.parent / "e" / f"{ipath.name}.{file_ext}"
