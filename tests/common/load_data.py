#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
r"""Functions to load test data.
"""
import collections
import json
import pathlib
import typing

from . import (
    load_py, paths,
)


FILE_EXT = typing.Literal[
    "py",
    "json"
]


def load_data(
    path: pathlib.Path, file_ext: FILE_EXT = "json", keep_order: bool = False
):
    """Load data.
    """
    if file_ext == "py":
        return load_py.load_literal_data_from_path(path)

    if file_ext == "json":
        if keep_order:
            return json.load(
                path.open(), object_pairs_hook=collections.OrderedDict
            )
        return json.load(path.open())

    return None


def load_test_data(
    loader_or_dumper: str, is_loader: bool = True,
    keep_order: bool = False, **kwargs
) -> typing.List[
    typing.Tuple[pathlib.Path, typing.Any]
]:
    """Make a list of tuples of test data pairs for loader or dumper.
    """
    return [
        (ipath, load_data(epath, keep_order=keep_order))
        for ipath, epath in paths.get_data_path_pairs(
            loader_or_dumper, is_loader=is_loader, **kwargs
        )
    ]
