#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import unittest

import anyconfig.backend.base.loaders as TT


FILE_PATH = __file__


class LoaderMixinTestCase(unittest.TestCase):

    def test_ropen(self):
        with TT.LoaderMixin().ropen(FILE_PATH) as fio:
            self.assertEqual(fio.mode, 'r')


class BinaryLoaderMixinTestCase(unittest.TestCase):

    def test_ropen(self):
        with TT.BinaryLoaderMixin().ropen(FILE_PATH) as fio:
            self.assertEqual(fio.mode, 'rb')

# vim:sw=4:ts=4:et:
