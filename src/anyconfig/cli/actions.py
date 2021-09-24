#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Actions for anyconfig.cli.*."""
from .. import api
from . import utils


def show_parsers_and_exit():
    """Show list of info of parsers available."""
    utils.exit_with_output(utils.make_parsers_txt())


def try_output_result(cnf, args):
    """Try to output result."""
    api.dump(
        cnf, args.output, args.otype,
        **(args.extra_opts if args.extra_opts else {})
    )

# vim:sw=4:ts=4:et:
