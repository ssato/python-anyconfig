#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import glob
import itertools
import logging
import re


INT_PATTERN = re.compile(r"^(\d|([1-9]\d+))$")
BOOL_PATTERN = re.compile(r"^(true|false)$", re.I)
STR_PATTERN = re.compile(r"^['\"](.*)['\"]$")


def parse_single(s):
    """
    Very simple parser to parse expressions represent some single values.

    >>> parse_single("0")
    0
    >>> parse_single("123")
    123
    >>> parse_single("True")
    True
    >>> parse_single("a string")
    'a string'
    >>> parse_single("0.1")
    '0.1'
    >>> parse_single("    a string contains extra whitespaces     ")
    'a string contains extra whitespaces'
    """
    def matched(pat, s):
        return pat.match(s) is not None

    s = s.strip()

    if not s:
        return ""

    if matched(BOOL_PATTERN, s):
        return bool(s)

    if matched(INT_PATTERN, s):
        return int(s)

    if matched(STR_PATTERN, s):
        return s[1:-1]

    return s


def parse_list(s, sep=","):
    """
    Simple parser to parse expressions reprensent some list values.

    @param sep: Char to separate items of list.

    >>> parse_list("")
    []
    >>> parse_list("a,b")
    ['a', 'b']
    >>> parse_list("1,2")
    [1, 2]
    >>> parse_list("a,b,")
    ['a', 'b']
    """
    return [parse_single(x) for x in s.split(sep) if x]


def parse_list_str(optstr, sep=","):
    """
    Simple parser for optstr gives a list of items separated with "," (comma).

    >>> parse_list_str("")
    []
    >>> parse_list_str("a,b")
    ['a', 'b']
    >>> parse_list_str("a,b,")
    ['a', 'b']
    """
    return [p for p in optstr.split(sep) if p]


def parse_attrlist(s, avs_sep=":", vs_sep=",", as_sep=";"):
    """
    Simple parser to parse expressions in the form of
    [ATTR1:VAL0,VAL1,...;ATTR2:VAL0,VAL2,..].

    :param s: input string
    :param avs_sep:  char to separate attribute and values
    :param vs_sep:  char to separate values
    :param as_sep:  char to separate attributes

    >>> parse_attrlist("requires:bash,zsh")
    [('requires', ['bash', 'zsh'])]
    >>> parse_attrlist("obsoletes:sysdata;conflicts:sysdata-old")
    [('obsoletes', ['sysdata']), ('conflicts', ['sysdata-old'])]
    """
    def attr_and_values(s):
        for rel in parse_list(s, as_sep):
            if avs_sep not in rel or rel.endswith(avs_sep):
                continue

            (_attr, _values) = parse_list(rel, avs_sep)
            _values = parse_list(_values, vs_sep)

            if _values:
                yield (_attr, _values)

    return [(a, vs) for a, vs in attr_and_values(s)]


def parse(s, lsep=",", avsep=":", vssep=",", avssep=";"):
    if avsep in s:
        return parse_attrlist(s, avsep, vssep, avssep)
    elif lsep in s:
        return parse_list(s, lsep)
    else:
        return parse_single(s)


# vim:sw=4:ts=4:et:
