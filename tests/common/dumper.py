#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Dumper test cases.
"""
import pathlib
import typing
import warnings

import tests.common.load
import anyconfig.ioinfo


class TestCase:
    """Base class for dumper test cases."""
    psr_cls = None

    def _get_all(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
    ):
        if self.psr_cls is None:
            warnings.warn(f"Failed to ini test target: {__file__}")
            psr = None
        else:
            psr = self.psr_cls()  # pylint: disable=not-callable

        idata = tests.common.load.load_data(ipath)

        return (
            aux["e"],  # It should NOT fail.
            aux.get("o", {}),
            psr,
            idata
        )

    def _assert_dumps(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
    ):
        (exp, opts, psr, idata) = self._get_all(ipath, aux)
        assert psr.loads(psr.dumps(idata, **opts), **opts) == exp

    def _assert_dump(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
        tmp_path: pathlib.Path
    ):
        (exp, opts, psr, idata) = self._get_all(ipath, aux)

        opath = tmp_path / f"{ipath.name}.{psr.extensions()[0]}"
        ioi = anyconfig.ioinfo.make(opath)
        psr.dump(idata, ioi)

        assert psr.load(ioi, **opts) == exp
