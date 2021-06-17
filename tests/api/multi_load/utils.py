#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""File based test data collector - utility functions.
"""
import pathlib
import typing
import warnings

from ... import base
#    load_data, maybe_data_path,

from .datatypes import TData


# .. seealso:: tests.api.multi_load.datatypes
MaybeDataT = typing.Optional[
    typing.Union[str, pathlib.Path, typing.Dict[str, typing.Any]]
]


def load_data_or_path(datadir: pathlib.Path,
                      should_exist: typing.Iterable[str] = (),
                      load: bool = True,
                      default: typing.Optional[typing.Any] = None
                      ) -> MaybeDataT:
    """
    Load data from a file in the ``datadir`` of which name matches ``pattern``.
    """
    maybe_file = base.maybe_data_path(datadir, '*', should_exist=should_exist)
    if maybe_file is None:
        return default

    if load:
        return base.load_data(maybe_file)

    return maybe_file


def each_data_from_dir(datadir: pathlib.Path,
                       pattern: str = '*.json',
                       should_exist: typing.Iterable[str] = ()
                       ) -> typing.Iterator[TData]:
    """
    Yield a collection of paths of data files under given dir.
    """
    if not datadir.is_dir():
        raise ValueError(f'Not look a data dir: {datadir!s}')

    for subdir in sorted(datadir.glob('*')):
        if not subdir.is_dir():
            warnings.warn(f'Not looks a dir: {subdir!s}')
            continue

        if not bool(list(subdir.glob('*.*'))):
            warnings.warn(f'No data in subdir: {subdir!s}')
            continue

        yield TData(
            subdir,
            sorted(
                inp for inp in subdir.glob(pattern) if inp.is_file()
            ),
            load_data_or_path(subdir / 'e', should_exist, default={}),
            load_data_or_path(subdir / 'o', should_exist, default={}),
            load_data_or_path(subdir / 's', should_exist, load=False),
            load_data_or_path(subdir / 'q', should_exist, default=''),
            load_data_or_path(subdir / 'c', should_exist, default={}),
        )

# vim:sw=4:ts=4:et:
