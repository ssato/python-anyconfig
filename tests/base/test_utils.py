#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for tests.base.utils."""
from __future__ import annotations

import pathlib
import typing

import pytest

from . import constants, utils as TT


RES_DIR = constants.RES_DIR / "base"
SELF = pathlib.Path(__file__)


@pytest.mark.parametrize(
    ("path", "exp"),
    ((None, "base"),
     (__file__, "base"),
     ),
)
def test_target_by_parent(path: typing.Optional[str], exp: str):
    if path is None:
        assert TT.target_by_parent() == exp
    else:
        assert TT.target_by_parent(path) == exp


CONSTANTS_PY: pathlib.Path = SELF.parent / "constants.py"


@pytest.mark.parametrize(
    ("args", "exp"),
    (((CONSTANTS_PY, ), constants.DATA),
     ((str(CONSTANTS_PY), ), constants.DATA),
     ((CONSTANTS_PY, 'RES_DIR'), constants.RES_DIR),
     ),
)
def test_load_from_py(args, exp):
    assert TT.load_from_py(*args) == exp


def test_load_literal_data_from_py():
    py_path: pathlib.Path = RES_DIR / "basics" / "20" / "00.py"
    exp = TT.json.load((RES_DIR / "basics" / "10" / "00.json").open())

    assert TT.load_literal_data_from_py(py_path) == exp
    assert TT.load_literal_data_from_py(str(py_path)) == exp


@pytest.mark.parametrize(
    ("datadir", "name", "exp"),
    ((SELF.parent, SELF.stem, SELF),
     (pathlib.Path("/not/exist/dir"), "foo", None),
     ),
)
def test_maybe_data_path(datadir, name, exp):
    assert TT.maybe_data_path(datadir, name) == exp


@pytest.mark.parametrize(
    ("args", ),
    (((SELF.parent, SELF.stem, (SELF.parent.name, ), ".xyz"), ),
     ),
)
def test_maybe_data_path_failures(args):
    with pytest.raises(OSError):
        TT.maybe_data_path(*args)


@pytest.mark.parametrize(
    ("args", "exp"),
    (((None, ), {}),
     ((None, 1), 1),
     ((RES_DIR / "basics" / "10" / "00.json", ),
      TT.json.load((RES_DIR / "basics" / "10" / "00.json").open())
      ),
     ((RES_DIR / "basics" / "20" / "00.py", ),
      TT.json.load((RES_DIR / "basics" / "10" / "00.json").open())
      ),
     ((RES_DIR / "basics" / "30" / "20.txt", ),
      (RES_DIR / "basics" / "10" / "20.json").read_text()
      ),
     ),
)
def test_load_data(args, exp):
    assert TT.load_data(*args) == exp


@pytest.mark.parametrize(
    ("args", ),
    (((pathlib.Path("not_exist.xyz"), ), ),
     ),
)
def test_load_data_failures(args):
    with pytest.raises(ValueError):
        TT.load_data(*args)


@pytest.mark.parametrize(
    ("args", "exp"),
    (((RES_DIR / "basics" / "10", "*.json"), 3),
     ((RES_DIR / "basics" / "20", "*.py"), 1),
     ((RES_DIR / "basics" / "30", "*.txt"), 3),
     ),
)
def test_load_datasets_from_dir(args, exp):
    res = TT.load_datasets_from_dir(
        args[0], lambda *xs: xs[1], pattern=args[1]
    )
    assert bool(res)
    assert len(res) == exp


def test_load_datasets_from_dir_failures():
    with pytest.raises(ValueError):
        _ = TT.load_datasets_from_dir(SELF, list)
