#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as Base
import anyconfig.Bunch as B
import anyconfig.parser as P

import logging
import os.path

try:
    import ConfigParser as configparser
except ImportError:
    import configparser  # python > 3.0


SUPPORTED = True  # It's always available.


class IniConfigParser(Base.BaseConfigParser):
    _type = "ini"
    _extentions = ["ini"]

    @classmethod
    def load(cls, config_path, sep=",", **kwargs):
        config = B.Bunch()

        if not os.path.exists(config_path):
            logging.warn("Not exist: " + config_path)
            return config

        logging.info("Loading config: " + config_path)

        # FIXME: Ugly
        def __parse(v):
            if v.startswith('"') and v.endswith('"'):
                return v[1:-1]
            elif sep in v:
                return [P.parse(x) for x in P.parse_list_str(v)]
            else:
                return P.parse(v)

        try:
            parser = configparser.SafeConfigParser()
            parser.read(config_path)

            # Treat key and value pairs in [DEFAULT] as special.
            for k, v in parser.defaults().iteritems():
                config[k] = __parse(v)

            for s in parser.sections():
                config[s] = B.Bunch()

                for k in parser.options(s):
                    v = parser.get(s, k)
                    config[s][k] = __parse(v)

        except Exception, e:
            logging.warn(e)

        return config

    @classmethod
    def dumps(cls, data, config_path, *args, **kwargs):
        raise NotImplementedError("Not yet")


# vim:sw=4:ts=4:et:
