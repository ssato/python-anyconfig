#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.Bunch as B
import anyconfig.backend.backends as Backends
import anyconfig.backend.json_ as BJ
import anyconfig.utils as U

import logging
import os.path


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
    else:
        cparser = Backends.find_by_file(config_path)
        if not cparser:
            logging.error(
                "No parser found for given file: " + config_path
            )

    if cparser:
        logging.info("Using config parser: " + str(cparser))

    return cparser


def load(config_path, forced_type=None, **kwargs):
    """
    Load single config file.

    :param config_path: Configuration file path
    :param forced_type: Forced configuration parser type
    """
    cparser = find_parser(config_path, forced_type)
    if not cparser:
        return None

    logging.info("Loading: " + config_path)
    return cparser.load(config_path, **kwargs)


def loads(config_content, forced_type, **kwargs):
    """
    :param config_content: Configuration file's content
    :param forced_type: Forced configuration parser type
    """
    cparser = find_parser("dummy_path", forced_type)
    if not cparser:
        return None

    logging.info("Loading")
    return cparser.loads(config_content, **kwargs)


def mload(paths=[], forced_type=None, update=B.ST_MERGE_DICTS):
    """
    Load multiple config files.

    :param paths: Configuration file path list
    :param forced_type: Forced configuration parser type
    :param update: Update merging strategy to use.
        see also: anyconfig.Bunch.update()
    """
    config = B.Bunch()
    for p in paths:
        config.update(load(p, forced_type), update)

    return config


def dump(data, config_path, forced_type=None):
    cparser = find_parser(config_path, forced_type)
    if not cparser or not getattr(cparser, "dump", False):
        logging.warn(
            "Dump method not implemented. Fallback to JsonConfigParser"
        )
        cparser = BJ.JsonConfigParser()
        config_path = os.path.splitext(config_path)[0] + ".json"

    logging.debug("Save to: " + config_path)
    cparser.dump(data, config_path)


def dumps(data, forced_type):
    cparser = find_parser("dummy_path", forced_type)
    if not cparser or not getattr(cparser, "dumps", False):
        logging.warn(
            "Dumps method not implemented. Fallback to JsonConfigParser"
        )
        cparser = BJ.JsonConfigParser()

    return cparser.dumps(data)


def mload_metaconf(metaconf_path, forced_type=None, conf_exts=".conf"):
    """
    Load meta config files to define ``meta`` config parameters such like
    config files' search paths and formats, etc.

    :param metaconf_path: Dir in which meta confs exit or meta conf path
    :param forced_type: Forced config parser type
    :param conf_exts: Config files' extension. `forced_type` or `conf_exts`
        must be given.
    """
    if os.path.isdir(metaconf_path):
        metaconfdir = metaconf_path
        confs = U.sglob(os.path.join(metaconf_path, conf_exts))
    else:
        metaconfdir = os.path.dirname(metaconf_path)
        confs = [metaconf_path]  # It's not a dir, just a file.

    d = mload(confs, forced_type)

    if "topdir" not in d:
        d["topdir"] = os.path.abspath(os.path.join(metaconfdir, ".."))

    return d

# vim:sw=4:ts=4:et:
