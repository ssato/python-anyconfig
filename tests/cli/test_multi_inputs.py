#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main with multiple inputs.
"""
from . import collectors, test_base


class Collector(collectors.MultiDataCollector):
    kind = 'multi_inputs'


class TestCase(test_base.BaseTestCase):
    collector = Collector()

    def make_args(self, tdata):  # pylint: disable=no-self-use
        """Make arguments to run cli.main.
        """
        return ['anyconfig_cli'] + tdata.opts + [str(p) for p in tdata.inputs]

# vim:sw=4:ts=4:et:
