#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import unittest
import anyconfig.parser as TT


# format: input, expected_result
CASES = dict(single_0=[("", "")],
             single=[("0", 0),
                     ("123", 123),
                     ("True", True),
                     ("a string", "a string"),
                     ("0.1", "0.1"),
                     ("    a string contains extra whitespaces     ",
                      "a string contains extra whitespaces"),
                     ],
             list=[("a,b", ["a", "b"]),
                   ("1,2", [1, 2]),
                   ("a,b,", ["a", "b"]),
                   ],
             attrlist_0=[("requires:bash,zsh",
                          [('requires', ['bash', 'zsh']), ]),
                         ("obsoletes:sysdata;conflicts:sysdata-old",
                          [('obsoletes', 'sysdata'),
                           ('conflicts', 'sysdata-old')]),
                         ],
             path_empty=[("", [])],
             path_single=[("", []), ("a", ['a']), ("/a", ['a']),
                          (".a", ['a']), ("a.", ['a']),
                          ],
             path_multi=[("/a/b/c/d", ['a', 'b', 'c', 'd']),
                         ("a.b.c.d", ['a', 'b', 'c', 'd']),
                         ],
             )


class Test_00_parse(unittest.TestCase):

    testcases = CASES

    def run_cases(self, category, tfunc):
        for inp, exp in self.testcases.get(category, []):
            self.assertEquals(tfunc(inp), exp)

    def test_00_parse_single(self):
        self.run_cases("single_0", TT.parse_single)
        self.run_cases("single", TT.parse_single)

    def test_10_parse_list(self):
        self.run_cases("list", TT.parse_list)

        # A few special cases:
        self.assertEquals(TT.parse_list(""), [])
        self.assertEquals(TT.parse_list("a|b|", "|"), ["a", "b"])

    def test_20_parse_attrlist_0(self):
        self.run_cases("attrlist_0", TT.parse_attrlist_0)

    def test_30_parse(self):
        self.run_cases("single", TT.parse)
        self.run_cases("list", TT.parse)

    def test_50_parse_path__empty(self):
        self.run_cases("path_empty", TT.parse_path)

    def test_52_parse_path__single(self):
        self.run_cases("path_single", TT.parse_path)

    def test_54_parse_path__multi(self):
        self.run_cases("path_multi", TT.parse_path)

# vim:sw=4:ts=4:et:
