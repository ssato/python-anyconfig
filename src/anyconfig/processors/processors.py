#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
"""A collection of models.processor.Processor and children classes."""
import operator
import typing

from . import utils
from .datatypes import (
    ProcT, ProcsT, ProcClsT, ProcClssT, MaybeProcT
)

if typing.TYPE_CHECKING:
    from .. import ioinfo


class Processors:
    """An abstract class of which instance holding processors."""

    _pgroup: str = ''  # processor group name to load plugins

    def __init__(self, processors: typing.Optional[ProcClssT] = None) -> None:
        """Initialize with ``processors``.

        :param processors:
            A list of :class:`anyconfig.models.processor.Processor` or its
            children class objects to initialize this, or None
        """
        # {<processor_class_id>: <processor_instance>}
        self._processors: typing.Dict[str, ProcT] = {}  # type: ignore
        if processors is not None:
            for pcls in processors:
                self.register(pcls)

        self.load_plugins()

    def register(self, pcls: ProcClsT) -> None:
        """Register processor or its children class objects."""
        if pcls.cid() not in self._processors:
            self._processors[pcls.cid()] = pcls()

    def load_plugins(self) -> None:
        """Load and register pluggable processor classes internally."""
        if self._pgroup:
            for pcls in utils.load_plugins(self._pgroup):
                self.register(pcls)

    def list(self, sort: bool = False) -> ProcClssT:
        """List processors.

        :param sort: Result will be sorted if it's True
        :return: A list of :class:`Processor` or its children classes
        """
        prs = self._processors.values()
        if sort:
            return sorted(prs, key=operator.methodcaller('cid'))

        return list(prs)

    def list_by_cid(self) -> typing.List[typing.Tuple[str, ProcsT]]:
        """List processors by those IDs.

        :return:
            A list of :class:`Processor` or its children classes grouped by
            each cid, [(cid, [:class:`Processor`)]]
        """
        prs = self._processors
        return sorted(((cid, [prs[cid]]) for cid in sorted(prs.keys())),
                      key=operator.itemgetter(0))

    def list_by_type(self) -> typing.List[typing.Tuple[str, ProcsT]]:
        """List processors by those types.

        :return:
            A list of :class:`Processor` or its children classes grouped by
            each type, [(type, [:class:`Processor`)]]
        """
        return utils.list_by_x(self.list(), 'type')  # type: ignore

    def list_by_x(self, item: typing.Optional[str] = None
                  ) -> typing.List[typing.Tuple[str, ProcsT]]:
        """List processors by those factor 'x'.

        :param item: Grouping key, one of 'cid', 'type' and 'extensions'
        :return:
            A list of :class:`Processor` or its children classes grouped by
            given 'item', [(cid, [:class:`Processor`)]] by default
        """
        prs = self._processors

        if item is None or item == 'cid':  # Default.
            res = [(cid, [prs[cid]]) for cid in sorted(prs.keys())]

        elif item in ('type', 'extensions'):
            res = utils.list_by_x(prs.values(), typing.cast(str, item))
        else:
            raise ValueError("keyword argument 'item' must be one of "
                             "None, 'cid', 'type' and 'extensions' "
                             f"but it was '{item}'")
        return res

    def list_x(self, key: typing.Optional[str] = None) -> typing.List[str]:
        """List the factor 'x' of processors.

        :param key: Which of key to return from 'cid', 'type', and 'extention'
        :return: A list of x 'key'
        """
        if key in ('cid', 'type'):
            return sorted(set(operator.methodcaller(key)(p)
                              for p in self._processors.values()))
        if key == 'extension':
            return sorted(k for k, _v in self.list_by_x('extensions'))

        raise ValueError("keyword argument 'key' must be one of "
                         "None, 'cid', 'type' and 'extension' "
                         f"but it was '{key}'")

    def findall(self, obj: typing.Optional['ioinfo.PathOrIOInfoT'],
                forced_type: typing.Optional[str] = None
                ) -> typing.List[ProcT]:
        """Find all of the processors match with tthe given conditions.

        :param obj:
            a file path, file, file-like object, pathlib.Path object or an
            'anyconfig.ioinfo.IOInfo' (namedtuple) object
        :param forced_type: Forced processor type to find

        :return: A list of instances of processor classes to process 'obj'
        :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
        """
        return utils.findall(obj, self.list(), forced_type=forced_type)

    def find(self, obj: typing.Optional['ioinfo.PathOrIOInfoT'],
             forced_type: MaybeProcT = None) -> ProcT:
        """Find the processor best match with tthe given conditions.

        :param obj:
            a file path, file, file-like object, pathlib.Path object or an
            'anyconfig.ioinfo.IOInfo' (namedtuple) object
        :param forced_type:
            Forced processor type to find or a processor class object or a
            processor intance

        :return: an instance of processor class to process 'obj'
        :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
        """
        return utils.find(obj, self.list(), forced_type=forced_type)

# vim:sw=4:ts=4:et:
