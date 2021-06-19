#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common utility functions.
"""
import pathlib


TESTS_DIR = pathlib.Path(__file__).parent.parent.resolve()
RES_DIR = TESTS_DIR / 'res'

NULL_CNTNR = dict()

DATA = '3.149265'  # for test_utils.py

# vim:sw=4:ts=4:et:
