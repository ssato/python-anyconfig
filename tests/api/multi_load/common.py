#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common utility functions.
"""
import unittest

from . import collector


class BaseTestCase(collector.DataCollector, unittest.TestCase):
    pass

# vim:sw=4:ts=4:et:
