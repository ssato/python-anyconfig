#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as Base
import anyconfig.backend.ini_ as BINI
import anyconfig.backend.json_ as BJSON
import anyconfig.backend.xml_ as BXML
import anyconfig.backend.yaml_ as BYAML
import anyconfig.utils as U


_CPs = [
    BINI.IniConfigParser,
    BJSON.JsonConfigPaser, 
    BYAML.YamlConfigPaser,
    BXML.XmlConfigParser,
]


def find_by_file(config_file, cps=_CPs):
    """
    Find config parser by file's extension.

    @param config_file: Config file path
    """
    fext = U.get_file_extension(config_file)
    for cp in cps:
        if cp.supports(fext):
            return cp

    return None


def find_by_type(cptype, cps=_CPs):
    """
    Find config parser by file's extension.

    @param cptype: Config file's type
    """
    for cp in cps:
        if cp.type() == cptype:
            return cp

    return None


# vim:sw=4:ts=4:et:
