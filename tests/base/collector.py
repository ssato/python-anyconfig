#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""File based test data collector.
"""
import inspect
import pathlib
import typing

from . import (
    constants, datatypes, utils
)


DICT_0 = dict()


class TDataCollector:
    """File based test data collector.
    """
    target: str = ''  # Initial value will be replaced in self.init.
    kind: str = 'basics'
    pattern: str = '*.json'  # input file name pattern

    # sub dir names of expected data files should be found always.
    should_exist: typing.Iterable[str] = ('e', )

    # True if you want to keep the order of keys of dicts loaded.
    ordered: bool = False

    root: typing.Optional[pathlib.Path] = None
    datasets: typing.List[datatypes.TData] = []
    initialized: bool = False

    @classmethod
    def resolve_target(cls) -> str:
        """
        Resolve target by this file path.
        """
        return utils.target_by_parent(inspect.getfile(cls))

    def init(self) -> None:
        """Initialize its members.
        """
        if not self.target:
            self.target = self.resolve_target()

        if not self.root:
            self.root = constants.RES_DIR / self.target / self.kind

        self.datasets = self.load_datasets()
        self.initialized = True

    def load_datasets(self) -> typing.List[datatypes.TData]:
        """Load test data from files.
        """
        _datasets = [
            (datadir,
             [datatypes.TData(
                data.datadir, data.inp,
                utils.load_data(data.inp, ordered=self.ordered),
                utils.load_data(data.exp, ordered=self.ordered),
                utils.load_data(data.opts, default=DICT_0),
                data.scm,
                utils.load_data(data.query, default=''),
                utils.load_data(data.ctx, default=DICT_0, ordered=self.ordered)
              )
              for data in utils.each_data_from_dir(
                  datadir, self.pattern, self.should_exist
              )]
             )
            for datadir in sorted(self.root.glob('*'))
        ]
        if not _datasets:
            raise ValueError(f'No data: {self.root!s}')

        for datadir, data in _datasets:
            if not data:
                raise ValueError(
                    f'No data in subdir: {datadir!s}, '
                    f'pattern={self.pattern}, '
                    f'should_exist={self.should_exist!r}'
                )

        return _datasets

    def each_data(self) -> typing.Iterable[datatypes.TData]:
        """Yields test data.
        """
        if not self.initialized:
            self.init()

        for _datadir, data in self.datasets:
            for tdata in data:
                yield tdata

# vim:sw=4:ts=4:et:
