#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

from ... import base


class BaseTestCase(base.TDataCollector, unittest.TestCase):
    target = 'open'

# vim:sw=4:ts=4:et:
