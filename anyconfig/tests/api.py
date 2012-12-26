#
# Copyright (C) 2012 Satoru SATOH <ssato at redhat.com>
#
import anyconfig.api as A
import anyconfig.Bunch as B
import anyconfig.tests.common as C

import anyconfig.backend.ini_ as BINI
import anyconfig.backend.json_ as BJSON
import anyconfig.backend.xml_ as BXML
import anyconfig.backend.yaml_ as BYAML
import anyconfig.backend.properties_ as BPROP

import os
import os.path
import unittest


class Test_10_pure_functions(unittest.TestCase):

    def test_10_find_parser__w_forced_type(self):
        cpath = "dummy.conf"

        # These parsers should be supported.
        self.assertEquals(A.find_parser(cpath, "ini"), BINI.IniConfigParser)
        self.assertEquals(A.find_parser(cpath, "json"), BJSON.JsonConfigParser)

        if BYAML.SUPPORTED:
            self.assertEquals(A.find_parser(cpath, "yaml"),
                              BYAML.YamlConfigParser)

        if BXML.SUPPORTED:
            self.assertEquals(A.find_parser(cpath, "xml"),
                              BXML.XmlConfigParser)

        if BPROP.SUPPORTED:
            self.assertEquals(A.find_parser(cpath, "properties"),
                              BPROP.PropertiesParser)

    def test_20_find_parser__by_file(self):
        self.assertEquals(A.find_parser("dummy.ini"), BINI.IniConfigParser)
        self.assertEquals(A.find_parser("dummy.json"), BJSON.JsonConfigParser)
        self.assertEquals(A.find_parser("dummy.jsn"), BJSON.JsonConfigParser)

        if BYAML.SUPPORTED:
            self.assertEquals(A.find_parser("dummy.yaml"),
                              BYAML.YamlConfigParser)
            self.assertEquals(A.find_parser("dummy.yml"),
                              BYAML.YamlConfigParser)

        if BXML.SUPPORTED:
            self.assertEquals(A.find_parser("dummy.xml"),
                              BXML.XmlConfigParser)

        if BPROP.SUPPORTED:
            self.assertEquals(A.find_parser("dummy.properties"),
                              BPROP.PropertiesParser)

    def test_30_dumps_and_loads(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))
        a1 = A.loads(A.dumps(a, "json"), "json")

        # FIXME: Too verbose
        self.assertEquals(a.name, a1.name)
        self.assertEquals(a.a, a1.a)
        self.assertEquals(a.b.b, a1.b.b)
        self.assertEquals(a.b.c, a1.b.c)


class Test_20_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        pass  # C.cleanup_workdir(self.workdir)

    def test_10_dump_and_load(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))

        a_path = os.path.join(self.workdir, "a.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        a1 = A.load(a_path)

        # FIXME: Too verbose
        self.assertEquals(a.name, a1.name)
        self.assertEquals(a.a, a1.a)
        self.assertEquals(a.b.b, a1.b.b)
        self.assertEquals(a.b.c, a1.b.c)

    def test_20_dump_and_mload(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))
        b = B.Bunch(a=2, b=B.Bunch(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        A.dump(b, b_path)
        self.assertTrue(os.path.exists(b_path))

        x = A.mload([a_path, b_path])

        # FIXME: Too verbose
        self.assertEquals(a.name, x.name)
        self.assertEquals(b.a, x.a)
        self.assertEquals(b.b.b, x.b.b)
        self.assertEquals(a.b.c, x.b.c)
        self.assertEquals(b.b.d, x.b.d)

        x = A.mload([a_path, b_path], update=B.ST_MERGE_DICTS_AND_LISTS)

        self.assertEquals(a.name, x.name)
        self.assertEquals(b.a, x.a)
        self.assertEquals([1, 2, 3, 4, 5], x.b.b)
        self.assertEquals(a.b.c, x.b.c)
        self.assertEquals(b.b.d, x.b.d)

    def test_50_mload_metaconf__single_file(self):
        m0_content = '{"topdir": "/tmp"}\n'
        m0_path = os.path.join(self.workdir, "m0.json")

        open(m0_path, 'w').write(m0_content)

        mc = A.mload_metaconf(m0_path)
        self.assertEquals(mc.topdir, "/tmp")

    def test_52_mload_metaconf__dir(self):
        m0_content = '{}\n'
        m1_content = '{"topdir": "/tmp"\n'

        subdir = "metaconf.d"
        confdir = os.path.join(self.workdir, subdir)

        os.makedirs(confdir)

        m0_path = os.path.join(confdir, "m0.json")
        m1_path = os.path.join(confdir, "m1.json")

        open(m0_path, 'w').write(m0_content)
        open(m1_path, 'w').write(m1_content)

        mc = A.mload_metaconf(confdir, conf_exts=".json")
        self.assertEquals(mc.topdir, self.workdir)


# vim:sw=4:ts=4:et:
