#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, protected-access, invalid-name
import pathlib
import unittest

import anyconfig.backend.base.base as TT  # stands for test target
import anyconfig.ioinfo


MZERO = TT.Parser()._container_factory()()


class TestCase(unittest.TestCase):

    def setUp(self):
        self.psr = TT.Parser()

    def test_10_type(self):
        self.assertEqual(self.psr.type(), str(TT.Parser._type))

    def test_20_loads__null_content(self):
        cnf = self.psr.loads('')
        self.assertEqual(cnf, MZERO)
        self.assertTrue(isinstance(cnf, type(MZERO)))

    def test_30_load__ac_ignore_missing(self):
        cpath = pathlib.Path.cwd() / 'conf_file_not_exist.json'
        assert not cpath.exists()

        ioi = anyconfig.ioinfo.make(str(cpath))
        cnf = self.psr.load(ioi, ac_ignore_missing=True)
        self.assertEqual(cnf, MZERO)
        self.assertTrue(isinstance(cnf, type(MZERO)))

# vim:sw=4:ts=4:et:
