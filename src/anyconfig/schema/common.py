#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Some common constants, utility functions and so on.
"""
import typing


DataT = typing.Dict[str, typing.Any]
ResultT = typing.Tuple[bool, typing.Union[str, typing.List[str]]]

MaybeDataT = typing.Union[DataT, bool, int, float, str, None]

# vim:sw=4:ts=4:et:
