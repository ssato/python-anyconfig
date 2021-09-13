#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main with -E or --env option.
"""
from . import test_base


class TestCase(test_base.TestCase):

    def test_show_env_with_long_option(self):
        self.run_main(
            ['--env', '-O', 'json'], test_base.Expected(words_in_stdout='PATH')
        )

    def test_show_env_with_short_option(self):
        self.run_main(
            ['-E', '-O', 'json'], test_base.Expected(words_in_stdout='PATH')
        )

# vim:sw=4:ts=4:et:
