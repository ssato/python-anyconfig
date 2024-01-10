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

    exact_match: bool = True

    def _get_all(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
    ):
        if self.psr_cls is None:
            warnings.warn(  # noqa
                f"Failed to initialize test target: {__file__}",
            )
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
        out_s: str = psr.dumps(idata, **opts)

        assert psr.loads(out_s, **opts) == idata
        if self.exact_match:
            assert out_s == exp, f"'{out_s}' vs. '{exp}'"

    def _assert_dump(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
        tmp_path: pathlib.Path
    ):
        (exp, opts, psr, idata) = self._get_all(ipath, aux)

        opath = tmp_path / f"{ipath.name}.{psr.extensions()[0]}"
        ioi = anyconfig.ioinfo.make(opath)
        psr.dump(idata, ioi, **opts)

        out_s: str = psr.ropen(str(opath)).read()

        assert psr.load(ioi, **opts) == idata
        if self.exact_match:
            assert out_s == exp, f"'{out_s}' vs. '{exp}'"
