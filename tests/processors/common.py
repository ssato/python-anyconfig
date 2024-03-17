#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
import anyconfig.models.processor


class A(anyconfig.models.processor.Processor):
    _cid = "A"
    _type = "json"
    _extensions = ["json", "jsn", "js"]


class A2(A):
    _cid = "A2"
    _priority = 20  # Higher priority than A.


class A3(A):
    _cid = "A3"
    _priority = 99  # Higher priority than A and A2.


class B(anyconfig.models.processor.Processor):
    _cid = "B"
    _type = "yaml"
    _extensions = ["yaml", "yml"]
    _priority = 99  # Higher priority than C.


class C(anyconfig.models.processor.Processor):
    _cid = "dummy"
    _type = "yaml"
    _extensions = ["yaml", "yml"]


PRS = [A, A2, A3, B, C]

# vim:sw=4:ts=4:et:
