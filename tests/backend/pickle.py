#
# Copyright (C) 2017 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
import anyconfig.backend.pickle as TT
import tests.backend.common as TBC


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = TBC.CNF_1
    cnf_s = TT.pickle.dumps(cnf)


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    load_options = dump_options = dict(protocol=TT.pickle.HIGHEST_PROTOCOL)
    empty_patterns = [('', {})]


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
