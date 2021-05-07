#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Abstract and basic dumpes.
"""
import io
import typing

from ... import utils
from .datatypes import (
    InDataT, IoiT
)
from .mixins import TextFilesMixin
from .utils import (
    ensure_outdir_exists, not_implemented
)


class DumperMixin:
    """
    Mixin class to dump data.

    Inherited classes must implement the following methods.

    - :meth:`dump_to_string`: Dump config as a string
    - :meth:`dump_to_stream`: Dump config to a file or file-like object
    - :meth:`dump_to_path`: Dump config to a file of given path

    Member variables:

    - _dump_opts: Backend specific options on dump
    """
    _dump_opts: typing.List[str] = []

    def dump_to_string(self, cnf: InDataT, **kwargs) -> str:
        """
        Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        not_implemented(self, cnf, **kwargs)
        return ''

    def dump_to_path(self, cnf: InDataT, filepath: str, **kwargs) -> None:
        """
        Dump config 'cnf' to a file 'filepath'.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        not_implemented(self, cnf, filepath, **kwargs)

    def dump_to_stream(self, cnf: InDataT, stream: typing.IO, **kwargs
                       ) -> None:
        """
        Dump config 'cnf' to a file-like object 'stream'.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        not_implemented(self, cnf, stream, **kwargs)

    def dumps(self, cnf: InDataT, **kwargs) -> str:
        """
        Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        kwargs = utils.filter_options(self._dump_opts, kwargs)
        return self.dump_to_string(cnf, **kwargs)

    def dump(self, cnf: InDataT, ioi: IoiT, **kwargs):
        """
        Dump config 'cnf' to output object of which 'ioi' refering.

        :param cnf: Configuration data to dump
        :param ioi:
            an 'anyconfig.cmmon.IOInfo' namedtuple object provides various
            info of input object to load data from

        :param kwargs: optional keyword parameters to be sanitized :: dict
        :raises IOError, OSError, AttributeError: When dump failed.
        """
        kwargs = utils.filter_options(self._dump_opts, kwargs)

        if utils.is_stream_ioinfo(ioi):
            self.dump_to_stream(cnf, typing.cast(typing.IO, ioi.src), **kwargs)
        else:
            ensure_outdir_exists(ioi.path)
            self.dump_to_path(cnf, ioi.path, **kwargs)


class ToStringDumperMixin(DumperMixin, TextFilesMixin):
    """
    Abstract config parser provides a method to dump configuration to a file or
    file-like object (stream) and a file of given path to help implement parser
    of which backend lacks of such functions.

    Parser classes inherit this class have to override the method
    :meth:`dump_to_string` at least.
    """
    def dump_to_path(self, cnf: InDataT, filepath: str, **kwargs) -> None:
        """
        Dump config 'cnf' to a file 'filepath'.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            out.write(self.dump_to_string(cnf, **kwargs))

    def dump_to_stream(self, cnf: InDataT, stream: typing.IO, **kwargs
                       ) -> None:
        """
        Dump config 'cnf' to a file-like object 'stream'.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        stream.write(self.dump_to_string(cnf, **kwargs))


class ToStreamDumperMixin(DumperMixin, TextFilesMixin):
    """
    Abstract config parser provides methods to dump configuration to a string
    content or a file of given path to help implement parser of which backend
    lacks of such functions.

    Parser classes inherit this class have to override the method
    :meth:`dump_to_stream` at least.
    """
    def dump_to_string(self, cnf: InDataT, **kwargs) -> str:
        """
        Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        stream = io.StringIO()
        self.dump_to_stream(cnf, stream, **kwargs)
        return stream.getvalue()

    def dump_to_path(self, cnf: InDataT, filepath: str, **kwargs) -> None:
        """
        Dump config 'cnf' to a file 'filepath`.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            self.dump_to_stream(cnf, out, **kwargs)

# vim:sw=4:ts=4:et:
