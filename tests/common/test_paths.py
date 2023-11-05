#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for tests.common.paths.
"""
import pathlib

import pytest

from . import paths


@pytest.mark.parametrize(
    ("mver", "exp"),
    ((1, paths.TEST_TOPDIR / "res" / "1"),
     (200, paths.TEST_TOPDIR / "res" / "200"),
     )
)
def test_resdir(mver: int, exp: pathlib.Path):
    assert paths.resdir(mver) == exp


@pytest.mark.parametrize(
    ("loader", "mver", "exp"),
    (("json.json", 1, paths.TEST_TOPDIR / "res" / "1" / "loaders" / "json.json"),
     ("toml.tomllib", 20, paths.TEST_TOPDIR / "res" / "20" / "loaders" / "toml.tomllib"),
     )
)
def test_loader(loader: str, mver: int, exp: pathlib.Path):
    assert paths.loader_resdir(loader, mver) == exp


@pytest.mark.parametrize(
    ("dumper", "mver", "exp"),
    (("json.json", 1, paths.TEST_TOPDIR / "res" / "1" / "dumpers" / "json.json"),
     ("toml.tomllib", 20, paths.TEST_TOPDIR / "res" / "20" / "dumpers" / "toml.tomllib"),
     )
)
def test_dumper(dumper: str, mver: int, exp: pathlib.Path):
    assert paths.dumper_resdir(dumper, mver) == exp


@pytest.mark.parametrize(
    ("ipath", "exp"),
    (("/tmp/a/tests/res/1/loaders/toml.tomllib/10/100_null.toml",
      "/tmp/a/tests/res/1/loaders/toml.tomllib/10/e/100_null.toml.json"),
     )
)
def test_get_expected_data_path(ipath, exp):
    assert paths.get_expected_data_path(
        pathlib.Path(ipath)
    ) == pathlib.Path(exp)
