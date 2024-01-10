#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Loader test cases.
"""
import pathlib
import typing
import warnings

import anyconfig.ioinfo


class TestCase:
    """Base class for loader test cases.
    """
    psr_cls = None

    def _get_all(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any]
    ):
        if self.psr_cls is None:
            warnings.warn(f"Failed to ini test target: {__file__}")
            psr = None
        else:
            psr = self.psr_cls()  # pylint: disable=not-callable

        ioi = anyconfig.ioinfo.make(ipath)

        return (
            aux["e"],  # It should NOT fail.
            aux.get("o", {}),
            psr,
            ioi
        )

    def _assert_loads(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any]
    ):
        (exp, opts, psr, _ioi) = self._get_all(ipath, aux)
        if 'b' in psr._open_read_mode:  # pylint: disable=protected-access
            res = psr.loads(ipath.read_bytes(), **opts)
        else:
            res = psr.loads(ipath.read_text(), **opts)

        assert res == exp, f"'{res!r}' vs. '{exp!r}'"

    def _assert_load(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any]
    ):
        (exp, opts, psr, ioi) = self._get_all(ipath, aux)
        res = psr.load(ioi, **opts)
        assert res == exp, f"'{res!r}' vs. '{exp!r}'"
