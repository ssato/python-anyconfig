#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Argument parser.
"""
import argparse

from .. import api
from . import constants


DEFAULTS = dict(
    loglevel=0, list=False, output=None, itype=None, otype=None, atype=None,
    merge=api.MS_DICTS, ignore_missing=False, template=False, env=False,
    schema=None, validate=False, gen_schema=False, extra_opts=None
)


def make_parser(defaults=None):
    """
    :param defaults: Default option values
    """
    if defaults is None:
        defaults = DEFAULTS

    ctypes = api.list_types()
    ctypes_s = ", ".join(ctypes)
    type_help = "Select type of %s config files from " + \
        ctypes_s + " [Automatically detected by file ext]"

    mts = api.MERGE_STRATEGIES
    mts_s = ", ".join(mts)
    mt_help = "Select strategy to merge multiple configs from " + \
        mts_s + " [%(merge)s]" % defaults

    apsr = argparse.ArgumentParser(usage=constants.USAGE)
    apsr.set_defaults(**defaults)

    apsr.add_argument("inputs", type=str, nargs='*', help="Input files")
    apsr.add_argument("--version", action="version",
                      version="%%(prog)s %s" % api.version())

    lpog = apsr.add_argument_group("List specific options")
    lpog.add_argument("-L", "--list", action="store_true",
                      help="List supported config types")

    spog = apsr.add_argument_group("Schema specific options")
    spog.add_argument("--validate", action="store_true",
                      help="Only validate input files and do not output. "
                           "You must specify schema file with -S/--schema "
                           "option.")
    spog.add_argument("--gen-schema", action="store_true",
                      help="Generate JSON schema for givne config file[s] "
                           "and output it instead of (merged) configuration.")

    gspog = apsr.add_argument_group("Query/Get/set options")
    gspog.add_argument("-Q", "--query", help=constants.QUERY_HELP)
    gspog.add_argument("--get", help=constants.GET_HELP)
    gspog.add_argument("--set", help=constants.SET_HELP)

    apsr.add_argument("-o", "--output", help="Output file path")
    apsr.add_argument("-I", "--itype", choices=ctypes, metavar="ITYPE",
                      help=(type_help % "Input"))
    apsr.add_argument("-O", "--otype", choices=ctypes, metavar="OTYPE",
                      help=(type_help % "Output"))
    apsr.add_argument("-M", "--merge", choices=mts, metavar="MERGE",
                      help=mt_help)
    apsr.add_argument("-A", "--args", help="Argument configs to override")
    apsr.add_argument("--atype", choices=ctypes, metavar="ATYPE",
                      help=constants.ATYPE_HELP_FMT % ctypes_s)

    cpog = apsr.add_argument_group("Common options")
    cpog.add_argument("-x", "--ignore-missing", action="store_true",
                      help="Ignore missing input files")
    cpog.add_argument("-T", "--template", action="store_true",
                      help="Enable template config support")
    cpog.add_argument("-E", "--env", action="store_true",
                      help="Load configuration defaults from "
                           "environment values")
    cpog.add_argument("-S", "--schema", help="Specify Schema file[s] path")
    cpog.add_argument("-e", "--extra-opts",
                      help="Extra options given to the API call, "
                           "--extra-options indent:2 (specify the "
                           "indent for pretty-printing of JSON outputs) "
                           "for example")
    cpog.add_argument("-v", "--verbose", action="count", dest="loglevel",
                      help="Verbose mode; -v or -vv (more verbose)")
    return apsr

# vim:sw=4:ts=4:et:
