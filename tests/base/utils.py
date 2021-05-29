#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common utility functions.
"""
import pathlib
import typing

from .common import TESTS_DIR


def resource_path(path: str) -> pathlib.Path:
    """
    Return the path of resources with given relative path.
    """
    return TESTS_DIR / 'res' / path


def list_resources(path: str) -> typing.Iterator[pathlib.Path]:
    if '*' not in path:
        raise ValueError(
            f"The first arg. must contain glob '*' patterns: {path}"
        )

    for ipath in (TESTS_DIR / 'res').glob(path):
        yield ipath

# vim:sw=4:ts=4:et:
