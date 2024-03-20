#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Collector to collect file based test data.
"""
import typing

from ... import base
from . import datatypes, utils


class DataCollector(base.TDataCollector):
    """Data collector for api.multi_load
    """
    def load_datasets(self) -> typing.List[datatypes.TData]:
        """Load test data from files.
        """
        _datasets = sorted(
            utils.each_data_from_dir(
                self.root, self.pattern, self.should_exist
            )
        )
        if not _datasets:
            raise ValueError(f'No data: {self.root!s}')

        for tdata in _datasets:
            if not tdata.inputs:
                raise ValueError(f'No data in subdir: {tdata.subdir!s}')

        return _datasets

    def each_data(self) -> typing.Iterator[datatypes.TData]:
        """Yields test data.
        """
        if not self.initialized:
            self.init()

        for tdata in self.datasets:
            yield tdata

# vim:sw=4:ts=4:et:
