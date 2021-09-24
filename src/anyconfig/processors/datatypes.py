#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common functions and variables."""
import typing

from ..models import processor


ProcT = typing.TypeVar('ProcT', bound=processor.Processor)
ProcsT = typing.List[ProcT]
ProcClsT = typing.Type[ProcT]
ProcClssT = typing.List[ProcClsT]

MaybeProcT = typing.Optional[typing.Union[str, ProcT, ProcClsT]]

# vim:sw=4:ts=4:et:
