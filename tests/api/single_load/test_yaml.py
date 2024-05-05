#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.load with input of other file types."""
from __future__ import annotations

import pytest

import anyconfig.api._load as TT

from . import common


NAMES: tuple[str, ...] = ("ipath", "exp")
DATA: list = common.load_datasets_by_test_filepath(__file__, (("e", None), ))
DATA_IDS: list[str] = common.get_test_ids(DATA)


@pytest.mark.skipif(
    "yaml" not in common.LOADER_TYPES,
    reason="yaml loader is not availabla."
)
@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_single_load_for_yaml_files(ipath, exp):
    assert TT.single_load(ipath) == exp
