#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for tests.common.paths.
"""
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
     (("an_aux_data.yml", ), ("e/an_aux_data.json", )),
     (("10_an_aux_data.yml", "50_an_aux_data.yml"),
      ("e/10_an_aux_data.json", "e/50_an_aux_data.json")),
     (("10_some_aux_data.yml", "99_some_aux_data.yml"),
      ("e/10_some_aux_data.json", "o/10_some_aux_data.yml",
       "e/99_some_aux_data.json", "o/99_some_aux_data.yml",)),
     )
)
def test_get_data(
    ipaths: typing.Tuple[str], aux_paths: typing.Tuple[str, ...],
    tmp_path: pathlib.Path
):
    for ipath in ipaths:
        (tmp_path / ipath).touch()

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
