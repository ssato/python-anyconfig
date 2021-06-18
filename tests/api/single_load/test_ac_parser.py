#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
from . import common


class TestCase(common.TestCase):
    kind = 'ac_parser'
    pattern = '*.conf'

# vim:sw=4:ts=4:et:
