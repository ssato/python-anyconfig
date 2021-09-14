#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""File based test data collector.
"""
import pathlib
import typing


DictT = typing.Dict[str, typing.Any]


class Expected(typing.NamedTuple):
    """Keeps expected result's info.
    """
    exit_code: int = 0
    exit_code_matches: bool = True
    words_in_stdout: str = ''
    words_in_stderr: str = ''
    exception: BaseException = SystemExit


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data.
    """
    datadir: pathlib.Path
    inp_path: pathlib.Path
    args: typing.List[str] = []
    exp: Expected = Expected()

# vim:sw=4:ts=4:et:
