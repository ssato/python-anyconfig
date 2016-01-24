#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, protected-access
from __future__ import absolute_import

import m9dicts
import os.path
import unittest

import anyconfig.backend.ini as TT
import anyconfig.tests.common

from anyconfig.compat import OrderedDict as ODict
from anyconfig.tests.common import dicts_equal


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


def keys_recur_itr(ndic):
    """
    :param ndic: Nested dict[-like] object
    """
    for key in ndic.keys():
        yield key
        if m9dicts.is_dict_like(ndic[key]):
            for nkey in keys_recur_itr(ndic[key]):
                yield nkey


def list_keys_recur(ndic):
    """
    :param ndic: Nested dict[-like] object
    :return: A list of keys of maybe nested dict[-like] object `ndic`.
    """
    return list(keys_recur_itr(ndic))


class Test00(unittest.TestCase):

    def test_list_keys_recur(self):
        self.assertEqual(list_keys_recur(CNF_0),
                         ['DEFAULT', 'a', 'b', 'c',
                          'sect0', 'a', 'b', 'c', 'd'])


class Test10(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S
    load_options = dict(allow_no_value=False, defaults=None)
    dump_options = dict()
    is_order_kept = True

    def setUp(self):
        self.psr = TT.Parser()

    def test_10_loads(self):
        cnf = self.psr.loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_12_loads__w_options(self):
        cnf = self.psr.loads(self.cnf_s, **self.load_options)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_20_dumps(self):
        cnf_s = self.psr.dumps(self.cnf)
        self.assertTrue(cnf_s)
        cnf = self.psr.loads(cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_22_dumps__w_options(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf, **self.dump_options))
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_30_loads_with_order_kept(self):
        cnf = self.psr.loads(self.cnf_s, ac_ordered=True)
        if self.is_order_kept:
            self.assertTrue(list_keys_recur(cnf), list_keys_recur(self.cnf))
        else:
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))


class Test11(Test10):

    cnf = CNF_1

    def test_10_loads(self):
        cnf = self.psr.loads(self.cnf_s, ac_parse_value=True)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_12_loads__w_options(self):
        cnf = self.psr.loads(self.cnf_s, ac_parse_value=True,
                             **self.load_options)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_20_dumps(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf), ac_parse_value=True)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_22_dumps__w_options(self):
        cnf = self.psr.loads(self.psr.dumps(self.cnf, **self.dump_options),
                             ac_parse_value=True)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))


class Test12(Test10):

    test_10_loads = test_12_loads__w_options = lambda: True
    test_20_loads = test_22_loads__w_options = lambda: True

    def test_12_loads__invalid_input(self):
        invalid_ini = "key=name"
        self.assertRaises(Exception, self.psr.loads, invalid_ini)


class Test20(unittest.TestCase):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = CNF_0_S
    cnf_fn = "conf0.ini"
    is_order_kept = True

    def setUp(self):
        self.psr = self.psr_cls()
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, self.cnf_fn)
        with self.psr.wopen(self.cpath) as out:
            out.write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_load(self):
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_20_dump(self):
        self.psr.dump(self.cnf, self.cpath)
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_30_load__from_stream(self):
        with self.psr.ropen(self.cpath) as strm:
            cnf = self.psr.load(strm)

        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_40_dump__to_stream(self):
        with self.psr.wopen(self.cpath) as strm:
            self.psr.dump(self.cnf, strm)

        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
        self.assertTrue(isinstance(cnf, m9dicts.UpdateWithReplaceDict))

    def test_50_load_with_order_kept(self):
        cnf = self.psr.load(self.cpath, ac_ordered=True)
        if self.is_order_kept:
            self.assertTrue(list(cnf.keys()), list(self.cnf.keys()))
        else:
            self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
