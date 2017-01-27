#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
#
# pylint: disable=missing-docstring,invalid-name,protected-access
from __future__ import absolute_import
import unittest
import m9dicts.relations as TT


class Test_10_functions(unittest.TestCase):

    def test_10_dict_to_rels_itr__simple(self):
        dic = dict(id=0, a=1, b="b")
        ref = [('ab', (('id', 0), ('a', 1), ('b', 'b')))]
        self.assertEqual(list(TT._dict_to_rels_itr(dic, "ab")), ref)

    def test_12_dict_to_rels_itr__lists(self):
        dic = dict(id=0, a=1, b=[2, 3], c="c")
        id_0 = TT._gen_id('b', 2)
        id_1 = TT._gen_id('b', 3)
        ref = [('ac', (('id', 0), ('a', 1), ('c', 'c'))),
               ('rel_ac_b', (('id', id_0), ('ac', 0), ('b', 2))),
               ('rel_ac_b', (('id', id_1), ('ac', 0), ('b', 3)))]
        self.assertEqual(list(TT._dict_to_rels_itr(dic, "ac")), ref)

    def test_14_dict_to_rels_itr__lists(self):
        dic = dict(id='01', a=1, b=[2, 3], c=["c"])
        id_0 = TT._gen_id('b', 2)
        id_1 = TT._gen_id('b', 3)
        id_2 = TT._gen_id('c', 'c')
        ref = [('A', (('id', '01'), ('a', 1))),
               ('rel_A_b', (('id', id_0), ('A', '01'), ('b', 2))),
               ('rel_A_b', (('id', id_1), ('A', '01'), ('b', 3))),
               ('rel_A_c', (('id', id_2), ('A', '01'), ('c', 'c')))]
        self.assertEqual(list(TT._dict_to_rels_itr(dic, "A")), ref)

    def test_16_dict_to_rels_itr__lists_of_dicts(self):
        dic = dict(id=0, a="AAA",
                   b=[dict(id=0, b=1, c=2), dict(id=1, b=0, c=3)])
        rest = sorted([('b', (('id', 0), ('b', 1), ('c', 2))),
                       ('b', (('id', 1), ('b', 0), ('c', 3))),
                       ('rel_A_b', (('b', 0), ('A', 0))),
                       ('rel_A_b', (('b', 1), ('A', 0)))])

        ref = [('A', (('id', 0), ('a', 'AAA')))] + rest
        res = list(TT._dict_to_rels_itr(dic, "A"))
        self.assertEqual(ref[0], res[0])
        self.assertEqual(sorted(ref[1:]), sorted(res[1:]))

    def test_20_dict_to_rels_itr__gen_id(self):
        dic = dict(a=1)
        oid = TT._gen_id(('a', 1))
        self.assertEqual(list(TT._dict_to_rels_itr(dic, "A")),
                         [('A', (('id', oid), ('a', 1)))])

# vim:sw=4:ts=4:et:
