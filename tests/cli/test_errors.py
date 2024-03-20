#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main without arguments and cause errors.
"""
from .. import base
from . import collectors, test_base


class Collector(collectors.Collector):
    kind = 'errors'


class TestCase(test_base.BaseTestCase):
    collector = Collector()

    def make_args(self, tdata):  # pylint: disable=no-self-use
        """Make arguments to run cli.main.
        """
        args = base.load_data(tdata.inp_path, default=[])
        return ['anyconfig_cli'] + tdata.opts + args

# vim:sw=4:ts=4:et:
