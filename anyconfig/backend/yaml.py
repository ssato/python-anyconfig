#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""YAML backend.

.. versionchanged:: 0.3
   Changed special keyword option 'ac_safe' from 'safe' to avoid possibility of
   option conflicts in the future.

- Format to support: YAML, http://yaml.org
- Requirements: PyYAML (yaml), http://pyyaml.org
- Limitations: None obvious
- Special options:

  - All keyword options of yaml.{safe\_,}load and yaml.{safe\_,}dump should
    work.

  - Use 'ac_safe' boolean keyword option if you prefer to call
    yaml.safe\_{load,dump} instead of yaml.{load,dump}

  - See also: http://pyyaml.org/wiki/PyYAMLDocumentation
"""
from __future__ import absolute_import

import yaml
import anyconfig.backend.base


def _yml_fnc(fname, *args, **kwargs):
    """An wrapper of yaml.{safe\_,}(load|dump).

    :param fname:
        "load" or "dump", not checked but it should be OK.
        see also :func:`_yml_load` and :func:`_yml_dump`
    :param args: [stream] for load or [cnf, stream] for dump
    :param kwargs: keyword args may contain "ac_safe" to load/dump safely
    """
    key = "ac_safe"
    fnc = getattr(yaml, key in kwargs and "safe\_" + fname or fname)
    kwargs = anyconfig.backend.base.mk_opt_args([k for k in kwargs.keys()
                                                 if k != key], kwargs)
    return fnc(*args, **kwargs)


def _yml_load(stream, **kwargs):
    """An wrapper of yaml.{safe\_,}load.

    :param stream: a file or file-like object to load YAML content
    """
    if "ac_safe" in kwargs:  # yaml.safe_load does not process Loader opts.
        kwargs = {}
    return _yml_fnc("load", stream, **kwargs)


def _yml_dump(cnf, stream, **kwargs):
    """An wrapper of yaml.{safe\_,}dump.

    :param cnf: Configuration data (dict-like object) to dump
    :param stream: a file or file-like object to load YAML content
    """
    return _yml_fnc("dump", cnf, stream, **kwargs)


class Parser(anyconfig.backend.base.LParser, anyconfig.backend.base.L2Parser,
             anyconfig.backend.base.D2Parser):
    """
    Parser for YAML files.
    """
    _type = "yaml"
    _extensions = ["yaml", "yml"]
    _load_opts = ["Loader", "ac_safe"]
    _dump_opts = ["stream", "Dumper"]

    load_from_stream = anyconfig.backend.base.to_method(_yml_load)
    dump_to_stream = anyconfig.backend.base.to_method(_yml_dump)

# vim:sw=4:ts=4:et:
