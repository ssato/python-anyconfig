#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import os.path
import os
import unittest

import anyconfig.compat
import anyconfig.ioinfo as TT
import anyconfig.utils

from anyconfig.globals import (
    IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
)

import tests.common as TC


IPATH_0 = os.path.join(TC.resdir(), "00-cnf.json")
IPATH_0_FULL = anyconfig.utils.normpath(IPATH_0)
IPATH_0_EXT = anyconfig.utils.get_file_extension(IPATH_0)


class Test_10_inspect_io_obj(unittest.TestCase):

    def test_10_path_str(self):
        self.assertEqual(TT.inspect_io_obj(IPATH_0),
                         (IOI_PATH_STR, IPATH_0_FULL, open, IPATH_0_EXT))

    def test_20_stream(self):
        self.assertEqual(TT.inspect_io_obj(open(IPATH_0)),
                         (IOI_STREAM, IPATH_0_FULL,
                          anyconfig.utils.noop, IPATH_0_EXT))

    def test_22_stream(self):
        stdin = os.fdopen(0)
        res = TT.inspect_io_obj(stdin)
        self.assertEqual(res[0], IOI_STREAM)
        self.assertEqual(res[2], anyconfig.utils.noop)

    def test_30_path_obj(self):
        if anyconfig.compat.pathlib is None:
            return

        ipo = anyconfig.compat.pathlib.Path(IPATH_0)
        self.assertEqual(TT.inspect_io_obj(ipo),
                         (IOI_PATH_OBJ, IPATH_0_FULL, ipo.open, IPATH_0_EXT))


class Test_30_make(unittest.TestCase):
    (ipath, ipath_full) = (IPATH_0, IPATH_0_FULL)

    def __init__(self, *args, **kwargs):
        super(Test_30_make, self).__init__(*args, **kwargs)
        self.fun = TT.make

    def __checks_helper(self, inp, *args):
        self.assertEqual(inp.src, args[0])
        self.assertEqual(inp.path, args[1])
        self.assertEqual(inp.type, args[2])
        self.assertEqual(inp.opener, args[3])
        self.assertEqual(inp.extension, args[4])

    def test_30__by_fileext(self):
        res = self.fun(self.ipath)
        self.__checks_helper(res, self.ipath, self.ipath_full, IOI_PATH_STR,
                             open, IPATH_0_EXT)

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

        res = self.fun(ipath)
        self.__checks_helper(res, ipath, self.ipath_full, itype, opener,
                             IPATH_0_EXT)

    def test_50__stream(self):
        ifo = open(self.ipath)
        res = self.fun(ifo)
        self.__checks_helper(res, ifo, self.ipath_full, IOI_STREAM,
                             anyconfig.utils.noop, IPATH_0_EXT)

# vim:sw=4:ts=4:et:
