#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
import anyconfig.api as A
import anyconfig.tests.common as C

import anyconfig.backend.ini_ as BINI
import anyconfig.backend.json_ as BJSON
import anyconfig.backend.xml_ as BXML
import anyconfig.backend.yaml_ as BYAML

import os
import os.path
import unittest


class Test_10_pure_functions(unittest.TestCase):

    def test_10_find_loader__w_forced_type(self):
        cpath = "dummy.conf"

        # These parsers should be supported.
        self.assertEquals(A.find_loader(cpath, "ini"), BINI.IniConfigParser)
        self.assertEquals(A.find_loader(cpath, "json"), BJSON.JsonConfigParser)

        if BYAML.SUPPORTED:
            self.assertEquals(A.find_loader(cpath, "yaml"),
                              BYAML.YamlConfigParser)

        if BXML.SUPPORTED:
            self.assertEquals(A.find_loader(cpath, "xml"),
                              BXML.XmlConfigParser)

    def test_20_find_loader__by_file(self):
        self.assertEquals(A.find_loader("dummy.ini"), BINI.IniConfigParser)
        self.assertEquals(A.find_loader("dummy.json"), BJSON.JsonConfigParser)
        self.assertEquals(A.find_loader("dummy.jsn"), BJSON.JsonConfigParser)

        if BYAML.SUPPORTED:
            self.assertEquals(A.find_loader("dummy.yaml"),
                              BYAML.YamlConfigParser)
            self.assertEquals(A.find_loader("dummy.yml"),
                              BYAML.YamlConfigParser)

        if BXML.SUPPORTED:
            self.assertEquals(A.find_loader("dummy.xml"),
                              BXML.XmlConfigParser)

    def test_30_dumps_and_loads(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        a1 = A.loads(A.dumps(a, "json"), "json")

        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_30_dumps_and_loads__w_options(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        a1 = A.loads(A.dumps(a, "json", indent=2), "json", ensure_ascii=False)

        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_40_loads_wo_type(self):
        a = dict(requires=["bash", "zsh"])
        a_s = "requires:bash,zsh"

        a1 = A.loads(a_s)

        self.assertEquals(a1["requires"],   a["requires"])


class Test_20_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_dump_and_single_load(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        a_path = os.path.join(self.workdir, "a.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        a1 = A.single_load(a_path)

        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_20_dump_and_multi_load(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        A.dump(b, b_path)
        self.assertTrue(os.path.exists(b_path))

        a1 = A.multi_load([a_path, b_path], merge=A.MS_DICTS)

        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      b["a"])
        self.assertEquals(a1["b"]["b"], b["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])
        self.assertEquals(a1["b"]["d"], b["b"]["d"])

        a2 = A.multi_load([a_path, b_path], merge=A.MS_DICTS_AND_LISTS)

        self.assertEquals(a2["name"],   a["name"])
        self.assertEquals(a2["a"],      b["a"])
        self.assertEquals(a2["b"]["b"], [0, 1, 2, 3, 4, 5])
        self.assertEquals(a2["b"]["c"], a["b"]["c"])
        self.assertEquals(a2["b"]["d"], b["b"]["d"])

        a3 = A.multi_load(os.path.join(self.workdir, "*.json"))

        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      b["a"])
        self.assertEquals(a1["b"]["b"], b["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])
        self.assertEquals(a1["b"]["d"], b["b"]["d"])

        a4 = A.multi_load([a_path, b_path], merge=A.MS_REPLACE)

        self.assertEquals(a4["name"],   a["name"])
        self.assertEquals(a4["a"],      b["a"])
        self.assertEquals(a4["b"]["b"], b["b"]["b"])
        self.assertFalse("c" in a4["b"])
        self.assertEquals(a4["b"]["d"], b["b"]["d"])

        a5 = A.multi_load([a_path, b_path], merge=A.MS_NO_REPLACE)

        self.assertEquals(a5["name"],   a["name"])
        self.assertEquals(a5["a"],      a["a"])
        self.assertEquals(a5["b"]["b"], a["b"]["b"])
        self.assertEquals(a5["b"]["c"], a["b"]["c"])
        self.assertFalse("d" in a5["b"])

    def test_30_dump_and_load(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        A.dump(b, b_path)
        self.assertTrue(os.path.exists(b_path))

        a1 = A.load(a_path)

        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

        a2 = A.load(os.path.join(self.workdir, '*.json'))

        self.assertEquals(a2["name"],   a["name"])
        self.assertEquals(a2["a"],      b["a"])
        self.assertEquals(a2["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEquals(a2["b"]["c"], a["b"]["c"])
        self.assertEquals(a2["b"]["d"], b["b"]["d"])

        a3 = A.load([a_path, b_path])

        self.assertEquals(a3["name"],   a["name"])
        self.assertEquals(a3["a"],      b["a"])
        self.assertEquals(a3["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEquals(a3["b"]["c"], a["b"]["c"])
        self.assertEquals(a3["b"]["d"], b["b"]["d"])

    def test_30_dump_and_load__w_options(self):
        a = dict(a=1, b=dict(b=[0, 1], c="C"), name="a")
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        A.dump(a, a_path, indent=2)
        self.assertTrue(os.path.exists(a_path))

        A.dump(b, b_path, indent=2)
        self.assertTrue(os.path.exists(b_path))

        a1 = A.load(a_path, parse_int=int)

        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

        a2 = A.load(os.path.join(self.workdir, '*.json'), parse_int=int)

        self.assertEquals(a2["name"],   a["name"])
        self.assertEquals(a2["a"],      b["a"])
        self.assertEquals(a2["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEquals(a2["b"]["c"], a["b"]["c"])
        self.assertEquals(a2["b"]["d"], b["b"]["d"])

        a3 = A.load([a_path, b_path], parse_int=int)

        self.assertEquals(a3["name"],   a["name"])
        self.assertEquals(a3["a"],      b["a"])
        self.assertEquals(a3["b"]["b"], [1, 2, 3, 4, 5])
        self.assertEquals(a3["b"]["c"], a["b"]["c"])
        self.assertEquals(a3["b"]["d"], b["b"]["d"])

# vim:sw=4:ts=4:et:
