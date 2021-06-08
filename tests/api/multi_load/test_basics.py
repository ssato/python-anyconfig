#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.api._load as TT

from .common import DIC_0, BaseTestCase


class TestCase(BaseTestCase):

    def test_multi_load_from_empty_path_list(self):
        self.assertEqual(TT.multi_load([]), DIC_0)

    def test_multi_load_from_path_objects(self):
        for rdir, exp, opts in self.datasets:
            res = TT.multi_load(sorted(rdir.glob('*.json')), **opts)
            self.assertEqual(res, exp, f'{rdir!s}')

    def test_multi_load_from_glob_path_str(self):
        for rdir, exp, opts in self.datasets:
            res = TT.multi_load(str(rdir / '*.json'), **opts)
            self.assertEqual(res, exp, f'{rdir!s}')

    def test_multi_load_from_streams(self):
        for rdir, exp, opts in self.datasets:
            paths = sorted(rdir.glob('*.json'))
            res = TT.multi_load((p.open() for p in paths), **opts)
            self.assertEqual(res, exp, f'{rdir!s}')

    def test_multi_load_with_wrong_merge_strategy(self):
        (rdir, _exp, _opts) = self.datasets[0]

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
