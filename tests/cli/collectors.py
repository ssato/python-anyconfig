#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""Provides base class to collect test data for cli test cases.
"""
from .. import base
from . import datatypes


class Collector(base.TDataCollector):

    def load_data(self, data):
        """Load dataset and make an object keeps it.
        """
        exp_data = base.load_data(data.exp)
        exp = datatypes.Expected(**exp_data)

        return datatypes.TData(
            data.datadir,
            data.inp,
            base.load_data(data.inp) or [],
            exp
        )

# vim:sw=4:ts=4:et:
