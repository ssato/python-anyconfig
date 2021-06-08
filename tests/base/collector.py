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

from anyconfig.api import InDataExT

from .common import RES_DIR


DictT = typing.Dict[str, typing.Any]
MaybePathT = typing.Optional[pathlib.Path]


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


class TDataPaths(typing.NamedTuple):
    """A namedtuple object keeps test data paths."""
    datadir: pathlib.Path
    inp: pathlib.Path
    exp: MaybePathT
    opts: MaybePathT
    scm: MaybePathT
    query: MaybePathT
    ctx: MaybePathT


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
        paths = list(datadir.glob(pattern))
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


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data.
    """
    datadir: pathlib.Path
    inp_path: pathlib.Path
    inp: InDataExT
    exp: DictT
    opts: DictT
    scm: typing.Union[pathlib.Path, str]
    query: typing.Union[pathlib.Path, str]
    ctx: DictT


DICT_0 = dict()


class TDataCollector:
    """File based test data collector.
    """
    target = 'base'
    kind = 'basics'
    pattern = '*.json'  # input file name pattern
    should_exist = ('e', )  # expected data files should be found always.

    root = None
    datasets = []
    initialized = False

    def init(self):
        """Initialize its members.
        """
        self.root = RES_DIR / self.target / self.kind
        self.datasets = self.load_datasets()
        self.initialized = True

    def load_datasets(self):
        """Load test data from files.
        """
        _datasets = [
            (datadir,
             [TData(data.datadir, data.inp,
                    load_data(data.inp),
                    load_data(data.exp),
                    load_data(data.opts, default=DICT_0),
                    data.scm,
                    load_data(data.query, default=''),
                    load_data(data.ctx, default=DICT_0)
                    )
              for data in each_data_from_dir(
                  datadir, self.pattern, self.should_exist
              )]
             )
            for datadir in sorted(self.root.glob('*'))
        ]
        if not _datasets:
            raise ValueError(f'No data: {self.root!s}')

        for datadir, data in _datasets:
            if not data:
                raise ValueError(f'No data in subdir: {datadir!s}')

        return _datasets

    def each_data(self):
        """Yields test data.
        """
        if not self.initialized:
            self.init()

        for _datadir, data in self.datasets:
            for tdata in data:
                yield tdata

# vim:sw=4:ts=4:et:
