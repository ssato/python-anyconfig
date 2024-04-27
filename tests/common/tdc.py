#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test Data Collecor."""
import pathlib
import re
import typing

from . import paths, globals_


NAME_FROM_TEST_FILENAME_RE: re.Pattern = re.compile(r"test_(.+).py")


def get_mod_target_pair_from_path(path: str):
    """Get (mod, target) from given file path."""
    fpath = pathlib.Path(path).resolve()
    return (
        fpath.parent.name,
        NAME_FROM_TEST_FILENAME_RE.match(fpath.name).groups()[0]
    )


def collect_for(
    mod: str, target: str, topdir: pathlib.Path = globals_.RESOURCE_DIR
) -> list[tuple[pathlib.Path, dict[str, typing.Any]]]:
    """Collct test data for mod.target."""
    datadir = topdir / mod / target  # e.g. tests/res/1/template/jinja2
    return paths.load_data_2(datadir)
