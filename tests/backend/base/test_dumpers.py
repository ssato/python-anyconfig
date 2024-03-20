#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
import pytest

import anyconfig.backend.base.dumpers as TT


@pytest.mark.parametrize(
    ("cls", "mode"),
    ((TT.DumperMixin, "w"),
     (TT.BinaryDumperMixin, "wb"),
     ),
)
def test_dumper_mixin_wopen(cls, mode, tmp_path):
    with cls().wopen(tmp_path / "test.txt") as fio:
        assert fio.mode == mode
