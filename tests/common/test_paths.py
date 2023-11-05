#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for tests.common.paths.
"""
import os.path
import pathlib

import pytest

from . import paths


def test_module_globals():
    assert str(paths.TESTDIR) == os.path.abspath(
        f"{os.path.dirname(__file__)}/.."
    )
    assert str(paths.RESOURCE_DIR) == os.path.abspath(
        f"{os.path.dirname(__file__)}/../res/{paths.TEST_DATA_MAJOR_VERSION!s}"
    )


@pytest.mark.parametrize(
    ("loader", "exp"),
    (("json.json", paths.TESTDIR / "res" / "1" / "loaders" / "json.json"),
     ("toml.tomllib",
      paths.TESTDIR / "res" / "1" / "loaders" / "toml.tomllib"),
     )
)
def test_loader(loader: str, exp: pathlib.Path):
    assert paths.loader_resdir(loader) == exp


@pytest.mark.parametrize(
    ("dumper", "exp"),
    (("json.json", paths.TESTDIR / "res" / "1" / "dumpers" / "json.json"),
     ("toml.tomllib",
      paths.TESTDIR / "res" / "1" / "dumpers" / "toml.tomllib"),
     )
)
def test_dumper(dumper: str, exp: pathlib.Path):
    assert paths.dumper_resdir(dumper) == exp


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
