#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Testcases for tests.common.load_data.
"""
import pathlib
import typing

import pytest

from . import (
    globals_,
    load as TT,
)


def test_load_data__unkown_file_type(tmp_path: pathlib.Path):
    with pytest.raises(ValueError):
        path = tmp_path / "foo.unknown_file_type_ext"
        TT.load_data(path)


@pytest.mark.parametrize(
    ("filename", "content"),
    (("null.txt", ""),
     ("a.txt", "aaa"),
     ("b_null.dat", b""),
     ("display.dat", b"\xe8\xa1\xa8\xe7\xa4\xba"),
     ),
)
def test_load_data__txt_or_bytes(
    filename: str, content: typing.Union[str, bytes],
    tmp_path: pathlib.Path
):
    path = tmp_path / filename

    if isinstance(content, str):
        path.write_text(content)
    else:
        path.write_bytes(content)

    assert TT.load_data(path) == content


@pytest.mark.parametrize(
    ("filename", "content", "exp"),
    [(f"{i!s}.py", c, e) for i, (c, e) in enumerate(globals_.DATA_PAIRS)]
)
def test_load_data__py(
    filename: str, content: str, exp: typing.Any, tmp_path: pathlib.Path
):
    path = tmp_path / filename
    path.write_text(content)

    assert TT.load_data(path) == exp
