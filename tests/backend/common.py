#
# Copyright (C) 2012 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import copy
import os.path
import unittest

import tests.common
from anyconfig.compat import OrderedDict


CNF_0 = OrderedDict((("DEFAULT", OrderedDict((("a", "0"), ("b", "bbb"),
                                              ("c", "5")))),
                     ("sect0", OrderedDict((("a", "0"), ("b", "bbb"),
                                            ("c", "5"),
                                            ("d", "x,y,z"))))))
CNF_1 = copy.deepcopy(CNF_0)
CNF_1["sect0"]["d"] = CNF_1["sect0"]["d"].split()


class MyDict(OrderedDict):
    pass


class TestBase(unittest.TestCase):

    psr = None

    def setUp(self):
        self.cnf_0 = globals()["CNF_0"]
        self.cnf_1 = globals()["CNF_1"]

        if "TT" in globals():
            self.psr_cls = globals()["TT"].Parser
            self.psr = self.psr_cls()

    def ordered(self):
        return self.psr.ordered()

    def _assert_dicts_equal(self, cnf, ordered=False, cls=None, ref=None):
        if ref is None:
            ref = self.cnf_0
        self.assertTrue(tests.common.dicts_equal(cnf, ref, ordered=ordered),
                        "\n %r\nvs.\n %r" % (cnf, ref))
        if cls is None:
            cls = OrderedDict if self.ordered() else dict
        self.assertTrue(isinstance(cnf, cls),
                        "cnf: %r vs. cls: %r" % (cnf, cls))


class TestBaseWithIO(TestBase):

    cnf_s = None
    cnf_fn = "conf0.ini"

    def setUp(self):
        super(TestBaseWithIO, self).setUp()
        self.workdir = tests.common.setup_workdir()

        if self.psr is not None:
            ext = self.psr.extensions() and self.psr.extensions()[0] or "conf"
            self.cnf_path = os.path.join(self.workdir, "cnf_0" + ext)

            if self.cnf_s is not None:
                with self.psr.wopen(self.cnf_path) as out:
                    out.write(self.cnf_s)

    def tearDown(self):
        tests.common.cleanup_workdir(self.workdir)

# vim:sw=4:ts=4:et:
