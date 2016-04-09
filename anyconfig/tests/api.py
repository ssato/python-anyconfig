#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, no-member
from __future__ import absolute_import

import logging
import os
import os.path
import unittest

import anyconfig.api as TT
import anyconfig.backends
import anyconfig.template
import anyconfig.tests.common

from anyconfig.tests.common import CNF_0, SCM_0, dicts_equal
from anyconfig.compat import OrderedDict, IS_PYTHON_3
from anyconfig.mdicts import convert_to


# suppress logging messages.
TT.set_loglevel(logging.CRITICAL)

CNF_TMPL_0 = """name: {{ name|default('a') }}
a: {{ a }}
b:
    b:
      {% for x in b.b -%}
      - {{ x }}
      {% endfor %}
    c: {{ b.c }}
"""

CNF_TMPL_1 = """a: {{ a }}
b:
    b:
        {% for x in b.b -%}
        - {{ x }}
        {% endfor %}
    c: {{ b.c }}

name: {{ name }}
"""

CNF_TMPL_2 = """a: {{ a }}
b:
    b:
        {% for x in b.b -%}
        - {{ x }}
        {% endfor %}
    d: {{ b.d }}
"""


class Test_10_find_loader(unittest.TestCase):

    def _assert_isinstance(self, obj, cls, msg=False):
        self.assertTrue(isinstance(obj, cls), msg or repr(obj))

    def test_10_find_loader__w_given_parser_type(self):
        cpath = "dummy.conf"
        for psr in anyconfig.backends.PARSERS:
            self._assert_isinstance(TT.find_loader(cpath, psr.type()), psr)

    def test_12_find_loader__w_given_parser_instance(self):
        cpath = "dummy.conf"
        for psr in anyconfig.backends.PARSERS:
            self._assert_isinstance(TT.find_loader(cpath, psr()), psr)

    def test_20_find_loader__by_file(self):
        for psr in anyconfig.backends.PARSERS:
            for ext in psr.extensions():
                self._assert_isinstance(TT.find_loader("dummy." + ext), psr,
                                        "ext=%s, psr=%r" % (ext, psr))

    def test_30_find_loader__not_found(self):
        self.assertEqual(TT.find_loader("a.cnf", "type_not_exist"), None)
        self.assertEqual(TT.find_loader("dummy.ext_not_found"), None)


class Test_20_dumps_and_loads(unittest.TestCase):

    cnf = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

    def test_30_dumps_and_loads(self):
        cnf = TT.loads(TT.dumps(self.cnf, "json"), "json")
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_dumps_and_loads__w_options(self):
        cnf = TT.loads(TT.dumps(self.cnf, "json", indent=2), "json",
                       ensure_ascii=False)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_32_dumps_and_loads__w_options__no_dumper(self):
        cnf = TT.loads(TT.dumps(self.cnf, "type_not_exist"), "json")
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_40_loads_wo_type(self):
        a_s = "requires:bash,zsh"

        a1 = TT.loads(a_s)
        # a = dict(requires=["bash", "zsh"])
        # self.assertEqual(a1["requires"], a["requires"])
        self.assertTrue(a1 is None)

    def test_42_loads_w_type_not_exist(self):
        a_s = "requires:bash,zsh"

        a1 = TT.loads(a_s, "type_not_exist")
        # a = dict(requires=["bash", "zsh"])
        # self.assertEqual(a1["requires"], a["requires"])
        self.assertTrue(a1 is None)

    def test_44_loads_w_type__template(self):
        if not anyconfig.template.SUPPORTED:
            return

        a_s = "requires: [{{ requires|join(', ') }}]"
        context = dict(requires=["bash", "zsh"], )

        a1 = TT.loads(a_s, ac_parser="yaml", ac_template=True,
                      ac_context=context)

        a = dict(requires=["bash", "zsh"])
        self.assertEqual(a1["requires"], a["requires"])

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
                         ac_validate=scm_s)

        self.assertEqual(cnf_2["name"], CNF_0["name"])
        self.assertEqual(cnf_2["a"], CNF_0["a"])
        self.assertEqual(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEqual(cnf_2["b"]["c"], CNF_0["b"]["c"])

    def test_49_loads_w_validation_error(self):
        cnf_s = """{"a": "aaa"}"""
        scm_s = TT.dumps(SCM_0, "json")
        cnf_2 = TT.loads(cnf_s, ac_parser="json", ac_schema=scm_s)
        self.assertTrue(cnf_2 is None, cnf_2)


class Test_30_single_load(unittest.TestCase):

    cnf = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_dump_and_single_load(self):
        cpath = os.path.join(self.workdir, "a.json")

        TT.dump(self.cnf, cpath)
        self.assertTrue(os.path.exists(cpath))
        cnf1 = TT.single_load(cpath)

        self.assertTrue(dicts_equal(self.cnf, cnf1), str(cnf1))

    def test_11_dump_and_single_load__to_from_stream(self):
        cpath = os.path.join(self.workdir, "a.json")

        TT.dump(self.cnf, open(cpath, 'w'))
        self.assertTrue(os.path.exists(cpath))
        cnf1 = TT.single_load(open(cpath))

        self.assertTrue(dicts_equal(self.cnf, cnf1), str(cnf1))

    def test_12_dump_and_single_load__no_parser(self):
        self.assertEqual(TT.single_load("dummy.ext_not_exist"), None)

    def test_13_dump_and_single_load__namedtuple(self):
        if not IS_PYTHON_3:  # TODO: it does not work with python3.
            cpath = os.path.join(self.workdir, "a.json")
            cnf = OrderedDict(sorted(self.cnf.items()))
            cnf0 = convert_to(cnf, ac_namedtuple=True)

            TT.dump(cnf0, cpath)
            self.assertTrue(os.path.exists(cpath))

            cnf1 = TT.single_load(cpath, ac_namedtuple=True)
            self.assertTrue(cnf0 == cnf1, "\n%r ->\n%r" % (cnf0, cnf1))

    def test_14_single_load__ignore_missing(self):
        null_cntnr = TT.to_container()
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        self.assertEqual(TT.single_load(cpath, "ini", ignore_missing=True),
                         null_cntnr)

    def test_15_single_load__fail_to_render_template(self):
        if not anyconfig.template.SUPPORTED:
            return

        cnf_s = "name: '{{ name'"  # Should cause template renering error.
        cpath = os.path.join(self.workdir, "a.yaml")
        open(cpath, 'w').write(cnf_s)

        cnf = TT.single_load(cpath, ac_template=True, ac_context=dict(a=1))
        self.assertEqual(cnf["name"], "{{ name")

    def test_16_single_load__template(self):
        if not anyconfig.template.SUPPORTED:
            return

        cpath = os.path.join(self.workdir, "a.yaml")
        open(cpath, 'w').write(CNF_TMPL_0)

        cnf = TT.single_load(cpath, ac_template=True, ac_context=self.cnf)
        self.assertTrue(dicts_equal(self.cnf, cnf), str(cnf))

        spath = os.path.join(self.workdir, "scm.json")
        TT.dump(dict(type="integer"), spath)  # Validation should fail.

        cnf2 = TT.single_load(cpath, ac_template=True, ac_context=self.cnf,
                              ac_schema=spath)
        self.assertTrue(cnf2 is None)

    def test_18_single_load__templates(self):
        if not anyconfig.template.SUPPORTED:
            return

        a_path = os.path.join(self.workdir, "a.yml")
        b_path = os.path.join(self.workdir, "b.yml")
        a2_path = os.path.join(self.workdir, "x/y/z", "a.yml")

        open(a_path, 'w').write("{% include 'b.yml' %}")
        open(b_path, 'w').write(CNF_TMPL_0)
        os.makedirs(os.path.dirname(a2_path))
        open(a2_path, 'w').write("a: 'xyz'")

        cnf1 = TT.single_load(a_path, ac_template=True, ac_context=self.cnf)
        self.assertTrue(dicts_equal(self.cnf, cnf1), str(cnf1))

        cnf2 = TT.single_load(a2_path, ac_template=True)
        self.assertEqual(cnf2["a"], "xyz")

    def test_19_dump_and_single_load_with_validation(self):
        cnf = CNF_0
        scm = SCM_0

        cnf_path = os.path.join(self.workdir, "cnf_19.json")
        scm_path = os.path.join(self.workdir, "scm_19.json")

        TT.dump(cnf, cnf_path)
        TT.dump(scm, scm_path)
        self.assertTrue(os.path.exists(cnf_path))
        self.assertTrue(os.path.exists(scm_path))

        cnf_1 = TT.single_load(cnf_path, ac_schema=scm_path)

        self.assertFalse(cnf_1 is None)  # Validation should succeed.
        self.assertTrue(dicts_equal(cnf_1, cnf), cnf_1)

        cnf_2 = cnf.copy()
        cnf_2["a"] = "aaa"  # It's type should be integer not string.
        cnf_2_path = os.path.join(self.workdir, "cnf_19_2.json")
        TT.dump(cnf_2, cnf_2_path)
        self.assertTrue(os.path.exists(cnf_2_path))

        cnf_3 = TT.single_load(cnf_2_path, ac_schema=scm_path)
        self.assertTrue(cnf_3 is None)  # Validation should fail.


class Test_40_multi_load(unittest.TestCase):

    cnf = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_dump_and_multi_load__default_merge_strategy(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")
        g_path = os.path.join(self.workdir, "*.json")

        TT.dump(a, a_path)
        TT.dump(b, b_path)

        a0 = TT.multi_load(g_path)
        a02 = TT.multi_load([g_path, b_path])

        self.assertEqual(a0["name"], a["name"])
        self.assertEqual(a0["a"], b["a"])
        self.assertEqual(a0["b"]["b"], b["b"]["b"])
        self.assertEqual(a0["b"]["c"], a["b"]["c"])
        self.assertEqual(a0["b"]["d"], b["b"]["d"])

        self.assertEqual(a02["name"], a["name"])
        self.assertEqual(a02["a"], b["a"])
        self.assertEqual(a02["b"]["b"], b["b"]["b"])
        self.assertEqual(a02["b"]["c"], a["b"]["c"])
        self.assertEqual(a02["b"]["d"], b["b"]["d"])

        a1 = TT.multi_load([a_path, b_path], ac_merge=TT.MS_DICTS)

        self.assertEqual(a1["name"], a["name"])
        self.assertEqual(a1["a"], b["a"])
        self.assertEqual(a1["b"]["b"], b["b"]["b"])
        self.assertEqual(a1["b"]["c"], a["b"]["c"])
        self.assertEqual(a1["b"]["d"], b["b"]["d"])

    def test_12_dump_and_multi_load__default_merge_strategy(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")
        g_path = os.path.join(self.workdir, "*.json")

        TT.dump(a, a_path)
        TT.dump(b, b_path)

        a2 = TT.multi_load([a_path, b_path], ac_merge=TT.MS_DICTS_AND_LISTS)

        self.assertEqual(a2["name"], a["name"])
        self.assertEqual(a2["a"], b["a"])
        self.assertEqual(a2["b"]["b"], [0, 1, 2, 3, 4, 5])
        self.assertEqual(a2["b"]["c"], a["b"]["c"])
        self.assertEqual(a2["b"]["d"], b["b"]["d"])

        a3 = TT.multi_load(g_path)

        self.assertEqual(a3["name"], a["name"])
        self.assertEqual(a3["a"], b["a"])
        self.assertEqual(a3["b"]["b"], b["b"]["b"])
        self.assertEqual(a3["b"]["c"], a["b"]["c"])
        self.assertEqual(a3["b"]["d"], b["b"]["d"])

        a4 = TT.multi_load([a_path, b_path], ac_merge=TT.MS_REPLACE)

        self.assertEqual(a4["name"], a["name"])
        self.assertEqual(a4["a"], b["a"])
        self.assertEqual(a4["b"]["b"], b["b"]["b"])
        self.assertFalse("c" in a4["b"])
        self.assertEqual(a4["b"]["d"], b["b"]["d"])

        a5 = TT.multi_load([a_path, b_path], ac_merge=TT.MS_NO_REPLACE)

        self.assertEqual(a5["name"], a["name"])
        self.assertEqual(a5["a"], a["a"])
        self.assertEqual(a5["b"]["b"], a["b"]["b"])
        self.assertEqual(a5["b"]["c"], a["b"]["c"])
        self.assertFalse("d" in a5["b"])

    def test_14_multi_load__wrong_merge_strategy(self):
        try:
            TT.multi_load("/dummy/*.json", ac_merge="merge_st_not_exist")
            raise RuntimeError("Wrong merge strategy was not handled!")
        except ValueError:
            self.assertTrue(1 == 1)  # To suppress warn of pylint.

    def test_15_multi_load__empty_path_list(self):
        self.assertEqual(TT.multi_load([]), TT.to_container())

    def test_16_dump_and_multi_load__mixed_file_types(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.yml")

        TT.dump(a, a_path)
        TT.dump(b, b_path)

        cnf = TT.multi_load([a_path, b_path])

        self.assertEqual(cnf["name"], a["name"])
        self.assertEqual(cnf["a"], b["a"])
        self.assertEqual(cnf["b"]["b"], b["b"]["b"])
        self.assertEqual(cnf["b"]["c"], a["b"]["c"])
        self.assertEqual(cnf["b"]["d"], b["b"]["d"])

    def test_18_dump_and_multi_load__namedtuple(self):
        a = convert_to(dict(a=1, b=dict(b=[0, 1], c="C"), name="a"),
                       ac_namedtuple=True)
        b = convert_to(dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D")),
                       ac_namedtuple=True)

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.yml")

        TT.dump(a, a_path)
        TT.dump(b, b_path)
        cnf = TT.multi_load([a_path, b_path], ac_namedtuple=True)

        self.assertEqual(cnf.name, a.name)
        self.assertEqual(cnf.a, b.a)
        self.assertEqual(cnf.b.b, b.b.b)
        self.assertEqual(cnf.b.c, a.b.c)
        self.assertEqual(cnf.b.d, b.b.d)

    def test_20_dump_and_multi_load__to_from_stream(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        TT.dump(a, open(a_path, 'w'))
        TT.dump(b, open(b_path, 'w'))
        self.assertTrue(os.path.exists(a_path))
        self.assertTrue(os.path.exists(b_path))

        cnf = TT.multi_load([open(a_path), open(b_path)])

        self.assertEqual(cnf["name"], a["name"])
        self.assertEqual(cnf["a"], b["a"])
        self.assertEqual(cnf["b"]["b"], b["b"]["b"])
        self.assertEqual(cnf["b"]["c"], a["b"]["c"])
        self.assertEqual(cnf["b"]["d"], b["b"]["d"])

    def test_30_multi_load__ignore_missing(self):
        null_cntnr = TT.to_container()
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        self.assertEqual(TT.multi_load([cpath], ac_parser="ini",
                                       ignore_missing=True),
                         null_cntnr)

    def test_40_multi_load__templates(self):
        if not anyconfig.template.SUPPORTED:
            return

        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        ma = TT.to_container(a, ac_merge=TT.MS_DICTS)
        ma.update(b)

        a_path = os.path.join(self.workdir, "a.yml")
        b_path = os.path.join(self.workdir, "b.yml")
        g_path = os.path.join(self.workdir, "*.yml")

        open(a_path, 'w').write(CNF_TMPL_1)
        open(b_path, 'w').write(CNF_TMPL_2)

        a0 = TT.multi_load(g_path, ac_merge=TT.MS_DICTS, ac_template=True,
                           ac_context=ma)
        a02 = TT.multi_load([g_path, b_path], ac_merge=TT.MS_DICTS,
                            ac_template=True, ac_context=ma)

        self.assertEqual(a0["name"], a["name"])
        self.assertEqual(a0["a"], b["a"])
        self.assertEqual(a0["b"]["b"], b["b"]["b"])
        self.assertEqual(a0["b"]["c"], a["b"]["c"])
        self.assertEqual(a0["b"]["d"], b["b"]["d"])

        self.assertEqual(a02["name"], a["name"])
        self.assertEqual(a02["a"], b["a"])
        self.assertEqual(a02["b"]["b"], b["b"]["b"])
        self.assertEqual(a02["b"]["c"], a["b"]["c"])
        self.assertEqual(a02["b"]["d"], b["b"]["d"])


class Test_50_load_and_dump(unittest.TestCase):

    cnf = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_30_dump_and_load(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        TT.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        TT.dump(b, b_path)
        self.assertTrue(os.path.exists(b_path))

        a1 = TT.load(a_path)

        self.assertEqual(a1["name"], a["name"])
        self.assertEqual(a1["a"], a["a"])
        self.assertEqual(a1["b"]["b"], a["b"]["b"])
        self.assertEqual(a1["b"]["c"], a["b"]["c"])

        a2 = TT.load(os.path.join(self.workdir, '*.json'))

        self.assertEqual(a2["name"], a["name"])
        self.assertEqual(a2["a"], b["a"])
        self.assertEqual(a2["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEqual(a2["b"]["c"], a["b"]["c"])
        self.assertEqual(a2["b"]["d"], b["b"]["d"])

        a3 = TT.load([a_path, b_path])

        self.assertEqual(a3["name"], a["name"])
        self.assertEqual(a3["a"], b["a"])
        self.assertEqual(a3["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEqual(a3["b"]["c"], a["b"]["c"])
        self.assertEqual(a3["b"]["d"], b["b"]["d"])

    def test_31_dump_and_load__to_from_stream(self):
        cnf = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        cpath = os.path.join(self.workdir, "a.json")

        with open(cpath, 'w') as strm:
            TT.dump(cnf, strm)

        self.assertTrue(os.path.exists(cpath))

        with open(cpath, 'r') as strm:
            cnf1 = TT.load(strm, ac_parser="json")

        self.assertTrue(dicts_equal(cnf, cnf1),
                        "cnf vs. cnf1: %s\n\n%s" % (str(cnf), str(cnf1)))

    def test_32_dump_and_load__w_options(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        TT.dump(a, a_path, indent=2)
        self.assertTrue(os.path.exists(a_path))

        TT.dump(b, b_path, indent=2)
        self.assertTrue(os.path.exists(b_path))

        a1 = TT.load(a_path, parse_int=int)

        self.assertEqual(a1["name"], a["name"])
        self.assertEqual(a1["a"], a["a"])
        self.assertEqual(a1["b"]["b"], a["b"]["b"])
        self.assertEqual(a1["b"]["c"], a["b"]["c"])

        a2 = TT.load(os.path.join(self.workdir, '*.json'), parse_int=int)

        self.assertEqual(a2["name"], a["name"])
        self.assertEqual(a2["a"], b["a"])
        self.assertEqual(a2["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEqual(a2["b"]["c"], a["b"]["c"])
        self.assertEqual(a2["b"]["d"], b["b"]["d"])

        a3 = TT.load([a_path, b_path], parse_int=int)

        self.assertEqual(a3["name"], a["name"])
        self.assertEqual(a3["a"], b["a"])
        self.assertEqual(a3["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEqual(a3["b"]["c"], a["b"]["c"])
        self.assertEqual(a3["b"]["d"], b["b"]["d"])

    def test_34_load__ignore_missing(self):
        null_cntnr = TT.to_container()
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        self.assertEqual(TT.load([cpath], ac_parser="ini",
                                 ignore_missing=True),
                         null_cntnr)

    def test_36_load_w_validation(self):
        cnf_path = os.path.join(self.workdir, "cnf.json")
        scm_path = os.path.join(self.workdir, "scm.json")
        TT.dump(CNF_0, cnf_path)
        TT.dump(SCM_0, scm_path)

        cnf_2 = TT.load(cnf_path, ac_context={}, ac_validate=scm_path)

        self.assertEqual(cnf_2["name"], CNF_0["name"])
        self.assertEqual(cnf_2["a"], CNF_0["a"])
        self.assertEqual(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEqual(cnf_2["b"]["c"], CNF_0["b"]["c"])

    def test_38_load_w_validation_yaml(self):
        cnf_path = os.path.join(self.workdir, "cnf.yml")
        scm_path = os.path.join(self.workdir, "scm.yml")
        TT.dump(CNF_0, cnf_path)
        TT.dump(SCM_0, scm_path)

        cnf_2 = TT.load(cnf_path, ac_context={}, ac_validate=scm_path)

        self.assertEqual(cnf_2["name"], CNF_0["name"])
        self.assertEqual(cnf_2["a"], CNF_0["a"])
        self.assertEqual(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEqual(cnf_2["b"]["c"], CNF_0["b"]["c"])

    def test_39_single_load__w_validation(self):
        (cnf, scm) = (CNF_0, SCM_0)
        cpath = os.path.join(self.workdir, "cnf.json")
        spath = os.path.join(self.workdir, "scm.json")

        TT.dump(cnf, cpath)
        TT.dump(scm, spath)

        cnf1 = TT.single_load(cpath, ac_schema=spath)
        self.assertTrue(dicts_equal(cnf, cnf1), str(cnf1))

# vim:sw=4:ts=4:et:
