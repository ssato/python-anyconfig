#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""Collector to collect file based test data.
"""
import pathlib
import typing

from ... import base
from .datatypes import TData
from .utils import each_data_from_dir


class DataCollector:
    """Data collector for api.multi_load
    """
    target: str = 'multi_load'
    kind: str = 'basics'
    pattern: str = '*.json'  # input file name pattern

    # expected data files should be found always.
    should_exist: typing.Iterable[str] = ('e', )

    root: typing.Optional[pathlib.Path] = None
    datasets: typing.List[TData] = []
    initialized: bool = False

    def init(self):
        """Initialize its members.
        """
        self.root = base.RES_DIR / self.target / self.kind
        self.datasets = self.load_datasets()
        self.initialized = True

    def load_datasets(self) -> typing.List[TData]:
        """Load test data from files.
        """
        _datasets = sorted(
            each_data_from_dir(self.root, self.pattern, self.should_exist)
        )
        if not _datasets:
            raise ValueError(f'No data: {self.root!s}')

        for tdata in _datasets:
            if not tdata.inputs:
                raise ValueError(f'No data in subdir: {tdata.subdir!s}')

        return _datasets

    def each_data(self) -> typing.Iterator[TData]:
        """Yields test data.
        """
        if not self.initialized:
            self.init()

        for tdata in self.datasets:
            yield tdata

# vim:sw=4:ts=4:et:
