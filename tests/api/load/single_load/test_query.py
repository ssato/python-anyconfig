#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.api._load as TT

from .common import BaseTestCase


class TestCase(BaseTestCase):

    kind = 'query'

    def test_single_load(self):
        iqes = (
            (inp,
             # see: tests/res/json/basic/query/q/
             inp.parent / 'q' / inp.name.replace('.json', '.txt'),
             # see: tests/res/json/basic/query/e/
             inp.parent / 'e' / inp.name
             )
            for inp, _exp in self.ies
        )
        for inp, query_path, exp_path in iqes:
            query = query_path.read_text().strip()
            exp = TT.single_load(exp_path)
            self.assertEqual(TT.single_load(inp, ac_query=query), exp)

    def test_single_load_with_wrong_queries(self):
        for inp, exp in self.ies:
            self.assertEqual(TT.single_load(inp, ac_query=None), exp)


# vim:sw=4:ts=4:et:
