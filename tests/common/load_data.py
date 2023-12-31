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


def load_data(
    path: pathlib.Path, keep_order: bool = False, **kwargs
):
    """Load data."""
    file_ext = path.suffix[1:]
    if not file_ext:
        return None

    if file_ext == "txt":
        return path.read_text()

    if file_ext == "dat":
        return path.read_bytes()

    if file_ext == "py":
        return load_py.load_literal_data_from_path(path)

    if file_ext == "json":
        if keep_order:
            kwargs["object_pairs_hook"] = collections.OrderedDict

        return json.load(path.open(), **kwargs)

    return None


def load_test_data(
    loader_or_dumper: str, is_loader: bool = True,
    keep_order: bool = False, **kwargs
) -> typing.List[
    typing.Tuple[pathlib.Path, typing.Any, typing.Any]
]:
    """Make a list of tuples of test data pairs for loader or dumper.

    :return:
        A list of tuples of (input_file_path, {subdir: loaded_data})
    """
    return [
        (
            ipath,
            {
                subdir: load_data(apath, keep_order=keep_order)
                for subdir, apath in apaths.items()
            }
        )
        for ipath, apaths in paths.get_data_paths(
            loader_or_dumper, is_loader=is_loader, **kwargs
        )
    ]
