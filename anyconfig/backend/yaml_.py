#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as Base
import anyconfig.Bunch as B

import logging

SUPPORTED = False
try:
    import yaml
    SUPPORTED = True
except ImportError:
    logging.warn("YAML module is not available. Disabled its support.")


# @see http://bit.ly/pxKVqS
class YamlBunchLoader(yaml.Loader):

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(
            u"tag:yaml.org,2002:map",
            type(self).construct_yaml_map
        )

    def construct_yaml_map(self, node):
        data = B.Bunch()
        yield data

        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                "expected a mapping node, but found %s" % node.id,
                node.start_mark
            )

        mapping = B.Bunch()

        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found unacceptable key (%s)" % exc,
                    key_node.start_mark
                )
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping


class YamlConfigParser(Base.BaseConfigParser):

    _type = "yaml"
    _extentions = ["yaml", "yml"]

    @classmethod
    def load(cls, config_path, *args, **kwargs):
        return yaml.load(open(config_path), Loader=YamlBunchLoader)

    @classmethod
    def dumps(cls, data, *args, **kwargs):
        return yaml.dump(data, None)

    @classmethod
    def dump(cls, data, config_path, *args, **kwargs):
        yaml.dump(data, open(config_path, "w"))


# vim:sw=4:ts=4:et:
