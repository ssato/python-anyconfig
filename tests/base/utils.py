#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""File based test data collector.
"""
import ast
import collections
import importlib.abc
import importlib.util
import json
import pathlib
import typing
import warnings

from .datatypes import (
    DictT, MaybePathT, TData
)


DICT_0 = {}


def target_by_parent(self: str = __file__):
    """
    >>> target_by_parent()
    'base'
    """
    return pathlib.Path(self).parent.name


def load_from_py(py_path: typing.Union[str, pathlib.Path],
                 data_name: str = 'DATA') -> DictT:
    """Load from .py files.

    .. note:: It's not safe always.
    """
    spec = importlib.util.spec_from_file_location('testmod', py_path)
    if spec and isinstance(spec.loader, importlib.abc.Loader):
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            return getattr(mod, data_name, None)
        except (TypeError, ValueError, AttributeError):
            pass

    return {}


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
              exec_py: bool = False,
              ordered: bool = False
              ) -> typing.Union[DictT, str]:
    """
    Return data loaded from given path or the default value.
    """
    if path is None or not path:
        if not should_exist:
            return {} if default is None else default

    if path and path.exists():
        if path.suffix == '.json':
            if ordered:
                return json.load(
                    path.open(), object_hook=collections.OrderedDict
                )

            return json.load(path.open())

        if path.suffix == '.py':
            return (
                load_from_py if exec_py else load_literal_data_from_py
            )(path)  # type: ignore

        if path.suffix == '.txt':
            return path.read_text()

        return path

    raise ValueError(f'Not exist or an invalid data: {path!s}')


def each_data_from_dir(datadir: pathlib.Path,
                       data_factory: typing.Callable,
                       pattern: str = '*.json',
                       ) -> typing.Iterator[TData]:
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

        yield data_factory(datadir, inp)


def load_datasets_from_dir(datadir: pathlib.Path,
                           data_factory: typing.Callable,
                           **kwargs
                           ) -> typing.List[TData]:
    """
    Load a collection of datasets from given dir ``datadir``.
    """
    return list(
        each_data_from_dir(datadir, data_factory, **kwargs)
    )

# vim:sw=4:ts=4:et:
