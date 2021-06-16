#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Abstract and basic loaders.
"""
import collections
import io
import pathlib
import typing

from ...utils import (
    filter_options, is_stream_ioinfo
)
from .datatypes import (
    InDataExT, IoiT, GenContainerT, OptionsT
)
from .utils import not_implemented


DATA_DEFAULT: InDataExT = dict()


class LoaderMixin:
    """
    Mixin class to load data.

    Inherited classes must implement the following methods.

    - :meth:`load_from_string`: Load config from string
    - :meth:`load_from_stream`: Load config from a file or file-like object
    - :meth:`load_from_path`: Load config from file of given path

    Member variables:

    - _load_opts: Backend specific options on load
    - _ordered: True if the parser keep the order of items by default
    - _allow_primitives: True if the parser.load* may return objects of
      primitive data types other than mapping types such like JSON parser
    - _dict_opts: Backend options to customize dict class to make results
    - _open_read_mode: Backend option to specify read mode passed to open()
    """
    _load_opts: typing.List[str] = []
    _ordered: bool = False
    _allow_primitives: bool = False
    _dict_opts: typing.List[str] = []
    _open_read_mode: str = 'r'

    @classmethod
    def ordered(cls) -> bool:
        """
        :return: True if parser can keep the order of keys else False.
        """
        return cls._ordered

    @classmethod
    def allow_primitives(cls) -> bool:
        """
        :return:
            True if the parser.load* may return objects of primitive data types
            other than mapping types such like JSON parser
        """
        return cls._allow_primitives

    @classmethod
    def dict_options(cls) -> typing.List[str]:
        """
        :return: List of dict factory options
        """
        return cls._dict_opts

    def ropen(self, filepath, **kwargs):
        """
        :param filepath: Path to file to open to read data
        """
        return open(filepath, self._open_read_mode, **kwargs)

    def _container_factory(self, **options) -> GenContainerT:
        """
        The order of prirorities are ac_dict, backend specific dict class
        option, ac_ordered.

        :param options: Keyword options may contain 'ac_ordered'.
        :return: Factory (class or function) to make an container.
        """
        ac_dict = options.get("ac_dict", False)
        _dicts = [x for x in (options.get(o) for o in self.dict_options())
                  if x]

        if self.dict_options() and ac_dict and callable(ac_dict):
            return ac_dict  # Higher priority than ac_ordered.
        if _dicts and callable(_dicts[0]):
            return _dicts[0]
        if self.ordered() and options.get("ac_ordered", False):
            return collections.OrderedDict

        return dict

    def _load_options(self, container: GenContainerT, **options) -> OptionsT:
        """
        Select backend specific loading options.
        """
        # Force set dict option if available in backend. For example,
        # options["object_hook"] will be OrderedDict if 'container' was
        # OrderedDict in JSON backend.
        for opt in self.dict_options():
            options.setdefault(opt, container)

        return filter_options(self._load_opts, options)

    def load_from_string(self, content: str, container: GenContainerT,
                         **kwargs) -> InDataExT:
        """
        Load config from given string 'content'.

        :param content: Config content string
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        not_implemented(self, content, container, **kwargs)
        return DATA_DEFAULT

    def load_from_path(self, filepath: str, container: GenContainerT,
                       **kwargs) -> InDataExT:
        """
        Load config from given file path 'filepath`.

        :param filepath: Config file path
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        not_implemented(self, filepath, container, **kwargs)
        return DATA_DEFAULT

    def load_from_stream(self, stream: typing.IO, container: GenContainerT,
                         **kwargs) -> InDataExT:
        """
        Load config from given file like object 'stream`.

        :param stream:  Config file or file like object
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        not_implemented(self, stream, container, **kwargs)
        return DATA_DEFAULT

    def loads(self, content: str, **options) -> InDataExT:
        """
        Load config from given string 'content' after some checks.

        :param content:  Config file content
        :param options:
            options will be passed to backend specific loading functions.
            please note that options have to be sanitized w/
            :func:`anyconfig.utils.filter_options` later to filter out options
            not in _load_opts.

        :return: dict or dict-like object holding configurations
        """
        container = self._container_factory(**options)
        if not content or content is None:
            return container()

        options = self._load_options(container, **options)
        return self.load_from_string(content, container, **options)

    def load(self, ioi: IoiT, ac_ignore_missing: bool = False,
             **options) -> InDataExT:
        """
        Load config from a file path or a file / file-like object which 'ioi'
        refering after some checks.

        :param ioi:
            'anyconfig.common.IOInfo' namedtuple object provides various info
            of input object to load data from

        :param ac_ignore_missing:
            Ignore and just return empty result if given `ioi` object does not
            exist in actual.
        :param options:
            options will be passed to backend specific loading functions.
            please note that options have to be sanitized w/
            :func:`anyconfig.utils.filter_options` later to filter out options
            not in _load_opts.

        :return: dict or dict-like object holding configurations
        """
        container = self._container_factory(**options)
        options = self._load_options(container, **options)

        if not ioi:
            return container()

        if is_stream_ioinfo(ioi):
            cnf = self.load_from_stream(
                typing.cast(typing.IO, ioi.src), container, **options
            )
        else:
            if ac_ignore_missing and not pathlib.Path(ioi.path).exists():
                return container()

            cnf = self.load_from_path(ioi.path, container, **options)

        return cnf


class BinaryLoaderMixin(LoaderMixin):
    """
    Mixin class to load binary (byte string) configuration files.
    """
    _open_read_mode: str = 'rb'


class FromStringLoaderMixin(LoaderMixin):
    """
    Abstract config parser provides a method to load configuration from string
    content to help implement parser of which backend lacks of such function.

    Parser classes inherit this class have to override the method
    :meth:`load_from_string` at least.
    """
    def load_from_stream(self, stream: typing.IO, container: GenContainerT,
                         **kwargs) -> InDataExT:
        """
        Load config from given stream 'stream'.

        :param stream: Config file or file-like object
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_string(stream.read(), container, **kwargs)

    def load_from_path(self, filepath: str, container: GenContainerT,
                       **kwargs) -> InDataExT:
        """
        Load config from given file path 'filepath'.

        :param filepath: Config file path
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        with self.ropen(filepath) as inp:
            return self.load_from_stream(inp, container, **kwargs)


class FromStreamLoaderMixin(LoaderMixin):
    """
    Abstract config parser provides a method to load configuration from string
    content to help implement parser of which backend lacks of such function.

    Parser classes inherit this class have to override the method
    :meth:`load_from_stream` at least.
    """
    def load_from_string(self, content: str, container: GenContainerT,
                         **kwargs) -> InDataExT:
        """
        Load config from given string 'cnf_content'.

        :param content: Config content string
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        return self.load_from_stream(io.StringIO(content),
                                     container, **kwargs)

    def load_from_path(self, filepath: str, container: GenContainerT,
                       **kwargs) -> InDataExT:
        """
        Load config from given file path 'filepath'.

        :param filepath: Config file path
        :param container: callble to make a container object later
        :param kwargs: optional keyword parameters to be sanitized :: dict

        :return: Dict-like object holding config parameters
        """
        with self.ropen(filepath) as inp:
            return self.load_from_stream(inp, container, **kwargs)

# vim:sw=4:ts=4:et:
