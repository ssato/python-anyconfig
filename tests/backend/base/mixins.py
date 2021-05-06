#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.backend.base.mixins as TT


FILE_PATH = '/dev/null'


class TestCase(unittest.TestCase):

    def test_TextFilesMixin_ropen(self):
        with TT.TextFilesMixin.ropen(FILE_PATH) as fileobj:
            self.assertEqual(fileobj.mode, 'r')

    def test_TextFilesMixin_wopen(self):
        with TT.TextFilesMixin.wopen(FILE_PATH) as fileobj:
            self.assertEqual(fileobj.mode, 'w')

    def test_BinaryFilesMixin_ropen(self):
        with TT.BinaryFilesMixin.ropen(FILE_PATH) as fileobj:
            self.assertEqual(fileobj.mode, 'rb')

    def test_BinaryFilesMixin_wopen(self):
        with TT.BinaryFilesMixin.wopen(FILE_PATH) as fileobj:
            self.assertEqual(fileobj.mode, 'wb')

# vim:sw=4:ts=4:et:
