#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import os.path
import unittest

import anyconfig.backend.ini
import anyconfig.backend.json
import anyconfig.compat
import anyconfig.inputs as TT
import anyconfig.utils

from anyconfig.backends import (
    _PARSERS_BY_EXT as CPS_BY_EXT,
    _PARSERS_BY_TYPE as CPS_BY_TYPE
)
from anyconfig.globals import UnknownParserTypeError, UnknownFileTypeError


IPATH_0 = os.path.join(os.path.dirname(__file__), "00-cnf.json")
IPATH_0_FULL = anyconfig.utils.normpath(IPATH_0)


class Test_60_make(unittest.TestCase):
    cpss = (CPS_BY_EXT, CPS_BY_TYPE)
    (ipath, ipath_full) = (IPATH_0, IPATH_0_FULL)

    def __checks_helper(self, inp, *args):
        self.assertEqual(inp.src, args[0])
        self.assertEqual(inp.path, args[1])
        self.assertEqual(inp.type, args[2])
        self.assertTrue(isinstance(inp.parser, args[3]))
        self.assertEqual(inp.opener, args[4])

    def test_10__ng_cases(self):
        self.assertRaises(ValueError, TT.make, None, *self.cpss)
        self.assertRaises(UnknownParserTypeError,
                          TT.make, None, CPS_BY_EXT, CPS_BY_TYPE,
                          forced_type="type_not_exist")
        self.assertRaises(UnknownFileTypeError,
                          TT.make, "cnf.unknown_ext", *self.cpss)

    def test_20__forced_type(self):
        inp = TT.make(None, CPS_BY_EXT, CPS_BY_TYPE, forced_type="ini")
        self.__checks_helper(inp, None, None, None,
                             anyconfig.backend.ini.Parser,
                             anyconfig.utils.noop)

    def test_30__by_fileext(self):
        inp = TT.make(self.ipath, *self.cpss)
        self.__checks_helper(inp, self.ipath, self.ipath_full, TT.PATH_STR,
                             anyconfig.backend.json.Parser, open)

    def test_40__pathlib(self):
        ipath = self.ipath
        if anyconfig.compat.pathlib is not None:
            # Replace w/ pathlib.Path object.
            ipath = anyconfig.compat.pathlib.Path(ipath)
            itype = TT.PATH_OBJ
            opener = ipath.open
        else:
            itype = TT.PATH_STR
            opener = open

        inp = TT.make(ipath, *self.cpss)
        self.__checks_helper(inp, ipath, self.ipath_full, itype,
                             anyconfig.backend.json.Parser, opener)

    def test_50__stream(self):
        ifo = open(self.ipath)
        inp = TT.make(ifo, *self.cpss)
        self.__checks_helper(inp, ifo, self.ipath_full, TT.STREAM,
                             anyconfig.backend.json.Parser,
                             anyconfig.utils.noop)

# vim:sw=4:ts=4:et:
