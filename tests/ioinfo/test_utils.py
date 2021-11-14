#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Test cases for anyconfig.utils.files.
"""
import pathlib

import pytest

import anyconfig.ioinfo.utils as TT


SELF: pathlib.Path = pathlib.Path(__file__)


@pytest.mark.parametrize(
    ('inp', 'exp'),
    (
     (SELF, (SELF.resolve(), 'py')),
     )
)
def test_get_path_and_ext(inp, exp):
    res = TT.get_path_and_ext(inp)
    assert res == exp


try:
    PATH_RESOLVE_SHOULD_WORK: bool = bool(
        pathlib.Path(
            '<stdout>'
        ).expanduser().resolve()
    )
except (RuntimeError, OSError):
    PATH_RESOLVE_SHOULD_WORK: bool = False


@pytest.mark.skipif(
    PATH_RESOLVE_SHOULD_WORK,
    reason='pathlib.Path.resolve() should work'
)
def test_get_path_and_ext_failures():
    path = pathlib.Path('<stdout>')
    res = TT.get_path_and_ext(path)
    assert res == (path, '')


def test_expand_from_path(tmp_path):
    tdir = tmp_path / 'a' / 'b' / 'c'
    tdir.mkdir(parents=True)

    pathlib.Path(tdir / 'd.txt').touch()
    pathlib.Path(tdir / 'e.txt').touch()
    pathlib.Path(tdir / 'f.json').write_text("{'a': 1}\n")

    path = tdir / 'd.txt'

    for inp, exp in ((path, [path]),
                     (tdir / '*.txt',
                      [tdir / 'd.txt', tdir / 'e.txt']),
                     (tdir.parent / '**' / '*.txt',
                      [tdir / 'd.txt', tdir / 'e.txt']),
                     (tdir.parent / '**' / '*.*',
                      [tdir / 'd.txt',
                       tdir / 'e.txt',
                       tdir / 'f.json']),
                     ):
        res = sorted(TT.expand_from_path(inp))
        assert res == sorted(exp), f'{inp!r} vs. {exp!r}'

# vim:sw=4:ts=4:et:
