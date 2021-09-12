#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utilities for anyconfig.cli.*.
"""
from .. import api, parser
from . import utils


def do_get(cnf, get_path):
    """
    :param cnf: Configuration object to print out
    :param get_path: key path given in --get option
    :return: updated Configuration object if no error
    """
    (cnf, err) = api.get(cnf, get_path)
    if cnf is None:  # Failed to get the result.
        utils.exit_with_output("Failed to get result: err=%s" % err, 1)

    return cnf


def do_filter(cnf, args):
    """
    :param cnf: Mapping object represents configuration data
    :param args: :class:`argparse.Namespace` object
    :return: 'cnf' may be updated
    """
    if args.query:
        cnf = api.try_query(cnf, args.query)
    elif args.get:
        cnf = do_get(cnf, args.get)
    elif args.set:
        (key, val) = args.set.split('=')
        api.set_(cnf, key, parser.parse(val))

    return cnf

# vim:sw=4:ts=4:et:
