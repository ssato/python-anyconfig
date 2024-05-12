#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.backend.base.utils."""
from __future__ import annotations

import pathlib

import pytest

import anyconfig.backend.base.utils as TT


FILENAME: str = "file_not_exist.txt"


def test_not_implemented():
    with pytest.raises(NotImplementedError):
        TT.not_implemented()


@pytest.mark.parametrize(
    ("rel_path", ),
    ((FILENAME, ),
     ("a/b/c", ),
     ),
)
def test_ensure_outdir_exists(
    rel_path: str, tmp_path: pathlib.Path
) -> None:
    outpath = tmp_path / rel_path

    TT.ensure_outdir_exists(outpath)
    assert outpath.parent.exists()
