#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
"""Abstract and basic dumpes."""
import io
import typing

from ... import ioinfo, utils
from .datatypes import (
    InDataExT, IoiT
)
from .utils import (
    ensure_outdir_exists, not_implemented
)


class DumperMixin:
    """Mixin class to dump data.

    Inherited classes must implement the following methods.

    - :meth:`dump_to_string`: Dump config as a string
    - :meth:`dump_to_stream`: Dump config to a file or file-like object
    - :meth:`dump_to_path`: Dump config to a file of given path

    Member variables:

    - _dump_opts: Backend specific options on dump
    - _open_write_mode: Backend option to specify write mode passed to open()
    """

    _dump_opts: typing.List[str] = []
    _open_write_mode = 'w'

    def wopen(self, filepath: str, **kwargs):
        """Open file ``filepath`` with the write mode ``_open_write_mode``."""
        return open(  # pylint: disable=consider-using-with
            filepath, self._open_write_mode, **kwargs
        )

    def dump_to_string(self, cnf: InDataExT, **kwargs) -> str:
        """Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        not_implemented(self, cnf, **kwargs)
        return ''

    def dump_to_path(self, cnf: InDataExT, filepath: str, **kwargs) -> None:
        """Dump config 'cnf' to a file 'filepath'.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        not_implemented(self, cnf, filepath, **kwargs)

    def dump_to_stream(self, cnf: InDataExT, stream: typing.IO, **kwargs
                       ) -> None:
        """Dump config 'cnf' to a file-like object 'stream'.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        not_implemented(self, cnf, stream, **kwargs)

    def dumps(self, cnf: InDataExT, **kwargs) -> str:
        """Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: string represents the configuration
        """
        kwargs = utils.filter_options(self._dump_opts, kwargs)
        return self.dump_to_string(cnf, **kwargs)

    def dump(self, cnf: InDataExT, ioi: IoiT, **kwargs):
        """Dump config 'cnf' to output object of which 'ioi' referring.

        :param cnf: Configuration data to dump
        :param ioi:
            an 'anyconfig.cmmon.IOInfo' namedtuple object provides various
            info of input object to load data from

        :param kwargs: optional keyword parameters to be sanitized :: dict
        :raises IOError, OSError, AttributeError: When dump failed.
        """
        kwargs = utils.filter_options(self._dump_opts, kwargs)

        if ioinfo.is_stream(ioi):
            self.dump_to_stream(cnf, typing.cast(typing.IO, ioi.src), **kwargs)
        else:
            ensure_outdir_exists(ioi.path)
            self.dump_to_path(cnf, ioi.path, **kwargs)


class BinaryDumperMixin(DumperMixin):
    """Mixin class to dump binary (byte string) configuration data."""

    _open_write_mode: str = 'wb'


class ToStringDumperMixin(DumperMixin):
    """Abstract config parser provides the followings.

    - a method to dump configuration to a file or file-like object (stream) and
      a file of given path to help implement parser of which backend lacks of
      such functions.

    Parser classes inherit this class have to override the method
    :meth:`dump_to_string` at least.
    """

    def dump_to_path(self, cnf: InDataExT, filepath: str, **kwargs) -> None:
        """Dump config 'cnf' to a file 'filepath'.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            out.write(self.dump_to_string(cnf, **kwargs))

    def dump_to_stream(self, cnf: InDataExT, stream: typing.IO, **kwargs
                       ) -> None:
        """Dump config 'cnf' to a file-like object 'stream'.

        TODO: How to process socket objects same as file objects ?

        :param cnf: Configuration data to dump
        :param stream:  Config file or file like object
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        stream.write(self.dump_to_string(cnf, **kwargs))


class ToStreamDumperMixin(DumperMixin):
    """Abstract config parser provides the following methods.

    - to dump configuration to a string content or a file of given path to help
      implement parser of which backend lacks of such functions.

    Parser classes inherit this class have to override the method
    :meth:`dump_to_stream` at least.
    """

    def dump_to_string(self, cnf: InDataExT, **kwargs) -> str:
        """Dump config 'cnf' to a string.

        :param cnf: Configuration data to dump
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        stream = io.StringIO()
        self.dump_to_stream(cnf, stream, **kwargs)
        return stream.getvalue()

    def dump_to_path(self, cnf: InDataExT, filepath: str, **kwargs) -> None:
        """Dump config 'cnf' to a file 'filepath`.

        :param cnf: Configuration data to dump
        :param filepath: Config file path
        :param kwargs: optional keyword parameters to be sanitized :: dict
        """
        with self.wopen(filepath) as out:
            self.dump_to_stream(cnf, out, **kwargs)

# vim:sw=4:ts=4:et:
