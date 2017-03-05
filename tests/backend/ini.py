#
# Copyright (C) 2012 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, protected-access
from __future__ import absolute_import

import os.path
import unittest

import anyconfig.backend.ini as TT
import tests.common

from anyconfig.compat import OrderedDict as ODict


CNF_0_S = """[DEFAULT]
a: 0
b: bbb
c: 5

[sect0]
d: x,y,z
"""

CNF_0 = ODict((("DEFAULT", ODict((("a", "0"), ("b", "bbb"), ("c", "5")))),
               ("sect0", ODict((("a", "0"), ("b", "bbb"), ("c", "5"),
                                ("d", "x,y,z"))))))
CNF_1 = ODict((("DEFAULT", ODict((("a", 0), ("b", "bbb"), ("c", 5)))),
               ("sect0", ODict((("a", 0), ("b", "bbb"), ("c", 5),
                                ("d", "x y z".split()))))))


class MyDict(ODict):
    pass


class TestBase(unittest.TestCase):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = CNF_0_S

    def setUp(self):
        self.psr = self.psr_cls()

    def ordered(self):
        return self.psr.ordered()

    def _assert_dicts_equal(self, cnf, ordered=False, ccls=dict, ref=False):
        if not ref:
            ref = self.cnf
        self.assertTrue(tests.common.dicts_equal(cnf, ref, ordered=ordered),
                        "\n %r\nvs.\n %r" % (cnf, ref))
        cls = ODict if self.ordered() and ordered else ccls
        self.assertTrue(isinstance(cnf, cls))


class Test10(TestBase):

    load_options = dict(allow_no_value=False, defaults=None)
    dump_options = dict()

    def test_10_loads(self):
        cnf = self.psr.loads(self.cnf_s)
        self._assert_dicts_equal(cnf)

    def test_12_loads__w_options(self):
        cnf = self.psr.loads(self.cnf_s, **self.load_options)
        self._assert_dicts_equal(cnf)

    def test_20_dumps(self):
        cnf_s = self.psr.dumps(self.cnf)
        self.assertTrue(cnf_s)
        cnf = self.psr.loads(cnf_s)
        self._assert_dicts_equal(cnf)

    def test_22_dumps__w_options(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf, **self.dump_options))
        self._assert_dicts_equal(cnf)

    def test_30_loads_with_order_kept(self):
        cnf = self.psr.loads(self.cnf_s, ac_ordered=True)
        self._assert_dicts_equal(cnf, ordered=self.ordered())


class Test11(Test10):

    cnf = CNF_1

    def test_10_loads(self):
        cnf = self.psr.loads(self.cnf_s, ac_parse_value=True)
        self._assert_dicts_equal(cnf)

    def test_12_loads__w_options(self):
        cnf = self.psr.loads(self.cnf_s, ac_parse_value=True,
                             **self.load_options)
        self._assert_dicts_equal(cnf)

    def test_14_loads__w_dict_factory(self):
        cnf = self.psr.loads(self.cnf_s, dict_type=MyDict)
        self._assert_dicts_equal(cnf, ccls=MyDict, ref=CNF_0)

    def test_15_loads__w_ac_dict_option(self):
        cnf = self.psr.loads(self.cnf_s, ac_dict=MyDict)
        self._assert_dicts_equal(cnf, ccls=MyDict, ref=CNF_0)

    def test_16_loads__w_dict_factory(self):
        if self.cnf:
            return  # FIXME.
        cnf = self.psr.loads(self.cnf_s, dict_type=MyDict, ac_parse_value=True)
        self._assert_dicts_equal(cnf, ccls=MyDict)

    def test_20_dumps(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf), ac_parse_value=True)
        self._assert_dicts_equal(cnf)

    def test_22_dumps__w_options(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf, **self.dump_options),
                             ac_parse_value=True)
        self._assert_dicts_equal(cnf)

    def test_30_loads_with_order_kept(self):
        cnf = self.psr.loads(self.cnf_s, ac_parse_value=True, ac_ordered=True)
        self._assert_dicts_equal(cnf, ordered=self.ordered())

    def test_32_loads_with_order_kept(self):
        cnf = self.psr.loads(self.cnf_s, ac_parse_value=True, dict_type=ODict)
        self._assert_dicts_equal(cnf, ordered=True)


class Test12(Test10):

    test_10_loads = test_12_loads__w_options = lambda: True
    test_20_loads = test_22_loads__w_options = lambda: True

    def test_10_loads__invalid_input(self):
        invalid_ini = "key=name"
        self.assertRaises(Exception, self.psr.loads, invalid_ini)

    def test_20_dumps__format(self):
        ref = self.cnf_s.replace(': ', ' = ')
        self.assertEqual(self.psr.dumps(self.cnf), ref)


class Test20(TestBase):

    cnf_fn = "conf0.ini"

    def setUp(self):
        self.psr = self.psr_cls()
        self.workdir = tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, self.cnf_fn)
        with self.psr.wopen(self.cpath) as out:
            out.write(self.cnf_s)

    def tearDown(self):
        tests.common.cleanup_workdir(self.workdir)

    def _assert_dicts_equal(self, cnf, ordered=False, instance_check=False,
                            ref=False):
        if not ref:
            ref = self.cnf
        self.assertTrue(tests.common.dicts_equal(cnf, ref),
                        "\n %r\nvs.\n %r" % (cnf, ref))
        if instance_check:
            cls = ODict if self.ordered() and ordered else dict
            self.assertTrue(isinstance(cnf, cls))

    def test_10_load(self):
        cnf = self.psr.load(self.cpath)
        self._assert_dicts_equal(cnf)

    def test_20_dump(self):
        self.psr.dump(self.cnf, self.cpath)
        cnf = self.psr.load(self.cpath)
        self._assert_dicts_equal(cnf)

    def test_30_load__from_stream(self):
        with self.psr.ropen(self.cpath) as strm:
            cnf = self.psr.load(strm)

        self._assert_dicts_equal(cnf)

    def test_40_dump__to_stream(self):
        with self.psr.wopen(self.cpath) as strm:
            self.psr.dump(self.cnf, strm)

        cnf = self.psr.load(self.cpath)
        self._assert_dicts_equal(cnf)

    def test_50_load_with_order_kept(self):
        cnf = self.psr.load(self.cpath, ac_ordered=True)
        if self.ordered():
            self.assertTrue(list(cnf.keys()), list(self.cnf.keys()))
        else:
            self.assertTrue(tests.common.dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
