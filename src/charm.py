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

# import to load interfaces to registry
import interfaces.copydata

from hpctlib.interface import interface_registry
from hpctlib.ops.charm.service import ServiceCharm


logger = logging.getLogger(__name__)


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

                appiface.bool = rappiface.bool
                appiface.int = rappiface.int
                appiface.float = rappiface.float
                appiface.privport = rappiface.privport
                appiface.ipaddr = rappiface.ipaddr
                appiface.ipnet = rappiface.ipnet

            else:
                # unit update
                unitiface = self.siface.select(self.unit)
                runitiface = self.siface.select(event.unit)

                unitiface.bool = runitiface.bool
                unitiface.int = runitiface.int
                unitiface.float = runitiface.float
                unitiface.privport = runitiface.privport
                unitiface.ipaddr = runitiface.ipaddr
                unitiface.ipnet = runitiface.ipnet
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
                iface.bool = event.params["bool"]
            if "int" in event.params:
                iface.int = event.params["int"]
            if "float" in event.params:
                iface.float = float(event.params["float"])
            if "privport" in event.params:
                iface.privport = event.params["privport"]
            if "ipaddr" in event.params:
                iface.ipaddr = ipaddress.IPv4Address(event.params["ipaddr"])
            if "ipnet" in event.params:
                iface.ipnet = ipaddress.IPv4Network(event.params["ipnet"])

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
                "APP"
                f" bool ({appiface.bool})"
                f" int ({appiface.int})"
                f" float ({appiface.float})"
                f" privport ({appiface.privport})"
                f" ipaddr ({appiface.ipaddr})"
                f" ipnet ({appiface.ipnet})"
                f" :: "
            )
        else:
            appmsg = ""

        # self/unit info
        unitmsg = (
            "UNIT"
            f" bool ({selfiface.bool})"
            f" int ({selfiface.int})"
            f" float ({selfiface.float})"
            f" privport ({selfiface.privport})"
            f" ipaddr ({selfiface.ipaddr})"
            f" ipnet ({selfiface.ipnet})"
        )

        self.unit.status = ActiveStatus(
            f"{tuple(self.service_get_updated())} :: {appmsg}{unitmsg}"
        )


if __name__ == "__main__":
    main(CopyDataCharm)
