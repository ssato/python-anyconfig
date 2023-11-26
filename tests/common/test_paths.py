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

from . import paths


def test_module_globals():
    assert str(paths.TESTDIR) == os.path.abspath(
        f"{os.path.dirname(__file__)}/.."
    )


@pytest.mark.parametrize(
    ("loader_or_dumper", "is_loader", "topdir", "exp"),
    (("json.json", True, None, paths.RESOURCE_DIR / "loaders" / "json.json"),
     ("toml.tomllib", True, None,
      paths.RESOURCE_DIR / "loaders" / "toml.tomllib"),
     ("json.json", False, None, paths.RESOURCE_DIR / "dumpers" / "json.json"),
     ("toml.tomllib", False, None,
      paths.RESOURCE_DIR / "dumpers" / "toml.tomllib"),
     ("yaml.yaml", True, pathlib.Path("/tmp"),
      pathlib.Path("/tmp") / "loaders" / "yaml.yaml"),
     )
)
def test_get_resource_dir(
    loader_or_dumper: str, is_loader: bool,
    topdir: typing.Optional[pathlib.Path], exp: pathlib.Path
):
    assert paths.get_resource_dir(
        loader_or_dumper, is_loader=is_loader, topdir=topdir
    ) == exp


@pytest.mark.parametrize(
    ("ipath", "file_ext", "exts_to_try", "exp"),
    ((paths.RESOURCE_DIR / "loaders/json.json/10/100_null.json",
      False, paths.EXTS_TO_TRY,
      paths.RESOURCE_DIR / "loaders/json.json/10/e/100_null.json.py"),
     (paths.RESOURCE_DIR / "loaders/json.json/10/100_null.json",
      "ext_not_exists", paths.EXTS_TO_TRY,
      paths.RESOURCE_DIR / "loaders/json.json/10/e/100_null.json.py"),
     (pathlib.Path("not/exist/dir/data.json"),
      False, paths.EXTS_TO_TRY, None),
     (paths.RESOURCE_DIR / "loaders/json.json/10/100_null.json",
      False, (), None),
     (paths.RESOURCE_DIR / "999_file_does_not_exist.json",
      False, (), None),
     )
)
def test_get_expected_data_path(
    ipath: pathlib.Path, file_ext: typing.Union[str, bool],
    exts_to_try: typing.Tuple[str, ...],
    exp: typing.Optional[pathlib.Path]
):
    assert paths.get_expected_data_path(
        ipath, file_ext=file_ext, exts_to_try=exts_to_try
    ) == exp


@pytest.mark.parametrize(
    ("loader_or_dumper", "is_loader"),
    (
        ("json.json", True),
    ),
)
def test_get_data_path_pairs(
    loader_or_dumper: str, is_loader: bool,
    tmp_path: pathlib.Path
):
    resdir = paths.get_resource_dir(
        loader_or_dumper, is_loader=is_loader, topdir=tmp_path
    )
    exp = [
        (resdir / "00" / "00_10.json",
         resdir / "00" / "e" / "00_10.json.py"),
        (resdir / "10" / "10_10.xyz",
         resdir / "10" / "e" / "10_10.xyz.json"),
    ]
    assert paths.get_data_path_pairs(
        loader_or_dumper, is_loader=is_loader, topdir=tmp_path
    ) == []

    for ipath, epath in exp:
        if not epath.parent.is_dir():
            epath.parent.mkdir(parents=True)

        ipath.touch()
        epath.touch()

    assert paths.get_data_path_pairs(
        loader_or_dumper, is_loader=is_loader, topdir=tmp_path
    ) == exp
