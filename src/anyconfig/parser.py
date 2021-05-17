#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
"""Misc parsers
"""
import re
import typing
import warnings


INT_PATTERN: typing.Pattern = re.compile(r"^(\d|([1-9]\d+))$")
BOOL_PATTERN: typing.Pattern = re.compile(r"^(true|false)$", re.I)
STR_PATTERN: typing.Pattern = re.compile(r"^['\"](.*)['\"]$")


PrimitiveT = typing.Union[str, int, bool]
PrimitivesT = typing.List[PrimitiveT]


def parse_single(str_: str) -> PrimitiveT:
    """
    Very simple parser to parse expressions represent some single values.

    :param str_: a string to parse
    :return: Int | Bool | String

    >>> parse_single(None)
    ''
    >>> parse_single('0')
    0
    >>> parse_single('123')
    123
    >>> parse_single('True')
    True
    >>> parse_single('a string')
    'a string'
    >>> parse_single('"a string"')
    'a string'
    >>> parse_single("'a string'")
    'a string'
    >>> parse_single('0.1')
    '0.1'
    >>> parse_single('    a string contains extra whitespaces     ')
    'a string contains extra whitespaces'
    """
    if str_ is None:
        return ''

    str_ = str_.strip()

    if not str_:
        return ''

    if BOOL_PATTERN.match(str_) is not None:
        return bool(str_)

    if INT_PATTERN.match(str_) is not None:
        return int(str_)

    if STR_PATTERN.match(str_) is not None:
        return str_[1:-1]

    return str_


def parse_list(str_: str, sep: str = ',') -> PrimitivesT:
    """
    Simple parser to parse expressions reprensent some list values.

    :param str_: a string to parse
    :param sep: Char to separate items of list
    :return: [Int | Bool | String]

    >>> parse_list('')
    []
    >>> parse_list('1')
    [1]
    >>> parse_list('a,b')
    ['a', 'b']
    >>> parse_list('1,2')
    [1, 2]
    >>> parse_list('a,b,')
    ['a', 'b']
    """
    return [parse_single(x) for x in str_.split(sep) if x]


AttrValsT = typing.Tuple[str, typing.Union[PrimitivesT, PrimitiveT]]


def attr_val_itr(str_: str, avs_sep: str = ':', vs_sep: str = ',',
                 as_sep: str = ';') -> typing.Iterator[AttrValsT]:
    """
    Atrribute and value pair parser.

    :param str_: String represents a list of pairs of attribute and value
    :param avs_sep: char to separate attribute and values
    :param vs_sep: char to separate values
    :param as_sep: char to separate attributes
    """
    for rel in parse_list(str_, as_sep):
        rel = typing.cast(str, rel)
        if avs_sep not in rel or rel.endswith(avs_sep):
            continue

        (_attr, _values, *_rest) = parse_list(rel, avs_sep)

        if _rest:
            warnings.warn(f'Extra strings {_rest!s} in {rel!s}'
                          f'It should be in the form of attr{avs_sep}value.')

        _attr = typing.cast(str, _attr)

        if vs_sep in str(_values):
            yield (_attr, parse_list(typing.cast(str, _values), vs_sep))
        elif _values:
            yield (_attr, typing.cast(PrimitiveT, _values))


def parse_attrlist_0(str_: str, avs_sep: str = ':', vs_sep: str = ',',
                     as_sep: str = ';') -> typing.List[AttrValsT]:
    """
    Simple parser to parse expressions in the form of
    [ATTR1:VAL0,VAL1,...;ATTR2:VAL0,VAL2,..].

    :param str_: input string
    :param avs_sep:  char to separate attribute and values
    :param vs_sep:  char to separate values
    :param as_sep:  char to separate attributes

    :return:
        a list of tuples of (key, value | [value])
            where key = (Int | String | ...),
            value = (Int | Bool | String | ...) | [Int | Bool | String | ...]

    >>> parse_attrlist_0('a:1')
    [('a', 1)]
    >>> parse_attrlist_0('a:1;b:xyz')
    [('a', 1), ('b', 'xyz')]
    >>> parse_attrlist_0('requires:bash,zsh')
    [('requires', ['bash', 'zsh'])]
    >>> parse_attrlist_0('obsoletes:sysdata;conflicts:sysdata-old')
    [('obsoletes', 'sysdata'), ('conflicts', 'sysdata-old')]
    """
    return list(attr_val_itr(str_, avs_sep, vs_sep, as_sep))


AttrValsDictT = typing.Dict[str, typing.Union[PrimitivesT, PrimitiveT]]


def parse_attrlist(str_: str, avs_sep: str = ':', vs_sep: str = ',',
                   as_sep: str = ';') -> AttrValsDictT:
    """
    Simple parser to parse expressions in the form of
    [ATTR1:VAL0,VAL1,...;ATTR2:VAL0,VAL2,..].

    :param str_: input string
    :param avs_sep:  char to separate attribute and values
    :param vs_sep:  char to separate values
    :param as_sep:  char to separate attributes

    >>> parse_attrlist('requires:bash,zsh')
    {'requires': ['bash', 'zsh']}
    """
    return dict(parse_attrlist_0(str_, avs_sep, vs_sep, as_sep))


ResultsT = typing.Union[
    PrimitiveT,
    PrimitivesT,
    AttrValsDictT
]


def parse(str_: str, lsep: str = ',', avsep: str = ':', vssep: str = ',',
          avssep: str = ';') -> ResultsT:
    """Generic parser"""
    if avsep in str_:
        return parse_attrlist(str_, avsep, vssep, avssep)
    if lsep in str_:
        return parse_list(str_, lsep)

    return parse_single(str_)

# vim:sw=4:ts=4:et:
