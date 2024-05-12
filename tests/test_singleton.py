#
# Copyright (C) 2018 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name, too-few-public-methods
from __future__ import annotations

import anyconfig.singleton as TT


def test_basic_singletons() -> None:
    class A(TT.Singleton):
        pass

    class B(TT.Singleton):
        pass

    (a1, a2) = (A(), A())
    (b1, b2) = (B(), B())
    assert a1 is a2
    assert b1 is b2
    assert a1 is not b1


def test_descendants() -> None:
    class A(TT.Singleton):
        pass

    class A2(A):
        pass

    (a1, a2) = (A(), A2())
    assert a1 is a2


def test_mixins() -> None:
    class Base:
        pass

    class A(Base, TT.Singleton):
        pass

    (a1, a2) = (A(), A())
    assert a1 is a2
