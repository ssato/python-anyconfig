#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""test cases for anyconfig.ioinfo.detectors."""
from __future__ import annotations

import pathlib

import pytest

import anyconfig.ioinfo
import anyconfig.ioinfo.detectors as TT


PATH_STR_10 = __file__
PATH_OBJ_10 = pathlib.Path(PATH_STR_10)
FILE_OBJ_10 = open(__file__, encoding="utf-8")
IOI_OBJ_10 = anyconfig.ioinfo.make(__file__)

PATH_OBJ_20 = PATH_OBJ_10.resolve()
PATH_STR_20 = str(PATH_OBJ_20)
IOI_OBJ_20 = anyconfig.ioinfo.make(FILE_OBJ_10)


@pytest.mark.parametrize(
    ("target_fn", "obj", "exp"),
    ((TT.is_path_str, None, False),
     (TT.is_path_str, 0, False),
     (TT.is_path_str, PATH_OBJ_10, False),
     (TT.is_path_str, PATH_OBJ_20, False),
     (TT.is_path_str, FILE_OBJ_10, False),
     (TT.is_path_str, IOI_OBJ_10, False),
     (TT.is_path_str, IOI_OBJ_20, False),
     (TT.is_path_str, PATH_STR_10, True),
     (TT.is_path_str, PATH_STR_20, True),
     (TT.is_path_obj, None, False),
     (TT.is_path_obj, 0, False),
     (TT.is_path_obj, PATH_STR_10, False),
     (TT.is_path_obj, PATH_STR_20, False),
     (TT.is_path_obj, FILE_OBJ_10, False),
     (TT.is_path_obj, IOI_OBJ_10, False),
     (TT.is_path_obj, IOI_OBJ_20, False),
     (TT.is_path_obj, PATH_OBJ_10, True),
     (TT.is_path_obj, PATH_OBJ_20, True),
     (TT.is_io_stream, None, False),
     (TT.is_io_stream, 0, False),
     (TT.is_io_stream, PATH_STR_10, False),
     (TT.is_io_stream, PATH_STR_20, False),
     (TT.is_io_stream, PATH_OBJ_10, False),
     (TT.is_io_stream, PATH_OBJ_20, False),
     (TT.is_io_stream, IOI_OBJ_10, False),
     (TT.is_io_stream, IOI_OBJ_20, False),
     (TT.is_io_stream, FILE_OBJ_10, True),
     (TT.is_ioinfo, None, False),
     (TT.is_ioinfo, 0, False),
     (TT.is_ioinfo, PATH_STR_10, False),
     (TT.is_ioinfo, PATH_STR_20, False),
     (TT.is_ioinfo, PATH_OBJ_10, False),
     (TT.is_ioinfo, PATH_OBJ_20, False),
     (TT.is_ioinfo, FILE_OBJ_10, False),
     (TT.is_ioinfo, IOI_OBJ_10, True),
     (TT.is_ioinfo, IOI_OBJ_20, True),
     (TT.is_stream, None, False),
     (TT.is_stream, 0, False),
     (TT.is_stream, PATH_STR_10, False),
     (TT.is_stream, PATH_STR_20, False),
     (TT.is_stream, PATH_OBJ_10, False),
     (TT.is_stream, PATH_OBJ_20, False),
     (TT.is_stream, FILE_OBJ_10, False),
     (TT.is_stream, IOI_OBJ_10, False),
     (TT.is_stream, IOI_OBJ_20, True),
     ),
)
def test_is_path_str(target_fn, obj, exp):
    assert (target_fn(obj) == exp if exp else not target_fn(obj))
