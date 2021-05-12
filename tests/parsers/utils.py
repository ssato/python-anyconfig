#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, no-member
import unittest

import anyconfig.parsers.parsers
import anyconfig.parsers.utils as TT
import anyconfig.processors.utils

from anyconfig.common import (
    UnknownFileTypeError, UnknownProcessorTypeError
)


class Test_10_find(unittest.TestCase):

    psrs = anyconfig.parsers.parsers.Parsers().list()

    def _assert_isinstances(self, obj, clss, msg=False):
        self.assertTrue(any(isinstance(obj, cls) for cls in clss),
                        msg or "%r vs %r" % (obj, clss))

    def test_10_find__w_parser_type_or_instance(self):
        def _findall_by_type(typ):
            fnc = anyconfig.processors.utils.findall_with_pred
            return fnc(lambda p: typ == p.type(), self.psrs)

        cpath = "dummy.conf"
        for psr in self.psrs:
            ldrs = _findall_by_type(psr.type())
            self._assert_isinstances(TT.find(cpath, psr.type()), ldrs)
            self._assert_isinstances(TT.find(cpath, psr()), ldrs)

    def test_20_find__w_parser_by_file(self):
        def _find_ldrs_by_ext(ext):
            fnc = anyconfig.processors.utils.findall_with_pred
            return fnc(lambda p: ext in p.extensions(), self.psrs)

        for psr in self.psrs:
            for ext in psr.extensions():
                ldrs = _find_ldrs_by_ext(ext)
                self._assert_isinstances(TT.find("dummy." + ext), ldrs)

    def test_30_find__unknown_parser_type(self):
        self.assertRaises(UnknownProcessorTypeError,
                          TT.find, "a.cnf", "type_not_exist")

    def test_40_find__unknown_file_type(self):
        self.assertRaises(UnknownFileTypeError,
                          TT.find, "dummy.ext_not_found")

# vim:sw=4:ts=4:et:
