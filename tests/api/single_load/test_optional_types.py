#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api

from . import common


LOADER_TYPES = frozenset(anyconfig.api.list_types())


@unittest.skipIf('yaml' not in LOADER_TYPES,
                 'yaml loader is not available')
class YamlTestCase(common.TestCase):
    kind = 'yaml'
    pattern = '*.yml'


@unittest.skipIf('toml' not in LOADER_TYPES,
                 'toml loader is not available')
class TomlTestCase(YamlTestCase):
    kind = 'toml'
    pattern = '*.toml'

# vim:sw=4:ts=4:et:
