#
# Copyright (C) 2011 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
r"""YAML backend:

- Format to support: YAML, http://yaml.org
- Requirements: PyYAML (yaml), http://pyyaml.org
- Development Status :: 5 - Production/Stable
- Limitations: ac_ordered is not effective and just ignored.
- Special options:

  - All keyword options of yaml.safe_load, yaml.load, yaml.safe_dump and
    yaml.dump should work.

  - Use 'ac_safe' boolean keyword option if you prefer to call yaml.safe_load
    and yaml.safe_dump instead of yaml.load and yaml.dump

  - See also: http://pyyaml.org/wiki/PyYAMLDocumentation

Changelog:

.. versionchanged:: 0.3

   - Changed special keyword option 'ac_safe' from 'safe' to avoid
     possibility of option conflicts in the future.
"""
from __future__ import absolute_import

import yaml
try:
    from yaml import CSafeLoader as Loader, CSafeDumper as Dumper
except ImportError:
    from yaml import SafeLoader as Loader, SafeDumper as Dumper

import anyconfig.backend.base
import anyconfig.utils


def _setup_loader_and_dumper(container, loader=Loader, dumper=Dumper):
    """
    Force set container (dict, OrderedDict, ...) used to construct python
    object from yaml node internally.

    .. note::
       It cannot be used with ac_safe keyword option at the same time yet.

    :param container: Set container used internally
    """
    map_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def construct_mapping(loader, node, deep=False):
        """Constructor to construct python object from yaml mapping node.

        :seealso: :meth:`yaml.BaseConstructor.construct_mapping`
        """
        if not isinstance(node, yaml.MappingNode):
            msg = "expected a mapping node, but found %s" % node.id
            raise yaml.constructor.ConstructorError(None, None, msg,
                                                    node.start_mark)
        mapping = container()
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                eargs = ("while constructing a mapping",
                         node.start_mark,
                         "found unacceptable key (%s)" % exc,
                         key_node.start_mark)
                raise yaml.constructor.ConstructorError(*eargs)
            value = loader.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping

    def container_representer(dumper, data):
        """Container representer.
        """
        return dumper.represent_mapping(map_tag, data.items())

    loader.add_constructor(map_tag, construct_mapping)
    dumper.add_representer(container, container_representer)


def _yml_fnc(fname, *args, **kwargs):
    """An wrapper of yaml.safe_load, yaml.load, yaml.safe_dump and yaml.dump.

    :param fname:
        "load" or "dump", not checked but it should be OK.
        see also :func:`_yml_load` and :func:`_yml_dump`
    :param args: [stream] for load or [cnf, stream] for dump
    :param kwargs: keyword args may contain "ac_safe" to load/dump safely
    """
    key = "ac_safe"
    fnc = getattr(yaml, kwargs.get(key, False) and r"safe_" + fname or fname)
    kwargs = anyconfig.utils.filter_options([k for k in kwargs.keys()
                                             if k != key], kwargs)
    return fnc(*args, **kwargs)


def _yml_load(stream, container, **kwargs):
    """An wrapper of yaml.safe_load and yaml.load.

    :param stream: a file or file-like object to load YAML content
    :param container: callble to make a container object
    """
    if "ac_safe" in kwargs:  # yaml.safe_load does not process Loader opts.
        kwargs = {}
    else:
        maybe_container = kwargs.get("ac_dict", None)
        loader = kwargs.get("Loader", Loader)
        dumper = kwargs.get("Dumper", Dumper)
        if maybe_container is not None and callable(maybe_container):
            _setup_loader_and_dumper(maybe_container, loader=loader,
                                     dumper=dumper)
            container = maybe_container

    return container(_yml_fnc("load", stream, **kwargs))


def _yml_dump(cnf, stream, **kwargs):
    """An wrapper of yaml.safe_dump and yaml.dump.

    :param cnf: Mapping object to dump
    :param stream: a file or file-like object to dump YAML data
    """
    if kwargs.get("ac_safe", False):
        cnf = anyconfig.dicts.convert_to(cnf)
    return _yml_fnc("dump", cnf, stream, **kwargs)


class Parser(anyconfig.backend.base.FromStreamLoader,
             anyconfig.backend.base.ToStreamDumper):
    """
    Parser for YAML files.
    """
    _type = "yaml"
    _extensions = ["yaml", "yml"]
    _load_opts = ["Loader", "ac_safe"]
    _dump_opts = ["stream", "ac_safe", "Dumper", "default_style",
                  "default_flow_style", "canonical", "indent", "width",
                  "allow_unicode", "line_break", "encoding", "explicit_start",
                  "explicit_end", "version", "tags"]
    # _ordered = True  # Not yet.

    load_from_stream = anyconfig.backend.base.to_method(_yml_load)
    dump_to_stream = anyconfig.backend.base.to_method(_yml_dump)

# vim:sw=4:ts=4:et:
