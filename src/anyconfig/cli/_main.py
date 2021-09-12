#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""CLI frontend module for anyconfig.
"""
import os
import sys

from .. import api, parser
from . import utils


def main(argv=None):
    """
    :param argv: Argument list to parse or None (sys.argv will be set).
    """
    args = utils.try_parse_args((argv if argv else sys.argv)[1:])
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
        cnf = utils.do_filter(cnf, args)

    utils.output_result(cnf, args, args.inputs, extra_opts=extra_opts)

# vim:sw=4:ts=4:et:
