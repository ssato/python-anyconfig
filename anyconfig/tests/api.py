#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import
from logging import CRITICAL

import os
import os.path
import unittest

import anyconfig.api as TT
import anyconfig.tests.common

from anyconfig.tests.common import CNF_0, SCM_0, dicts_equal

import anyconfig.backend.ini
import anyconfig.backend.json
import anyconfig.backend.xml

try:
    import anyconfig.template
    TEMPLATE_SUPPORT = True
except ImportError:
    TEMPLATE_SUPPORT = False

try:
    import anyconfig.backend.yaml as BYAML
except ImportError:
    BYAML = None


class Test10(unittest.TestCase):

    def test_10_find_loader__w_forced_type(self):
        cpath = "dummy.conf"

        # These parsers should work for python >= 2.6.
        self.assertEquals(TT.find_loader(cpath, "ini"),
                          anyconfig.backend.ini.Parser)
        self.assertEquals(TT.find_loader(cpath, "json"),
                          anyconfig.backend.json.Parser)
        self.assertEquals(TT.find_loader(cpath, "xml"),
                          anyconfig.backend.xml.Parser)

        if BYAML is not None:
            self.assertEquals(TT.find_loader(cpath, "yaml"), BYAML.Parser)

    def test_12_find_loader__w_forced_type__none(self):
        TT.set_loglevel(CRITICAL)  # suppress the logging msg "[Error] ..."
        cpath = "dummy.conf"
        self.assertEquals(TT.find_loader(cpath, "type_not_exist"), None)

    def test_20_find_loader__by_file(self):
        self.assertEquals(TT.find_loader("dummy.ini"),
                          anyconfig.backend.ini.Parser)
        self.assertEquals(TT.find_loader("dummy.json"),
                          anyconfig.backend.json.Parser)
        self.assertEquals(TT.find_loader("dummy.jsn"),
                          anyconfig.backend.json.Parser)
        self.assertEquals(TT.find_loader("dummy.xml"),
                          anyconfig.backend.xml.Parser)

        if BYAML is not None:
            self.assertEquals(TT.find_loader("dummy.yaml"), BYAML.Parser)
            self.assertEquals(TT.find_loader("dummy.yml"), BYAML.Parser)

    def test_22_find_loader__by_file__none(self):
        # see self.test_12_find_loader__w_forced_type__none
        TT.set_loglevel(CRITICAL)
        self.assertEquals(TT.find_loader("dummy.ext_not_found"), None)

    def test_30_dumps_and_loads(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        a1 = TT.loads(TT.dumps(a, "json"), "json")

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_30_dumps_and_loads__w_options(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        a1 = TT.loads(TT.dumps(a, "json", indent=2), "json",
                      ensure_ascii=False)

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_32_dumps_and_loads__w_options__no_dumper(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        a1 = TT.loads(TT.dumps(a, "type_not_exist"), "json")

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_40_loads_wo_type(self):
        a = dict(requires=["bash", "zsh"])
        a_s = "requires:bash,zsh"

        a1 = TT.loads(a_s)
        self.assertEquals(a1["requires"], a["requires"])

    def test_42_loads_w_type_not_exist(self):
        a = dict(requires=["bash", "zsh"])
        a_s = "requires:bash,zsh"

        a1 = TT.loads(a_s, "type_not_exist")
        self.assertEquals(a1["requires"], a["requires"])

    def test_44_loads_w_type__template(self):
        if not TEMPLATE_SUPPORT:
            return

        a = dict(requires=["bash", "zsh"])
        a_s = "requires: [{{ requires|join(', ') }}]"
        context = dict(requires=["bash", "zsh"], )

        a1 = TT.loads(a_s, forced_type="yaml", ac_template=True,
                      ac_context=context)

        self.assertEquals(a1["requires"], a["requires"])

    def test_46_loads_w_type__broken_template(self):
        if not TEMPLATE_SUPPORT:
            return

        a = dict(requires="{% }}", )
        a_s = 'requires: "{% }}"'
        a1 = TT.loads(a_s, forced_type="yaml", ac_template=True,
                      ac_context={})

        self.assertEquals(a1["requires"], a["requires"])

    def test_48_loads_w_validation(self):
        cnf_s = TT.dumps(CNF_0, "json")
        scm_s = TT.dumps(SCM_0, "json")
        cnf_2 = TT.loads(cnf_s, forced_type="json", ac_context={},
                         ac_validate=scm_s)

        self.assertEquals(cnf_2["name"], CNF_0["name"])
        self.assertEquals(cnf_2["a"], CNF_0["a"])
        self.assertEquals(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEquals(cnf_2["b"]["c"], CNF_0["b"]["c"])

    def test_49_loads_w_validation_error(self):
        cnf_s = """{"a": "aaa"}"""
        scm_s = TT.dumps(SCM_0, "json")
        cnf_2 = TT.loads(cnf_s, forced_type="json", ac_schema=scm_s)
        self.assertTrue(cnf_2 is None, cnf_2)


class Test20(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_dump_and_single_load(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        a_path = os.path.join(self.workdir, "a.json")

        TT.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        a1 = TT.single_load(a_path)

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_12_dump_and_single_load__no_parser(self):
        self.assertEquals(TT.single_load("dummy.ext_not_exist"), None)

    def test_14_single_load__ignore_missing(self):
        null_cntnr = TT.container()
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        self.assertEquals(TT.single_load(cpath, "ini", ignore_missing=True),
                          null_cntnr)

    def test_16_single_load__template(self):
        if not TEMPLATE_SUPPORT:
            return

        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        a_path = os.path.join(self.workdir, "a.yaml")

        open(a_path, 'w').write("""name: {{ name|default('a') }}
a: {{ a }}
b:
    b:
      {% for x in b.b -%}
      - {{ x }}
      {% endfor %}
    c: {{ b.c }}
""")

        a1 = TT.single_load(a_path, ac_template=True, ac_context=a)

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_18_single_load__templates(self):
        if not TEMPLATE_SUPPORT:
            return

        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        a_path = os.path.join(self.workdir, "a.yml")
        b_path = os.path.join(self.workdir, "b.yml")
        a2_path = os.path.join(self.workdir, "x/y/z", "a.yml")

        open(a_path, 'w').write("{% include 'b.yml' %}")
        open(b_path, 'w').write("""name: {{ name|default('a') }}
a: {{ a }}
b:
    b:
      {% for x in b.b -%}
      - {{ x }}
      {% endfor %}
    c: {{ b.c }}
""")
        os.makedirs(os.path.dirname(a2_path))
        open(a2_path, 'w').write("a: 'xyz'")

        a1 = TT.single_load(a_path, ac_template=True, ac_context=a)

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

        a2 = TT.single_load(a2_path, ac_template=True)
        self.assertEquals(a2["a"], "xyz")

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

    def test_20_dump_and_multi_load(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")
        g_path = os.path.join(self.workdir, "*.json")

        TT.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        TT.dump(b, b_path)
        self.assertTrue(os.path.exists(b_path))

        a0 = TT.multi_load(g_path, merge=TT.MS_DICTS)
        a02 = TT.multi_load([g_path, b_path], merge=TT.MS_DICTS)

        self.assertEquals(a0["name"], a["name"])
        self.assertEquals(a0["a"], b["a"])
        self.assertEquals(a0["b"]["b"], b["b"]["b"])
        self.assertEquals(a0["b"]["c"], a["b"]["c"])
        self.assertEquals(a0["b"]["d"], b["b"]["d"])

        self.assertEquals(a02["name"], a["name"])
        self.assertEquals(a02["a"], b["a"])
        self.assertEquals(a02["b"]["b"], b["b"]["b"])
        self.assertEquals(a02["b"]["c"], a["b"]["c"])
        self.assertEquals(a02["b"]["d"], b["b"]["d"])

        a1 = TT.multi_load([a_path, b_path], merge=TT.MS_DICTS)

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], b["a"])
        self.assertEquals(a1["b"]["b"], b["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])
        self.assertEquals(a1["b"]["d"], b["b"]["d"])

        a2 = TT.multi_load([a_path, b_path], merge=TT.MS_DICTS_AND_LISTS)

        self.assertEquals(a2["name"], a["name"])
        self.assertEquals(a2["a"], b["a"])
        self.assertEquals(a2["b"]["b"], [0, 1, 2, 3, 4, 5])
        self.assertEquals(a2["b"]["c"], a["b"]["c"])
        self.assertEquals(a2["b"]["d"], b["b"]["d"])

        a3 = TT.multi_load(os.path.join(self.workdir, "*.json"))

        self.assertEquals(a3["name"], a["name"])
        self.assertEquals(a3["a"], b["a"])
        self.assertEquals(a3["b"]["b"], b["b"]["b"])
        self.assertEquals(a3["b"]["c"], a["b"]["c"])
        self.assertEquals(a3["b"]["d"], b["b"]["d"])

        a4 = TT.multi_load([a_path, b_path], merge=TT.MS_REPLACE)

        self.assertEquals(a4["name"], a["name"])
        self.assertEquals(a4["a"], b["a"])
        self.assertEquals(a4["b"]["b"], b["b"]["b"])
        self.assertFalse("c" in a4["b"])
        self.assertEquals(a4["b"]["d"], b["b"]["d"])

        a5 = TT.multi_load([a_path, b_path], merge=TT.MS_NO_REPLACE)

        self.assertEquals(a5["name"], a["name"])
        self.assertEquals(a5["a"], a["a"])
        self.assertEquals(a5["b"]["b"], a["b"]["b"])
        self.assertEquals(a5["b"]["c"], a["b"]["c"])
        self.assertFalse("d" in a5["b"])

    def test_22_multi_load__ignore_missing(self):
        null_cntnr = TT.container()
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        self.assertEquals(TT.multi_load([cpath], forced_type="ini",
                                        ignore_missing=True),
                          null_cntnr)

    def test_24_multi_load__templates(self):
        if not TEMPLATE_SUPPORT:
            return

        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        ma = TT.container.create(a)
        ma.update(b, TT.MS_DICTS)

        a_path = os.path.join(self.workdir, "a.yml")
        b_path = os.path.join(self.workdir, "b.yml")
        g_path = os.path.join(self.workdir, "*.yml")

        open(a_path, 'w').write("""\
a: {{ a }}
b:
    b:
        {% for x in b.b -%}
        - {{ x }}
        {% endfor %}
    c: {{ b.c }}

name: {{ name }}
""")
        open(b_path, 'w').write("""\
a: {{ a }}
b:
    b:
        {% for x in b.b -%}
        - {{ x }}
        {% endfor %}
    d: {{ b.d }}
""")

        a0 = TT.multi_load(g_path, merge=TT.MS_DICTS, ac_template=True,
                           ac_context=ma)
        a02 = TT.multi_load([g_path, b_path], merge=TT.MS_DICTS,
                            ac_template=True, ac_context=ma)

        self.assertEquals(a0["name"], a["name"])
        self.assertEquals(a0["a"], b["a"])
        self.assertEquals(a0["b"]["b"], b["b"]["b"])
        self.assertEquals(a0["b"]["c"], a["b"]["c"])
        self.assertEquals(a0["b"]["d"], b["b"]["d"])

        self.assertEquals(a02["name"], a["name"])
        self.assertEquals(a02["a"], b["a"])
        self.assertEquals(a02["b"]["b"], b["b"]["b"])
        self.assertEquals(a02["b"]["c"], a["b"]["c"])
        self.assertEquals(a02["b"]["d"], b["b"]["d"])

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

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

        a2 = TT.load(os.path.join(self.workdir, '*.json'))

        self.assertEquals(a2["name"], a["name"])
        self.assertEquals(a2["a"], b["a"])
        self.assertEquals(a2["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEquals(a2["b"]["c"], a["b"]["c"])
        self.assertEquals(a2["b"]["d"], b["b"]["d"])

        a3 = TT.load([a_path, b_path])

        self.assertEquals(a3["name"], a["name"])
        self.assertEquals(a3["a"], b["a"])
        self.assertEquals(a3["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEquals(a3["b"]["c"], a["b"]["c"])
        self.assertEquals(a3["b"]["d"], b["b"]["d"])

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

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

        a2 = TT.load(os.path.join(self.workdir, '*.json'), parse_int=int)

        self.assertEquals(a2["name"], a["name"])
        self.assertEquals(a2["a"], b["a"])
        self.assertEquals(a2["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEquals(a2["b"]["c"], a["b"]["c"])
        self.assertEquals(a2["b"]["d"], b["b"]["d"])

        a3 = TT.load([a_path, b_path], parse_int=int)

        self.assertEquals(a3["name"], a["name"])
        self.assertEquals(a3["a"], b["a"])
        self.assertEquals(a3["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEquals(a3["b"]["c"], a["b"]["c"])
        self.assertEquals(a3["b"]["d"], b["b"]["d"])

    def test_34_load__ignore_missing(self):
        null_cntnr = TT.container()
        cpath = os.path.join(os.curdir, "conf_file_should_not_exist")
        assert not os.path.exists(cpath)

        self.assertEquals(TT.load([cpath], forced_type="ini",
                                  ignore_missing=True),
                          null_cntnr)

    def test_36_load_w_validation(self):
        cnf_path = os.path.join(self.workdir, "cnf.json")
        scm_path = os.path.join(self.workdir, "scm.json")
        TT.dump(CNF_0, cnf_path)
        TT.dump(SCM_0, scm_path)

        cnf_2 = TT.load(cnf_path, ac_context={}, ac_validate=scm_path)

        self.assertEquals(cnf_2["name"], CNF_0["name"])
        self.assertEquals(cnf_2["a"], CNF_0["a"])
        self.assertEquals(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEquals(cnf_2["b"]["c"], CNF_0["b"]["c"])

    def test_38_load_w_validation_yaml(self):
        cnf_path = os.path.join(self.workdir, "cnf.yml")
        scm_path = os.path.join(self.workdir, "scm.yml")
        TT.dump(CNF_0, cnf_path)
        TT.dump(SCM_0, scm_path)

        cnf_2 = TT.load(cnf_path, ac_context={}, ac_validate=scm_path)

        self.assertEquals(cnf_2["name"], CNF_0["name"])
        self.assertEquals(cnf_2["a"], CNF_0["a"])
        self.assertEquals(cnf_2["b"]["b"], CNF_0["b"]["b"])
        self.assertEquals(cnf_2["b"]["c"], CNF_0["b"]["c"])

    def test_50_validate(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        a_path = os.path.join(self.workdir, "a.json")

        TT.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        a1 = TT.single_load(a_path)

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

# vim:sw=4:ts=4:et:
