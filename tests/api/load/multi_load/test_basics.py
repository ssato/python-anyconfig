#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import pathlib
import unittest

import anyconfig.api._load as TT

from .common import RES_DIR, DIC_0


def datasets_itr():
    for rdir in sorted(pathlib.Path(RES_DIR / 'multi').glob('*')):
        if not rdir.is_dir():
            continue

        exp = TT.single_load(rdir / 'e' / 'exp.json')
        opts = TT.single_load(rdir / 'options' / '00.json')

        yield (rdir, exp, opts)


def gen_datasets():
    datasets = sorted(datasets_itr())
    if not datasets:
        raise RuntimeError('No test data was found!')

    return datasets


class TestCase(unittest.TestCase):

    def test_multi_load_from_empty_path_list(self):
        self.assertEqual(TT.multi_load([]), DIC_0)

    def test_multi_load_from_path_objects(self):
        for rdir, exp, opts in gen_datasets():
            res = TT.multi_load(sorted(rdir.glob('*.json')), **opts)
            self.assertEqual(res, exp, f'{rdir!s}')

    def test_multi_load_from_glob_path_str(self):
        for rdir, exp, opts in gen_datasets():
            res = TT.multi_load(str(rdir / '*.json'), **opts)
            self.assertEqual(res, exp, f'{rdir!s}')

    def test_multi_load_from_streams(self):
        for rdir, exp, opts in gen_datasets():
            paths = sorted(rdir.glob('*.json'))
            res = TT.multi_load((p.open() for p in paths), **opts)
            self.assertEqual(res, exp, f'{rdir!s}')

    def test_multi_load_with_wrong_merge_strategy(self):
        data = gen_datasets()
        (rdir, _exp, _opts) = data[0]

        with self.assertRaises(ValueError):
            TT.multi_load(
                sorted(rdir.glob('*.json')), ac_merge='wrong_merge_strategy'
            )
            raise RuntimeError('Wrong merge strategy was not handled!')

    def test_multi_load_with_ignore_missing_option(self):
        paths = [
            'file_not_exist_0.json',
            'file_not_exist_1.json',
            'file_not_exist_2.json',
        ]
        with self.assertRaises(FileNotFoundError):
            TT.multi_load(paths)

        self.assertEqual(
            TT.multi_load(paths, ac_ignore_missing=True),
            DIC_0
        )

# vim:sw=4:ts=4:et:
