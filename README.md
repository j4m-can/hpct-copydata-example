# HPCT Copy Data Example

## Description

Copy app and unit relation data from "provider" to "requirer". All the items are named the same. A variety
of types are provided for demonstration.

## How It Works

When anything changes (app or unit) on the provider side, the requirer is notified via an event, and the corresponding (1:1 name) data is copied.

Interface member names are explicitly used to demonstrate functionality. ```setattr``` could also have been used.

## Usage

To deploy and set up:

1. ```juju deploy <charmfile> copydata-feed```
2. ```juju deploy <charmfile> copydata-sink```
3. ```juju relate copydata-feed:feed copydata-sink:sink```

Note: The relation names are being specified explicitly because the same operator (just using different app names) is being used for this example. Normally, if two different operators are being used, then the relation name can be the same and the ```relate``` step does not need the actual relation names.

To configure feed app setting:

```juju run-action copydata-feed/leader configure-app bool=true --wait```

To configure feed unit setting:

```juju run-action copydata-feed/<unit> configure-unit int=5 --wait```

Any changes made on the sink side (app or unit) will affect that side only and will put it out of sync with the feed side. This can be useful for testing.

Note that an action that does not actually result in a change to an data item will *not* result in an event.

`CONTRIBUTING.md` for developer guidance.
