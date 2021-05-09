#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
r"""A class collect anyconfig.models.processor.Processor and inherited class
objects inherited from it.
"""
import operator
import typing

from ..common import PathOrIOInfoT
from . import utils
from .common import (
    ProcT, ProcClsT, ProcClssT
)


class Processors:
    """An abstract class of which instance holding processors.
    """
    _pgroup: str = ''  # processor group name to load plugins

    def __init__(self, processors: typing.Optional[ProcClssT] = None) -> None:
        """
        :param processors:
            A list of :class:`anyconfig.models.processor.Processor` or its
            children class objects to initialize this, or None
        """
        # {<processor_class_id>: <processor_class>}
        self._processors: typing.Dict[str, ProcClsT] = dict()
        if processors is not None:
            for pcls in processors:
                self.register(pcls)

        self.load_plugins()

    def register(self, pcls: ProcClsT) -> None:
        """
        :param pclss: :class:`Processor` or its children class objects
        """
        if pcls.cid() not in self._processors:
            self._processors[pcls.cid()] = pcls

    def load_plugins(self) -> None:
        """Load and register pluggable processor classes internally.
        """
        if self._pgroup:
            for pcls in utils.load_plugins(self._pgroup):
                self.register(pcls)

    def list(self, sort: bool = False) -> ProcClssT:
        """
        :param sort: Result will be sorted if it's True
        :return: A list of :class:`Processor` or its children classes
        """
        prs = self._processors.values()
        if sort:
            return sorted(prs, key=operator.methodcaller("cid"))

        return list(prs)

    def list_by_cid(self) -> typing.List[typing.Tuple[str, ProcClssT]]:
        """
        :return:
            A list of :class:`Processor` or its children classes grouped by
            each cid, [(cid, [:class:`Processor`)]]
        """
        prs = self._processors
        return sorted(((cid, [prs[cid]]) for cid in sorted(prs.keys())),
                      key=operator.itemgetter(0))

    def list_by_type(self) -> typing.List[typing.Tuple[str, ProcClssT]]:
        """
        :return:
            A list of :class:`Processor` or its children classes grouped by
            each type, [(type, [:class:`Processor`)]]
        """
        return utils.list_by_x(self.list(), "type")

    def list_by_x(self, item: typing.Optional[str] = None
                  ) -> typing.List[typing.Tuple[str, ProcClssT]]:
        """
        :param item: Grouping key, one of "cid", "type" and "extensions"
        :return:
            A list of :class:`Processor` or its children classes grouped by
            given 'item', [(cid, [:class:`Processor`)]] by default
        """
        prs = self._processors

        if item is None or item == "cid":  # Default.
            res = [(cid, [prs[cid]]) for cid in sorted(prs.keys())]

        elif item in ("type", "extensions"):
            res = utils.list_by_x(prs.values(), typing.cast(str, item))
        else:
            raise ValueError("keyword argument 'item' must be one of "
                             "None, 'cid', 'type' and 'extensions' "
                             "but it was '%s'" % item)
        return res

    def list_x(self, key: typing.Optional[str] = None) -> typing.List[str]:
        """
        :param key: Which of key to return from "cid", "type", and "extention"
        :return: A list of x 'key'
        """
        if key in ("cid", "type"):
            return sorted(set(operator.methodcaller(key)(p)
                              for p in self._processors.values()))
        if key == "extension":
            return sorted(k for k, _v in self.list_by_x("extensions"))

        raise ValueError("keyword argument 'key' must be one of "
                         "None, 'cid', 'type' and 'extension' "
                         "but it was '%s'" % key)

    def findall(self, obj: typing.Optional[PathOrIOInfoT],
                forced_type: typing.Optional[str] = None
                ) -> typing.List[ProcT]:
        """
        :param obj:
            a file path, file, file-like object, pathlib.Path object or an
            'anyconfig.common.IOInfo' (namedtuple) object
        :param forced_type: Forced processor type to find
        :param cls: A class object to compare with 'ptype'

        :return: A list of instances of processor classes to process 'obj'
        :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
        """
        return [
            p() for p
            in utils.findall(obj, self.list(), forced_type=forced_type)
        ]

    def find(self, obj: typing.Optional[PathOrIOInfoT],
             forced_type: typing.Optional[str] = None) -> ProcT:
        """
        :param obj:
            a file path, file, file-like object, pathlib.Path object or an
            'anyconfig.common.IOInfo' (namedtuple) object
        :param forced_type: Forced processor type to find
        :param cls: A class object to compare with 'ptype'

        :return: an instance of processor class to process 'obj'
        :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
        """
        return utils.find(obj, self.list(), forced_type=forced_type)

# vim:sw=4:ts=4:et:
