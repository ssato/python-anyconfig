#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for tests.common.paths.
"""
import os.path

from . import globals_ as TT


def test_module_globals():
    assert str(TT.TESTDIR) == os.path.abspath(
        f"{os.path.dirname(__file__)}/.."
    )
