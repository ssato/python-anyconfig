#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, too-many-public-methods

import pathlib
import shutil
import tempfile
import unittest

import anyconfig.cli as TT
import anyconfig.api
import anyconfig.query
import anyconfig.schema
import anyconfig.template
import tests.common
import tests.api


CNF_0_PATH = tests.common.respath('00-cnf.yml')


def _run(*args):
    return TT.main(["dummy"] + [str(a) for a in args])


class RunTestBase(unittest.TestCase):

    def run_and_check_exit_code(self, args=None, code=0, _not=False,
                                exc_cls=SystemExit):
        if args is None:
            args = []
        try:
            _run(*args)
        except exc_cls as exc:
            ecode = getattr(exc, "code", 1)
            (self.assertNotEqual if _not else self.assertEqual)(ecode, code)


class RunTestWithTmpdir(RunTestBase):
    def setUp(self):
        self.tmpdir = pathlib.Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(str(self.tmpdir))


class Test_20_Base(RunTestBase):

    def setUp(self):
        self.workdir = pathlib.Path(tests.common.setup_workdir())

    def tearDown(self):
        tests.common.cleanup_workdir(str(self.workdir))

    def _assert_run_and_exit(self, *args):
        self.assertRaises(SystemExit, _run, *args)


class Test_30_single_input(Test_20_Base):

    def test_52_wo_schema(self):
        self.run_and_check_exit_code(["--validate", CNF_0_PATH], 1)

    def test_70_no_template(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        infile = self.workdir / "a.json"
        output = self.workdir / "b.json"

        anyconfig.api.dump(a, infile)
        self.assertTrue(infile.exists())

        _run("-o", output, infile)
        self.assertTrue(output.exists())

    def test_80_w_extra_opts(self):
        infile = tests.common.respath('00-00-cnf.json')
        output = self.workdir / "out.json"
        ref = tests.common.respath('00-00-cnf_indented.json')

        _run("-o", output, "--extra-opts", "indent:2", infile)
        self.assertTrue(output.exists())
        self.assertEqual(output.read_text().strip().rstrip(),
                         open(ref).read().strip().rstrip())


class Test_40_multi_inputs(Test_20_Base):

    def test_10(self):
        xs = [dict(a=1, ),
              dict(b=dict(b=[1, 2], c="C")), ]

        a = xs[0].copy()
        a.update(xs[1])

        output = self.workdir / "b.json"

        inputs = []
        for i in [0, 1]:
            infile = self.workdir / "a{!s}.json".format(i)
            inputs.append(infile)

            anyconfig.api.dump(xs[i], infile)
            self.assertTrue(infile.exists())

        _run("-o", output, *inputs)
        self.assertTrue(output.exists())

    @unittest.skipIf(not anyconfig.template.SUPPORTED,
                     "jinja2 is not available")
    def test_20_w_template(self):
        infile = tests.common.respath('30-00-template-cnf.json')
        output = self.workdir / "output.json"

        _run("--template", "-o", output, infile)
        self.assertTrue(output.exists())

    @unittest.skipIf(not anyconfig.template.SUPPORTED,
                     "jinja2 is not available")
    def test_30_w_template(self):
        infile = tests.common.respath('30-*-template-cnf.json')
        output = self.workdir / "output.json"

        _run("--template", "-o", output, infile)
        self.assertTrue(output.exists())

# vim:sw=4:ts=4:et:
