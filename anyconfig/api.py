#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Public APIs of anyconfig module.
"""

import logging

import anyconfig.globals as G
import anyconfig.mergeabledict as M
import anyconfig.backend.backends as Backends
import anyconfig.backend.json_ as BJ
import anyconfig.parser as P
import anyconfig.template as AT
import anyconfig.utils as U

# pylint: disable=W0611
# Import some global constants will be re-exported:
from anyconfig.mergeabledict import MS_REPLACE, MS_NO_REPLACE, \
    MS_DICTS, MS_DICTS_AND_LISTS, MERGE_STRATEGIES, \
    get, set_  # flake8: noqa
from anyconfig.parser import PATH_SEPS
# pylint: enable=W0611

# pylint: disable=C0103
# Re-export:
list_types = Backends.list_types  # flake8: noqa

# aliases:
container = M.MergeableDict
# pylint: enable=C0103

logger = logging.getLogger(__name__)


def set_loglevel(level):
    """
    :param level: Log level, e.g. logging.INFO and logging.WARN.
    """
    logger.setLevel(level)


def find_loader(config_path, forced_type=None):
    """
    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    :return: ConfigParser-inherited class object
    """
    if forced_type is not None:
        cparser = Backends.find_by_type(forced_type)
        if not cparser:
            logger.error("No parser found for given type: %s", forced_type)
            return None
    else:
        cparser = Backends.find_by_file(config_path)
        if not cparser:
            logger.error("No parser found for given file: %s", config_path)
            return None

    logger.debug("Using config parser of type: %s", cparser.type())
    return cparser


def single_load(config_path, forced_type=None, ignore_missing=False,
                template=True, context={}, **kwargs):
    """
    Load single config file.

    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore and just return empty result if given file
        (``config_path``) does not exist
    :param template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param context: Context dict to instantiate template
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    config_path = U.ensure_expandusr(config_path)

    cparser = find_loader(config_path, forced_type)
    if cparser is None:
        return None

    logger.info("Loading: %s", config_path)
    if template:
        try:
            logger.debug("Compiling: %s", config_path)
            config_content = AT.render(config_path, context)
            return cparser.loads(config_content, ignore_missing=ignore_missing,
                                 **kwargs)
        except:
            logger.warn("Failed to compile %s, fallback to no template "
                         "mode", config_path)

    return cparser.load(config_path, ignore_missing=ignore_missing,
                        **kwargs)


def multi_load(paths, forced_type=None, merge=MS_DICTS, marker='*',
               ignore_missing=False, template=True, context={}, **kwargs):
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
    :param merge: Strategy to merge config results of multiple config files
        loaded. see also: anyconfig.mergeabledict.MergeableDict.update()
    :param marker: Globbing markerer to detect paths patterns
    :param ignore_missing: Ignore missing config files
    :param template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param context: Context dict
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    assert merge in MERGE_STRATEGIES, "Invalid merge strategy: " + merge

    if marker in paths:
        paths = U.sglob(paths)

    config = container.create(context) if context else container()
    for path in paths:
        if marker in path:  # Nested patterns like ['*.yml', '/a/b/c.yml'].
            conf_updates = multi_load(path, forced_type, merge, marker,
                                      ignore_missing, template, config,
                                      **kwargs)
        else:
            conf_updates = single_load(path, forced_type, ignore_missing,
                                       template, config, **kwargs)

        config.update(conf_updates, merge)

    return config


def load(path_specs, forced_type=None, merge=MS_DICTS, marker='*',
         ignore_missing=False, template=True, context={}, **kwargs):
    """
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs:
        Configuration file path or paths or its pattern such as '/a/b/*.json'
    :param forced_type: Forced configuration parser type
    :param merge: Merging strategy to use
    :param marker: Globbing marker to detect paths patterns
    :param ignore_missing: Ignore missing config files
    :param template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param context: Context dict to instantiate template
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if marker in path_specs or U.is_iterable(path_specs):
        return multi_load(path_specs, forced_type, merge, marker,
                          ignore_missing, template, context, **kwargs)
    else:
        return single_load(path_specs, forced_type, ignore_missing,
                           template, context, **kwargs)


def loads(config_content, forced_type=None, template=True, context={},
          **kwargs):
    """
    :param config_content: Configuration file's content
    :param forced_type: Forced configuration parser type
    :param ignore_missing: Ignore missing config files
    :param template: Assume configuration file may be a template file and
        try to compile it AAR if True
    :param context: Context dict to instantiate template
    :param kwargs: Backend specific optional arguments, e.g. {"indent": 2} for
        JSON loader/dumper backend
    :return: Dict-like object (instance of
        anyconfig.mergeabledict.MergeableDict by default) supports merge
        operations.
    """
    if forced_type is None:
        return P.parse(config_content)

    cparser = find_loader(None, forced_type)
    if cparser is None:
        return P.parse(config_content)

    if template:
        try:
            logger.debug("Compiling")
            config_content = AT.render_s(config_content, context)
        except:
            logger.warn("Failed to compile and fallback to no template "
                         "mode: '%s'", config_content[:50] + '...')

    return cparser.loads(config_content, **kwargs)


def _find_dumper(config_path, forced_type=None):
    """
    Find configuration parser to dump data.

    :param config_path: Output filename
    :param forced_type: Forced configuration parser type
    :return: ConfigParser-inherited class object
    """
    cparser = find_loader(config_path, forced_type)

    if cparser is None or not getattr(cparser, "dump", False):
        logger.warn("Dump method not implemented. Fallback to "
                     "JsonConfigParser")
        cparser = BJ.JsonConfigParser()

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

    logger.info("Dumping: %s", config_path)
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
