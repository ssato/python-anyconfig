#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main without arguments to show info.
"""
import anyconfig.api

from . import test_base


class TestCase(test_base.TestCase):

    def test_show_vesion(self):
        ver = '.'.join(anyconfig.api.version())
        self.run_main(
            ['--version'], test_base.Expected(words_in_stdout=ver)
        )

    def test_show_help_with_short_option(self):
        self.run_main(
            ['-h'], test_base.Expected(words_in_stdout='usage: ')
        )

    def test_show_help_with_long_option(self):
        self.run_main(
            ['--help'], test_base.Expected(words_in_stdout='usage: ')
        )

    def test_show_lists_with_short_option(self):
        self.run_main(
            ['-L'], test_base.Expected(words_in_stdout='json')
        )

    def test_show_lists_with_long_option(self):
        self.run_main(
            ['--list'], test_base.Expected(words_in_stdout='ini')
        )

# vim:sw=4:ts=4:et:
