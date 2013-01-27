#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.mergeabledict as M
import anyconfig.backend.backends as Backends
import anyconfig.backend.json_ as BJ
import anyconfig.parser as P
import anyconfig.utils as U

import logging
import os.path


MS_REPLACE = "replace"
MS_DICTS = "merge_dicts"
MS_DICTS_AND_LISTS = "merge_dicts_and_lists"

MERGE_STRATEGIES = dict(
    replace=M.ST_REPLACE,
    merge_dicts=M.ST_MERGE_DICTS,
    merge_dicts_and_lists=M.ST_MERGE_DICTS_AND_LISTS,
)

# Re-export:
list_types = Backends.list_types

# alias:
container = M.MergeableDict


def find_parser(config_path, forced_type=None):
    """
    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    """
    if forced_type is not None:
        cparser = Backends.find_by_type(forced_type)
        if not cparser:
            logging.error(
                "No parser found for given type: " + forced_type
            )
            return None
    else:
        cparser = Backends.find_by_file(config_path)
        if not cparser:
            logging.error(
                "No parser found for given file: " + config_path
            )
            return None

    logging.debug("Using config parser: " + str(cparser))
    return cparser


def single_load(config_path, forced_type=None, **kwargs):
    """
    Load single config file.

    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    """
    cparser = find_parser(config_path, forced_type)
    if cparser is None:
        return None

    logging.debug("Loading: " + config_path)
    return cparser.load(config_path, **kwargs)


def multi_load(paths, forced_type=None, merge=MS_DICTS_AND_LISTS, marker='*'):
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
    """
    merge_st = MERGE_STRATEGIES.get(merge, False)

    if not merge_st:
        raise RuntimeError("Invalid merge strategy given: " + merge)

    if marker in paths:
        paths = U.sglob(paths)

    config = container()
    for p in paths:
        if marker in p:  # Nested pattern cases, e.g. ['*.yml', '/a/b/c.yml'].
            conf_updates = multi_load(p, forced_type, merge, marker)
        else:
            conf_updates = single_load(p, forced_type)

        config.update(conf_updates, merge_st)

    return config


def load(path_specs, forced_type=None, merge=MS_DICTS_AND_LISTS, marker='*'):
    """
    Load single or multiple config files or multiple config files specified in
    given paths pattern.

    :param path_specs:
        Configuration file path or paths or its pattern such as '/a/b/*.json'
    :param forced_type: Forced configuration parser type
    :param merge: Merging strategy to use
    :param marker: Globbing marker to detect paths patterns
    """
    if marker in path_specs or U.is_iterable(path_specs):
        return multi_load(path_specs, forced_type, merge, marker)
    else:
        return single_load(path_specs, forced_type)


def loads(config_content, forced_type=None, **kwargs):
    """
    :param config_content: Configuration file's content
    :param forced_type: Forced configuration parser type
    """
    if forced_type is None:
        return P.parse(config_content)

    cparser = find_parser(None, forced_type)
    if cparser is None:
        return P.parse(config_content)

    return cparser.loads(config_content, **kwargs)


def _find_dumper(config_path, forced_type=None):
    """
    Find configuration parser to dump data.

    :param config_path: Output filename
    :param forced_type: Forced configuration parser type
    """
    cparser = find_parser(config_path, forced_type)

    if cparser is None or not getattr(cparser, "dump", False):
        logging.warn(
            "Dump method not implemented. Fallback to JsonConfigParser"
        )
        cparser = BJ.JsonConfigParser()

    return cparser


def dump(data, config_path, forced_type=None):
    """
    Save `data` as `config_path`.

    :param data: Data object to dump
    :param config_path: Output filename
    :param forced_type: Forced configuration parser type
    """
    _find_dumper(config_path, forced_type).dump(data, config_path)


def dumps(data, forced_type):
    """
    Return string representation of `data` in forced type format.

    :param data: Data object to dump
    :param forced_type: Forced configuration parser type
    """
    return _find_dumper(None, forced_type).dumps(data)


# vim:sw=4:ts=4:et:
