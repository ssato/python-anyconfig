#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
from . import common


class TestCase(common.TestCase):
    kind = 'mixed_types'
    pattern = '*.*'

# vim:sw=4:ts=4:et:
