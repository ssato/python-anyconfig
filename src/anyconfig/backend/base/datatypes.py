#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Utility functions in anyconfig.backend.base.
"""
import typing

from ...common import (
    InDataT, IOInfo, PathOrIOInfoT
)


PrimitiveT = typing.Union[str, int, None, float, bool, InDataT]

InDataExT = typing.Union[PrimitiveT, InDataT]
OutDataExT = InDataExT

IoiT = IOInfo
MaybeFilePathT = typing.Optional[PathOrIOInfoT]

GenContainerT = typing.Callable[..., InDataT]
OptionsT = typing.Dict[str, typing.Any]

# vim:sw=4:ts=4:et:
