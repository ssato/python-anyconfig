#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Loader test cases.
"""
import pathlib
import typing

import anyconfig.ioinfo


class TestCase:
    """Base class for loader test cases.
    """
    psr_cls = None

    def assert_loads_and_load_impl(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
        debug: bool = False,
    ):
        exp = aux["e"]  # It should NOT fail.
        opts = aux.get("o", {})
        ioi = anyconfig.ioinfo.make(ipath)

        if self.psr_cls is None:
            return

        psr = self.psr_cls()  # pylint: disable=not-callable

        if debug:
            assert not exp, exp
            assert not opts, opts

        assert psr.loads(ipath.read_text(), **opts) == exp
        assert psr.load(ioi, **opts) == exp
