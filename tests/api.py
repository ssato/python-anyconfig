#
# Copyright (C) 2012 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, no-member
from __future__ import absolute_import

import collections
import copy
import io
import os
import pathlib
import unittest

import anyconfig.api as TT
import anyconfig.backends
import anyconfig.backend.json
import anyconfig.dicts
import anyconfig.processors
import anyconfig.schema
import anyconfig.template
import tests.common

from tests.common import (
    CNF_0, SCM_0, CNF_1, respath
)


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

NULL_CNTNR = TT.anyconfig.dicts.convert_to({})


class MyODict(collections.OrderedDict):
    pass


def _is_file_object(obj):
    try:
        return isinstance(obj, file)
    except NameError:  # python 3.x
        return isinstance(obj, io.IOBase)


class Test_10_find(unittest.TestCase):

    psrs = anyconfig.backends.Parsers().list()

    def _assert_isinstances(self, obj, clss, msg=False):
        self.assertTrue(any(isinstance(obj, cls) for cls in clss),
                        msg or "%r vs %r" % (obj, clss))

    def test_10_find__w_parser_type_or_instance(self):
        def _findall_by_type(typ):
            fnc = anyconfig.processors.findall_with_pred
            return fnc(lambda p: typ == p.type(), self.psrs)

        cpath = "dummy.conf"
        for psr in self.psrs:
            ldrs = _findall_by_type(psr.type())
            self._assert_isinstances(TT.find(cpath, psr.type()), ldrs)
            self._assert_isinstances(TT.find(cpath, psr()), ldrs)

    def test_20_find__w_parser_by_file(self):
        def _find_ldrs_by_ext(ext):
            fnc = anyconfig.processors.findall_with_pred
            return fnc(lambda p: ext in p.extensions(), self.psrs)

        for psr in self.psrs:
            for ext in psr.extensions():
                ldrs = _find_ldrs_by_ext(ext)
                self._assert_isinstances(TT.find("dummy." + ext), ldrs)

    def test_30_find__unknown_parser_type(self):
        self.assertRaises(TT.UnknownProcessorTypeError,
                          TT.find, "a.cnf", "type_not_exist")

    def test_40_find__unknown_file_type(self):
        self.assertRaises(TT.UnknownFileTypeError,
                          TT.find, "dummy.ext_not_found")


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

    def test_40_loads_wo_type(self):
        cnf_s = "requires:bash,zsh"
        self.assertTrue(TT.loads(cnf_s) is None)

    def test_42_loads_w_type_not_exist(self):
        a_s = "requires:bash,zsh"
        self.assertRaises(TT.UnknownProcessorTypeError,
                          TT.loads, a_s, "type_not_exist")

    def test_44_loads_w_type__template(self):
        if not anyconfig.template.SUPPORTED:
            return

        a_s = "requires: [{{ requires|join(', ') }}]"
        reqs = dict(requires=["bash", "zsh"])

        a1 = TT.loads(a_s, ac_parser="yaml", ac_template=True,
                      ac_context=reqs)

        self.assertEqual(a1["requires"], reqs["requires"])

    def test_46_loads_w_type__broken_template(self):
        if not anyconfig.template.SUPPORTED:
            return

        a = dict(requires="{% }}", )
        a_s = 'requires: "{% }}"'
        a1 = TT.loads(a_s, ac_parser="yaml", ac_template=True,
                      ac_context={})

        self.assertEqual(a1["requires"], a["requires"])

    def test_48_loads_w_validation(self):
        cnf_s = TT.dumps(CNF_0, "json")
        scm_s = TT.dumps(SCM_0, "json")
        cnf_2 = TT.loads(cnf_s, ac_parser="json", ac_context={},
                         ac_schema=scm_s)

        self.assertEqual(cnf_2["name"], CNF_0["name"])
        self.assertEqual(cnf_2["a"], CNF_0["a"])
        self.assertEqual(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEqual(cnf_2["b"]["c"], CNF_0["b"]["c"])

    @unittest.skipIf(not anyconfig.schema.JSONSCHEMA_IS_AVAIL,
                     "json schema lib is not available")
    def test_49_loads_w_validation_error(self):
        cnf_s = """{"a": "aaa"}"""
        scm_s = TT.dumps(SCM_0, "json")
        cnf_2 = TT.loads(cnf_s, ac_parser="json", ac_schema=scm_s)
        self.assertTrue(cnf_2 is None, cnf_2)


class Test_22_single_load(TestBase):

    a_path = respath('00-cnf.json')
    cnf = CNF_1

    def test_10__single_load(self):
        res = TT.single_load(self.a_path)
        self.assert_dicts_equal(res, self.cnf)

    def test_12__single_load__ac_parser(self):
        res = TT.single_load(self.a_path, ac_parser="json")
        self.assert_dicts_equal(res, self.cnf)

    def test_14__single_load__ac_parser_by_id(self):
        cid = anyconfig.backend.json.Parser.cid()
        res = TT.single_load(self.a_path, ac_parser=cid)
        self.assert_dicts_equal(res, self.cnf)

    def test_20__single_load__stream(self):
        res = TT.single_load(open(self.a_path), ac_parser="json")
        self.assert_dicts_equal(res, self.cnf)

    def test_30__single_load__pathlib(self):
        pobj = pathlib.Path(self.a_path)
        res = TT.single_load(pobj)
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

    def test_14_single_load__ignore_missing(self):
        cpath = pathlib.Path(os.curdir) / "conf_file_should_not_exist"
        assert not cpath.exists()

        self.assertEqual(TT.single_load(cpath, "ini", ac_ignore_missing=True),
                         NULL_CNTNR)

    def test_15_single_load__fail_to_render_template(self):
        if not anyconfig.template.SUPPORTED:
            return

        cnf_s = "name: '{{ name'"  # Should cause template renering error.
        cpath = self.workdir / "a.yaml"
        cpath.write_text(cnf_s)

        cnf = TT.single_load(cpath, ac_template=True, ac_context=dict(a=1))
        self.assertEqual(cnf["name"], "{{ name")

    def test_16_single_load__template(self):
        if not anyconfig.template.SUPPORTED:
            return

        cpath = respath('30-00-template-cnf.json')
        cnf = TT.single_load(cpath, ac_template=True, ac_context=self.cnf)
        self.assert_dicts_equal(cnf, self.cnf)

        spath = respath('30-00-template-cnf-ng-scm.json')

        # Validation should fail.
        cnf2 = TT.single_load(cpath, ac_template=True, ac_context=self.cnf,
                              ac_schema=spath)
        self.assertTrue(cnf2 is None)

    def test_18_single_load__templates(self):
        if not anyconfig.template.SUPPORTED:
            return

        a_path = respath('30-00-cnf.json')
        a2_path = respath('00-00-cnf.json')  # Not a template

        cnf1 = TT.single_load(a_path, ac_template=True, ac_context=self.cnf)
        self.assertEqual(self.cnf, cnf1, str(cnf1))

        cnf2 = TT.single_load(a2_path, ac_template=True)
        self.assertEqual(cnf2["a"], 1)

    @unittest.skipIf(not anyconfig.schema.JSONSCHEMA_IS_AVAIL,
                     "json schema lib is not available")
    def test_19_dump_and_single_load_with_validation(self):
        cnf = CNF_0
        scm = SCM_0

        cnf_path = self.workdir / "cnf_19.json"
        scm_path = self.workdir / "scm_19.json"

        TT.dump(cnf, cnf_path)
        TT.dump(scm, scm_path)
        self.assertTrue(cnf_path.exists())
        self.assertTrue(scm_path.exists())

        cnf_1 = TT.single_load(cnf_path, ac_schema=scm_path)

        self.assertFalse(cnf_1 is None)  # Validation should succeed.
        self.assertEqual(cnf_1, cnf, cnf_1)

        cnf_2 = cnf.copy()
        cnf_2["a"] = "aaa"  # It's type should be integer not string.
        cnf_2_path = self.workdir / "cnf_19_2.json"
        TT.dump(cnf_2, cnf_2_path)
        self.assertTrue(cnf_2_path.exists())

        cnf_3 = TT.single_load(cnf_2_path, ac_schema=scm_path)
        self.assertTrue(cnf_3 is None)  # Validation should fail.

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


class Test_34_single_load(TestBaseWithIO):

    def test_10_single_load_w_validation(self):
        cnf_path = self.workdir / "cnf.json"
        scm_path = self.workdir / "scm.json"
        TT.dump(CNF_0, cnf_path)
        TT.dump(SCM_0, scm_path)

        cnf_2 = TT.single_load(cnf_path, ac_context={}, ac_schema=scm_path)

        self.assertEqual(cnf_2["name"], CNF_0["name"])
        self.assertEqual(cnf_2["a"], CNF_0["a"])
        self.assertEqual(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEqual(cnf_2["b"]["c"], CNF_0["b"]["c"])

    def test_20_single_load_w_query(self):
        cpath = self.workdir / "cnf.json"
        TT.dump(CNF_0, cpath)

        try:
            if TT.query.jmespath:
                self.assertEqual(TT.single_load(cpath, ac_query="a"), 1)
                self.assertEqual(TT.single_load(cpath, ac_query="b.b"), [1, 2])
                self.assertEqual(TT.single_load(cpath, ac_query="b.b[1]"), 2)
                self.assertEqual(TT.single_load(cpath, ac_query="b.b[1:]"),
                                 [2])
                self.assertEqual(TT.single_load(cpath, ac_query="b.b[::-1]"),
                                 [2, 1])
                self.assertEqual(TT.single_load(cpath, ac_query="length(b.b)"),
                                 2)
        except (NameError, AttributeError):
            pass  # jmespath is not available.


class TestBaseWithIOMultiFiles(TestBaseWithIO):

    def setUp(self):
        super().setUp()
        self.b_path = self.workdir / "b.json"
        self.g_path = self.workdir / "*.json"

        exp = copy.deepcopy(self.upd)  # Assume MS_DICTS strategy was used.
        exp["b"]["c"] = self.dic["b"]["c"]
        exp["name"] = self.dic["name"]
        self.exp = exp


class Test_40_multi_load_with_strategies(TestBaseWithIOMultiFiles):

    def _check_multi_load_with_strategy(self, exp, merge=TT.MS_DICTS):
        TT.dump(self.dic, self.a_path)
        TT.dump(self.upd, self.b_path)

        self.assertTrue(self.a_path.exists())
        self.assertTrue(self.b_path.exists())

        res0 = TT.multi_load(self.g_path, ac_merge=merge)
        res1 = TT.multi_load([self.g_path, self.b_path], ac_merge=merge)

        self.assertTrue(res0)
        self.assertTrue(res1)

        self.assert_dicts_equal(res0, exp)
        self.assert_dicts_equal(res1, exp)

    def test_10_default_merge_strategy(self):
        exp = copy.deepcopy(self.upd)
        exp["b"]["c"] = self.dic["b"]["c"]
        exp["name"] = self.dic["name"]

        self._check_multi_load_with_strategy(exp, merge=None)
        self._check_multi_load_with_strategy(exp)

    def test_20_merge_dicts_and_lists(self):
        exp = copy.deepcopy(self.upd)
        exp["b"]["b"] = [0] + self.upd["b"]["b"]
        exp["b"]["c"] = self.dic["b"]["c"]
        exp["name"] = self.dic["name"]
        self._check_multi_load_with_strategy(exp, merge=TT.MS_DICTS_AND_LISTS)

    def test_30_merge_with_replace(self):
        exp = copy.deepcopy(self.upd)
        exp["name"] = self.dic["name"]
        self._check_multi_load_with_strategy(exp, merge=TT.MS_REPLACE)

    def test_40_merge_wo_replace(self):
        exp = copy.deepcopy(self.dic)
        exp["e"] = self.upd["e"]
        self._check_multi_load_with_strategy(exp, merge=TT.MS_NO_REPLACE)

    def test_60_wrong_merge_strategy(self):
        cpath = self.workdir / "a.json"
        TT.dump(dict(a=1, b=2), cpath)
        try:
            TT.multi_load([cpath, cpath], ac_merge="merge_st_not_exist")
            raise RuntimeError("Wrong merge strategy was not handled!")
        except ValueError:
            self.assertTrue(bool(1))  # To suppress warn of pylint.


class Test_42_multi_load(TestBaseWithIOMultiFiles):

    def test_10_multi_load__empty_path_list(self):
        self.assertEqual(TT.multi_load([]), NULL_CNTNR)

    def test_20_dump_and_multi_load__mixed_file_types(self):
        c_path = self.workdir / "c.yml"

        TT.dump(self.dic, self.a_path)  # JSON
        try:
            TT.dump(self.upd, c_path)  # YAML
        except (TT.UnknownProcessorTypeError, TT.UnknownFileTypeError):
            return  # YAML backend is not available in this env.

        self.assertTrue(self.a_path.exists())
        self.assertTrue(c_path.exists())

        res = TT.multi_load([self.a_path, c_path])
        self.assert_dicts_equal(res, self.exp)

    def test_30_dump_and_multi_load__to_from_stream(self):
        TT.dump(self.dic, self.a_path)
        TT.dump(self.upd, self.b_path)

        res = TT.multi_load([TT.open(self.a_path), TT.open(self.b_path)])
        self.assert_dicts_equal(res, self.exp)

    def test_40_multi_load__ignore_missing(self):
        cpath = pathlib.Path(os.curdir) / "conf_file_should_not_exist"
        assert not cpath.exists()

        self.assertEqual(TT.multi_load([cpath], ac_parser="ini",
                                       ac_ignore_missing=True),
                         NULL_CNTNR)
        # It will be remove after 'ignore_missing' was deprecated and removed.
        self.assertEqual(TT.multi_load([cpath], ac_parser="ini",
                                       ignore_missing=True),
                         NULL_CNTNR)

    def test_50_multi_load__templates(self):
        if not anyconfig.template.SUPPORTED:
            return

        ctx = self.dic.copy()
        TT.merge(ctx, self.upd, ac_merge=TT.MS_DICTS)

        # a_path = respath('30-00-template-cnf.json')
        b_path = respath('30-10-template-cnf.json')
        g_path = respath('30-*-template-cnf.json')

        opts = dict(ac_merge=TT.MS_DICTS, ac_template=True, ac_context=ctx)
        try:
            res0 = TT.multi_load(g_path, **opts)
            res1 = TT.multi_load([g_path, b_path], **opts)
        except (TT.UnknownProcessorTypeError, TT.UnknownFileTypeError):
            return

        self.assert_dicts_equal(res0, self.exp)
        self.assert_dicts_equal(res1, self.exp)

    def test_60_multi_load__w_ac_dict_option(self):
        TT.dump(self.dic, self.a_path)
        TT.dump(self.upd, self.b_path)

        res = TT.multi_load(self.g_path, ac_dict=MyODict)
        self.assert_dicts_equal(res, self.exp)
        self.assertTrue(isinstance(res, MyODict))


class Test_44_multi_load(TestBase):

    def test_10_multi_load_w_validation_for_partial_single_config_files(self):
        cpaths = [respath('00-00-cnf.json'),
                  respath('00-01-cnf.json'),
                  respath('00-02-cnf.json')]
        spath = respath('00-scm.json')

        cnf = TT.multi_load(cpaths, ac_schema=spath)
        ref = TT.multi_load(cpaths)
        self.assert_dicts_equal(cnf, ref, ordered=False)


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
                                 ignore_missing=True),
                         NULL_CNTNR)

    def test_36_load_w_validation(self):
        cnf_path = self.workdir / "cnf.json"
        scm_path = self.workdir / "scm.json"
        TT.dump(CNF_0, cnf_path)
        TT.dump(SCM_0, scm_path)

        cnf_2 = TT.load(cnf_path, ac_context={}, ac_schema=scm_path)

        self.assertEqual(cnf_2["name"], CNF_0["name"])
        self.assertEqual(cnf_2["a"], CNF_0["a"])
        self.assertEqual(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEqual(cnf_2["b"]["c"], CNF_0["b"]["c"])

    @unittest.skipIf('yml' not in TT.list_types(), "yaml lib is not available")
    def test_38_load_w_validation_yaml(self):
        cnf_path = self.workdir / "cnf.yml"
        scm_path = self.workdir / "scm.yml"
        TT.dump(CNF_0, cnf_path)
        TT.dump(SCM_0, scm_path)

        cnf_2 = TT.load(cnf_path, ac_context={}, ac_schema=scm_path)

        self.assertEqual(cnf_2["name"], CNF_0["name"])
        self.assertEqual(cnf_2["a"], CNF_0["a"])
        self.assertEqual(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEqual(cnf_2["b"]["c"], CNF_0["b"]["c"])

    def test_39_single_load__w_validation(self):
        (cnf, scm) = (CNF_0, SCM_0)
        cpath = self.workdir / "cnf.json"
        spath = self.workdir / "scm.json"

        TT.dump(cnf, cpath)
        TT.dump(scm, spath)

        cnf1 = TT.single_load(cpath, ac_schema=spath)
        self.assert_dicts_equal(cnf, cnf1)

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
