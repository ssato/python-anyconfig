#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT

from tests.base import list_resources


def inp_exp_itr(ftype=None, fext=None):
    if ftype is None or not ftype:
        return

    if fext is None or not fext:
        fext = ftype

    for inp in list_resources(f'{ftype}/*.{fext}'):
        # see: tests/res/ini/e/ for example
        yield (
            inp,
            inp.parent / 'e' / inp.name.replace(f'.{fext}', '.json')
        )


class TestCase(unittest.TestCase):

    def helper(self, ftype, fext=None, ordred=True, force_type=False):
        for inp, exp_path in inp_exp_itr(ftype=ftype, fext=fext):
            exp = TT.single_load(exp_path, ac_ordered=ordred)

            if force_type:
                res = TT.single_load(inp, ac_parser=ftype)
            else:
                res = TT.single_load(inp)

            self.assertEqual(res, exp)

    def test_single_load_ini(self):
        self.helper('ini')

    def test_single_load_properties(self):
        self.helper('properties')

    def test_single_load_shellvars(self):
        self.helper('shellvars', fext='sh', force_type=True)

    def test_single_load_xml(self):
        self.helper('xml')

# vim:sw=4:ts=4:et:
