#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.Bunch as B
import anyconfig.backend.backends as Backends
import anyconfig.backend.json_ as BJ

import logging
import os.path


def __find_parser(config_path, forced_type=None):
    """
    @param config_path: Configuration file path
    @param forced_type: Forced configuration parser type
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
    @param config_path: Configuration file path
    @param forced_type: Forced configuration parser type
    """
    cparser = __find_parser(config_path, forced_type)
    if not cparser:
        return None

    return cparser.load(config_path, **kwargs)


def loads(paths=[]):
    """
    @param paths: Configuration file path list
    """
    config = B.Bunch()
    for p in paths:
        config.update(load(p))
    
    return config


def dump(data, config_path, forced_type=None):
    cparser = __find_parser(config_path, forced_type)
    if not cparser:
        return B.Bunch()

    if not getattr(cparser, "dump", False):
        logging.warn(
            "Dump method not implemented. Fallback to JsonConfigPaser"
        )
        cparser = BJ.JsonConfigPaser()
        config_path = os.path.splitext(config_path)[0] + ".json"

    logging.debug("Save to: " + config_path)
    cparser.dump(data, config_path)


# vim:sw=4:ts=4:et:
