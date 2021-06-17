#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api._load as TT
import anyconfig.api

from . import common


LOADER_TYPES = frozenset(anyconfig.api.list_types())


@unittest.skipIf('yaml' not in LOADER_TYPES,
                 'yaml loader is not available')
class YamlTestCase(common.BaseTestCase):
    kind = 'yaml'
    pattern = '*.yml'

    def test_single_load(self):
        for data in self.each_data():
            self.assertEqual(
                TT.single_load(data.inp_path, **data.opts),
                data.exp,
                data
            )

    def test_single_load_intentional_failures(self):
        for data in self.each_data():
            with self.assertRaises(AssertionError):
                self.assertEqual(
                    TT.single_load(data.inp_path, **data.opts),
                    None
                )


@unittest.skipIf('toml' not in LOADER_TYPES,
                 'toml loader is not available')
class TomlTestCase(YamlTestCase):
    kind = 'toml'
    pattern = '*.toml'

# vim:sw=4:ts=4:et:
