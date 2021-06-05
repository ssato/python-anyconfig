#
# Copyright (C) 2012 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, no-member
import collections
import copy
import io
import os
import pathlib
import unittest

import anyconfig.api as TT
import anyconfig.backend.json
import anyconfig.dicts
import anyconfig.template
import tests.common

from tests.common import CNF_0


CNF_XML_1 = {'config': {'@attrs': {'name': 'foo'},
                        'a': '0',
                        'b': {'@attrs': {'id': 'b0'}, '@text': 'bbb'},
                        'c': None,
                        'sect0': {'d': 'x, y, z'},
                        'list1': [{'item': '0'}, {'item': '1'},
                                  {'item': '2'}],
                        'list2': {'@attrs': {'id': 'list2'},
                                  '@children': [{'item': 'i'},
                                                {'item': 'j'}]}}}

NULL_CNTNR = anyconfig.dicts.convert_to({})


class MyODict(collections.OrderedDict):
    pass


def _is_file_object(obj):
    try:
        return isinstance(obj, file)
    except NameError:  # python 3.x
        return isinstance(obj, io.IOBase)


class TestBase(unittest.TestCase):

    cnf = dic = CNF_0
    upd = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"), e=0)

    def assert_dicts_equal(self, dic, ref, ordered=False):
        self.assertEqual(
            dic, ref,
            "%r%s vs.%s%r" % (dic, os.linesep, os.linesep, ref)
        )


class Test_20_dumps_and_loads(TestBase):

    def test_30_dumps_and_loads(self):
        res = TT.loads(TT.dumps(self.cnf, "json"), "json")
        self.assert_dicts_equal(res, self.cnf)

    def test_30_dumps_and_loads__w_options(self):
        res = TT.loads(TT.dumps(self.cnf, "json", indent=2), "json",
                       ensure_ascii=False)
        self.assert_dicts_equal(res, self.cnf)


class TestBaseWithIO(TestBase):

    def setUp(self):
        self.workdir = pathlib.Path(tests.common.setup_workdir())
        self.a_path = self.workdir / "a.json"
        self.exp = copy.deepcopy(self.dic)

    def tearDown(self):
        tests.common.cleanup_workdir(str(self.workdir))


class Test_30_single_load(TestBaseWithIO):

    def test_10_dump_and_single_load(self):
        TT.dump(self.cnf, self.a_path)
        self.assertTrue(self.a_path.exists())

        res = TT.single_load(self.a_path)
        self.assert_dicts_equal(res, self.cnf)

    def test_11_dump_and_single_load__to_from_stream(self):
        TT.dump(self.cnf, self.a_path.open('w'))
        self.assertTrue(self.a_path.exists())

        res = TT.single_load(self.a_path.open())
        self.assert_dicts_equal(res, self.cnf)

    def test_12_dump_and_single_load__no_parser(self):
        self.assertRaises(TT.UnknownFileTypeError,
                          TT.single_load, "dummy.ext_not_exist")

    def test_20_dump_and_single_load__w_ordered_option(self):
        TT.dump(self.cnf, self.a_path)
        self.assertTrue(self.a_path.exists())

        # It works w/ JSON backend but some backend cannot keep the order of
        # items and the tests might fail.
        res = TT.single_load(self.a_path, ac_ordered=True)
        self.assert_dicts_equal(res, self.cnf, ordered=True)
        self.assertTrue(isinstance(res, collections.OrderedDict))

    def test_22_dump_and_single_load__w_ac_dict_option(self):
        TT.dump(self.cnf, self.a_path)
        self.assertTrue(self.a_path.exists())

        res = TT.single_load(self.a_path, ac_dict=MyODict)
        self.assert_dicts_equal(res, self.cnf, ordered=True)
        self.assertTrue(isinstance(res, MyODict))


class Test_32_single_load(unittest.TestCase):

    cnf = CNF_XML_1

    def setUp(self):
        self.workdir = pathlib.Path(tests.common.setup_workdir())

    def tearDown(self):
        tests.common.cleanup_workdir(str(self.workdir))

    def _load_and_dump_with_opened_files(self, filename, rmode='r', wmode='w',
                                         **oopts):
        cpath = self.workdir / filename

        with TT.open(cpath, 'w', **oopts) as out:
            TT.dump(self.cnf, out)
            self.assertTrue(_is_file_object(out))
            self.assertEqual(out.mode, wmode)

        with TT.open(cpath, 'rb', **oopts) as inp:
            cnf1 = TT.single_load(inp)
            self.assertTrue(_is_file_object(inp))
            self.assertEqual(inp.mode, rmode)
            cpair = (self.cnf, cnf1)
            self.assertEqual(*cpair)

    def test_10_open_json_file(self):
        self._load_and_dump_with_opened_files("a.json")

    def test_20_open_xml_file(self):
        if "xml" in TT.list_types():
            self._load_and_dump_with_opened_files("a.xml", 'rb', 'wb')

    def test_40_open_yaml_file(self):
        if "yaml" in TT.list_types():
            self._load_and_dump_with_opened_files("a.yaml")
            self._load_and_dump_with_opened_files("a.yml")


class TestBaseWithIOMultiFiles(TestBaseWithIO):

    def setUp(self):
        super().setUp()
        self.b_path = self.workdir / "b.json"
        self.g_path = self.workdir / "*.json"

        exp = copy.deepcopy(self.upd)  # Assume MS_DICTS strategy was used.
        exp["b"]["c"] = self.dic["b"]["c"]
        exp["name"] = self.dic["name"]
        self.exp = exp


class Test_42_multi_load(TestBaseWithIOMultiFiles):

    def test_60_multi_load__w_ac_dict_option(self):
        TT.dump(self.dic, self.a_path)
        TT.dump(self.upd, self.b_path)

        res = TT.multi_load(self.g_path, ac_dict=MyODict)
        self.assert_dicts_equal(res, self.exp)
        self.assertTrue(isinstance(res, MyODict))


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
