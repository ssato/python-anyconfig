#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2024 Satoru SATOH <satoru.satoh gmail.com>
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import annotations

import anyconfig.dicts as TT

from .. import base
from . import common


class TestCase(common.TestCase):
    kind = 'get'

    def test_get(self):
        for data in self.each_data():
            emsg = base.load_data(data.scm)  # diversion.
            (res, err) = TT.get(data.inp, data.query)

            if emsg:
                self.assertTrue(bool(err), data)
            else:  # emsg = ''
                self.assertEqual(err, '', data)

            self.assertEqual(res, data.exp, data)
