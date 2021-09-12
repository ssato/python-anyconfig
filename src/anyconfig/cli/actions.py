#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utilities for anyconfig.cli.*.
"""
import os
import sys

from .. import api, utils as base_utils
from . import utils


def show_parsers():
    """Show list of info of parsers available
    """
    sep = os.linesep

    types = "Supported types: " + ", ".join(api.list_types())
    cids = "IDs: " + ", ".join(c for c, _ps in api.list_by_cid())

    x_vs_ps = ["  %s: %s" % (x, ", ".join(p.cid() for p in ps))
               for x, ps in api.list_by_extension()]
    exts = "File extensions:" + sep + sep.join(x_vs_ps)

    utils.exit_with_output(sep.join([types, exts, cids]))


def output_type_by_input_path(inpaths, itype, fmsg):
    """
    :param inpaths: List of input file paths
    :param itype: Input type or None
    :param fmsg: message if it cannot detect otype by 'inpath'
    :return: Output type :: str
    """
    msg = ("Specify inpath and/or outpath type[s] with -I/--itype "
           "or -O/--otype option explicitly")
    if itype is None:
        try:
            otype = api.find(inpaths[0]).type()
        except api.UnknownFileTypeError:
            utils.exit_with_output((fmsg % inpaths[0]) + msg, 1)
        except (ValueError, IndexError):
            utils.exit_with_output(msg, 1)
    else:
        otype = itype

    return otype


def try_dump(cnf, outpath, otype, fmsg, extra_opts=None):
    """
    :param cnf: Configuration object to print out
    :param outpath: Output file path or None
    :param otype: Output type or None
    :param fmsg: message if it cannot detect otype by 'inpath'
    :param extra_opts: Map object will be given to api.dump as extra options
    """
    if extra_opts is None:
        extra_opts = {}
    try:
        api.dump(cnf, outpath, otype, **extra_opts)
    except api.UnknownFileTypeError:
        utils.exit_with_output(fmsg % outpath, 1)
    except api.UnknownProcessorTypeError:
        utils.exit_with_output("Invalid output type '%s'" % otype, 1)


def output_result(cnf, args, inpaths=None, extra_opts=None):
    """
    :param cnf: Configuration object to print out
    :param args: :class:`argparse.Namespace` object
    :param inpaths: List of input file paths
    :param extra_opts: Map object will be given to api.dump as extra options
    """
    fmsg = ("Uknown file type and cannot detect appropriate backend "
            "from its extension, '%s'")
    (outpath, otype) = (args.output, args.otype or "json")

    if not base_utils.is_dict_like(cnf):
        utils.exit_with_output(str(cnf))  # Print primitive types as it is.

    if not outpath or outpath == "-":
        outpath = sys.stdout
        if otype is None:
            otype = output_type_by_input_path(inpaths, args.itype, fmsg)

    try_dump(cnf, outpath, otype, fmsg, extra_opts=extra_opts)

# vim:sw=4:ts=4:et:
