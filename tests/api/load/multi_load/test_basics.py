#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import pathlib
import unittest

import anyconfig.api._load as TT

from .common import RES_DIR


def datasets_itr():
    for rdir in pathlib.Path(RES_DIR / 'multi').glob('*'):
        if not rdir.is_dir():
            continue

        exp = TT.single_load(rdir / 'e' / 'exp.json')
        opts = TT.single_load(rdir / 'options' / '00.json')

        yield (rdir, exp, opts)


def gen_datasets():
    datasets = datasets_itr()
    if not datasets:
        raise RuntimeError('No test data was found!')

    return datasets


class TestCase(unittest.TestCase):

    def test_multi_load_from_path_objects(self):
        for rdir, exp, opts in gen_datasets():
            res = TT.multi_load(rdir.glob('*.*'), **opts)
            self.assertEqual(res, exp)

    def test_multi_load_from_glob_path_str(self):
        for rdir, exp, opts in gen_datasets():
            res = TT.multi_load(str(rdir / '*.*'), **opts)
            self.assertEqual(res, exp)

# vim:sw=4:ts=4:et:
