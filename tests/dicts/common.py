#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import pathlib

from ..common import tdc


MOD: str = pathlib.Path(__file__).parent.name


def collect_data(target: str, mod: str = MOD):
    return tdc.collect_for(mod, target)
