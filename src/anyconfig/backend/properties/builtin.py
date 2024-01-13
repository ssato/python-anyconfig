#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
r"""A backend module to load and dump (Java) properties files.

- Format to support: Java Properties file, e.g.
  http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html
- Requirements: None (built-in)
- Development Status :: 4 - Beta
- Limitations:

  - Key and value separator of white spaces is not supported
  - Keys contain escaped white spaces is not supported

- Special options: None

Changelog:

.. versionchanged:: 0.7.0

   - Fix handling of empty values, pointed by @ajays20078
   - Fix handling of values contain strings start with '#' or '!' by
     @ajays20078

.. versionadded:: 0.2

   - Added native Java properties parser instead of a plugin utilizes
     pyjavaproperties module.
"""
import re
import typing
import warnings

from .. import base


_COMMENT_MARKERS: typing.Tuple[str, ...] = ('#', '!')


def parseline(line: str) -> typing.Tuple[typing.Optional[str], str]:
    """Parse a line of Java properties file.

    :param line:
        A string to parse, must not start with ' ', '#' or '!' (comment)
    :return: A tuple of (key, value), both key and value may be None
    """
    pair = re.split(r"(?:\s+)?(?:(?<!\\)[=:])", line.strip(), maxsplit=1)
    key = pair[0].rstrip()

    if len(pair) < 2:
        warnings.warn(
            f'Invalid line found: {line}', category=SyntaxWarning, stacklevel=2
        )
        return (key or None, '')

    return (key, pair[1].strip())


def _pre_process_line(
    line: str,
    comment_markers: typing.Tuple[str, ...] = _COMMENT_MARKERS
):
    """Preprocess a line in properties; strip comments, etc.

    :param line:
        A string not starting w/ any white spaces and ending w/ line breaks.
        It may be empty. see also: :func:`load`.
    :param comment_markers: Comment markers, e.g. '#' (hash)
    """
    if not line:
        return None

    if any(c in line for c in comment_markers):
        if line.startswith(comment_markers):
            return None

    return line


def unescape(in_s: str) -> str:
    """Un-escape and take out the content from given str ``in_s``."""
    return re.sub(r'\\(.)', r'\1', in_s)


def _escape_char(in_c: str) -> str:
    """Escape some special characters in java .properties files."""
    return '\\' + in_c if in_c in (':', '=', '\\') else in_c


def escape(in_s: str) -> str:
    """Escape special characters in given str."""
    return ''.join(_escape_char(c) for c in in_s)


def load(stream, container=dict, comment_markers=_COMMENT_MARKERS):
    """Load data from a java properties files given as ``stream``.

    :param stream: A file or file like object of Java properties files
    :param container:
        Factory function to create a dict-like object to store properties
    :param comment_markers: Comment markers, e.g. '#' (hash)
    :return: Dict-like object holding properties
    """
    ret = container()
    prev = ""

    for line in stream:
        line = _pre_process_line(prev + line.strip().rstrip(),
                                 comment_markers)
        # I don't think later case may happen but just in case.
        if line is None or not line:
            continue

        prev = ""  # re-initialize for later use.

        if line.endswith("\\"):
            prev += line.rstrip(" \\")
            continue

        (key, val) = parseline(line)
        if key is None:
            warnings.warn(
                f'Failed to parse the line: {line}',
                category=SyntaxWarning, stacklevel=2
            )
            continue

        ret[key] = unescape(val)

    return ret


class Parser(base.StreamParser):
    """Parser for Java properties files."""

    _cid = 'properties.builtin'
    _type = 'properties'
    _extensions = ['properties']
    _ordered = True
    _dict_opts = ['ac_dict']

    def load_from_stream(self, stream, container, **kwargs):
        """Load config from given file like object 'stream'.

        :param stream: A file or file like object of Java properties files
        :param container: callble to make a container object
        :param kwargs: optional keyword parameters (ignored)

        :return: Dict-like object holding config parameters
        """
        return load(stream, container=container)

    def dump_to_stream(self, cnf, stream, **kwargs):
        """Dump config 'cnf' to a file or file-like object 'stream'.

        :param cnf: Java properties config data to dump
        :param stream: Java properties file or file like object
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        for key, val in cnf.items():
            stream.write(f"{key} = {escape(val)}\n")

# vim:sw=4:ts=4:et:
