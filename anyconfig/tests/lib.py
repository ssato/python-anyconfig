#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import os.path
import subprocess
import unittest

import anyconfig.tests.common as C


SCRIPT_TO_USE_ANYCONFIG = """\
#! /usr/bin/env python
import anyconfig

c = anyconfig.load("/") or {}
anyconfig.dump(c, "/dev/null", "yaml")
"""


class Test_00(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()
        self.script = os.path.join(self.workdir, "a.py")

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_00_run_script(self):
        with open(self.script, 'w') as f:
            f.write(SCRIPT_TO_USE_ANYCONFIG)

            args = ["python", self.script]
            devnull = open('/dev/null', 'w')

            out = subprocess.check_output(args, stderr=devnull)
            self.assertEquals(out, "")

# vim:sw=4:ts=4:et:
