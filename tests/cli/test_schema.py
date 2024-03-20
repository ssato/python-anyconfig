#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main with schema options.
"""
import unittest
import warnings

import anyconfig.schema

from . import collectors, test_base


ERR = 'Library for JSON schema validation is not available'


class Collector(collectors.Collector):
    kind = 'schema'


@unittest.skipIf(not anyconfig.schema.SUPPORTED, ERR)
class TestCase(test_base.BaseTestCase):
    collector = Collector()

    def make_args(self, tdata):  # pylint: disable=no-self-use
        """Make arguments to run cli.main.
        """
        return [
            'anyconfig_cli', '--validate', '--schema', str(tdata.scm),
            str(tdata.inp_path), *tdata.opts
        ]

    def _run_main(self, tdata):
        """Override it to suppress some warnings.
        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            super()._run_main(tdata)


class SchemaErrorsCollector(collectors.Collector):
    kind = 'schema_errors'


@unittest.skipIf(not anyconfig.schema.SUPPORTED, ERR)
class SchemaErrorsTestCase(test_base.BaseTestCase):
    collector = SchemaErrorsCollector()

# vim:sw=4:ts=4:et:
