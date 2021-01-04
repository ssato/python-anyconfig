#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, too-many-public-methods
from __future__ import absolute_import

import os
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

from tests.common import CNF_0


CNF_0_PATH = tests.common.respath('00-cnf.yml')


def _run(*args):
    return TT.main(["dummy"] + [str(a) for a in args])


class Test_00(unittest.TestCase):
    """

    >>> psr = TT.make_parser()
    >>> assert isinstance(psr, TT.argparse.ArgumentParser)
    >>> args = psr.parse_args([])
    >>> ref = dict(args=None, atype=None, env=False, extra_opts=None,
    ...            gen_schema=False, get=None, ignore_missing=False, inputs=[],
    ...            itype=None, list=False, loglevel=0, merge='merge_dicts',
    ...            otype=None, output=None, query=None, schema=None, set=None,
    ...            template=False, validate=False)
    >>> assert vars(args) == ref
    """


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


class Test_10(RunTestBase):
    infile = tests.common.respath('00-cnf.json')

    def test_10_show_usage(self):
        self.run_and_check_exit_code(["--help"])

    def test_20_wo_args(self):
        self.run_and_check_exit_code(_not=True)

    def test_30_wrong_option(self):
        self.run_and_check_exit_code(["--wrong-option-xyz"], _not=True)

    def test_40_list(self):
        self.run_and_check_exit_code(["--list"])

    def test_50_unknown_input_file_type(self):
        self.run_and_check_exit_code([__file__], _not=True)

    def test_52_unknown_input_parser_type(self):
        self.run_and_check_exit_code([__file__, "-I", "unknown_psr"],
                                     _not=True)

    def test_54_no_input_type_and_unknown_out_file_type(self):
        self.run_and_check_exit_code([__file__, __file__ + '.un_ext'],
                                     _not=True)


class Test_12(RunTestWithTmpdir):
    infile = tests.common.respath('00-cnf.json')

    def test_60_unknown_out_file_type(self):
        opath = str(self.tmpdir / "t.unknown_ext")
        self.run_and_check_exit_code([self.infile, "-o", opath], _not=True)

    def test_62_unknown_out_parser_type(self):
        opath = str(self.tmpdir / "t.unknown_psr")
        self.run_and_check_exit_code([self.infile, "-O", opath], _not=True)


class Test_20_Base(RunTestBase):

    def setUp(self):
        self.workdir = pathlib.Path(tests.common.setup_workdir())

    def tearDown(self):
        tests.common.cleanup_workdir(str(self.workdir))

    def _assert_run_and_exit(self, *args):
        self.assertRaises(SystemExit, _run, *args)


class Test_30_single_input(Test_20_Base):

    def test_10(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        infile = self.workdir / "a.json"
        output = self.workdir / "b.json"

        anyconfig.api.dump(a, infile)
        self.assertTrue(infile.exists())

        _run("-o", output, infile)
        self.assertTrue(output.exists())

    def test_20_wo_input_type(self):
        self._assert_run_and_exit("a.conf")

    def test_30_w_get_option(self):
        d = dict(name="a", a=dict(b=dict(c=[1, 2], d="C")))

        infile = self.workdir / "a.json"
        output = self.workdir / "b.json"

        anyconfig.api.dump(d, infile)
        self.assertTrue(infile.exists())

        _run("-o", output, "--get", "a.b", infile)
        self.assertTrue(output.exists())

        x = anyconfig.api.load(output)
        self.assertEqual(x, d['a']['b'])

    def test_31_w_get_option_failure(self):
        (key, no_get_q) = ('a', "wrong_key_0.wrong_key_1")
        infile = self.workdir / "a.json"
        anyconfig.api.dump({key: "A"}, infile)
        self.assertTrue(infile.exists())

        self.run_and_check_exit_code(["--get", no_get_q, infile], 1)

    def test_32_w_set_option(self):
        d = dict(name="a", a=dict(b=dict(c=[1, 2], d="C")))

        infile = self.workdir / "a.json"
        output = self.workdir / "b.json"

        anyconfig.api.dump(d, infile)
        self.assertTrue(infile.exists())

        _run("-o", output, "--set", "a.b.d=E", infile)
        self.assertTrue(output.exists())

        ref = d.copy()
        ref['a']['b']['d'] = 'E'

        x = anyconfig.api.load(output)
        self.assertEqual(x, ref)

    def test_40_ignore_missing(self):
        infile = pathlib.Path(os.curdir) / "conf_file_should_not_exist.json"
        assert not infile.exists()

        self.assertFalse(_run("-O", "json", "--ignore-missing", infile))

    @unittest.skipIf(not anyconfig.schema.JSONSCHEMA_IS_AVAIL,
                     "json schema lib is not available")
    def test_50_w_schema(self):
        infile = CNF_0_PATH
        scmfile = tests.common.respath('00-scm.yml')

        output = self.workdir / "output.json"
        self.run_and_check_exit_code(["--schema", scmfile, "--validate",
                                      infile], 0)
        self.run_and_check_exit_code(["--schema", scmfile, "-o", output,
                                      infile], 0)

        infile2 = self.workdir / "input.yml"
        cnf = CNF_0.copy()
        cnf["a"] = "aaa"  # Validation should fail.
        anyconfig.api.dump(cnf, infile2)
        self.run_and_check_exit_code(["--schema", scmfile, "--validate",
                                      infile2], 1)

    def test_52_wo_schema(self):
        self.run_and_check_exit_code(["--validate", CNF_0_PATH], 1)

    def test_54_gen_schema_and_validate_with_it(self):
        cnf = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        infile = self.workdir / "cnf.json"
        output = self.workdir / "out.json"
        anyconfig.api.dump(cnf, infile)

        self.run_and_check_exit_code(["--gen-schema", "-o", output, infile], 0)
        self.assertTrue(output.exists())
        self.run_and_check_exit_code(["--schema", output, "--validate",
                                      infile], 0)

    def test_60_w_arg_option(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), d=[1, 2])

        infile = self.workdir / "a.json"
        output = self.workdir / "b.json"

        anyconfig.api.dump(a, infile)
        self.assertTrue(infile.exists())

        _run("-o", output, "-A", "a:10;name:x;d:3,4", infile)
        self.assertTrue(output.exists())

        x = anyconfig.api.load(output)

        self.assertNotEqual(a["name"], x["name"])
        self.assertNotEqual(a["a"], x["a"])
        self.assertNotEqual(a["d"], x["d"])

        self.assertEqual(x["name"], 'x')
        self.assertEqual(x["a"], 10)
        self.assertEqual(x["d"], [3, 4])

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


class Test_50_others_w_input(Test_20_Base):

    def setUp(self):
        super().setUp()
        dic = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), d=[1, 2])
        self.infile = self.workdir / "a.json"
        anyconfig.api.dump(dic, self.infile)

    def test_10_output_wo_output_option_w_otype(self):
        self.run_and_check_exit_code(["--otype", "json", self.infile])

    def test_12_output_wo_output_option_and_otype_w_itype(self):
        self.run_and_check_exit_code(["--itype", "json", self.infile])

    def test_20_no_out_dumper(self):
        outfile = self.workdir / "out.conf"
        self.run_and_check_exit_code(["-o", outfile, self.infile], 1)

    def test_22_no_out_dumper_nor_itype(self):
        infile = str(self.infile).replace(".json", ".conf")
        outfile = self.workdir / "out.conf"
        self.run_and_check_exit_code(["-o", outfile, infile], 1)

    @unittest.skipIf(not getattr(anyconfig.query, "jmespath", False),
                     "jmespath lib is not available")
    def test_30_w_query_option(self):
        self.run_and_check_exit_code(["-Q", "b.b[::-1]", self.infile], 0)


class Test_50_others_wo_input(Test_20_Base):

    def test_30_no_itype_and_otype(self):
        outfile = self.workdir / "out.conf"
        self.run_and_check_exit_code(["-o", outfile, "in.conf"], 1)

    def test_40_no_inputs__w_env_option(self):
        output = self.workdir / "out.json"
        self.run_and_check_exit_code(["--env", "-o", output], 0)
        data = anyconfig.api.load(output)

        for env_var, env_val in os.environ.items():
            self.assertTrue(env_var in data)
            self.assertEqual(env_val, os.environ[env_var])

# vim:sw=4:ts=4:et:
