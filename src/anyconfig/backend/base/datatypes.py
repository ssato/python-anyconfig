#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utility functions in anyconfig.backend.base."""
import pathlib
import typing

from ...common import (
    InDataT, InDataExT
)
from ...ioinfo import (
    IOInfo, PathOrIOInfoT
)


OutDataExT = InDataExT

IoiT = IOInfo
MaybeFilePathT = typing.Optional[PathOrIOInfoT]

GenContainerT = typing.Callable[..., InDataT]
OptionsT = typing.Dict[str, typing.Any]

PathOrStrT = typing.Union[str, pathlib.Path]
