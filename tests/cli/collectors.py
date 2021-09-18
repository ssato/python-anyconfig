#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""Provides base class to collect test data for cli test cases.
"""
import pathlib
import typing

from .. import base
from . import datatypes


class Collector(base.TDataCollector):
    """Test data collector for test cases with no file outputs.

    .. seealso:: tests.base.collector.TDataCollector
    """
    def load_dataset(self, datadir: pathlib.Path, inp: pathlib.Path):
        """
        .. seealso:: tests.base.collector.TDataCollector.load_dataset
        """
        name = inp.stem
        opts = base.maybe_data_path(datadir / 'o', name, self.should_exist)
        exp_data = base.load_data(
            base.maybe_data_path(datadir / 'e', name, self.should_exist)
        )
        outname = base.maybe_data_path(datadir / 'on', name, self.should_exist)
        ref = base.maybe_data_path(datadir / 'r', name, self.should_exist)
        oo_opts = base.maybe_data_path(datadir / 'oo', name, self.should_exist)
        scm = base.maybe_data_path(datadir / 's', name, self.should_exist)

        return datatypes.TData(
            datadir,
            inp,
            base.load_data(opts, default=[]),
            datatypes.Expected(**exp_data),
            base.load_data(outname, default=''),
            base.load_data(ref),
            base.load_data(oo_opts, default={}),
            scm or None
        )


class MultiDataCollector(base.TDataCollector):
    """Test data collector for test cases with no file outputs.

    .. seealso:: tests.base.collector.TDataCollector
    """
    def load_data_from_dir(self, datadir: pathlib.Path):
        """
        .. seealso:: tests.base.collector.TDataCollector.load_dataset
        .. seealso:: tests.base.utils.each_data_from_dir
        """
        if not datadir.is_dir():
            raise ValueError(f'Not look a data dir: {datadir!s}')

        # There should be multiple input files match with self.pattern.
        inputs = sorted(datadir.glob(self.pattern))
        if not inputs:
            raise ValueError(f'No any inputs in: {datadir!s}')

        for inp in inputs:
            if not inp.is_file():
                raise ValueError(f'Not a file: {inp!s} in {datadir!s}')

        name = inputs[0].stem

        # Load a glob pattern or a list of inputs.
        inp_data = base.load_data(
            base.maybe_data_path(datadir / 'i', name, self.should_exist)
        ) or '*.json'

        if isinstance(inp_data, list):
            inputs = [datadir / i for i in inp_data]
        else:
            if not isinstance(inp_data, str):
                raise ValueError(f'Invalid inputs: {inp_data} in {datadir!s}')
            inputs = [datadir / inp_data]

        opts = base.maybe_data_path(datadir / 'o', name, self.should_exist)
        exp_data = base.load_data(
            base.maybe_data_path(datadir / 'e', name, self.should_exist)
        )
        outname = base.maybe_data_path(datadir / 'on', name, self.should_exist)
        ref = base.maybe_data_path(datadir / 'r', name, self.should_exist)
        oo_opts = base.maybe_data_path(datadir / 'oo', name, self.should_exist)
        scm = base.maybe_data_path(datadir / 's', name, self.should_exist)

        return datatypes.TDataSet(
            datadir,
            inputs,
            base.load_data(opts, default=[]),
            datatypes.Expected(**exp_data),
            base.load_data(outname, default=''),
            base.load_data(ref),
            base.load_data(oo_opts, default={}),
            scm or None
        )

    def load_datasets(self) -> typing.List[datatypes.TData]:
        """Load test data from files.
        """
        _datasets = [
            (datadir, [self.load_data_from_dir(datadir)])
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

# vim:sw=4:ts=4:et:
