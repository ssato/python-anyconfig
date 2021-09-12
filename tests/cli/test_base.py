#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, too-many-public-methods
"""test cases for anyconfig.cli module.
"""
import contextlib
import io
import typing
import unittest

import anyconfig.cli as TT


def _run(*args: typing.Iterable[str]) -> None:
    """Run anyconfig.cli.main.
    """
    TT.main(['dummy'] + [str(a) for a in args])


class TestCase(unittest.TestCase):

    def run_main(self,
                 args: typing.Optional[typing.Iterable[str]] = None,
                 ref_code: int = 0,
                 expected: bool = True,
                 words_in_stdout: typing.Optional[str] = None,
                 words_in_stderr: typing.Optional[str] = None,
                 exc_cls=SystemExit
                 ) -> None:
        """
        Run anyconfig.cli.main and check if the exit code was expected one.
        """
        if args is None:
            args = []

        with self.assertRaises(exc_cls) as ctx:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                with contextlib.redirect_stderr(io.StringIO()) as stderr:
                    _run(*args)

        exc = ctx.exception
        self.assertTrue(isinstance(exc, exc_cls))
        ecode = getattr(exc, 'error_code', getattr(exc, 'code', 1))
        (self.assertEqual if expected else self.assertNotEqual)(
            ecode, ref_code
        )
        if words_in_stdout:
            self.assertTrue(words_in_stdout in stdout.getvalue())
        if words_in_stderr:
            self.assertTrue(words_in_stderr in stderr.getvalue())

# vim:sw=4:ts=4:et:
