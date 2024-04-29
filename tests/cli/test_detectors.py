#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.detectors."""
from __future__ import annotations

import contextlib
import io
import warnings
import typing

import pytest

import anyconfig.cli.detectors as TT
import anyconfig.cli.parse_args


@pytest.mark.parametrize(
    ("paths", "exp"),
    (([], False),
     (['/tmp/a/b/c.conf'], True),
     (['/tmp/a/b/c.yml', '/tmp/a/b/d.yml'], True),
     )
)
def test_are_same_file_types(paths: list[str], exp: bool) -> None:
    assert TT.are_same_file_types(paths) == exp


@pytest.mark.parametrize(
    ("typ", "exp"),
    (('', None),
     (None, None),
     ('json', 'json'),
     ('type_not_exit', None),
     )
)
def test_find_by_the_type(typ: str, exp: typing.Optional[str]):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        assert TT.find_by_the_type(typ) == exp


@pytest.mark.parametrize(
    ("paths", "exp"),
    (([], None),
     (['/tmp/a/b/c.yml', '/tmp/a/b/d.json'], None),
     (['-'], None),
     (['-', '/tmp/a/b/d.json'], None),
     (['/tmp/a/b/c.json', '/tmp/a/b/d.json'], 'json'),
     )
)
def test_find_by_the_paths(
    paths: list[str], exp: typing.Optional[str]
) -> None:
    assert TT.find_by_the_paths(paths) == exp


@pytest.mark.parametrize(
    ("argv", "exp"),
    (([], None),
     (['-'], None),
     (['a.conf'], None),
     (['-I', 'json', 'a.conf'], 'json'),
     (['a.json'], 'json'),
     )
)
def test_try_detecting_input_type(
    argv: list[str], exp: typing.Optional[str]
) -> None:
    (_psr, args) = anyconfig.cli.parse_args.parse(
        argv, prog='anyconfig_cli'
    )
    assert TT.try_detecting_input_type(args) == exp


@pytest.mark.parametrize(
    ("argv", "exp"),
    ((['-I', 'json', 'a.conf'], 'json'),
     (['a.json'], 'json'),
     (['-I', 'json', 'a.conf', '-o', 'b.conf'], 'json'),
     (['a.json', '-o', 'b.conf'], 'json'),
     (['a.json', '-O', 'json', '-o', 'b.conf'], 'json'),
     )
)
def test_try_detecting_output_type(
    argv: list[str], exp: typing.Optional[str]
) -> None:
    (_psr, args) = anyconfig.cli.parse_args.parse(
        argv, prog='anyconfig_cli'
    )
    assert TT.try_detecting_output_type(args) == exp


@pytest.mark.parametrize(
    ("argv", ),
    ((['-'], ),
     (['a.conf'], ),
     (['a.conf', '-o', 'b.conf'], ),
     )
)
def test_try_detecting_output_type__failures(argv: list[str]) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        (_psr, args) = anyconfig.cli.parse_args.parse(
            argv, prog='anyconfig_cli'
        )
        with pytest.raises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()):
                with contextlib.redirect_stderr(io.StringIO()):
                    TT.try_detecting_output_type(args)
