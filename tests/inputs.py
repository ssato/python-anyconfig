#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.backend.ini
import anyconfig.backend.json
import anyconfig.inputs as TT
import anyconfig.utils

from anyconfig.backends import (
    _PARSERS_BY_EXT as CPS_BY_EXT,
    _PARSERS_BY_TYPE as CPS_BY_TYPE
)
from anyconfig.globals import UnknownParserTypeError, UnknownFileTypeError


class Test(unittest.TestCase):
    cpss = (CPS_BY_EXT, CPS_BY_TYPE)

    def test_50_make__ng_cases(self):
        self.assertRaises(ValueError, TT.make, None, *self.cpss)
        self.assertRaises(UnknownParserTypeError,
                          TT.make, None, CPS_BY_EXT, CPS_BY_TYPE,
                          forced_type="type_not_exist")
        self.assertRaises(UnknownFileTypeError,
                          TT.make, "cnf.unknown_ext", *self.cpss)

    def test_52_make__forced_type(self):
        inp = TT.make(None, CPS_BY_EXT, CPS_BY_TYPE, forced_type="ini")

        self.assertEqual(inp.src, None)
        self.assertEqual(inp.path, None)
        self.assertEqual(inp.type, None)
        self.assertTrue(isinstance(inp.parser, anyconfig.backend.ini.Parser))
        self.assertEqual(inp.opener, anyconfig.utils.noop)

    def test_53_make__by_fileext(self):
        ipath = "/a/b/c.json"
        inp = TT.make(ipath, *self.cpss)

        self.assertEqual(inp.src, ipath)
        self.assertEqual(inp.path, ipath)
        self.assertEqual(inp.type, TT.PATH_STR)
        self.assertTrue(isinstance(inp.parser, anyconfig.backend.json.Parser))
        self.assertEqual(inp.opener, open)

    def test_54_make__pathlib(self):
        ipath = ipath_0 = "/a/b/c.json"
        if TT.pathlib is not None:
            ipath = TT.pathlib.Path(ipath)  # Replace w/ pathlib.Path object.
            itype = TT.PATH_OBJ
            opener = ipath.open
        else:
            itype = TT.PATH_STR
            opener = open

        inp = TT.make(ipath, *self.cpss)

        self.assertEqual(inp.src, ipath)
        self.assertEqual(inp.path, ipath_0)
        self.assertEqual(inp.type, itype)
        self.assertTrue(isinstance(inp.parser, anyconfig.backend.json.Parser))
        self.assertEqual(inp.opener, opener)

# vim:sw=4:ts=4:et:
