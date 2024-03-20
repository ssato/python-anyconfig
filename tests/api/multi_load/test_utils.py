#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import json
import pathlib
import unittest
import tempfile

from ... import base
from . import utils as TT


RES_DIR = base.RES_DIR / 'multi_load'
SELF = pathlib.Path(__file__)


class TestCase(unittest.TestCase):

    datadir = RES_DIR / 'basics'

    def test_load_data_or_path_no_data(self):
        with tempfile.TemporaryDirectory() as tdir:
            tmp_path = pathlib.Path(tdir)
            aes = [
                ((tmp_path, ), {}, None),
                ((tmp_path, ), dict(default='abc'), 'abc'),
            ]
            for args, kwargs, exp in aes:
                self.assertEqual(
                    TT.load_data_or_path(*args, **kwargs),
                    exp
                )

    def test_load_data_or_path(self):
        # tests/res/multi_load/basics/00/00.json
        ddir = self.datadir / '00'
        inp = ddir / '00.json'
        aes = [
            # datadir, should_exist, load, default
            # .. seealso:: tests/res/multi_load/basics/00/00.json
            ((ddir, ), dict(load=False), inp),
            ((ddir, ), {}, json.load(inp.open())),
        ]
        for args, kwargs, exp in aes:
            self.assertEqual(
                TT.load_data_or_path(*args, **kwargs),
                exp
            )

    def test_load_data_or_path_failures(self):
        datadir = pathlib.Path().cwd() / 'dir_not_exist'
        aes = [
            ((datadir, ), dict(should_exist=(datadir.name, )), OSError),
        ]
        for args, kwargs, exc in aes:
            with self.assertRaises(exc):
                TT.load_data_or_path(*args, **kwargs)

    def test_each_data_from_dir(self):
        inp_refs = list(self.datadir.glob('*/*.json'))
        assert bool(inp_refs)

        e_refs = list(self.datadir.glob('*/e/*.json'))
        assert bool(e_refs)

        o_refs = list(self.datadir.glob('*/o/*.json'))
        assert bool(o_refs)

        aes = [
            ((self.datadir, ), {}, (1, inp_refs, e_refs, o_refs))
        ]
        for args, kwargs, exp in aes:
            res = list(TT.each_data_from_dir(*args, **kwargs))
            self.assertTrue(bool(res))
            self.assertTrue(len(res) > exp[0])

            for inp in exp[1]:
                self.assertTrue(any(inp in td.inputs for td in res))

            for e_file in exp[2]:
                e_ref = json.load(e_file.open())
                self.assertTrue(any(e_ref == td.exp for td in res))

            for o_file in exp[3]:
                o_ref = json.load(o_file.open())
                self.assertTrue(any(o_ref == td.opts for td in res))

    def test_each_data_from_dir_failures(self):
        with self.assertRaises(ValueError):
            _ = list(TT.each_data_from_dir(SELF))

# vim:sw=4:ts=4:et:
