#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import json
import unittest

from . import collector as TT


class NoDataCollector(TT.DataCollector):
    kind = 'not_exist'


class TestCase(unittest.TestCase):

    def test_load_datasets_failures(self):
        collector = NoDataCollector()
        with self.assertRaises(ValueError):
            collector.init()

    def test_load_datasets(self):
        collector = TT.DataCollector()
        collector.init()
        res = collector.datasets

        inp_refs = list(collector.root.glob(f'*/{collector.pattern}'))
        assert bool(inp_refs)

        e_refs = list(collector.root.glob('*/e/*.json'))
        assert bool(e_refs)

        o_refs = list(collector.root.glob('*/o/*.json'))
        assert bool(o_refs)

        s_refs = list(collector.root.glob('*/s/*.json'))
        assert bool(s_refs)

        for inp in inp_refs:
            self.assertTrue(any(inp in td.inputs for td in res))

        for e_file in e_refs:
            e_ref = json.load(e_file.open())
            self.assertTrue(any(e_ref == td.exp for td in res))

        for o_file in o_refs:
            o_ref = json.load(o_file.open())
            self.assertTrue(any(o_ref == td.opts for td in res))

        for s_file in s_refs:
            self.assertTrue(any(s_file == td.scm for td in res))

# vim:sw=4:ts=4:et:
