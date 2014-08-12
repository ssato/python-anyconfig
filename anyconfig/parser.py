#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Misc parsers"""
import re


INT_PATTERN = re.compile(r"^(\d|([1-9]\d+))$")
BOOL_PATTERN = re.compile(r"^(true|false)$", re.I)
STR_PATTERN = re.compile(r"^['\"](.*)['\"]$")

PATH_SEPS = ('/', '.')


def parse_single(s):
    """
    Very simple parser to parse expressions represent some single values.

    :param s: a string to parse
    :return: Int | Bool | String

    >>> parse_single(None)
    ''
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

    if s is None:
        return ''

    s = s.strip()

    if not s:
        return ''

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

    :param s: a string to parse
    :param sep: Char to separate items of list
    :return: [Int | Bool | String]

    >>> parse_list("")
    []
    >>> parse_list("1")
    [1]
    >>> parse_list("a,b")
    ['a', 'b']
    >>> parse_list("1,2")
    [1, 2]
    >>> parse_list("a,b,")
    ['a', 'b']
    """
    return [parse_single(x) for x in s.split(sep) if x]


def parse_attrlist_0(s, avs_sep=":", vs_sep=",", as_sep=";"):
    """
    Simple parser to parse expressions in the form of
    [ATTR1:VAL0,VAL1,...;ATTR2:VAL0,VAL2,..].

    :param s: input string
    :param avs_sep:  char to separate attribute and values
    :param vs_sep:  char to separate values
    :param as_sep:  char to separate attributes

    :return: a list of tuples of (key, value | [value])
        where key = (Int | String | ...),
              value = (Int | Bool | String | ...) | [Int | Bool | String | ...]

    >>> parse_attrlist_0("a:1")
    [('a', 1)]
    >>> parse_attrlist_0("a:1;b:xyz")
    [('a', 1), ('b', 'xyz')]
    >>> parse_attrlist_0("requires:bash,zsh")
    [('requires', ['bash', 'zsh'])]
    >>> parse_attrlist_0("obsoletes:sysdata;conflicts:sysdata-old")
    [('obsoletes', 'sysdata'), ('conflicts', 'sysdata-old')]
    """
    def attr_and_values(s):
        for rel in parse_list(s, as_sep):
            if avs_sep not in rel or rel.endswith(avs_sep):
                continue

            (_attr, _values) = parse_list(rel, avs_sep)

            if vs_sep in str(_values):
                _values = parse_list(_values, vs_sep)

            if _values:
                yield (_attr, _values)

    return [(a, vs) for a, vs in attr_and_values(s)]


def parse_attrlist(s, avs_sep=":", vs_sep=",", as_sep=";"):
    """
    Simple parser to parse expressions in the form of
    [ATTR1:VAL0,VAL1,...;ATTR2:VAL0,VAL2,..].

    :param s: input string
    :param avs_sep:  char to separate attribute and values
    :param vs_sep:  char to separate values
    :param as_sep:  char to separate attributes

    >>> parse_attrlist("requires:bash,zsh")
    {'requires': ['bash', 'zsh']}
    """
    return dict(parse_attrlist_0(s, avs_sep, vs_sep, as_sep))


def parse(s, lsep=",", avsep=":", vssep=",", avssep=";"):
    """Generic parser"""
    if avsep in s:
        return parse_attrlist(s, avsep, vssep, avssep)
    elif lsep in s:
        return parse_list(s, lsep)
    else:
        return parse_single(s)


def parse_path(path, seps=PATH_SEPS):
    """
    Parse path expression and return list of path items.

    :param path: Path expression may contain separator chars.
    :param seps: Separator char candidates.

    :return: A list of keys to fetch object[s] later.

    >>> parse_path('')
    []
    >>> parse_path('/a/b/c/d')
    ['a', 'b', 'c', 'd']
    >>> parse_path('a.b.c.d')
    ['a', 'b', 'c', 'd']
    >>> parse_path('abc')
    ['abc']
    """
    if not path:
        return []

    for sep in seps:
        if sep in path:
            return [x for x in path.split(sep) if x]

    return [path]

# vim:sw=4:ts=4:et:
