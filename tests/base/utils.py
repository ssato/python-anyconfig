#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""File based test data collector.
"""
import ast
import importlib.util
import json
import pathlib
import typing
import warnings

from .datatypes import (
    DictT, MaybePathT, TDataPaths
)


def target_by_parent(self: str = __file__):
    """
    >>> target_by_parent()
    'base'
    """
    return pathlib.Path(self).parent.name


def load_from_py(py_path: typing.Union[str, pathlib.Path],
                 data_name: str = 'DATA') -> DictT:
    """.. note:: It's not safe always.
    """
    spec = importlib.util.spec_from_file_location('testmod', py_path)
    mod = spec.loader.load_module()
    return getattr(mod, data_name, None)


def load_literal_data_from_py(py_path: typing.Union[str, pathlib.Path]
                              ) -> DictT:
    """.. note:: It might be safer than the above function.
    """
    return ast.literal_eval(pathlib.Path(py_path).read_text().strip())


def maybe_data_path(datadir: pathlib.Path, name: str,
                    should_exist: typing.Iterable[str] = (),
                    file_ext: str = '*'
                    ) -> typing.Optional[pathlib.Path]:
    """
    Get and return the file path of extra data file. Its filename will be
    computed from the filename of the base data file given.
    """
    pattern = f'{name}.{file_ext}'
    if datadir.exists() and datadir.is_dir():
        paths = sorted(datadir.glob(pattern))
        if paths:
            return paths[0]  # There should be just one file found.

    if datadir.name in should_exist:
        raise OSError(f'{datadir!s}/{pattern} should exists but not')

    return None


def load_data(path: MaybePathT,
              default: typing.Optional[typing.Any] = None,
              should_exist: bool = False,
              exec_py: bool = False
              ) -> typing.Union[DictT, str]:
    """
    Return data loaded from given path or the default value.
    """
    if path is None and not should_exist:
        return default

    if path.exists():
        if path.suffix == '.json':
            return json.load(path.open())

        if path.suffix == '.py':
            return (
                load_from_py if exec_py else load_literal_data_from_py
            )(path)

        if path.suffix == '.txt':
            return path.read_text()

        return path

    raise ValueError(f'Not exist or an invalid data: {path!s}')


def each_data_from_dir(datadir: pathlib.Path, pattern: str = '*.json',
                       should_exist: typing.Iterable[str] = ()
                       ) -> typing.Iterator[TDataPaths]:
    """
    Yield a collection of paths of data files under given dir.
    """
    if not datadir.is_dir():
        raise ValueError(f'Not look a data dir: {datadir!s}')

    for inp in sorted(datadir.glob(pattern)):
        if not inp.exists():
            warnings.warn(f'Not exists: {inp!s}')
            continue

        if not inp.is_file():
            warnings.warn(f'Not looks a file: {inp!s}')
            continue

        name = inp.stem

        yield TDataPaths(
            datadir,
            inp,
            maybe_data_path(datadir / 'e', name, should_exist),
            maybe_data_path(datadir / 'o', name, should_exist),
            maybe_data_path(datadir / 's', name, should_exist),
            maybe_data_path(datadir / 'q', name, should_exist),
            maybe_data_path(datadir / 'c', name, should_exist)
        )

# vim:sw=4:ts=4:et:
