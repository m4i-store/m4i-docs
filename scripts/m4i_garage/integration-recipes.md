# Integration Recipes — M4I Garage

The complete current Garage-specific integration examples have moved to **[Required Changes in Other Scripts](integrations.md)**.

This is the authoritative place to see the **exact file to edit** and the **Garage-side call** required when using:

- Dealer: allowlist the exact resource and call server `GetGarageCharacterId` → `RegisterOwnedVehicle` after verified payment.
- Mechanic: trusted server `BeginFullRepair` plus client `NotifyVehicleRepaired` after actual full repair.
- Cover Item: correct QB/ESX/Ox Inventory registration and Usable callback, with five-use accounting.
- Keys: plate-based QB versus entity-based Qbox adapters.
- Radial/Target/TextUI: only change an actual matching Bridge provider; `keys` is the Garage baseline alternative to radial.
- Phone: LB/QS supported custom app, `phone` inventory item; QB Phone/NPWD need specific compatible integration.
- Migration: existing `player_vehicles`/`owned_vehicles` are not auto-imported.
- Vehicle photos: optional Upload ID, not an automatic change to unrelated NUI.

**API documentation is now split properly:** [Client Exports](client-exports.md) and [Server Exports](server-exports.md), each with arguments, results and Lua examples.

This page remains so previously shared links still reach the up-to-date guides.