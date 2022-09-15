#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# interfaces/copydata.py

"""Interfaces for operator relations.
"""


import ipaddress

from hpctlib.interface import checker
from hpctlib.interface import interface_registry
from hpctlib.interface.relation import (
    AppBucketInterface,
    RelationSuperInterface,
    UnitBucketInterface,
)
from hpctlib.interface.value import Boolean, Integer, Float, String
from hpctlib.interface.value.network import IPAddress, IPNetwork, PrivilegedPort


class CopyDataRelationSuperInterface(RelationSuperInterface):

    """Relation super interface."""

    class ProviderAppInterface(AppBucketInterface):

        bool = Boolean(False)
        int = Integer(0)
        float = Float(0.0)
        str = String("")
        privport = PrivilegedPort(0)
        ipaddr = IPAddress(ipaddress.IPv4Address("0.0.0.0"))
        ipnet = IPNetwork(ipaddress.IPv4Network("0.0.0.0"))

    class ProviderUnitInterface(UnitBucketInterface):

        bool = Boolean(False)
        int = Integer(0)
        float = Float(0.0)
        str = String("")
        privport = PrivilegedPort(0)
        ipaddr = IPAddress(ipaddress.IPv4Address("0.0.0.0"))
        ipnet = IPNetwork(ipaddress.IPv4Network("0.0.0.0"))

    class RequirerAppInterface(AppBucketInterface):

        bool = Boolean(False)
        int = Integer(0)
        float = Float(0.0)
        str = String("")
        privport = PrivilegedPort(0)
        ipaddr = IPAddress(ipaddress.IPv4Address("0.0.0.0"))
        ipnet = IPNetwork(ipaddress.IPv4Network("0.0.0.0"))

    class RequirerUnitInterface(UnitBucketInterface):

        bool = Boolean(False)
        int = Integer(0)
        float = Float(0.0)
        str = String("")
        privport = PrivilegedPort(0)
        ipaddr = IPAddress(ipaddress.IPv4Address("0.0.0.0"))
        ipnet = IPNetwork(ipaddress.IPv4Network("0.0.0.0"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interface_classes[("provider", "app")] = self.ProviderAppInterface
        self.interface_classes[("provider", "unit")] = self.ProviderUnitInterface
        self.interface_classes[("requirer", "app")] = self.RequirerAppInterface
        self.interface_classes[("requirer", "unit")] = self.RequirerUnitInterface


interface_registry.register("relation-copy-data", CopyDataRelationSuperInterface)

if __name__ == "__main__":
    siface = interface_registry.load("relation-copy-data", None, "copy-data")
    siface.print_doc()
