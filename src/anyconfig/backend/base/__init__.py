#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Backend basic classes, functions and constants.
"""
import typing

from .compat import BinaryFilesMixin
from .dumpers import (
    ToStringDumperMixin, ToStreamDumperMixin, BinaryDumperMixin
)
from .loaders import (
    FromStringLoaderMixin, FromStreamLoaderMixin, BinaryLoaderMixin
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
ParserClssT = typing.List[typing.Type[ParserT]]


__all__ = [
    'BinaryFilesMixin',
    'ToStringDumperMixin', 'ToStreamDumperMixin', 'BinaryDumperMixin',
    'FromStringLoaderMixin', 'FromStreamLoaderMixin', 'BinaryLoaderMixin',
    'ensure_outdir_exists', 'to_method',
    'Parser',
    'StringParser', 'StreamParser', 'StringStreamFnParser',
    'ParserT', 'ParsersT', 'ParserClssT',
]

# vim:sw=4:ts=4:et:
