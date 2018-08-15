#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import os.path
import unittest

import anyconfig.backends
import anyconfig.backend.ini
import anyconfig.backend.json
import anyconfig.compat
import anyconfig.ioinfo as TT
import anyconfig.utils

from anyconfig.globals import (
    IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
)

import tests.common as TC


IPATH_0 = os.path.join(TC.resdir(), "00-cnf.json")
IPATH_0_FULL = anyconfig.utils.normpath(IPATH_0)


class Test_10_inspect_io_obj(unittest.TestCase):

    def test_10_path_str(self):
        self.assertEqual(TT.inspect_io_obj(IPATH_0),
                         (IOI_PATH_STR, IPATH_0_FULL, open))

    def test_20_stream(self):
        self.assertEqual(TT.inspect_io_obj(open(IPATH_0)),
                         (IOI_STREAM, IPATH_0_FULL,
                          anyconfig.utils.noop))

    def test_30_path_obj(self):
        if anyconfig.compat.pathlib is None:
            return

        ipo = anyconfig.compat.pathlib.Path(IPATH_0)
        self.assertEqual(TT.inspect_io_obj(ipo),
                         (IOI_PATH_OBJ, IPATH_0_FULL, ipo.open))


class Test_30_make(unittest.TestCase):
    (ipath, ipath_full) = (IPATH_0, IPATH_0_FULL)
    prs = anyconfig.backends.PARSERS

    def __init__(self, *args, **kwargs):
        super(Test_30_make, self).__init__(*args, **kwargs)
        self.fun = TT.make

    def __checks_helper(self, inp, *args):
        self.assertEqual(inp.src, args[0])
        self.assertEqual(inp.path, args[1])
        self.assertEqual(inp.type, args[2])
        self.assertTrue(isinstance(inp.processor, args[3]))
        self.assertEqual(inp.opener, args[4])

    def test_20__forced_type(self):
        res = self.fun(None, anyconfig.backends.PARSERS, forced_type="ini")
        self.__checks_helper(res, None, None, None,
                             anyconfig.backend.ini.Parser,
                             anyconfig.utils.noop)

    def test_30__by_fileext(self):
        res = self.fun(self.ipath, self.prs)
        self.__checks_helper(res, self.ipath, self.ipath_full, IOI_PATH_STR,
                             anyconfig.backend.json.Parser, open)

    def test_40__pathlib(self):
        ipath = self.ipath
        if anyconfig.compat.pathlib is not None:
            # Replace w/ pathlib.Path object.
            ipath = anyconfig.compat.pathlib.Path(ipath)
            itype = IOI_PATH_OBJ
            opener = ipath.open
        else:
            itype = IOI_PATH_STR
            opener = open

        res = self.fun(ipath, self.prs)
        self.__checks_helper(res, ipath, self.ipath_full, itype,
                             anyconfig.backend.json.Parser, opener)

    def test_50__stream(self):
        ifo = open(self.ipath)
        res = self.fun(ifo, self.prs)
        self.__checks_helper(res, ifo, self.ipath_full, IOI_STREAM,
                             anyconfig.backend.json.Parser,
                             anyconfig.utils.noop)

# vim:sw=4:ts=4:et:
