#
# Copyright (C) 2013 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Common constants and functions for test cases of anyconfig.cli."""
from __future__ import annotations

import contextlib
import io
import pathlib
import sys
import typing

import pytest

import anyconfig.api
import anyconfig.cli as TT

from . import datatypes


NAMES: list[str] = ("ipath", "opts", "exp")
NAMES_WITH_REF: list[str] = (*NAMES, "oname", "ref")


def _run_main(
    tdata: datatypes.TData, tmp_path: pathlib.Path
) -> None:
    args = ["anyconfig_cli", *tdata.opts, *tdata.ipaths]

    if tdata.outname:  # Running cli.main will output files.
        assert tdata.ref is not None
        opath = tmp_path / tdata.outname

        # Run anyconfig.cli.main with arguments.
        TT.main([*args, "-o", str(opath)])

        if tdata.exp.exit_code_matches and tdata.exp.exit_code == 0:
            assert opath.exists()

            try:
                odata = anyconfig.api.load(opath, **tdata.oo_opts)
            except anyconfig.api.UnknownFileTypeError:
                odata = anyconfig.api.load(opath, ac_parser='json')

            assert odata == tdata.ref, f"{odata} vs. {tdata.ref!r}"
    else:
        # Likewise but without -o <output_path> option.
        TT.main(args)

    sys.exit(0)


def run_main(
    tdata: datatypes.TData, tmp_path: pathlib.Path,
    post_checks: typing.Optional[typing.Callable] = None
) -> None:
    """Run anyconfig.cli.main and check if the exit code was expected one.
    """
    expected: datatypes.Expected = tdata.exp

    with pytest.raises(expected.exception) as exci:
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                _run_main(tdata, tmp_path)

    assert isinstance(exci.value, expected.exception)
    ecode = getattr(
        exci.value, "error_code", getattr(exci.value, "code", 1)
    )

    if post_checks is not None:
        post_checks(tdata, stdout, stderr)

    log = f"ecode: {ecode!r},  expected: {expected!r}, opts: {tdata.opts}"
    if expected.exit_code_matches:
        assert ecode == expected.exit_code, log
    else:
        assert ecode != expected.exit_code, log

    if expected.words_in_stdout:
        assert expected.words_in_stdout in stdout.getvalue()

    if expected.words_in_stderr:
        assert expected.words_in_stderr in stderr.getvalue()
