#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""Provides base class to collect test data for cli test cases.
"""
import pathlib

from .. import base
from . import datatypes


class NoOutputDataCollector(base.TDataCollector):
    """Test data collector for test cases with no file outputs.
    """

    def load_dataset(self, datadir: pathlib.Path, inp: pathlib.Path):
        """Load dataset and make an object keeps it.

        .. seealso:: tests.base.collector.TDataCollector.load_dataset
        """
        name = inp.stem
        exp_data = base.load_data(
            base.maybe_data_path(datadir / 'e', name, self.should_exist)
        )

        return datatypes.NoOutputData(
            datadir,
            inp,
            base.load_data(inp) or [],
            datatypes.Expected(**exp_data)
        )

# vim:sw=4:ts=4:et:
