#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Copy data example.

See README.md for more.
"""


import ipaddress
import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, WaitingStatus

from hpctlib.interface import codec, checker
from hpctlib.interface import interface_registry
from hpctlib.interface.base import Value
from hpctlib.interface.relation import (
    AppBucketInterface,
    RelationSuperInterface,
    UnitBucketInterface,
)
from hpctlib.interface import value
from hpctlib.ops.charm.service import ServiceCharm


logger = logging.getLogger(__name__)


class CopyDataRelationSuperInterface(RelationSuperInterface):

    """Relation super interface."""

    class ProviderAppInterface(AppBucketInterface):

        _bool = Value(codec.Boolean(), False)
        _int = Value(codec.Integer(), 0)
        _float = Value(codec.Float(), 0.0)
        _str = Value(codec.String(), "")
        _privport = Value(codec.Integer(), 0, checker.PrivilegedPort())
        _ipaddr = Value(codec.IPAddress(), ipaddress.IPv4Address("0.0.0.0"))
        _ipnet = Value(codec.IPNetwork(), ipaddress.IPv4Network("0.0.0.0"))

    class ProviderUnitInterface(UnitBucketInterface):

        _bool = Value(codec.Boolean(), False)
        _int = Value(codec.Integer(), 0)
        _float = Value(codec.Float(), 0.0)
        _str = Value(codec.String())
        _privport = Value(codec.Integer(), 0, checker.PrivilegedPort())
        _ipaddr = Value(codec.IPAddress(), ipaddress.IPv4Address("0.0.0.0"))
        _ipnet = Value(codec.IPNetwork(), ipaddress.IPv4Network("0.0.0.0"))

    class RequirerAppInterface(AppBucketInterface):

        _bool = Value(codec.Boolean(), False)
        _int = Value(codec.Integer(), 0)
        _float = Value(codec.Float(), 0.0)
        _str = Value(codec.String(), "")
        _privport = Value(codec.Integer(), 0, checker.PrivilegedPort())
        _ipaddr = Value(codec.IPAddress(), ipaddress.IPv4Address("0.0.0.0"))
        _ipnet = Value(codec.IPNetwork(), ipaddress.IPv4Network("0.0.0.0"))

    class RequirerUnitInterface(UnitBucketInterface):

        _bool = Value(codec.Boolean(), False)
        _int = Value(codec.Integer(), 0)
        _float = Value(codec.Float(), 0.0)
        _str = Value(codec.String())
        _privport = Value(codec.Integer(), 0, checker.PrivilegedPort())
        _ipaddr = Value(codec.IPAddress(), ipaddress.IPv4Address("0.0.0.0"))
        _ipnet = Value(codec.IPNetwork(), ipaddress.IPv4Network("0.0.0.0"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interface_classes[("provider", "app")] = self.ProviderAppInterface
        self.interface_classes[("provider", "unit")] = self.ProviderUnitInterface
        self.interface_classes[("requirer", "app")] = self.RequirerAppInterface
        self.interface_classes[("requirer", "unit")] = self.RequirerUnitInterface


class CopyDataRelationSuperInterface(RelationSuperInterface):

    """Relation super interface."""

    class ProviderAppInterface(AppBucketInterface):

        _bool = value.Boolean(False)
        _int = value.Integer(0)
        _float = value.Float(0.0)
        _str = value.String("")
        _privport = value.Integer(0, checker.PrivilegedPort())
        _ipaddr = value.IPAddress(ipaddress.IPv4Address("0.0.0.0"))
        _ipnet = value.IPNetwork(ipaddress.IPv4Network("0.0.0.0"))

    class ProviderUnitInterface(UnitBucketInterface):

        _bool = value.Boolean(False)
        _int = value.Integer(0)
        _float = value.Float(0.0)
        _str = value.String("")
        _privport = value.Integer(0, checker.PrivilegedPort())
        _ipaddr = value.IPAddress(ipaddress.IPv4Address("0.0.0.0"))
        _ipnet = value.IPNetwork(ipaddress.IPv4Network("0.0.0.0"))

    class RequirerAppInterface(AppBucketInterface):

        _bool = value.Boolean(False)
        _int = value.Integer(0)
        _float = value.Float(0.0)
        _str = value.String("")
        _privport = value.Integer(0, checker.PrivilegedPort())
        _ipaddr = value.IPAddress(ipaddress.IPv4Address("0.0.0.0"))
        _ipnet = value.IPNetwork(ipaddress.IPv4Network("0.0.0.0"))

    class RequirerUnitInterface(UnitBucketInterface):

        _bool = value.Boolean(False)
        _int = value.Integer(0)
        _float = value.Float(0.0)
        _str = value.String("")
        _privport = value.Integer(0, checker.PrivilegedPort())
        _ipaddr = value.IPAddress(ipaddress.IPv4Address("0.0.0.0"))
        _ipnet = value.IPNetwork(ipaddress.IPv4Network("0.0.0.0"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interface_classes[("provider", "app")] = self.ProviderAppInterface
        self.interface_classes[("provider", "unit")] = self.ProviderUnitInterface
        self.interface_classes[("requirer", "app")] = self.RequirerAppInterface
        self.interface_classes[("requirer", "unit")] = self.RequirerUnitInterface


class CopyDataCharm(ServiceCharm):
    """Copy data example."""

    def __init__(self, *args):
        super().__init__(*args)

        if self.app.name.endswith("-feed"):
            self.relname = "feed"
        elif self.app.name.endswith("-sink"):
            self.relname = "sink"

        self.siface = interface_registry.load("relation-copy-data", self, self.relname)

        self.framework.observe(self.on.feed_relation_changed, self._on_feed_relation_changed)
        self.framework.observe(self.on.sink_relation_changed, self._on_sink_relation_changed)

        self.framework.observe(self.on.configure_app_action, self._on_configure_app_action)
        self.framework.observe(self.on.configure_unit_action, self._on_configure_unit_action)

    def _on_leader_elected(self, event):
        """leader-elected."""

        self.service_set_updated("leader-elected")
        self.service_update_status()

    def _on_feed_relation_changed(self, event):
        """Nothing to do for this exercise."""

        self.service_set_updated("feed-relation-changed")
        self.service_update_status()

    def _on_sink_relation_changed(self, event):
        """Copy information (app/unit) from provider to reqiurer."""

        try:
            if event.unit == None:
                # app update
                appiface = self.siface.select(self.app)
                rappiface = self.siface.select(event.app)

                appiface._bool = rappiface._bool
                appiface._int = rappiface._int
                appiface._float = rappiface._float
                appiface._privport = rappiface._privport
                appiface._ipaddr = rappiface._ipaddr
                appiface._ipnet = rappiface._ipnet

            else:
                # unit update
                unitiface = self.siface.select(self.unit)
                runitiface = self.siface.select(event.unit)

                unitiface._bool = runitiface._bool
                unitiface._int = runitiface._int
                unitiface._float = runitiface._float
                unitiface._privport = runitiface._privport
                unitiface._ipaddr = runitiface._ipaddr
                unitiface._ipnet = runitiface._ipnet
        finally:
            self.service_set_updated("sink-relation-changed")
            self.service_update_status()

    def _on_configure_app_action(self, event):
        return self._on_configure_action("app", event)

    def _on_configure_unit_action(self, event):
        return self._on_configure_action("unit", event)

    def _on_configure_action(self, what, event):
        """Configure settings (for app and unit)."""

        try:
            if what == "app":
                if self.unit.is_leader():
                    iface = self.siface.select(self.app)
                else:
                    return
            else:
                iface = self.siface.select(self.unit)

            # yes, this could have been done with a loop and setattr, but is
            # intended to demonstrate interfaces
            if "bool" in event.params:
                iface._bool = event.params["bool"]
            if "int" in event.params:
                iface._int = event.params["int"]
            if "float" in event.params:
                iface._float = float(event.params["float"])
            if "privport" in event.params:
                iface._privport = event.params["privport"]
            if "ipaddr" in event.params:
                iface._ipaddr = ipaddress.IPv4Address(event.params["ipaddr"])
            if "ipnet" in event.params:
                iface._ipnet = ipaddress.IPv4Network(event.params["ipnet"])

        finally:
            self.service_set_updated("configure-action")
            self.service_update_status()

    def service_update_status(self):
        """Report information via the status message."""

        relation = self.model.get_relation(self.relname)
        if not relation:
            self.unit.status = WaitingStatus(f"no relation yet")
            return

        appiface = self.siface.select(self.app)
        selfiface = self.siface.select(self.unit)

        if self.unit.is_leader():
            # app info
            appmsg = (
                f" _bool ({appiface._bool})"
                f" _int ({appiface._int})"
                f" _float ({appiface._float})"
                f" _privport ({appiface._privport})"
                f" _ipaddr ({appiface._ipaddr})"
                f" _ipnet ({appiface._ipnet})"
                f" :: "
            )
        else:
            appmsg = ""

        # self/unit info
        unitmsg = (
            f" _bool ({selfiface._bool})"
            f" _int ({selfiface._int})"
            f" _float ({selfiface._float})"
            f" _privport ({selfiface._privport})"
            f" _ipaddr ({selfiface._ipaddr})"
            f" _ipnet ({selfiface._ipnet})"
        )

        self.unit.status = ActiveStatus(f"{tuple(self.service_get_updated())} {appmsg}{unitmsg}")


if __name__ == "__main__":
    interface_registry.register("relation-copy-data", CopyDataRelationSuperInterface)

    main(CopyDataCharm)
