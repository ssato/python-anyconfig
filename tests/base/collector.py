#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""File based test data collector.
"""
import pathlib

from . import (
    common, datatypes, utils
)


DICT_0 = dict()


class TDataCollector:
    """File based test data collector.
    """
    target = pathlib.Path(__file__).parent.name
    kind = 'basics'
    pattern = '*.json'  # input file name pattern
    should_exist = ('e', )  # expected data files should be found always.

    root = None
    datasets = []
    initialized = False

    def init(self):
        """Initialize its members.
        """
        self.root = common.RES_DIR / self.target / self.kind
        self.datasets = self.load_datasets()
        self.initialized = True

    def load_datasets(self):
        """Load test data from files.
        """
        _datasets = [
            (datadir,
             [datatypes.TData(
                data.datadir, data.inp,
                utils.load_data(data.inp),
                utils.load_data(data.exp),
                utils.load_data(data.opts, default=DICT_0),
                data.scm,
                utils.load_data(data.query, default=''),
                utils.load_data(data.ctx, default=DICT_0)
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

    def each_data(self):
        """Yields test data.
        """
        if not self.initialized:
            self.init()

        for _datadir, data in self.datasets:
            for tdata in data:
                yield tdata

# vim:sw=4:ts=4:et:
