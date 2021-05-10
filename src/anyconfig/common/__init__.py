#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""misc global constants, variables, classes and so on.
"""
from .datatypes import (
    IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
    IOI_TYPES, IOInfo, IOI_KEYS,
    PathT, PathOrIOT, PathOrIOInfoT,
    InDataT, InDataExT, PrimitiveT
)
from .errors import (
    UnknownParserTypeError, UnknownProcessorTypeError, UnknownFileTypeError,
    ValidationError
)


__all__ = [
    'IOI_PATH_STR', 'IOI_PATH_OBJ', 'IOI_STREAM', 'IOI_TYPES',
    'IOInfo', 'IOI_KEYS',
    'PathT', 'PathOrIOT', 'PathOrIOInfoT',
    'InDataT', 'InDataExT', 'PrimitiveT',
    'UnknownParserTypeError', 'UnknownProcessorTypeError',
    'UnknownFileTypeError', 'ValidationError',
]

# vim:sw=4:ts=4:et:
