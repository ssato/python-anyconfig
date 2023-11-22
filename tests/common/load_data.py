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


def load_test_data_for_loader(
    loader: str, file_ext: FILE_EXT = "*",
    exp_ext: FILE_EXT = "json",
    keep_order: bool = False
) -> typing.List[
    typing.Tuple[pathlib.Path, typing.Any]
]:
    """Make a list of tples of test resource data pairs for loaders.
    """
    return [
        (f, load_data(
            paths.get_expected_data_path(f, exp_ext),
            file_ext=exp_ext, keep_order=keep_order
        ))
        for f in paths.loader_resdir(loader).glob(f"*/*.{file_ext}")
        if f.is_file()
    ]


def load_test_data_for_dumper(
    dumper: str, file_ext: FILE_EXT = "*",
    exp_ext: FILE_EXT = "json",
    keep_order: bool = False
) -> typing.List[
    typing.Tuple[pathlib.Path, pathlib.Path, typing.Any]
]:
    """Make a list of tples of test resource data pairs for loaders.
    """
    path_pairs = [  # [(input_filepath, expected_filepath)]
        (f, paths.get_expected_data_path(f, exp_ext))
        for f in paths.dumper_resdir(dumper).glob(f"*/*.{file_ext}")
        if f.is_file()
    ]

    return [
        (f, e, load_data(e, file_ext=exp_ext, keep_order=keep_order))
        for f, e in path_pairs
    ]
