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
    ("ipath", "subdir", "file_ext", "exts_to_try", "exp"),
    ((TT.RESOURCE_DIR / "loaders/json.json/10/100_null.json",
      "e", False, TT.EXTS_TO_TRY,
      TT.RESOURCE_DIR / "loaders/json.json/10/e/100_null.json.py"),
     (TT.RESOURCE_DIR / "loaders/json.json/10/100_null.json",
      "e", "ext_not_exists", TT.EXTS_TO_TRY,
      TT.RESOURCE_DIR / "loaders/json.json/10/e/100_null.json.py"),
     (pathlib.Path("not/exist/dir/data.json"),
      "e", False, TT.EXTS_TO_TRY, None),
     (TT.RESOURCE_DIR / "loaders/json.json/10/100_null.json",
      "e", False, (), None),
     (TT.RESOURCE_DIR / "999_file_does_not_exist.json",
      "e", False, (), None),
     )
)
def test_get_aux_data_path(
    ipath: pathlib.Path,
    subdir: str,
    file_ext: typing.Union[str, bool],
    exts_to_try: typing.Tuple[str, ...],
    exp: typing.Optional[pathlib.Path]
):
    assert TT.get_aux_data_path(
        ipath, subdir=subdir, file_ext=file_ext, exts_to_try=exts_to_try
    ) == exp


@pytest.mark.parametrize(
    ("loader_or_dumper", "is_loader", "rel_epaths"),
    (
        ("json.json", True, [("00/00_10.json", {})]),
        ("json.json", True, [("00/00_10.json", {}), ("00/00_20.json", {})]),
        ("json.json", True, [("00/00_10.json", {"e": "00/e/00_10.json.py"})]),
        ("json.json", True,
         [("00/00_10.json", {"e": "00/e/00_10.json.py"}),
          ("00/00_20.json", {"e": "00/e/00_20.json.py"})]),
    ),
)
def test_get_data_paths(
    loader_or_dumper: str, is_loader: bool,
    rel_epaths: typing.List[
        typing.Tuple[str, typing.Dict[str, pathlib.Path]]
    ],
    tmp_path: pathlib.Path
):
    resdir = TT.get_resource_dir(
        loader_or_dumper, is_loader=is_loader, topdir=tmp_path
    )
    exp = [
        (resdir / ipath, {d: resdir / a for d, a in d_apaths.items()})
        for ipath, d_apaths in rel_epaths
    ]

    assert TT.get_data_paths(
        loader_or_dumper, is_loader=is_loader, topdir=tmp_path
    ) == []

    for ipath, apaths in exp:
        ipath.parent.mkdir(parents=True, exist_ok=True)
        ipath.touch()

        for apath in apaths.values():
            adir = apath.parent
            if not adir.exists():
                adir.mkdir()
            apath.touch()

    assert TT.get_data_paths(
        loader_or_dumper, is_loader=is_loader, topdir=tmp_path
    ) == exp
