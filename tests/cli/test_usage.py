#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, too-many-public-methods
"""test cases of anyconfig.cli.main without arguments.
"""
import tempfile

from .. import base
from . import test_base


JSON_PATH_0 = str(base.RES_DIR / 'base/basics/10/00.json')


class TestCase(test_base.TestCase):

    def test_help_option(self):
        self.run_main(['--help'])

    def test_no_arguments(self):
        self.run_main(expected=False)

    def test_wrong_options(self):
        self.run_main(['--wrong-option-xyz'], expected=False)

    def test_input_argument_of_unknown_type(self):
        self.run_main([__file__], expected=False)

    def test_input_type_option_of_unknown_type(self):
        self.run_main([__file__, '-I', 'unknown_parser'], expected=False)

    def test_input_argument_of_unknown_type_and_no_output_type_option(self):
        self.run_main([__file__, __file__ + '.un_ext'], expected=False)

    def test_output_argument_of_unknown_type(self):
        with tempfile.TemporaryDirectory() as tdir:
            self.run_main(
                [JSON_PATH_0, '-o', f'{tdir}/t.unknown_ext'], expected=False
            )

    def test_output_option_of_unknown_type(self):
        with tempfile.TemporaryDirectory() as tdir:
            self.run_main(
                [JSON_PATH_0, '-O', 'unknown_parser_type', '-o',
                 f'{tdir}/t.unknown_ext'],
                expected=False
            )

# vim:sw=4:ts=4:et:
