#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=inherit-non-class,too-few-public-methods
"""anyconfig basic data types."""
import typing


InDataT = typing.Mapping[str, typing.Any]

PrimitiveT = typing.Union[None, int, float, bool, str, InDataT]
InDataExT = typing.Union[PrimitiveT, InDataT]

# vim:sw=4:ts=4:et:
