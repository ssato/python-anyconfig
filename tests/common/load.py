#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,bare-except
r"""Functions to load test data.
"""
import json
import pathlib

from . import (
    load_py,
)


def load_data(
    path: pathlib.Path, **kwargs
):
    """Load data."""
    file_ext = path.suffix[1:]
    if not file_ext:
        return None

    try:
        if file_ext == "txt":
            return path.read_text()

        if file_ext == "dat":
            return path.read_bytes()

        if file_ext == "py":
            return load_py.load_from_path(path, **kwargs)

        if file_ext == "json":
            return json.load(path.open(), **kwargs)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load from: {path}, exc: {exc!r}"
        ) from exc

    raise ValueError(f"Unknown type of file was gigven: {path!r}")
