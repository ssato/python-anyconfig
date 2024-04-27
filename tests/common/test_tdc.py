#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Test cases for Test Data Collecor."""
from __future__ import annotations

import json
import typing

import pytest

from . import tdc as TT, globals_ as G

if typing.TYPE_CHECKING:
    import pathlib


def test_get_mod_target_pair_from_path() -> None:
    assert TT.get_mod_target_pair_from_path(__file__) == (
        "common", "tdc"
    )


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
    ("mod", "target", "topdir", "exp"),
    (("foo", "bar", None, TEST_DATA_10),
     (*TT.get_mod_target_pair_from_path(__file__),
      G.RESOURCE_DIR, TEST_DATA_20),
     ),
)
def test_collect_for(
    mod: str, target: str, topdir: pathlib.Path,
    exp: list[tuple[pathlib.Path, dict[str, typing.Any]]],
    tmp_path: pathlib.Path
) -> None:
    if topdir is None:
        exp_new = []

        for rpath, data, opts in exp:
            path = tmp_path / mod / target / rpath
            path.parent.mkdir(parents=True, exist_ok=True)
            json.dump(data, path.open("w"))

            for subdir, val in opts.items():
                (path.parent / subdir).mkdir(exist_ok=True)

                aname = path.name.replace(path.suffix, ".py")
                (path.parent / subdir / aname).write_text(repr(val))

            exp_new.append((path, data, opts))

        assert TT.collect_for(mod, target, tmp_path) == exp_new

    else:
        assert TT.collect_for(mod, target, topdir) == exp
