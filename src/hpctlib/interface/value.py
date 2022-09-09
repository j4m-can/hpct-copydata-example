# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# hpctlib/interface/value.py

"""Supported interface value objects.

Note: Test exposing values rather than codecs. Codecs would be hidden.
"""

from .base import Value
from . import codec


class AutoCodecValue(Value):
    def __init__(self, default, checker=None):
        clsname = self.__class__.__name__
        codeccls = getattr(codec, clsname)
        super().__init__(codeccls(), default, checker))


class Boolean(AutoCodecValue):
    pass


class Blob(AutoCodecValue):
    pass


class Dict(AutoCodecValue):
    pass


class Float(AutoCodecValue):
    pass


class Integer(AutoCodecValue):
    pass


class IPAddress(AutoCodecValue):
    pass


class IPNetwork(AutoCodecValue):
    pass


class Noop(AutoCodecValue):
    pass


class Ready(AutoCodecValue):
    pass


class String(AutoCodecValue):
    pass
