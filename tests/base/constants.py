#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common utility functions.
"""
from __future__ import annotations

import pathlib
import typing


TESTS_DIR = pathlib.Path(__file__).parent.parent.resolve()
RES_DIR = TESTS_DIR / 'res'

NULL_CNTNR: dict[str, typing.Any] = dict()

DATA = '3.149265'  # for test_utils.py
