#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Backend basic classes, functions and constants.
"""
import typing

from .dumpers import (
    ToStringDumperMixin, ToStreamDumperMixin,
)
from .loaders import (
    FromStringLoaderMixin, FromStreamLoaderMixin
)
from .mixins import (
    TextFilesMixin, BinaryFilesMixin
)
from .utils import (
    ensure_outdir_exists, to_method
)
from .parsers import (
    Parser,
    StringParser, StreamParser, StringStreamFnParser,
)


ParserT = typing.TypeVar('ParserT', bound=Parser)
ParsersT = typing.List[ParserT]

__all__ = [
    'ToStringDumperMixin', 'ToStreamDumperMixin',
    'FromStringLoaderMixin', 'FromStreamLoaderMixin',
    'TextFilesMixin', 'BinaryFilesMixin',
    'ensure_outdir_exists', 'to_method',
    'Parser',
    'StringParser', 'StreamParser', 'StringStreamFnParser',
    'ParserT', 'ParsersT',
]

# vim:sw=4:ts=4:et:
