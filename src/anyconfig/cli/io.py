#
# Copyright (C) 2011 - 2023 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Initialize sys.std{out,err}."""
import io
import sys

from .. import ioinfo


def make():
    """Initialize sys.std{out,err} and returns them."""
    encoding = ioinfo.get_encoding()

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
