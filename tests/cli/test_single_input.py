#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main without arguments and cause errors.
"""
from . import collectors, test_base


class Collector(collectors.Collector):
    kind = 'single_input'


class TestCase(test_base.BaseTestCase):
    collector = Collector()

# vim:sw=4:ts=4:et:
