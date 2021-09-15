#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main without arguments and cause errors.
"""
from .. import base
from . import test_base


class TestCase(test_base.BaseTestCase):
    kind = 'errors'

    def make_args(self, tdata):  # pylint: disable=no-self-use
        """Make arguments to run cli.main.
        """
        args = base.load_data(tdata.inp_path, default=[])
        return ['anyconfig_cli'] + tdata.opts + args

# vim:sw=4:ts=4:et:
