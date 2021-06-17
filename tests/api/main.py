#
# Copyright (C) 2012 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, no-member
import copy
import os
import pathlib
import unittest

import anyconfig.api as TT
import anyconfig.dicts
import tests.common

from tests.common import CNF_0


NULL_CNTNR = anyconfig.dicts.convert_to({})


class TestBase(unittest.TestCase):

    cnf = dic = CNF_0
    upd = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"), e=0)

    def assert_dicts_equal(self, dic, ref, ordered=False):
        self.assertEqual(
            dic, ref,
            "%r%s vs.%s%r" % (dic, os.linesep, os.linesep, ref)
        )


class TestBaseWithIO(TestBase):

    def setUp(self):
        self.workdir = pathlib.Path(tests.common.setup_workdir())
        self.a_path = self.workdir / "a.json"
        self.exp = copy.deepcopy(self.dic)

    def tearDown(self):
        tests.common.cleanup_workdir(str(self.workdir))


class TestBaseWithIOMultiFiles(TestBaseWithIO):

    def setUp(self):
        super().setUp()
        self.b_path = self.workdir / "b.json"
        self.g_path = self.workdir / "*.json"

        exp = copy.deepcopy(self.upd)  # Assume MS_DICTS strategy was used.
        exp["b"]["c"] = self.dic["b"]["c"]
        exp["name"] = self.dic["name"]
        self.exp = exp


class Test_50_load_and_dump(TestBaseWithIOMultiFiles):

    def test_30_dump_and_load(self):
        TT.dump(self.dic, self.a_path)
        TT.dump(self.upd, self.b_path)

        self.assertTrue(self.a_path.exists())
        self.assertTrue(self.b_path.exists())

        res = TT.load(self.a_path)
        self.assert_dicts_equal(res, self.dic)

        res = TT.load(self.g_path)
        self.assert_dicts_equal(res, self.exp)

        res = TT.load([self.a_path, self.b_path])
        self.assert_dicts_equal(res, self.exp)

    def test_31_dump_and_load__to_from_stream(self):
        with TT.open(self.a_path, mode='w') as strm:
            TT.dump(self.dic, strm)

        self.assertTrue(self.a_path.exists())

        with TT.open(self.a_path) as strm:
            res = TT.load(strm, ac_parser="json")
            self.assert_dicts_equal(res, self.dic)

    def test_32_dump_and_load__w_options(self):
        TT.dump(self.dic, self.a_path, indent=2)
        self.assertTrue(self.a_path.exists())

        TT.dump(self.upd, self.b_path, indent=2)
        self.assertTrue(self.b_path.exists())

        res = TT.load(self.a_path, parse_int=int)
        dic = copy.deepcopy(self.dic)
        self.assert_dicts_equal(res, dic)

        res = TT.load(self.g_path, parse_int=int)
        exp = copy.deepcopy(self.exp)
        self.assert_dicts_equal(res, exp)

        res = TT.load([self.a_path, self.b_path], parse_int=int)
        exp = copy.deepcopy(self.exp)
        self.assert_dicts_equal(res, exp)

    def test_34_load__ignore_missing(self):
        cpath = pathlib.Path(os.curdir) / "conf_file_should_not_exist"
        assert not cpath.exists()

        self.assertEqual(TT.load([cpath], ac_parser="ini",
                                 ac_ignore_missing=True),
                         NULL_CNTNR)

    def test_40_load_w_query(self):
        cnf_path = self.workdir / "cnf.json"
        TT.dump(CNF_0, cnf_path)

        try:
            if TT.query.jmespath:
                self.assertEqual(TT.load(cnf_path, ac_query="a"), 1)
                self.assertEqual(TT.load(cnf_path, ac_query="b.b"), [1, 2])
                self.assertEqual(TT.load(cnf_path, ac_query="b.b[1]"), 2)
                self.assertEqual(TT.load(cnf_path, ac_query="b.b[1:]"), [2])
                self.assertEqual(TT.load(cnf_path, ac_query="b.b[::-1]"),
                                 [2, 1])
                self.assertEqual(TT.load(cnf_path, ac_query="length(b.b)"), 2)
        except (NameError, AttributeError):
            pass  # jmespath is not available.

# vim:sw=4:ts=4:et:
