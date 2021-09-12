#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""CLI frontend module for anyconfig.
"""
import os
import sys
import warnings

from .. import api, parser
from . import actions, filters, parse_args, utils


def try_parse_args(argv):
    """
    Show supported config format types or usage.

    :param argv: Argument list to parse or None (sys.argv will be set).
    :return: argparse.Namespace object or None (exit before return)
    """
    (psr, args) = parse_args.parse(argv)
    if args.loglevel:
        warnings.simplefilter("always")

    if args.inputs:
        if '-' in args.inputs:
            args.inputs = sys.stdin
    else:
        if args.list:
            actions.show_parsers()
        elif args.env:
            cnf = os.environ.copy()
            actions.output_result(cnf, args)
            sys.exit(0)
        else:
            psr.print_usage()
            sys.exit(1)

    if args.validate and args.schema is None:
        utils.exit_with_output("--validate option requires --scheme option", 1)

    return args


def main(argv=None):
    """
    :param argv: Argument list to parse or None (sys.argv will be set).
    """
    args = try_parse_args((argv if argv else sys.argv)[1:])
    cnf = os.environ.copy() if args.env else {}

    extra_opts = dict()
    if args.extra_opts:
        extra_opts = parser.parse(args.extra_opts)

    diff = utils.load_diff(args, extra_opts)

    if cnf:
        api.merge(cnf, diff)
    else:
        cnf = diff

    if args.args:
        diff = parser.parse(args.args)
        api.merge(cnf, diff)

    if args.validate:
        utils.exit_with_output("Validation succeeds")

    if args.gen_schema:
        cnf = api.gen_schema(cnf)
    else:
        cnf = filters.do_filter(cnf, args)

    actions.output_result(cnf, args, args.inputs, extra_opts=extra_opts)

# vim:sw=4:ts=4:et:
