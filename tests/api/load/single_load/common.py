#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.parsers

from tests.base import (
    DATA_00, list_resources
)


class BaseTestCase(unittest.TestCase):

    # see: tests/res/json/basic/
    kind = 'basic'

    @property
    def ies(self):
        return (
            (inp, DATA_00[inp])
            for inp in list_resources('json/{self.kind}/*.json')
        )

    @property
    def psr(self):
        return anyconfig.parsers.find(self.ies[0][0], 'json')

# vim:sw=4:ts=4:et:
