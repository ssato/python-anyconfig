#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""Basic data types for file based test data collectors.
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
    """A namedtuple object keeps test data to test cases with no file outputs.
    """
    datadir: pathlib.Path
    inp_path: pathlib.Path
    args: typing.List[str] = []
    exp: Expected = Expected()


class TData2(typing.NamedTuple):
    """A namedtuple object keeps test data to test cases with file outputs.
    """
    datadir: pathlib.Path
    inp_path: pathlib.Path
    opts: typing.List[str] = []
    exp: Expected = Expected()
    ref: DictT = {}

# vim:sw=4:ts=4:et:
