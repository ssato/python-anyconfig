#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
""""Common functions of test cases for anyconfig.api.single_load."""
from __future__ import annotations

import pathlib
import typing

from ...common import tdc


MOD: str = pathlib.Path(__file__).parent.name

VALUES: tuple[tuple[str, typing.Optional[dict], ...], ...] = (
    ("c", {}), ("e", None), ("o", {})
)


def load_datasets(
    target: str, mod: str = MOD, values = VALUES,
) -> list[tuple[pathlib.Path, dict, typing.Optional[dict], dict]]:
    return [
        (ipath, *[data.get(k, v) for k, v in values])
        for ipath, data
        in tdc.collect_for(mod, target, subdir="api", load=False)
    ]
