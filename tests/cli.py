#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, too-many-public-methods
from __future__ import absolute_import

import os
import os.path
import unittest

import anyconfig.cli as TT
import anyconfig.api
import anyconfig.template
import tests.common
import tests.api

from tests.common import CNF_0


CNF_0_PATH = os.path.join(tests.common.selfdir(), "00-cnf.yml")
SCM_0_PATH = os.path.join(tests.common.selfdir(), "00-scm.yml")
CNF_TMPL_0 = tests.api.CNF_TMPL_1


def _run(*args):
    TT.main(["dummy", "--silent"] + list(args))


class Test_00(unittest.TestCase):
    """

    >>> psr = TT.make_parser()
    >>> assert isinstance(psr, TT.argparse.ArgumentParser)
    >>> psr.parse_args([])  # doctest: +NORMALIZE_WHITESPACE
    Namespace(args=None, atype=None, env=False, gen_schema=False, get=None,
              ignore_missing=False, inputs=[], itype=None, list=False,
              loglevel=1, merge='merge_dicts', otype=None, output=None,
              query=None, schema=None, set=None, template=False,
              validate=False)
    """


class RunTestBase(unittest.TestCase):

    def run_and_check_exit_code(self, args=None, code=0, _not=False,
                                exc_cls=SystemExit):
        try:
            TT.main(["dummy", "--silent"] + ([] if args is None else args))
        except exc_cls as exc:
            ecode = getattr(exc, "code", 1)
            (self.assertNotEqual if _not else self.assertEqual)(ecode, code)


class Test_10(RunTestBase):

    def test_10_show_usage(self):
        self.run_and_check_exit_code(["--help"])

    def test_20_wo_args(self):
        self.run_and_check_exit_code(_not=True)

    def test_30_wrong_option(self):
        self.run_and_check_exit_code(["--wrong-option-xyz"], _not=True)

    def test_40_list(self):
        self.run_and_check_exit_code(["--list"])


class Test_20_Base(RunTestBase):

    def setUp(self):
        self.workdir = tests.common.setup_workdir()
        self.script = os.path.join(tests.common.selfdir(),
                                   "..", "cli.py")

    def tearDown(self):
        tests.common.cleanup_workdir(self.workdir)

    def _assert_run_and_exit(self, *args):
        raised = False
        try:
            _run(*args)
        except SystemExit:
            raised = True

        self.assertTrue(raised)


class Test_30_single_input(Test_20_Base):

    def test_10(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        infile = os.path.join(self.workdir, "a.json")
        output = os.path.join(self.workdir, "b.json")

        anyconfig.api.dump(a, infile)
        self.assertTrue(os.path.exists(infile))

        TT.main(["dummy", "--silent", "-o", output, infile])
        self.assertTrue(os.path.exists(output))

    def test_20_wo_input_type(self):
        self._assert_run_and_exit("a.conf")

    def test_30_w_get_option(self):
        d = dict(name="a", a=dict(b=dict(c=[1, 2], d="C")))

        infile = os.path.join(self.workdir, "a.json")
        output = os.path.join(self.workdir, "b.json")

        anyconfig.api.dump(d, infile)
        self.assertTrue(os.path.exists(infile))

        TT.main(["dummy", "--silent", "-o", output, "--get", "a.b", infile])
        self.assertTrue(os.path.exists(output))

        x = anyconfig.api.load(output)
        self.assertEqual(x, d['a']['b'])

    def test_31_w_get_option_failure(self):
        (key, no_get_q) = ('a', "wrong_key_0.wrong_key_1")
        infile = os.path.join(self.workdir, "a.json")
        anyconfig.api.dump({key: "A"}, infile)
        self.assertTrue(os.path.exists(infile))

        self.run_and_check_exit_code(["--get", no_get_q, infile], 1)

    def test_32_w_set_option(self):
        d = dict(name="a", a=dict(b=dict(c=[1, 2], d="C")))

        infile = os.path.join(self.workdir, "a.json")
        output = os.path.join(self.workdir, "b.json")

        anyconfig.api.dump(d, infile)
        self.assertTrue(os.path.exists(infile))

        TT.main(["dummy", "-q", "-o", output, "--set", "a.b.d=E", infile])
        self.assertTrue(os.path.exists(output))

        ref = d.copy()
        ref['a']['b']['d'] = 'E'

        x = anyconfig.api.load(output)
        self.assertEqual(x, ref)

    def test_40_ignore_missing(self):
        infile = os.path.join(os.curdir, "conf_file_should_not_exist.json")
        assert not os.path.exists(infile)

        self.assertFalse(TT.main(["dummy", "--silent", "-O", "json",
                                  "--ignore-missing", infile]))

    def test_50_w_schema(self):
        (infile, scmfile) = (CNF_0_PATH, SCM_0_PATH)
        output = os.path.join(self.workdir, "output.json")
        self.run_and_check_exit_code(["--schema", scmfile, "--validate",
                                      infile], 0)
        self.run_and_check_exit_code(["--schema", scmfile, "-o", output,
                                      infile], 0)

        infile2 = os.path.join(self.workdir, "input.yml")
        cnf = CNF_0.copy()
        cnf["a"] = "aaa"  # Validation should fail.
        anyconfig.api.dump(cnf, infile2)
        self.run_and_check_exit_code(["--schema", scmfile, "--validate",
                                      infile2], 1)

    def test_52_wo_schema(self):
        self.run_and_check_exit_code(["--validate", CNF_0_PATH], 1)

    def test_54_gen_schema_and_validate_with_it(self):
        cnf = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        infile = os.path.join(self.workdir, "cnf.json")
        output = os.path.join(self.workdir, "out.yml")
        anyconfig.api.dump(cnf, infile)

        self.run_and_check_exit_code(["--gen-schema", "-o", output, infile], 0)
        self.assertTrue(os.path.exists(output))
        self.run_and_check_exit_code(["--schema", output, "--validate",
                                      infile], 0)

    def test_60_w_arg_option(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), d=[1, 2])

        infile = os.path.join(self.workdir, "a.json")
        output = os.path.join(self.workdir, "b.json")

        anyconfig.api.dump(a, infile)
        self.assertTrue(os.path.exists(infile))

        TT.main(["dummy", "--silent", "-o", output, "-A",
                 "a:10;name:x;d:3,4", infile])
        self.assertTrue(os.path.exists(output))

        x = anyconfig.api.load(output)

        self.assertNotEqual(a["name"], x["name"])
        self.assertNotEqual(a["a"], x["a"])
        self.assertNotEqual(a["d"], x["d"])

        self.assertEqual(x["name"], 'x')
        self.assertEqual(x["a"], 10)
        self.assertEqual(x["d"], [3, 4])

    def test_70_no_template(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        infile = os.path.join(self.workdir, "a.json")
        output = os.path.join(self.workdir, "b.json")

        anyconfig.api.dump(a, infile)
        self.assertTrue(os.path.exists(infile))

        TT.main(["dummy", "--silent", "-o", output, infile])
        self.assertTrue(os.path.exists(output))


class Test_40_multi_inputs(Test_20_Base):

    def test_10(self):
        xs = [dict(a=1, ),
              dict(b=dict(b=[1, 2], c="C")), ]

        a = xs[0].copy()
        a.update(xs[1])

        output = os.path.join(self.workdir, "b.json")

        inputs = []
        for i in [0, 1]:
            infile = os.path.join(self.workdir, "a%d.json" % i)
            inputs.append(infile)

            anyconfig.api.dump(xs[i], infile)
            self.assertTrue(os.path.exists(infile))

        TT.main(["dummy", "--silent", "-o", output] + inputs)
        self.assertTrue(os.path.exists(output))

    def test_20_w_template(self):
        if not anyconfig.template.SUPPORTED:
            return

        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        inputsdir = os.path.join(self.workdir, "in")
        os.makedirs(inputsdir)

        anyconfig.api.dump(a, os.path.join(inputsdir, "a0.yml"))
        open(os.path.join(inputsdir, "a1.yml"), 'w').write(CNF_TMPL_0)
        output = os.path.join(self.workdir, "b.json")

        TT.main(["dummy", "--silent", "--template", "-o", output,
                 os.path.join(inputsdir, "*.yml")])
        self.assertTrue(os.path.exists(output))

    def test_30_w_template(self):
        if not anyconfig.template.SUPPORTED:
            return

        curdir = tests.common.selfdir()

        infile = os.path.join(curdir, "*template-c*.yml")
        output = os.path.join(self.workdir, "output.yml")

        TT.main(["dummy", "--silent", "--template", "-o", output, infile])


class Test_50_others_w_input(Test_20_Base):

    def setUp(self):
        super(Test_50_others_w_input, self).setUp()
        dic = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), d=[1, 2])
        self.infile = os.path.join(self.workdir, "a.json")
        anyconfig.api.dump(dic, self.infile)

    def test_10_output_wo_output_option_w_otype(self):
        self.run_and_check_exit_code(["--otype", "json", self.infile])

    def test_12_output_wo_output_option_and_otype_w_itype(self):
        self.run_and_check_exit_code(["--itype", "json", self.infile])

    def test_20_no_out_dumper(self):
        outfile = os.path.join(self.workdir, "out.conf")
        self.run_and_check_exit_code(["-o", outfile, self.infile], 1)

    def test_22_no_out_dumper_nor_itype(self):
        infile = self.infile.replace(".json", ".conf")
        outfile = os.path.join(self.workdir, "out.conf")
        self.run_and_check_exit_code(["-o", outfile, infile], 1)

    def test_30_w_query_option(self):
        self.run_and_check_exit_code(["-Q", "b.b[::-1]", self.infile], 0)


class Test_50_others_wo_input(Test_20_Base):

    def test_30_no_itype_and_otype(self):
        outfile = os.path.join(self.workdir, "out.conf")
        self.run_and_check_exit_code(["-o", outfile, "in.conf"], 1)

    def test_40_no_inputs__w_env_option(self):
        output = os.path.join(self.workdir, "out.json")
        self.run_and_check_exit_code(["--silent", "--env", "-o", output], 0)
        data = anyconfig.api.load(output)

        for env_var, env_val in os.environ.items():
            self.assertTrue(env_var in data)
            self.assertEqual(env_val, os.environ[env_var])

# vim:sw=4:ts=4:et:
