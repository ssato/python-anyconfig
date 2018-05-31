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
import anyconfig.ioobjects as TT
import anyconfig.utils

from anyconfig.backends import (
    _PARSERS_BY_EXT as CPS_BY_EXT,
    _PARSERS_BY_TYPE as CPS_BY_TYPE
)
from anyconfig.globals import UnknownParserTypeError, UnknownFileTypeError


IPATH_0 = os.path.join(os.path.dirname(__file__), "00-cnf.json")
IPATH_0_FULL = anyconfig.utils.normpath(IPATH_0)


class Test_30_inspect_input(unittest.TestCase):

    def test_10_path_str(self):
        self.assertEqual(TT.inspect_input(IPATH_0),
                         (TT.PATH_STR, IPATH_0_FULL, open))

    def test_20_stream(self):
        self.assertEqual(TT.inspect_input(open(IPATH_0)),
                         (TT.STREAM, IPATH_0_FULL,
                          anyconfig.utils.noop))

    def test_30_path_obj(self):
        if anyconfig.compat.pathlib is None:
            return

        ipo = anyconfig.compat.pathlib.Path(IPATH_0)
        self.assertEqual(TT.inspect_input(ipo),
                         (TT.PATH_OBJ, IPATH_0_FULL, ipo.open))


class Test_50_find_parser(unittest.TestCase):
    cpss = (CPS_BY_EXT, CPS_BY_TYPE)
    (ipath, ipath_full) = (IPATH_0, IPATH_0_FULL)

    def __init__(self, *args, **kwargs):
        super(Test_50_find_parser, self).__init__(*args, **kwargs)
        self.fun = TT.find_parser

    def __checks_helper(self, psr, pcls):
        self.assertTrue(isinstance(psr, pcls))

    def test_10__ng_cases(self):
        with self.assertRaises(ValueError):
            self.fun(None, CPS_BY_EXT, CPS_BY_TYPE)

        with self.assertRaises(UnknownParserTypeError):
            self.fun(None, CPS_BY_EXT, CPS_BY_TYPE,
                     forced_type="type_not_exist")
        with self.assertRaises(UnknownFileTypeError):
            self.fun("cnf.unknown_ext", *self.cpss)

    def test_20__forced_type(self):
        res = self.fun(None, CPS_BY_EXT, CPS_BY_TYPE, forced_type="ini")
        self.__checks_helper(res, anyconfig.backend.ini.Parser)

    def test_30__by_fileext(self):
        res = self.fun(self.ipath, *self.cpss)
        self.__checks_helper(res, anyconfig.backend.json.Parser)


class Test_60_make(Test_50_find_parser):

    def __init__(self, *args, **kwargs):
        super(Test_60_make, self).__init__(*args, **kwargs)
        self.fun = TT.make

    def __checks_helper(self, inp, *args):
        self.assertEqual(inp.src, args[0])
        self.assertEqual(inp.path, args[1])
        self.assertEqual(inp.type, args[2])
        self.assertTrue(isinstance(inp.parser, args[3]))
        self.assertEqual(inp.opener, args[4])

    def test_20__forced_type(self):
        res = self.fun(None, CPS_BY_EXT, CPS_BY_TYPE, forced_type="ini")
        self.__checks_helper(res, None, None, None,
                             anyconfig.backend.ini.Parser,
                             anyconfig.utils.noop)

    def test_30__by_fileext(self):
        res = self.fun(self.ipath, *self.cpss)
        self.__checks_helper(res, self.ipath, self.ipath_full, TT.PATH_STR,
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

        res = self.fun(ipath, *self.cpss)
        self.__checks_helper(res, ipath, self.ipath_full, itype,
                             anyconfig.backend.json.Parser, opener)

    def test_50__stream(self):
        ifo = open(self.ipath)
        res = self.fun(ifo, *self.cpss)
        self.__checks_helper(res, ifo, self.ipath_full, TT.STREAM,
                             anyconfig.backend.json.Parser,
                             anyconfig.utils.noop)

# vim:sw=4:ts=4:et:
