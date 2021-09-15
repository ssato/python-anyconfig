#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases for anyconfig.cli module.
"""
import contextlib
import io
import pathlib
import tempfile
import unittest

import anyconfig.cli as TT

from .. import base
from . import collectors, datatypes


def make_args(_self, tdata):
    """Make arguments to run cli.main.
    """
    return ['anyconfig_cli'] + tdata.opts + [str(tdata.inp_path)]


class BaseTestCase(unittest.TestCase):
    """Base Test case.
    """
    collector = collectors.Collector()
    make_args = make_args

    def setUp(self):
        if self.collector:
            self.collector.init()

    def _run_main(self, tdata):
        """Wrapper for cli.main."""
        args = self.make_args(tdata)

        if tdata.outname:  # Running cli.main will output files.
            self.assertTrue(
                tdata.ref is not None,
                'No reference data was given, {tdata!r}'
            )
            with tempfile.TemporaryDirectory() as tdir:
                opath = pathlib.Path(tdir) / tdata.outname

                # Run anyconfig.cli.main with arguments.
                TT.main(args + ['-o', str(opath)])

                odata = base.load_data(opath, should_exist=True)
                self.assertEqual(odata, tdata.ref)
        else:
            # Likewise but without -o <output_path> option.
            TT.main(args)

    def run_main(self, tdata) -> None:
        """
        Run anyconfig.cli.main and check if the exit code was expected one.
        """
        expected: datatypes.Expected = tdata.exp

        with self.assertRaises(expected.exception) as ctx:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                with contextlib.redirect_stderr(io.StringIO()) as stderr:
                    self._run_main(tdata)

        exc = ctx.exception
        self.assertTrue(isinstance(exc, expected.exception))
        ecode = getattr(exc, 'error_code', getattr(exc, 'code', 1))
        if expected.exit_code_matches:
            self.assertEqual(ecode, expected.exit_code, f'{tdata!r}')
        else:
            self.assertNotEqual(ecode, expected.exit_code, f'{tdata!r}')

        if expected.words_in_stdout:
            msg = stdout.getvalue()
            self.assertTrue(expected.words_in_stdout in msg, msg)

        if expected.words_in_stderr:
            msg = stderr.getvalue()
            self.assertTrue(expected.words_in_stderr in msg, msg)

    def test_runs_for_datasets(self) -> None:
        if self.collector and self.collector.initialized:
            if self.collector.kind == base.TDataCollector.kind:
                return

            for tdata in self.collector.each_data():
                self.run_main(tdata)


class NoInputTestCase(BaseTestCase):
    """Test cases which does not require inputs.
    """
    def make_args(self, tdata):  # pylint: disable=no-self-use
        """Make arguments to run cli.main.
        """
        return ['anyconfig_cli'] + tdata.opts

# vim:sw=4:ts=4:et:
