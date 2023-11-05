#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Compute paths.
"""
import functools
import pathlib


def test_topdir() -> pathlib.Path:
    """Resove the dir this .py module exists.
    """
    return pathlib.Path(__file__).parent.parent.resolve()


@functools.lru_cache(maxsize=None)
def resdir(major_version: int = 1) -> pathlib.Path:
    """Top dir to provide test resource data.
    """
    return test_topdir() / "res" / str(major_version)


def loader_resdir(loader: str, major_version: int = 1) -> pathlib.Path:
    """Top dir to provide test resource data for the loader ``loader``.
    """
    return resdir(major_version=major_version) / "loaders" / loader


def dumper_resdir(dumper: str, major_version: int = 1) -> pathlib.Path:
    """Top dir to provide test resource data for the dumper ``dumper``.
    """
    return resdir(major_version=major_version) / "dumpers" / dumper


def get_expected_data_path(
    ipath: pathlib.Path, file_ext: str = "json"
) -> pathlib.Path:
    """Get a path to expected data for input, `ipath`.
    """
    return ipath.parent / "e" / f"{ipath.name}.{file_ext}"
