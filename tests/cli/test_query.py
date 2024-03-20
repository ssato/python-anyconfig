#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main to query using JMESPath expression.
"""
import unittest

import anyconfig.query

from . import collectors, test_base


class Collector(collectors.Collector):
    kind = 'query'


@unittest.skipIf(not anyconfig.query.SUPPORTED,
                 'Library to query using JMESPath is not available')
class TestCase(test_base.BaseTestCase):
    collector = Collector()

# vim:sw=4:ts=4:et:
