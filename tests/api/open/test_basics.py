#
# Copyright (C) 2012 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name, no-member
import pathlib
import pickle
import tempfile

import anyconfig.api._open as TT
import anyconfig.api._load as LD

from . import common


class TestCase(common.BaseTestCase):

    def test_open_text_io(self):
        for data in self.each_data():
            with TT.open(data.inp_path, **data.opts) as inp:
                self.assertEqual(LD.loads(inp.read(), **data.opts), data.inp)

    def test_open_byte_io(self):
        cnf = dict(a=1, b='b')

        with tempfile.TemporaryDirectory() as workdir:
            path = pathlib.Path(workdir) / 'test.pkl'
            pickle.dump(cnf, path.open(mode='wb'))

            with TT.open(path) as fio:
                self.assertEqual(fio.mode, 'rb')
                self.assertEqual(
                    LD.loads(fio.read(), ac_parser='pickle'),
                    LD.load(path)
                )

# vim:sw=4:ts=4:et:
