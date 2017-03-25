#
# Copyright (C) 2012 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

import copy
import os.path
import unittest

from os import linesep as lsep

import tests.common

from anyconfig.compat import OrderedDict
from tests.common import to_bytes as _bytes


CNF_0 = OrderedDict((("DEFAULT", OrderedDict((("a", "0"), ("b", "bbb"),
                                              ("c", "5")))),
                     ("sect0", OrderedDict((("a", "0"), ("b", "bbb"),
                                            ("c", "5"),
                                            ("d", "x,y,z"))))))
CNF_1 = copy.deepcopy(CNF_0)
CNF_1["sect0"]["d"] = CNF_1["sect0"]["d"].split()

CNF_2 = OrderedDict((("a", 0.1), ("b", _bytes("bbb")),
                     ("sect0", OrderedDict((("c", [_bytes("x"), _bytes("y"),
                                                   _bytes("z")]), )))))


class MyDict(dict):
    pass


class HasParserTrait(object):

    psr = None  # Must be a parser instance.
    cnf_s = None  # Do.
    cnf = cnf_0 = CNF_0
    cnf_1 = CNF_1

    def is_ready(self):
        return self.psr is not None


class TestBase(unittest.TestCase, HasParserTrait):

    def _assert_dicts_equal(self, cnf, ordered=False, cls=None, ref=None):
        if ref is None:
            ref = self.cnf
        self.assertTrue(tests.common.dicts_equal(cnf, ref, ordered=ordered),
                        "%s %r%svs.%s %r" % (lsep, cnf, lsep, lsep, ref))
        # .. note::
        #    `cnf` may not be an instance of `cls` even if ac_dict option was
        #    given because parsers may not allow customize dict class to used
        #    for making results.
        if cls is None or not self.psr.dict_options():
            cls = OrderedDict if ordered else dict
        self.assertTrue(isinstance(cnf, cls),
                        "cnf=%r [type: %r], cls=%r" % (cnf, type(cnf), cls))


class Test_10_dumps_and_loads(TestBase):

    load_options = {}  # Must be set to a dict in children classes.
    dump_options = {}  # Do.
    empty_patterns = ['']  # Do.

    def test_10_loads(self):
        if self.is_ready():
            cnf = self.psr.loads(self.cnf_s)
            self.assertTrue(cnf)  # Check if it's not None nor {}.
            self._assert_dicts_equal(cnf)

    def test_12_loads_with_options(self):
        if self.is_ready():
            cnf = self.psr.loads(self.cnf_s, **self.load_options)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf)

    def test_14_loads_with_invalid_options(self):
        if self.is_ready():
            cnf = self.psr.loads(self.cnf_s, not_exist_option_a=True)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf)

    def test_16_loads_with_ac_ordered_option(self):
        if self.is_ready():
            cnf = self.psr.loads(self.cnf_s, ac_ordered=True)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf, ordered=self.psr.ordered())

    def test_18_loads_with_ac_dict_option(self):
        if self.is_ready():
            cnf = self.psr.loads(self.cnf_s, ac_dict=MyDict)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf, cls=MyDict)
            # for debug:
            # raise RuntimeError("psr=%r, cnf=%r "
            #                    "[%r]" % (self.psr, cnf, type(cnf)))

    def test_20_loads_with_dict_option(self):
        if self.is_ready():
            dopts = self.psr.dict_options()
            if dopts:
                opts = {dopts[0]: MyDict}
                cnf = self.psr.loads(self.cnf_s, **opts)
                self.assertTrue(cnf)
                self._assert_dicts_equal(cnf, cls=MyDict)

    def test_22_loads_empty_data(self):
        if self.is_ready():
            for pat in self.empty_patterns:
                cnf = self.psr.loads(pat)
                self.assertEqual(cnf, dict())

    def test_30_dumps(self):
        if self.is_ready():
            cnf_s = self.psr.dumps(self.cnf)
            self.assertTrue(cnf_s)  # Check if it's not empty.
            cnf = self.psr.loads(cnf_s)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf)

    def test_32_dumps_with_options(self):
        if self.is_ready():
            cnf = self.psr.loads(self.psr.dumps(self.cnf, **self.dump_options))
            self._assert_dicts_equal(cnf)


class TestBaseWithIO(TestBase):

    def setUp(self):
        super(TestBaseWithIO, self).setUp()
        if self.is_ready():
            self.workdir = tests.common.setup_workdir()

            exts = self.psr.extensions()
            ext = exts[0] if exts else "conf"
            self.cnf_path = os.path.join(self.workdir, "cnf_0." + ext)

            with self.psr.wopen(self.cnf_path) as out:
                out.write(self.cnf_s)

    def tearDown(self):
        if self.is_ready():
            tests.common.cleanup_workdir(self.workdir)


class Test_20_dump_and_load(TestBaseWithIO):

    def test_10_load(self):
        if self.is_ready():
            cnf = self.psr.load(self.cnf_path)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf)

    def test_12_load_from_stream(self):
        if self.is_ready():
            with self.psr.ropen(self.cnf_path) as strm:
                cnf = self.psr.load(strm)

            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf)

    def test_14_load_with_ac_ordered_option(self):
        if self.is_ready():
            cnf = self.psr.load(self.cnf_path, ac_ordered=True)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf, ordered=self.psr.ordered())

    def test_16_load_with_ac_dict_option(self):
        if self.is_ready():
            cnf = self.psr.load(self.cnf_path, ac_dict=MyDict)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf, cls=MyDict)

    def test_30_dump(self):
        if self.is_ready():
            self.psr.dump(self.cnf, self.cnf_path)
            cnf = self.psr.load(self.cnf_path)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf)

    def test_32_dump_to_stream(self):
        if self.is_ready():
            with self.psr.wopen(self.cnf_path) as strm:
                self.psr.dump(self.cnf, strm)

            cnf = self.psr.load(self.cnf_path)
            self.assertTrue(cnf)
            self._assert_dicts_equal(cnf)

# vim:sw=4:ts=4:et:
