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

from . import (
    load_py,
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
        return load_py.load_from_path(path, **kwargs)

    if file_ext == "json":
        if keep_order:
            kwargs["object_pairs_hook"] = collections.OrderedDict

        return json.load(path.open(), **kwargs)

    raise ValueError(f"Unknown type of file was gigven: {path!r}")
