#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""Provides base class to collect test data for cli test cases.
"""
import pathlib

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

# vim:sw=4:ts=4:et:
