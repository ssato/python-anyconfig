#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Test cases for Test Data Collecor."""
from __future__ import annotations

import json
import pathlib

import pytest

from . import tdc as TT, globals_ as G


SELF = pathlib.Path(__file__)
CUDIR = SELF.parent


@pytest.mark.parametrize(
    ("path", "level", "exp"),
    (("a/b/c/d/e.py", TT.LVL_DEFAULT, "c/d/e.py"),
     ("/a/b/c/d/e.py", TT.LVL_DEFAULT, "c/d/e.py"),
     ("/a/b/c/d/e.py", 4, "b/c/d/e.py"),
     ),
)
def test_get_test_id(path, level, exp) -> None:
    exp = str(pathlib.Path(exp))
    assert TT.get_test_id(pathlib.Path(path), level=level) == exp


@pytest.mark.parametrize(
    ("data", "level", "exp"),
    (([], 1, []),
     ([(pathlib.Path("a/b/c/d/e.py"), {}, None)],
      TT.LVL_DEFAULT, ["c/d/e.py"]),
     ),
)
def test_get_test_ids(data, level, exp) -> None:
    exp = [str(pathlib.Path(e)) for e in exp]
    assert TT.get_test_ids(data, level=level) == exp


TEST_FILE_10 = "foobar/baz/test_xyz.py"
TEST_TOP_DIR_10 = pathlib.Path("/home/foo/projects/bar/tests")
TEST_RES_DIR_10 = TEST_TOP_DIR_10 / "resources"
TEST_DATA_PATH_10 = TEST_RES_DIR_10 / "foobar" / "baz" / "xyz"


@pytest.mark.parametrize(
    ("path", "opts", "exp"),
    ((str(SELF), {}, G.RESOURCE_DIR / "common" / "tdc"),
     (str(CUDIR / "test_paths.py"), {}, G.RESOURCE_DIR / "common" / "paths"),
     (str(TEST_TOP_DIR_10 / TEST_FILE_10),
      {"topdir": TEST_TOP_DIR_10, "resdir": TEST_RES_DIR_10},
      TEST_DATA_PATH_10),
     ),
    ids=(SELF.name, "test_paths.py", TEST_FILE_10),
)
def test_get_test_resdir(path, opts, exp):
    assert TT.get_test_resdir(path, **opts) == exp


# .. note:: See files under tests/res/1/common/tdc/.
TEST_DATA_10 = [
    ("10/00.json", {}, {}),
    ("20/10.json", [1, 2], {"a": "aaa"}),
    ("30/20.json", {"a": "A"}, {"b": [1, 2], "c": {"baz": "fbz"}}),
]
TEST_DATA_20 = [
    (
        G.RESOURCE_DIR / "common" / "tdc" / "10" / "100_null.json",
        None,
        {"e": None}
    ),
    (
        G.RESOURCE_DIR / "common" / "tdc" / "20" / "220_a_list.json",
        [1, 2],
        {"e": [1, 2], "o": {"ac_ordered": True}}
    ),
]


@pytest.mark.parametrize(
    ("testfile", "kwargs", "exp"),
    (pytest.param(
        __file__, {},
        [(i, *[a.get(k, v) for k, v in TT.VALUES])
         for i, _, a in TEST_DATA_20],
        id=f"{CUDIR.name}/{SELF.name} without loading data from ipath"),
     pytest.param(
        __file__, {"load_idata": True},
        [(i, d, *[a.get(k, v) for k, v in TT.VALUES])
         for i, d, a in TEST_DATA_20],
        id=f"{CUDIR.name}/{SELF.name} with loading data from ipath"),
     # ("foo/bar/test_baz.py", {"values": (("b", []), ("c", {}))},
     #  TEST_DATA_10),
     ),
)
def test_load_data_for_testfile(
    testfile, kwargs, exp, tmp_path
):
    if pathlib.Path(testfile).exists():
        assert TT.load_data_for_testfile(testfile, **kwargs) == exp
    else:
        testfile = tmp_path / testfile
        testfile.parent.mkdir(parents=True, exist_ok=True)
        testfile.touch()

        # kwargs for TT.get_test_resdir
        kwargs.update(topdir=tmp_path, resdir=tmp_path)
        resdir = tmp_path / TT.get_test_resdir(testfile, tmp_path, tmp_path)

        exp_new = []

        for ipath, data, opts in exp:
            path = resdir / ipath
            path.parent.mkdir(parents=True, exist_ok=True)
            json.dump(data, path.open("w"))

            opts_new = []
            for subdir, val in opts.items():
                if subdir not in kwargs.get("values", TT.VALUES):
                    continue

                (path.parent / subdir).mkdir(exist_ok=True)

                aname = path.name.replace(path.suffix, ".py")
                (path.parent / subdir / aname).write_text(repr(val))
                opts_new.append({subdir: val})

            if kwargs.get("load_idata", False):
                exp_new.append((path, data, *opts_new))
            else:
                exp_new.append((path, *opts_new))

        assert TT.load_data_for_testfile(str(testfile), **kwargs) == exp_new
