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
    load_data as TT,
    paths
)


@pytest.mark.parametrize(
    ("filename", "content"),
    (("null.txt", ""),
     ("a.txt", "aaa"),
    ),
)
def test_load_data__txt(filename: str, content: str, tmp_path: pathlib.Path):
    path = tmp_path / filename
    path.write_text(content)

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


@pytest.mark.skip(reason="not implemente yet")
@pytest.mark.parametrize(
    ("loader_or_dumper", "is_loader"),
    (
        ("json.json", True),
    ),
)
def test_load_test_data(
    loader_or_dumper: str, is_loader: bool,
    tmp_path: pathlib.Path
):
    resdir = paths.get_resource_dir(
        loader_or_dumper, is_loader=is_loader, topdir=tmp_path
    )
    pss = [
        (resdir / "00" / "00_10.json",
         resdir / "00" / "e" / "00_10.json.py",
         resdir / "00" / "o" / "00_10.json.py"),
        (resdir / "10" / "10_10.json",
         resdir / "10" / "e" / "10_10.json.py",
         resdir / "10" / "o" / "10_10.json.py"),
    ]
    kwargs = {
        "topdir": tmp_path
    }

    res = TT.load_test_data(loader_or_dumper, is_loader=is_loader, **kwargs)
    assert res == [], res

    for ipath, epath in pss:
        if not epath.parent.is_dir():
            epath.parent.mkdir(parents=True)
        ipath.touch()
        epath.touch()

    (resdir / "00" / "e" / "00_10.json.py").write_text("{}")
    (resdir / "10" / "e" / "10_10.json.py").write_text("[1, 42]")

    exp = [
        (pss[0][0], {}),
        (pss[1][0], [1, 42]),
    ]

    assert TT.load_test_data(
        loader_or_dumper, is_loader=is_loader, **kwargs
    ) == exp
