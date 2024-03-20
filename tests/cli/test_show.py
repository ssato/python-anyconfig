#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main without arguments to show info.
"""
import anyconfig.api

from . import collectors, datatypes, test_base


class Collector(collectors.Collector):
    kind = 'show'


class TestCase(test_base.NoInputTestCase):
    collector = Collector()


class VersionCollector(collectors.Collector):
    kind = 'show_version'

    def load_dataset(self, datadir, inp):
        ver = '.'.join(anyconfig.api.version())
        tdata = super().load_dataset(datadir, inp)

        return datatypes.TData(
            tdata.datadir, tdata.inp_path, tdata.opts,
            datatypes.Expected(words_in_stdout=ver)
        )


class VersionTestCase(test_base.NoInputTestCase):
    collector = VersionCollector()

# vim:sw=4:ts=4:et:
