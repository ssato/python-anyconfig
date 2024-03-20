#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
import pytest

import anyconfig.backend.base.loaders as TT


@pytest.mark.parametrize(
    ("cls", "mode"),
    (
     (TT.LoaderMixin, "r"),
     (TT.BinaryLoaderMixin, "rb"),
     ),
)
def test_loader_mixin_ropen(cls, mode):
    with cls().ropen(__file__) as fio:
        assert fio.mode == mode
