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
import sys
import tempfile
import unittest

import anyconfig.api
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

    def post_checks(self, tdata, *args, **kwargs):
        """Placeholder to do more post checks.
        """
        pass

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

                if tdata.exp.exit_code_matches and tdata.exp.exit_code == 0:
                    self.assertTrue(opath.exists(), str(opath))

                    try:
                        odata = anyconfig.api.load(opath, **tdata.oo_opts)
                    except anyconfig.api.UnknownFileTypeError:
                        odata = anyconfig.api.load(opath, ac_parser='json')
                    self.assertEqual(odata, tdata.ref, repr(tdata))

                    self.post_checks(tdata, opath)
        else:
            # Likewise but without -o <output_path> option.
            TT.main(args)
            self.post_checks(tdata)

        sys.exit(0)

    def run_main(self, tdata) -> None:
        """
        Run anyconfig.cli.main and check if the exit code was expected one.
        """
        expected: datatypes.Expected = tdata.exp

        with self.assertRaises(expected.exception, msg=repr(tdata)) as ctx:
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
            self.assertTrue(expected.words_in_stdout in msg, f'tdata: {tdata!r}, msg: {msg}')

        if expected.words_in_stderr:
            err = stderr.getvalue()
            self.assertTrue(expected.words_in_stderr in err, err)

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
