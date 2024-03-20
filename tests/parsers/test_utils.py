#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
import operator
import unittest

import anyconfig.parsers.utils as TT

from anyconfig.common import (
    UnknownFileTypeError, UnknownProcessorTypeError
)
from anyconfig.backend.json import PARSERS as JSON_PSR_CLSS
from anyconfig.parsers.parsers import Parsers


PSRS = Parsers().list()
JSON_PSRS = sorted(
    (p() for p in JSON_PSR_CLSS),
    key=operator.methodcaller("priority"), reverse=True
)


class TestCase(unittest.TestCase):

    def test_load_plugins(self):
        TT.load_plugins()
        self.assertTrue(PSRS)

    def test_list_types(self):
        res = TT.list_types()
        self.assertTrue(bool(res))
        self.assertTrue(any(x in res for x in ("json", "ini", "xml")))

    def test_list_by_x(self):
        for lfn in (TT.list_by_cid, TT.list_by_type, TT.list_by_extension):
            psrs = lfn()
            self.assertTrue(bool(psrs))

    def test_findall_ng_cases(self):
        ies = (((None, None), ValueError),  # w/o path nor type
               (("/tmp/x.xyz", None), UnknownFileTypeError),
               (("/dev/null", None), UnknownFileTypeError),
               ((None, "xyz"), UnknownProcessorTypeError),
               )
        for inp, exc in ies:
            with self.assertRaises(exc):
                TT.findall(*inp)

    def test_findall(self):
        argss = (("foo.json", None),
                 (None, "json"),
                 )
        for args in argss:
            psrs = TT.findall(*args)

            self.assertTrue(bool(psrs))
            self.assertEqual(psrs, JSON_PSRS)

    def test_find(self):
        argss = (("foo.json", None),
                 (None, "json"),
                 (None, JSON_PSR_CLSS[0]),
                 (None, JSON_PSRS[0]),
                 )
        for args in argss:
            psr = TT.find(*args)
            self.assertEqual(psr, JSON_PSRS[0])

# vim:sw=4:ts=4:et:
