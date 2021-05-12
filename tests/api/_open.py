#
# Copyright (C) 2012 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, no-member
import pathlib
import pickle
import tempfile
import unittest

import anyconfig.api._open as TT


from ..common import respath


class TestCase(unittest.TestCase):

    def test_open_text_io(self):
        path = respath('common/10.json')
        with TT.open(path) as fio:
            self.assertEqual(fio.mode, 'r')

    def test_open_byte_io(self):
        cnf = dict(a=1, b='b')

        with tempfile.TemporaryDirectory() as workdir:
            path = pathlib.Path(workdir) / 'test.pkl'
            pickle.dump(cnf, path.open(mode='wb'))

            with TT.open(path) as fio:
                self.assertEqual(fio.mode, 'rb')

# vim:sw=4:ts=4:et:
