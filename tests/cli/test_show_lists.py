#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main to show list of parsers.
"""
from . import test_base


class TestCase(test_base.TestCase):

    def test_show_lists_with_short_option(self):
        self.run_main(['-L'], words_in_stdout='json')

    def test_show_lists_with_long_option(self):
        self.run_main(['--list'], words_in_stdout='ini')

# vim:sw=4:ts=4:et:
