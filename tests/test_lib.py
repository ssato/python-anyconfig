#
# Copyright (C) 2015 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import pathlib
import subprocess


SCRIPT_TO_USE_ANYCONFIG = """#! /usr/bin/env python
import anyconfig

c = anyconfig.load("/") or {}
anyconfig.dump(c, "/dev/null", "yaml")
"""

NULL_DEV = "/dev/null"
if not pathlib.Path(NULL_DEV).exists():
    NULL_DEV = "NUL"


def check_output(cmd):
    with open(NULL_DEV, mode="w", encoding="utf-8") as devnull:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=devnull) as proc:
            return proc.communicate()[0]


def test_run_script(tmp_path: pathlib.Path):
    script = tmp_path / "a.py"
    script.write_text(SCRIPT_TO_USE_ANYCONFIG)
    out = check_output(["python", str(script)])

    assert out in (b"", "")
