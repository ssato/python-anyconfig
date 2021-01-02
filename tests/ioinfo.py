#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import os
import pathlib
import unittest

import anyconfig.ioinfo as TT
import anyconfig.utils

from anyconfig.globals import (
    IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM, IOI_NONE
)

import tests.common as TC


IPATH_0 = TC.respath('00-cnf.json')
IPATH_0_FULL = str(pathlib.Path(IPATH_0).expanduser().resolve())
IPATH_0_EXT = anyconfig.utils.get_file_extension(IPATH_0)


class Test_00(unittest.TestCase):

    def test_10_guess_io_type(self):
        this = pathlib.Path(__file__)

        self.assertEqual(TT.guess_io_type(None), IOI_NONE)
        self.assertEqual(TT.guess_io_type(str(this)), IOI_PATH_STR)
        self.assertEqual(TT.guess_io_type(this), IOI_PATH_OBJ)

        with this.open() as fio:
            self.assertEqual(TT.guess_io_type(fio), IOI_STREAM)

        with self.assertRaises(ValueError):
            TT.guess_io_type(0)


class Test_10_inspect_io_obj(unittest.TestCase):

    def test_20_stream(self):
        self.assertEqual(TT.inspect_io_obj(open(IPATH_0), IOI_STREAM),
                         (IPATH_0_FULL, IPATH_0_EXT))

    def test_22_stream(self):
        stdin = os.fdopen(0)
        res = TT.inspect_io_obj(stdin, IOI_STREAM)
        self.assertEqual(res[0], None)
        self.assertEqual(res[1], None)

    def test_30_path_obj(self):
        ipo = pathlib.Path(IPATH_0)
        self.assertEqual(TT.inspect_io_obj(ipo, IOI_PATH_OBJ),
                         (IPATH_0_FULL, IPATH_0_EXT))


class Test_30_make(unittest.TestCase):
    (ipath, ipath_full) = (IPATH_0, IPATH_0_FULL)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fun = TT.make

    def __checks_helper(self, inp, *args):
        self.assertEqual(inp.src, args[0])
        self.assertEqual(inp.path, args[1])
        self.assertEqual(inp.type, args[2])
        self.assertEqual(inp.extension, args[3])

    def test_30__by_fileext(self):
        res = self.fun(self.ipath)
        ipath = pathlib.Path(self.ipath)
        self.__checks_helper(res, ipath, self.ipath_full, IOI_PATH_OBJ,
                             IPATH_0_EXT)

    def test_40__pathlib(self):
        ipath = self.ipath
        # Replace w/ pathlib.Path object.
        ipath = pathlib.Path(ipath)
        itype = IOI_PATH_OBJ

        res = self.fun(ipath)
        self.__checks_helper(res, ipath, self.ipath_full, itype, IPATH_0_EXT)

    def test_50__stream(self):
        ifo = open(self.ipath)
        res = self.fun(ifo)
        self.__checks_helper(res, ifo, self.ipath_full, IOI_STREAM,
                             IPATH_0_EXT)

# vim:sw=4:ts=4:et:
