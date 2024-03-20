#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.detectors.
"""
import contextlib
import io
import unittest
import warnings

import anyconfig.cli.detectors as TT
import anyconfig.cli.parse_args


class TestCase(unittest.TestCase):

    def test_are_same_file_types(self):
        ies = (([], False),
               (['/tmp/a/b/c.conf'], True),
               (['/tmp/a/b/c.yml', '/tmp/a/b/d.yml'], True),
               )
        for inp, exp in ies:
            (self.assertTrue if exp else self.assertFalse)(
                TT.are_same_file_types(inp)
            )

    def test_find_by_the_type(self):
        ies = (('', None),
               (None, None),
               ('json', 'json'),
               ('type_not_exit', None),
               )
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            for inp, exp in ies:
                self.assertEqual(
                    TT.find_by_the_type(inp), exp
                )

    def test_find_by_the_paths(self):
        ies = (([], None),
               (['/tmp/a/b/c.yml', '/tmp/a/b/d.json'], None),
               (['-'], None),
               (['-', '/tmp/a/b/d.json'], None),
               (['/tmp/a/b/c.json', '/tmp/a/b/d.json'], 'json'),
               )
        for inp, exp in ies:
            self.assertEqual(
                TT.find_by_the_paths(inp), exp
            )

    def test_try_detecting_input_type(self):
        ies = (([], None),
               (['-'], None),
               (['a.conf'], None),
               (['-I', 'json', 'a.conf'], 'json'),
               (['a.json'], 'json'),
               )
        for inp, exp in ies:
            (_psr, args) = anyconfig.cli.parse_args.parse(
                inp, prog='anyconfig_cli'
            )
            self.assertEqual(
                TT.try_detecting_input_type(args), exp, args
            )

    def test_try_detecting_output_type(self):
        ies = ((['-I', 'json', 'a.conf'], 'json'),
               (['a.json'], 'json'),
               (['-I', 'json', 'a.conf', '-o', 'b.conf'], 'json'),
               (['a.json', '-o', 'b.conf'], 'json'),
               (['a.json', '-O', 'json', '-o', 'b.conf'], 'json'),
               )
        for inp, exp in ies:
            (_psr, args) = anyconfig.cli.parse_args.parse(
                inp, prog='anyconfig_cli'
            )
            self.assertEqual(
                TT.try_detecting_output_type(args), exp, args
            )

    def test_try_detecting_output_type__failures(self):
        ies = (['-'],
               ['a.conf'],
               ['a.conf', '-o', 'b.conf'],
               )
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            for inp in ies:
                (_psr, args) = anyconfig.cli.parse_args.parse(
                    inp, prog='anyconfig_cli'
                )
                with self.assertRaises(SystemExit):
                    with contextlib.redirect_stdout(io.StringIO()):
                        with contextlib.redirect_stderr(io.StringIO()):
                            TT.try_detecting_output_type(args)

# vim:sw=4:ts=4:et:
