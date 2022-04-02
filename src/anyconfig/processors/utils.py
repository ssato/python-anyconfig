#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unidiomatic-typecheck
"""Utility functions for anyconfig.processors."""
import operator
import typing
import warnings

import pkg_resources

from .. import common, ioinfo, models, utils
from .datatypes import (
    ProcT, ProcsT, ProcClsT, MaybeProcT
)


def sort_by_prio(prs: typing.Iterable[ProcT]) -> ProcsT:
    """Sort an iterable of processor classes by each priority.

    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :return: Sambe as above but sorted by priority
    """
    return sorted(prs, key=operator.methodcaller('priority'), reverse=True)


def select_by_key(
    items: typing.Iterable[
        typing.Tuple[typing.List[str], typing.Any]],
        sort_fn: typing.Callable[..., typing.Any] = sorted
) -> typing.List[
        typing.Tuple[str, typing.List[typing.Any]]
]:
    """Select items from ``items`` by key.

    :param items: A list of tuples of keys and values, [([key], val)]
    :return: A list of tuples of key and values, [(key, [val])]

    >>> select_by_key([(['a', 'aaa'], 1), (['b', 'bb'], 2), (['a'], 3)])
    [('a', [1, 3]), ('aaa', [1]), ('b', [2]), ('bb', [2])]
    """
    itr = utils.concat(((k, v) for k in ks) for ks, v in items)
    return list((k, sort_fn(t[1] for t in g))
                for k, g in utils.groupby(itr, operator.itemgetter(0)))


def list_by_x(prs: typing.Iterable[ProcT], key: str
              ) -> typing.List[typing.Tuple[str, ProcsT]]:
    """List items by the factor 'x'.

    :param key: Grouping key, 'type' or 'extensions'
    :return:
        A list of :class:`Processor` or its children classes grouped by
        given 'item', [(cid, [:class:`Processor`)]] by default
    """
    if key == 'type':
        kfn = operator.methodcaller(key)
        res = sorted(((k, sort_by_prio(g)) for k, g
                      in utils.groupby(prs, kfn)),
                     key=operator.itemgetter(0))

    elif key == 'extensions':
        res: typing.List[  # type: ignore
            typing.Tuple[str, ProcsT]
        ] = select_by_key(((p.extensions(), p) for p in prs),
                          sort_fn=sort_by_prio)
    else:
        raise ValueError(
            f"Argument 'key' must be 'type' or 'extensions' but it was '{key}'"
        )

    return res


def findall_with_pred(predicate: typing.Callable[..., bool],
                      prs: ProcsT) -> ProcsT:
    """Find all of the items match with given predicates.

    :param predicate: any callable to filter results
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :return: A list of appropriate processor classes or []
    """
    return sorted((p for p in prs if predicate(p)),
                  key=operator.methodcaller('priority'), reverse=True)


def maybe_processor(type_or_id: typing.Union[ProcT, ProcClsT],
                    cls: ProcClsT = models.processor.Processor
                    ) -> typing.Optional[ProcT]:
    """Try to get the processor.

    :param type_or_id:
        Type of the data to process or ID of the processor class or
        :class:`anyconfig.models.processor.Processor` class object or its
        instance
    :param cls: A class object to compare with 'type_or_id'
    :return: Processor instance or None
    """
    if isinstance(type_or_id, cls):
        return type_or_id

    try:
        if issubclass(typing.cast(ProcClsT, type_or_id), cls):
            return type_or_id()  # type: ignore
    except TypeError:
        pass

    return None


def find_by_type_or_id(type_or_id: str, prs: ProcsT) -> ProcsT:
    """Find the processor by types or IDs.

    :param type_or_id: Type of the data to process or ID of the processor class
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :return:
        A list of processor classes to process files of given data type or
        processor 'type_or_id' found by its ID
    :raises: anyconfig.common.UnknownProcessorTypeError
    """
    def pred(pcls):
        """Provide a predicate."""
        return pcls.cid() == type_or_id or pcls.type() == type_or_id

    pclss = findall_with_pred(pred, prs)
    if not pclss:
        raise common.UnknownProcessorTypeError(type_or_id)

    return pclss


def find_by_fileext(fileext: str, prs: ProcsT) -> ProcsT:
    """Find the processor by file extensions.

    :param fileext: File extension
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :return: A list of processor class to processor files with given extension
    :raises: common.UnknownFileTypeError
    """
    def pred(pcls):
        """Provide a predicate."""
        return fileext in pcls.extensions()

    pclss = findall_with_pred(pred, prs)
    if not pclss:
        raise common.UnknownFileTypeError(f'file extension={fileext}')

    return pclss  # :: [Processor], never []


def find_by_maybe_file(obj: ioinfo.PathOrIOInfoT, prs: ProcsT) -> ProcsT:
    """Find the processor appropariate for the given file ``obj``.

    :param obj:
        a file path, file or file-like object, pathlib.Path object or an
        'anyconfig.ioinfo.IOInfo' (namedtuple) object
    :param cps_by_ext: A list of processor classes
    :return: A list of processor classes to process given (maybe) file
    :raises: common.UnknownFileTypeError
    """
    # :: [Processor], never []
    return find_by_fileext(ioinfo.make(obj).extension, prs)


def findall(obj: typing.Optional[ioinfo.PathOrIOInfoT], prs: ProcsT,
            forced_type: typing.Optional[str] = None,
            ) -> ProcsT:
    """Find all of the processors match with the conditions.

    :param obj:
        a file path, file, file-like object, pathlib.Path object or an
        'anyconfig.ioinfo.IOInfo` (namedtuple) object
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :param forced_type:
        Forced processor type of the data to process or ID of the processor
        class or None

    :return: A list of instances of processor classes to process 'obj' data
    :raises:
        ValueError, common.UnknownProcessorTypeError,
        common.UnknownFileTypeError
    """
    if (obj is None or not obj) and forced_type is None:
        raise ValueError(
            "The first argument 'obj' or the second argument 'forced_type' "
            "must be something other than None or False."
        )

    if forced_type is None:
        pclss = find_by_maybe_file(typing.cast(ioinfo.PathOrIOInfoT, obj),
                                   prs)  # :: [Processor], never []
    else:
        pclss = find_by_type_or_id(forced_type, prs)  # Do.

    return pclss


def find(obj: typing.Optional[ioinfo.PathOrIOInfoT], prs: ProcsT,
         forced_type: MaybeProcT = None,
         ) -> ProcT:
    """Find the processors best match with the conditions.

    :param obj:
        a file path, file, file-like object, pathlib.Path object or an
        'anyconfig.ioinfo.IOInfo' (namedtuple) object
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :param forced_type:
        Forced processor type of the data to process or ID of the processor
        class or :class:`anyconfig.models.processor.Processor` class object or
        its instance itself
    :param cls: A class object to compare with 'forced_type' later

    :return: an instance of processor class to process 'obj' data
    :raises:
        ValueError, common.UnknownProcessorTypeError,
        common.UnknownFileTypeError
    """
    if forced_type is not None and not isinstance(forced_type, str):
        proc = maybe_processor(
            typing.cast(typing.Union[ProcT, ProcClsT], forced_type)
        )
        if proc is None:
            raise ValueError('Wrong processor class or instance '
                             f'was given: {forced_type!r}')

        return proc

    procs = findall(obj, prs, forced_type=typing.cast(str, forced_type))
    return procs[0]


def load_plugins(pgroup: str) -> typing.Iterator[ProcClsT]:
    """Load processor plugins.

    A generator function to yield a class object of
    :class:`anyconfig.models.processor.Processor`.

    :param pgroup: A string represents plugin type, e.g. anyconfig_backends
    """
    for res in pkg_resources.iter_entry_points(pgroup):
        try:
            yield res.load()
        except ImportError as exc:
            warnings.warn(f'Failed to load plugin, exc={exc!s}')

# vim:sw=4:ts=4:et:
