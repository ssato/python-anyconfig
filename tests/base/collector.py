#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""File based test data collector.
"""
from .common import RES_DIR
from .datatypes import TData
from .utils import load_data, each_data_from_dir


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
