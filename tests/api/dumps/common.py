#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import unittest

from ... import base


class BaseTestCase(base.TDataCollector, unittest.TestCase):
    target = 'dumps'

# vim:sw=4:ts=4:et:
