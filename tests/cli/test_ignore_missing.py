#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main of which input does not exist but ignored.
"""
from . import collectors, test_base


class Collector(collectors.Collector):
    kind = 'ignore_missing'


class TestCase(test_base.BaseTestCase):
    collector = Collector()

    def make_args(self, tdata):  # pylint: disable=no-self-use
        """Make arguments to run cli.main.
        """
        return ['anyconfig_cli'] + tdata.opts + ['file_not_exist.json']

# vim:sw=4:ts=4:et:
