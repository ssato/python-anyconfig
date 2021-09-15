#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main without arguments to show info.
"""
import anyconfig.api

from . import datatypes, test_base


class TestCase(test_base.NoOutputDataTestCase):
    kind = 'show'

    def test_show_vesion(self):
        ver = '.'.join(anyconfig.api.version())
        self.run_main(
            ['--version'], datatypes.Expected(words_in_stdout=ver)
        )

# vim:sw=4:ts=4:et:
