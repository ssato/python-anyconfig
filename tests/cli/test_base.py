#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases for anyconfig.cli module.
"""
import contextlib
import io
import typing
import unittest

import anyconfig.cli as TT

from . import collectors, datatypes


def _run(*args: typing.Iterable[str]) -> None:
    """Run anyconfig.cli.main.
    """
    TT.main(['dummy'] + [str(a) for a in args])


class TestCase(unittest.TestCase, collectors.Collector):

    def setUp(self):
        self.init()

    def run_main(self,
                 args: typing.Optional[typing.Iterable[str]] = None,
                 expected: datatypes.Expected = datatypes.Expected()
                 ) -> None:
        """
        Run anyconfig.cli.main and check if the exit code was expected one.
        """
        with self.assertRaises(expected.exception) as ctx:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                with contextlib.redirect_stderr(io.StringIO()) as stderr:
                    _run(*args)

        exc = ctx.exception
        self.assertTrue(isinstance(exc, expected.exception))
        ecode = getattr(exc, 'error_code', getattr(exc, 'code', 1))
        if expected.exit_code_matches:
            self.assertEqual(ecode, expected.exit_code)
        else:
            self.assertNotEqual(ecode, expected.exit_code)

        if expected.words_in_stdout:
            msg = stdout.getvalue()
            self.assertTrue(expected.words_in_stdout in msg, msg)

        if expected.words_in_stderr:
            msg = stderr.getvalue()
            self.assertTrue(expected.words_in_stderr in msg, msg)

    def test_runs_for_datasets(self) -> None:
        for tdata in self.each_data():
            self.run_main(tdata.args, tdata.exp)

# vim:sw=4:ts=4:et:
