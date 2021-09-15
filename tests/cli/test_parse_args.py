#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, too-many-public-methods
"""test cases of anyconfig.cli.main without arguments.
"""
import unittest

import anyconfig.cli.parse_args as TT


class TestCase(unittest.TestCase):

    def test_make_parser(self):
        psr = TT.make_parser()
        self.assertTrue(
            isinstance(psr, TT.argparse.ArgumentParser)
        )

        # ref = TT.DEFAULTS.copy()
        ref = dict(
            args=None, atype=None, env=False, extra_opts=None,
            gen_schema=False, get=None, ignore_missing=False, inputs=[],
            itype=None, list=False, loglevel=0, merge='merge_dicts',
            otype=None, output=None, query=None, schema=None, set=None,
            template=False, validate=False
        )
        self.assertEqual(
            vars(psr.parse_args([])), ref
        )

# vim:sw=4:ts=4:et:
