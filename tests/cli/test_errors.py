#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main without arguments.
"""
import tempfile

from .. import base
from . import datatypes, test_base


JSON_PATH_0 = str(base.RES_DIR / 'base/basics/10/00.json')


class TestCase(test_base.TestCase):
    kind = 'errors'

    def test_output_option_of_unknown_type(self):
        with tempfile.TemporaryDirectory() as tdir:
            self.run_main(
                [
                    JSON_PATH_0,
                    '-O', 'unknown_parser_type',
                    '-o', f'{tdir}/t.unknown_ext'
                ],
                datatypes.Expected(exit_code_matches=False)
            )

# vim:sw=4:ts=4:et:
