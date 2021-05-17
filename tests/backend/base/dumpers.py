#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import tempfile
import unittest

import anyconfig.backend.base.dumpers as TT


class DumperMixinTestCase(unittest.TestCase):

    def test_ropen(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with TT.DumperMixin().wopen(temp_dir + '/test.txt') as fio:
                self.assertEqual(fio.mode, 'w')


class BinaryDumperMixinTestCase(unittest.TestCase):

    def test_ropen(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with TT.BinaryDumperMixin().wopen(temp_dir + '/test.txt') as fio:
                self.assertEqual(fio.mode, 'wb')

# vim:sw=4:ts=4:et:
