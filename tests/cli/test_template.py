#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main with template options.
"""
import unittest

import anyconfig.template

from . import collectors, test_base


class Collector(collectors.Collector):
    kind = 'template'


@unittest.skipIf(not anyconfig.template.SUPPORTED,
                 'Library for template rendering is not available')
class TestCase(test_base.BaseTestCase):
    collector = Collector()


class NoTemplateCollector(collectors.Collector):
    kind = 'no_template'


@unittest.skipIf(anyconfig.template.SUPPORTED,
                 'Library for template rendering is available')
class SchemaErrorsTestCase(test_base.BaseTestCase):
    collector = NoTemplateCollector()

# vim:sw=4:ts=4:et:
