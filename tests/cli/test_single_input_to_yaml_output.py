#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""
Test cases of anyconfig.cli.main to load single input with support
using extra libraries.
"""
import unittest

import anyconfig.api
from . import collectors, test_base


class Collector(collectors.Collector):
    kind = 'single_input_to_yaml_output'


@unittest.skipIf('yaml' not in anyconfig.api.list_types(),
                 'loading and dumping yaml support is not available')
class TestCase(test_base.BaseTestCase):
    collector = Collector()

# vim:sw=4:ts=4:et:
