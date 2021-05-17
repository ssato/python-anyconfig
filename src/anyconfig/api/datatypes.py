#
# Copyright (C) 2012 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unused-import,import-error,invalid-name
r"""Public APIs to dump configurations data.
"""
import typing

from ..backend import base
from ..common import InDataT


MaybeDataT = typing.Optional[InDataT]
ParserT = base.Parser

# vim:sw=4:ts=4:et:
