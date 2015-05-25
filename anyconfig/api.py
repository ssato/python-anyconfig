#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Public APIs of anyconfig module.
"""
from __future__ import absolute_import
from anyconfig.globals import LOGGER

import anyconfig.backend.backends
import anyconfig.backend.json_
import anyconfig.compat
import anyconfig.mergeabledict
import anyconfig.parser
import anyconfig.template
import anyconfig.utils

# pylint: disable=W0611
# Import some global constants will be re-exported:
from anyconfig.mergeabledict import MS_REPLACE, MS_NO_REPLACE, \
    MS_DICTS, MS_DICTS_AND_LISTS, MERGE_STRATEGIES, \
    get, set_  # flake8: noqa
from anyconfig.parser import PATH_SEPS
# pylint: enable=W0611

# pylint: disable=C0103
# Re-export:
list_types = anyconfig.backend.backends.list_types  # flake8: noqa

# aliases:
container = anyconfig.mergeabledict.MergeableDict
# pylint: enable=C0103


def set_loglevel(level):
    """
    :param level: Log level, e.g. logging.INFO and logging.WARN.
    """
    LOGGER.setLevel(level)


def find_loader(config_path, forced_type=None):
    """
    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type

    :return: Parser-inherited class object
    """
    if forced_type is not None:
        cparser = anyconfig.backend.backends.find_by_type(forced_type)
        if not cparser:
            LOGGER.error("No parser found for given type: %s", forced_type)
            return None
    else:
        cparser = anyconfig.backend.backends.find_by_file(config_path)
        if not cparser:
            LOGGER.error("No parser found for given file: %s", config_path)
            return None

    LOGGER.debug("Using config parser of type: %s", cparser.type())
    return cparser


def single_load(config_path, forced_type=None, ignore_missing=False,
                ac_template=False, ac_context=None, **kwargs):
    """
    Load single config file.

    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore and just return empty result if given file
        (``config_path``) does not exist
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    config_path = anyconfig.utils.ensure_expandusr(config_path)

    cparser = find_loader(config_path, forced_type)
    if cparser is None:
        return None

    LOGGER.info("Loading: %s", config_path)
    if ac_template:
        try:
            LOGGER.debug("Compiling: %s", config_path)
            config_content = anyconfig.template.render(config_path, ac_context)
            return cparser.loads(config_content, ignore_missing=ignore_missing,
                                 **kwargs)
        except:
            LOGGER.warn("Failed to compile %s, fallback to no template "
                        "mode", config_path)

    return cparser.load(config_path, ignore_missing=ignore_missing,
                        **kwargs)


def multi_load(paths, forced_type=None, ignore_missing=False,
               merge=MS_DICTS, marker='*', ac_template=False, ac_context=None,
               **kwargs):
    """
    Load multiple config files.

    The first argument `paths` may be a list of config file paths or
    a glob pattern specifying that. That is, if a.yml, b.yml and c.yml are in
    the dir /etc/foo/conf.d/, the followings give same results::

      multi_load(["/etc/foo/conf.d/a.yml", "/etc/foo/conf.d/b.yml",
                  "/etc/foo/conf.d/c.yml", ])

      multi_load("/etc/foo/conf.d/*.yml")

    :param paths: List of config file paths or a glob pattern to list paths
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore missing config files
    :param merge: Strategy to merge config results of multiple config files
        loaded. see also: anyconfig.mergeabledict.MergeableDict.update()
    :param marker: Globbing markerer to detect paths patterns
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if merge not in MERGE_STRATEGIES:
        raise ValueError("Invalid merge strategy: " + merge)

    if marker in paths:
        paths = anyconfig.utils.sglob(paths)

    config = container.create(ac_context) if ac_context else container()
    for path in paths:
        if marker in path:  # Nested patterns like ['*.yml', '/a/b/c.yml'].
            conf_updates = multi_load(path, forced_type=forced_type,
                                      ignore_missing=ignore_missing,
                                      merge=merge, marker=marker,
                                      ac_template=ac_template,
                                      ac_context=config, **kwargs)
        else:
            conf_updates = single_load(path, forced_type=forced_type,
                                       ignore_missing=ignore_missing,
                                       ac_template=ac_template,
                                       ac_context=config, **kwargs)

        config.update(conf_updates, merge)

    return config


def load(path_specs, forced_type=None, ignore_missing=False,
         merge=MS_DICTS, marker='*', ac_template=False, ac_context=None,
         **kwargs):
    """
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs:
        Configuration file path or paths or its pattern such as '/a/b/*.json'
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore missing config files
    :param merge: Merging strategy to use
    :param marker: Globbing marker to detect paths patterns
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: A dict presents context to instantiate template
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if marker in path_specs or anyconfig.utils.is_iterable(path_specs):
        return multi_load(path_specs, forced_type, ignore_missing,
                          merge, marker, ac_template, ac_context, **kwargs)
    else:
        return single_load(path_specs, forced_type, ignore_missing,
                           ac_template, ac_context, **kwargs)


def loads(config_content, forced_type=None, ac_template=False, ac_context=None,
          **kwargs):
    """
    :param config_content: Configuration file's content
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore missing config files
    :param ac_template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param ac_context: Context dict to instantiate template
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if forced_type is None:
        return anyconfig.parser.parse(config_content)

    cparser = find_loader(None, forced_type)
    if cparser is None:
        return anyconfig.parser.parse(config_content)

    if ac_template:
        try:
            LOGGER.debug("Compiling")
            config_content = anyconfig.template.render_s(config_content,
                                                         ac_context)
        except:
            LOGGER.warn("Failed to compile and fallback to no template "
                        "mode: '%s'", config_content[:50] + '...')

    return cparser.loads(config_content, **kwargs)


def _find_dumper(config_path, forced_type=None):
    """
    Find configuration parser to dump data.

    :param config_path: Output filename
    :param forced_type: Forced configuration parser type

    :return: Parser-inherited class object
    """
    cparser = find_loader(config_path, forced_type)

    if cparser is None or not getattr(cparser, "dump", False):
        LOGGER.warn("Dump method not implemented. Fallback to json.Parser")
        cparser = anyconfig.backend.json_.Parser()

    return cparser


def dump(data, config_path, forced_type=None, **kwargs):
    """
    Save `data` as `config_path`.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param config_path: Output filename
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    """
    dumper = _find_dumper(config_path, forced_type)

    LOGGER.info("Dumping: %s", config_path)
    dumper.dump(data, config_path, **kwargs)


def dumps(data, forced_type, **kwargs):
    """
    Return string representation of `data` in forced type format.

    :param data: Config data object to dump ::
        anyconfig.mergeabledict.MergeableDict by default
    :param forced_type: Forced configuration parser type
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend

    :return: Backend-specific string representation for the given data
    """
    return _find_dumper(None, forced_type).dumps(data, **kwargs)

# vim:sw=4:ts=4:et:
