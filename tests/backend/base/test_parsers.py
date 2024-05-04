#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,protected-access
"""Test cases for anyconfig.backend.base.parsers."""
from __future__ import annotations

import pathlib

import anyconfig.backend.base.parsers as TT
import anyconfig.ioinfo


MZERO = TT.Parser()._container_factory()()


def test_type():
    assert TT.Parser().type() == str(TT.Parser._type)


def test_loads__null_content():
    psr = TT.Parser()
    cnf = psr.loads('')
    assert cnf == MZERO
    assert isinstance(cnf, type(MZERO))


def test_load__ac_ignore_missing():
    cpath = pathlib.Path.cwd() / 'conf_file_not_exist.json'
    assert not cpath.exists()

    psr = TT.Parser()
    ioi = anyconfig.ioinfo.make(str(cpath))
    cnf = psr.load(ioi, ac_ignore_missing=True)
    assert cnf == MZERO
    assert isinstance(cnf, type(MZERO))
