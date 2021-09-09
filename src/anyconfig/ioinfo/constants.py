#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh @ gmmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""ioinfo.constants to provide global constant variables.
"""
import os.path
import re
import typing


GLOB_MARKER: str = '*'
PATH_SEP: str = os.path.sep

SPLIT_PATH_RE: typing.Pattern = re.compile(
    fr'([^{GLOB_MARKER}]+)'
    fr'{PATH_SEP}'
    fr'(.*{GLOB_MARKER}.*)'
)

# vim:sw=4:ts=4:et:
