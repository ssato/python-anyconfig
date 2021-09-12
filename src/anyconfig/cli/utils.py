#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utilities for anyconfig.cli.*.
"""
import functools
import os
import sys
import warnings

from .. import api, parser, utils
from . import parse_args


@functools.lru_cache(None)
def list_parser_types():
    """An wrapper to api.list_types() to memoize its result.
    """
    return api.list_types()


def exit_with_output(content, exit_code=0):
    """
    Exit the program with printing out messages.

    :param content: content to print out
    :param exit_code: Exit code
    """
    (sys.stdout if exit_code == 0 else sys.stderr).write(content + os.linesep)
    sys.exit(exit_code)


def show_psrs():
    """Show list of info of parsers available
    """
    sep = os.linesep

    types = "Supported types: " + ", ".join(api.list_types())
    cids = "IDs: " + ", ".join(c for c, _ps in api.list_by_cid())

    x_vs_ps = ["  %s: %s" % (x, ", ".join(p.cid() for p in ps))
               for x, ps in api.list_by_extension()]
    exts = "File extensions:" + sep + sep.join(x_vs_ps)

    exit_with_output(sep.join([types, exts, cids]))


def exit_if_load_failure(cnf, msg):
    """
    :param cnf: Loaded configuration object or None indicates load failure
    :param msg: Message to print out if failure
    """
    if cnf is None:
        exit_with_output(msg, 1)


def try_parse_args(argv):
    """
    Show supported config format types or usage.

    :param argv: Argument list to parse or None (sys.argv will be set).
    :return: argparse.Namespace object or None (exit before return)
    """
    apsr = parse_args.make_parser()
    args = apsr.parse_args(argv)
    if args.loglevel:
        warnings.simplefilter("always")

    if args.inputs:
        if '-' in args.inputs:
            args.inputs = sys.stdin
    else:
        if args.list:
            show_psrs()
        elif args.env:
            cnf = os.environ.copy()
            output_result(cnf, args)
            sys.exit(0)
        else:
            apsr.print_usage()
            sys.exit(1)

    if args.validate and args.schema is None:
        exit_with_output("--validate option requires --scheme option", 1)

    return args


def do_get(cnf, get_path):
    """
    :param cnf: Configuration object to print out
    :param get_path: key path given in --get option
    :return: updated Configuration object if no error
    """
    (cnf, err) = api.get(cnf, get_path)
    if cnf is None:  # Failed to get the result.
        exit_with_output("Failed to get result: err=%s" % err, 1)

    return cnf


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
            exit_with_output((fmsg % inpaths[0]) + msg, 1)
        except (ValueError, IndexError):
            exit_with_output(msg, 1)
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
        exit_with_output(fmsg % outpath, 1)
    except api.UnknownProcessorTypeError:
        exit_with_output("Invalid output type '%s'" % otype, 1)


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

    if not utils.is_dict_like(cnf):
        exit_with_output(str(cnf))  # Print primitive types as it is.

    if not outpath or outpath == "-":
        outpath = sys.stdout
        if otype is None:
            otype = output_type_by_input_path(inpaths, args.itype, fmsg)

    try_dump(cnf, outpath, otype, fmsg, extra_opts=extra_opts)


def load_diff(args, extra_opts):
    """
    :param args: :class:`argparse.Namespace` object
    :param extra_opts: Map object given to api.load as extra options
    """
    try:
        diff = api.load(args.inputs, args.itype,
                        ac_ignore_missing=args.ignore_missing,
                        ac_merge=args.merge,
                        ac_template=args.template,
                        ac_schema=args.schema,
                        **extra_opts)
    except api.UnknownProcessorTypeError:
        exit_with_output("Wrong input type '%s'" % args.itype, 1)
    except api.UnknownFileTypeError:
        exit_with_output("No appropriate backend was found for given file "
                         "type='%s', inputs=%s" % (args.itype,
                                                   ", ".join(args.inputs)),
                         1)
    exit_if_load_failure(diff,
                         "Failed to load: args=%s" % ", ".join(args.inputs))

    return diff


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
