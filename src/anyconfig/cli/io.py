#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Initialize sys.std{out,err}."""
import io
import locale
import sys


def make():
    """Initialize sys.std{out,err} and returns them."""
    encoding = (locale.getdefaultlocale()[1] or 'UTF-8').lower()

    # TODO: What should be done for an error, "AttributeError: '_io.StringIO'
    # object has no attribute 'buffer'"?
    try:
        return (
            io.TextIOWrapper(sys.stdout.buffer, encoding=encoding),
            io.TextIOWrapper(sys.stderr.buffer, encoding=encoding)
        )
    except AttributeError:
        pass

    return None

# vim:sw=4:ts=4:et:
