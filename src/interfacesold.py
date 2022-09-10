#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# old-interfaces.py

"""Interfaces (old) for operator relations.
"""


import ipaddress
import logging

from hpctlib.interface import codec, checker
from hpctlib.interface import interface_registry
from hpctlib.interface.base import Value
from hpctlib.interface.relation import (
    AppBucketInterface,
    RelationSuperInterface,
    UnitBucketInterface,
)


logger = logging.getLogger(__name__)


class CopyDataRelationSuperInterface(RelationSuperInterface):

    """Relation super interface."""

    class ProviderAppInterface(AppBucketInterface):

        bool = Value(codec.Boolean(), False)
        int = Value(codec.Integer(), 0)
        float = Value(codec.Float(), 0.0)
        str = Value(codec.String(), "")
        privport = Value(codec.Integer(), 0, checker.PrivilegedPort())
        ipaddr = Value(codec.IPAddress(), ipaddress.IPv4Address("0.0.0.0"))
        ipnet = Value(codec.IPNetwork(), ipaddress.IPv4Network("0.0.0.0"))

    class ProviderUnitInterface(UnitBucketInterface):

        bool = Value(codec.Boolean(), False)
        int = Value(codec.Integer(), 0)
        float = Value(codec.Float(), 0.0)
        str = Value(codec.String(), "")
        privport = Value(codec.Integer(), 0, checker.PrivilegedPort())
        ipaddr = Value(codec.IPAddress(), ipaddress.IPv4Address("0.0.0.0"))
        ipnet = Value(codec.IPNetwork(), ipaddress.IPv4Network("0.0.0.0"))

    class RequirerAppInterface(AppBucketInterface):

        bool = Value(codec.Boolean(), False)
        int = Value(codec.Integer(), 0)
        float = Value(codec.Float(), 0.0)
        str = Value(codec.String(), "")
        privport = Value(codec.Integer(), 0, checker.PrivilegedPort())
        ipaddr = Value(codec.IPAddress(), ipaddress.IPv4Address("0.0.0.0"))
        ipnet = Value(codec.IPNetwork(), ipaddress.IPv4Network("0.0.0.0"))

    class RequirerUnitInterface(UnitBucketInterface):

        bool = Value(codec.Boolean(), False)
        int = Value(codec.Integer(), 0)
        float = Value(codec.Float(), 0.0)
        str = Value(codec.String(), "")
        privport = Value(codec.Integer(), 0, checker.PrivilegedPort())
        ipaddr = Value(codec.IPAddress(), ipaddress.IPv4Address("0.0.0.0"))
        ipnet = Value(codec.IPNetwork(), ipaddress.IPv4Network("0.0.0.0"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interface_classes[("provider", "app")] = self.ProviderAppInterface
        self.interface_classes[("provider", "unit")] = self.ProviderUnitInterface
        self.interface_classes[("requirer", "app")] = self.RequirerAppInterface
        self.interface_classes[("requirer", "unit")] = self.RequirerUnitInterface


interface_registry.register("relation-copy-data", CopyDataRelationSuperInterface)
