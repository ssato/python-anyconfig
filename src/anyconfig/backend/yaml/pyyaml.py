#
# Copyright (C) 2011 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# type() is used to exactly match check instead of isinstance here.
# pylint: disable=unidiomatic-typecheck
"""A backend module to load and dump YAML data files using yaml lib.

- Format to support: YAML, http://yaml.org
- Requirements: PyYAML (yaml), http://pyyaml.org
- Development Status :: 5 - Production/Stable
- Limitations:

  - Resuls is not ordered even if 'ac_ordered' or 'ac_dict' was given.
  - This parser (loader) cannot return None for empty inputs.

- Special options:

  - All keyword options of yaml.safe_load, yaml.load, yaml.safe_dump and
    yaml.dump should work.

  - Use 'ac_safe' boolean keyword option if you prefer to call yaml.safe_load
    and yaml.safe_dump instead of yaml.load and yaml.dump. Please note that
    this option conflicts with 'ac_dict' option and these options cannot be
    used at the same time.

  - See also: http://pyyaml.org/wiki/PyYAMLDocumentation

Changelog:

.. versionchanged:: 0.14.0

   - change CID.

.. versionchanged:: 0.9.6

   - Add support of loading primitives other than mapping objects.

.. versionchanged:: 0.3

   - Changed special keyword option 'ac_safe' from 'safe' to avoid
     possibility of option conflicts in the future.
"""
import yaml
try:
    from yaml import CSafeLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import SafeLoader as Loader, Dumper  # type: ignore

from ...dicts import convert_to
from ...utils import is_dict_like
from .. import base
from . import common


_MAPPING_TAG = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def _customized_loader(container, loader=Loader, mapping_tag=_MAPPING_TAG):
    """Get the customized loader.

    Create or update loader with making given callble 'container' to make
    mapping objects such as dict and OrderedDict, used to construct python
    object from yaml mapping node internally.

    :param container: Set container used internally
    """
    def construct_mapping(loader, node, deep=False):
        """Construct python object from yaml mapping node.

        It is based on :meth:`yaml.BaseConstructor.construct_mapping` in PyYAML
        (MIT).
        """
        loader.flatten_mapping(node)
        if not isinstance(node, yaml.MappingNode):
            raise yaml.constructor.ConstructorError(
                None, None, f'expected a mapping node, but found {node.id}',
                node.start_mark
            )
        mapping = container()
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                eargs = ('while constructing a mapping',
                         node.start_mark,
                         f'found unacceptable key ({exc!s})',
                         key_node.start_mark)
                raise yaml.constructor.ConstructorError(*eargs)
            value = loader.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping

    tag = 'tag:yaml.org,2002:python/unicode'

    def construct_ustr(loader, node):
        """Unicode string constructor."""
        return loader.construct_scalar(node)

    try:
        loader.add_constructor(tag, construct_ustr)
    except NameError:
        pass

    if container is not dict:
        loader.add_constructor(mapping_tag, construct_mapping)
    return loader


def _customized_dumper(container, dumper=Dumper):
    """Counterpart of :func:`_customized_loader` for dumpers."""
    def container_representer(dumper, data, mapping_tag=_MAPPING_TAG):
        """Container representer."""
        return dumper.represent_mapping(mapping_tag, data.items())

    def ustr_representer(dumper, data):
        """Unicode string representer."""
        tag = 'tag:yaml.org,2002:python/unicode'
        return dumper.represent_scalar(tag, data)

    try:
        dumper.add_representer(unicode, ustr_representer)
    except NameError:
        pass

    if container is not dict:
        dumper.add_representer(container, container_representer)
    return dumper


def yml_fnc_by_name(fname, **options):
    """Get yaml loading/dumping function by name.

    :param fname:
        "load" or "dump", not checked but it should be OK.
        see also :func:`yml_load` and :func:`yml_dump`
    :param options: keyword args may contain "ac_safe" to load/dump safely
    """
    return getattr(yaml, f'safe_{fname}' if options.get('ac_safe') else fname)


def yml_fnc_(fname, *args, **options):
    """Call yaml.safe_load, yaml.load, yaml.safe_dump and yaml.dump.

    :param fname:
        "load" or "dump", not checked but it should be OK.
        see also :func:`yml_load` and :func:`yml_dump`
    :param args: [stream] for load or [cnf, stream] for dump
    :param options: keyword args may contain "ac_safe" to load/dump safely
    """
    fnc = yml_fnc_by_name(fname, **options)
    return fnc(*args, **common.filter_from_options('ac_safe', options))


def yml_load(stream, container, yml_fnc=yml_fnc_, **options):
    """Call yaml.safe_load and yaml.load.

    :param stream: a file or file-like object to load YAML content
    :param container: callble to make a container object

    :return: Mapping object
    """
    if options.get('ac_safe', False):
        # .. note:: yaml.safe_load does not support any keyword options.
        options = {"ac_safe": True}

    elif not options.get('Loader', False):
        maybe_container = options.get('ac_dict', False)
        if maybe_container and callable(maybe_container):
            container = maybe_container

        options['Loader'] = _customized_loader(container)

    ret = yml_fnc('load', stream,
                  **common.filter_from_options('ac_dict', options))
    if ret is None:
        return container()

    return ret


def yml_dump(data, stream, yml_fnc=yml_fnc_, **options):
    """Call yaml.safe_dump and yaml.dump.

    :param data: Some data to dump
    :param stream: a file or file-like object to dump YAML data
    """
    _is_dict = is_dict_like(data)

    if options.get('ac_safe', False):
        options = {"ac_safe": True}  # Same as yml_load.

    elif not options.get('Dumper', False) and _is_dict:
        # TODO: Any other way to get its constructor?
        maybe_container = options.get('ac_dict', type(data))
        options['Dumper'] = _customized_dumper(maybe_container)

    if _is_dict:
        # Type information and the order of items are lost on dump currently.
        data = convert_to(data, ac_dict=dict)
        options = common.filter_from_options('ac_dict', options)

    return yml_fnc('dump', data, stream, **options)


class Parser(common.Parser):
    """Parser for YAML files."""

    _cid = 'yaml.pyyaml'
    _priority = 30  # Higher priority than ruamel.yaml.
    _load_opts = ['Loader', 'ac_safe', 'ac_dict']
    _dump_opts = ['stream', 'ac_safe', 'Dumper', 'default_style',
                  'default_flow_style', 'canonical', 'indent', 'width',
                  'allow_unicode', 'line_break', 'encoding', 'explicit_start',
                  'explicit_end', 'version', 'tags']

    load_from_stream = base.to_method(yml_load)
    dump_to_stream = base.to_method(yml_dump)

# vim:sw=4:ts=4:et:
