#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common datasets.
"""
import pathlib
import typing

from .common import TESTS_DIR


DATA_00: typing.Dict[pathlib.Path, typing.Dict[str, typing.Any]] = {
    str(TESTS_DIR / 'res/json/basic/00.json'): dict(a=1),
    str(TESTS_DIR / 'res/json/basic/10.json'): dict(
        a=1, b=dict(b=[1, 2], c='C'), name='aaa'
    ),
    str(TESTS_DIR / 'res/json/basic/20.json'): dict(
        a=1, b=dict(b=[1, 2], c='C', d=True), e=None, name='aaa'
    ),
}

# vim:sw=4:ts=4:et:
