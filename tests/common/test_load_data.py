#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Testcases for tests.common.load_py.
"""
import pathlib
import typing

import pytest

from . import (
    globals_,
    load_data as TT,
    load_py,
    paths
)


JSON_DATA_DIR: pathlib.Path = paths.loader_resdir("json.json") / "10"


@pytest.mark.parametrize(
    ("filename", "content", "exp"),
    [(f"{i!s}.py", c, e) for i, (c, e) in enumerate(globals_.DATA_PAIRS)]
)
def test_load_data__py(
    filename: str, content: str, exp: typing.Any, tmp_path: pathlib.Path
):
    path = tmp_path / filename
    path.write_text(content)

    assert TT.load_data(path, file_ext="py") == exp


@pytest.mark.parametrize(
    ("path", "exp"),
    [(p, TT.load_data(p.parent / "e" / f"{p.name}.py", file_ext="py"))
     for p in JSON_DATA_DIR.glob("*.json")]
)
def test_load_data__json(path: pathlib.Path, exp: typing.Any):
    assert TT.load_data(path, file_ext="json") == exp
    assert TT.load_data(path) == exp

    # python > 3.7.0 keeps insertion order of items in dicts.
    #
    # .. seealso::
    #    https://docs.python.org/3.7/whatsnew/3.7.html
    #    https://mail.python.org/pipermail/python-dev/2017-December/151283.html
    assert TT.load_data(path, keep_order=True) == exp


@pytest.mark.parametrize(
    ("loader", "file_ext", "exp_ext"),
    (("json.json", "json", "py"),
     ("toml.tomllib", "toml", "json"),
     )
)
def test_load_test_data_for_loader(
    loader: str, file_ext: TT.FILE_EXT, exp_ext: TT.FILE_EXT
):
    res = TT.load_test_data_for_loader(
        loader, file_ext=file_ext, exp_ext=exp_ext
    )
    assert res

    # implicit cases.
    res = TT.load_test_data_for_loader(loader, exp_ext=exp_ext)
    assert res
