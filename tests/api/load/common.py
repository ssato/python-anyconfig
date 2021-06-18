#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.api._load as TT


class Basa:
    @staticmethod
    def target_fn(*args, **kwargs):
        return TT.load(*args, **kwargs)


class MultiBase:
    target: str = 'load/multi'


class SingleBase:
    target: str = 'load/single'

# vim:sw=4:ts=4:et:
