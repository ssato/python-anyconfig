#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common utility functions.
"""
import pathlib

import anyconfig.dicts


RES_DIR = pathlib.Path(__file__).parent / '../../../' / 'res'
DIC_0 = anyconfig.dicts.convert_to(dict())

# vim:sw=4:ts=4:et:
