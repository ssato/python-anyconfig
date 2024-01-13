#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for tests.common.paths.
"""
import json
import os.path
import pathlib
import typing

import pytest

from . import paths as TT


def test_module_globals():
    assert str(TT.TESTDIR) == os.path.abspath(
        f"{os.path.dirname(__file__)}/.."
    )


@pytest.mark.parametrize(
    ("loader_or_dumper", "is_loader", "topdir", "exp"),
    (("json.json", True, None, TT.RESOURCE_DIR / "loaders" / "json.json"),
     ("toml.tomllib", True, None,
      TT.RESOURCE_DIR / "loaders" / "toml.tomllib"),
     ("json.json", False, None, TT.RESOURCE_DIR / "dumpers" / "json.json"),
     ("toml.tomllib", False, None,
      TT.RESOURCE_DIR / "dumpers" / "toml.tomllib"),
     ("yaml.yaml", True, pathlib.Path("/tmp"),
      pathlib.Path("/tmp") / "loaders" / "yaml.yaml"),
     )
)
def test_get_resource_dir(
    loader_or_dumper: str, is_loader: bool,
    topdir: typing.Optional[pathlib.Path], exp: pathlib.Path
):
    assert TT.get_resource_dir(
        loader_or_dumper, is_loader=is_loader, topdir=topdir
    ) == exp


@pytest.mark.parametrize(
    ("ipath", "aux_paths"),
    (("no_aux_data.json", ()),
     ("an_aux_data.yml", ("e/an_aux_data.json", )),
     ("some_aux_data.yml",
      ("e/some_aux_data.json", "o/some_aux_data.yml")),
     )
)
def test_get_aux_data_paths(
    ipath: str, aux_paths: typing.Tuple[str, ...],
    tmp_path: pathlib.Path
):
    (tmp_path / ipath).touch()
    paths = [tmp_path / a for a in aux_paths]
    for apath in paths:
        adir = apath.parent

        if not adir.exists():
            adir.mkdir(parents=True)
            apath.touch()

            (adir / "file_to_be_ignored_012.json").touch()

    expected = {p.parent.name: p for p in paths}

    res = TT.get_aux_data_paths(tmp_path / ipath)
    assert res == expected


@pytest.mark.parametrize(
    ("ipaths", "aux_paths"),
    ((("no_aux_data.json", ), ()),
     (("10_no_aux_data.json", "20_no_aux_data.json"), ()),
     (("10/10_no_aux_data.json", "20/20_no_aux_data.json"), ()),
     (("an_aux_data.yml", ), ("e/an_aux_data.json", )),
     (("10_an_aux_data.yml", "50_an_aux_data.yml"),
      ("e/10_an_aux_data.json", "e/50_an_aux_data.json")),
     (("10_some_aux_data.yml", "99_some_aux_data.yml"),
      ("e/10_some_aux_data.json", "o/10_some_aux_data.yml",
       "e/99_some_aux_data.json", "o/99_some_aux_data.yml",)),
     (("10/10_some_aux_data.yml", "20/99_some_aux_data.yml"),
      ("10/e/10_some_aux_data.json", "10/o/10_some_aux_data.yml",
       "20/e/99_some_aux_data.json", "20/o/99_some_aux_data.yml",)),
     )
)
def test_get_data(
    ipaths: typing.Tuple[str], aux_paths: typing.Tuple[str, ...],
    tmp_path: pathlib.Path
):
    for ipath in ipaths:
        ifpath = tmp_path / ipath
        idir = ifpath.parent

        if not idir.exists():
            idir.mkdir(parents=True)

        ifpath.touch()

    paths = [tmp_path / a for a in aux_paths]
    for apath in paths:
        adir = apath.parent

        if not adir.exists():
            adir.mkdir(parents=True)
            apath.touch()

            (adir / "file_to_be_ignored_012.json").touch()

    expected = sorted(
        (tmp_path / ipath, TT.get_aux_data_paths(tmp_path / ipath))
        for ipath in ipaths
    )

    res = TT.get_data(tmp_path)
    assert res == expected


@pytest.mark.parametrize(
    ("ipaths", "aux_data"),
    ((("no_aux_data.json", ), ()),
     (("10_no_aux_data.json", "20_no_aux_data.json"), ()),
     (("an_aux_data.yml", ), (("e/an_aux_data.json", 1), )),
     (("10/an_aux_data.yml", ), (("10/e/an_aux_data.json", 1), )),
     (("10_an_aux_data.yml", "50_an_aux_data.yml"),
      (("e/10_an_aux_data.json", "aaa"), ("e/50_an_aux_data.json", [1, 2]))),
     (("10_some_aux_data.yml", "99_some_aux_data.yml"),
      (("e/10_some_aux_data.json", 1),
       ("o/10_some_aux_data.json", {"a": 2}),
       ("e/99_some_aux_data.json", [2, 3]),
       ("o/99_some_aux_data.json", {"a": "a"}))),
     (("10/10_an_aux_data.yml", "20/50_an_aux_data.yml"),
      (("10/e/10_an_aux_data.json", "aaa"),
       ("20/e/50_an_aux_data.json", [1, 2]))),
     )
)
def test_load_data(
    ipaths: typing.Tuple[str],
    aux_data: typing.Tuple[typing.Tuple[str, typing.Any], ...],
    tmp_path: pathlib.Path
):
    for ipath in ipaths:
        if not (tmp_path / ipath).parent.exists():
            (tmp_path / ipath).parent.mkdir(parents=True)

        (tmp_path / ipath).touch()

    for apath, adata in aux_data:
        apath = tmp_path / apath
        adir = apath.parent

        if not adir.exists():
            adir.mkdir(parents=True)
            json.dump(adata, apath.open(mode='w'))

            (adir / "file_to_be_ignored_012.json").touch()

    amap = {tmp_path / p: d for p, d in aux_data}
    expected = sorted(
        (
            tmp_path / ipath,
            {
                s: amap[p] for s, p
                in TT.get_aux_data_paths(tmp_path / ipath).items()
            }
        )
        for ipath in ipaths
    )

    res = TT.load_data(tmp_path)
    assert res
    assert res == expected
