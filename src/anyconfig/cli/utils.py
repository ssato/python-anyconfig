#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utilities for anyconfig.cli.*."""
import functools
import os
import sys
import typing

from .. import api


@functools.lru_cache(None)
def list_parser_types() -> typing.List[str]:
    """Provide an wrapper of api.list_types() to memoize its result."""
    return api.list_types()


def make_parsers_txt() -> str:
    """Make up a text shows list and info of parsers available."""
    sep = os.linesep
    indent = "  "

    parser_types = ", ".join(list_parser_types())
    file_ext_vs_parsers = sep.join(
        f"{indent}{x}: " + ", ".join(p.cid() for p in ps)
        for x, ps in api.list_by_extension()
    )

    return sep.join(
        [
            "Supported file types:",
            f"{indent}{parser_types}",
            "Supported file extensions [extension: parsers]:",
            f"{file_ext_vs_parsers}",
        ]
    )


def exit_with_output(content, exit_code=0):
    """Exit the program with printing out messages.

    :param content: content to print out
    :param exit_code: Exit code
    """
    (sys.stdout if exit_code == 0 else sys.stderr).write(content + os.linesep)
    sys.exit(exit_code)


def exit_if_load_failure(cnf, msg):
    """Exit the program with errors if loading data was failed.

    :param cnf: Loaded configuration object or None indicates load failure
    :param msg: Message to print out if failure
    """
    if cnf is None:
        exit_with_output(msg, 1)


def load_diff(args, extra_opts):
    """Load update data.

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
        exit_with_output(f"Wrong input type '{args.itype}'", 1)
    except api.UnknownFileTypeError:
        exit_with_output(
            "No appropriate backend was found for given file "
            f"type=n{args.itype}', inputs={', '.join(args.inputs)}",
            1
        )
    exit_if_load_failure(
        diff, f"Failed to load: args={', '.join(args.inputs)}"
    )

    return diff

# vim:sw=4:ts=4:et:
