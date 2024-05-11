#
# Copyright (C) 2013 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases of anyconfig.cli.main without arguments."""
from __future__ import annotations

import anyconfig.cli.parse_args as TT


def test_make_parser() -> None:
    psr = TT.make_parser()
    assert isinstance(psr, TT.argparse.ArgumentParser)

    # ref = TT.DEFAULTS.copy()
    ref = {
        "args": None, "atype": None, "env": False,
        "extra_opts": None, "gen_schema": False,
        "get": None, "ignore_missing": False, "inputs": [],
        "itype": None, "list": False, "loglevel": 0,
        "merge": 'merge_dicts', "otype": None, "output": None,
        "query": None, "schema": None, "set": None,
        "template": False, "validate": False
    }
    assert vars(psr.parse_args([])) == ref
