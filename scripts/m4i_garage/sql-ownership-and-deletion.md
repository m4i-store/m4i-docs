# Vehicle SQL Ownership, Native Sync and Admin Deletion

**M4I Garage:** `0.1.139-alpha` · source-verified against the installed `m4i_garage/server/native_vehicle_compat.lua` and `server/exports.lua` on 8 November 2026.

**Most important rule:** **`m4ig_vehicles` is the authoritative Garage-owned vehicle table.** On supported external frameworks, `player_vehicles` (QBCore/Qbox) and `owned_vehicles` (ESX) may be optional **native compatibility projections**, not automatic ownership sources for Garage.

## Which database table controls the Garage vehicle?

| Framework | Garage-owned record | Native framework record |
| --- | --- | --- |
| M4I Core | `m4ig_vehicles` | No QB/ESX native projection |
| QBCore | **`m4ig_vehicles`** | Optional `player_vehicles` |
| Qbox / QBX | **`m4ig_vehicles`** | Optional `player_vehicles` |
| ESX Legacy | **`m4ig_vehicles`** | Optional `owned_vehicles` |
| Ox Core | **`m4ig_vehicles`** | No native projection implemented by the reviewed compatibility code |

The optional `m4ig_identity_map` associates a Garage numeric character ID with the native external player identifier, and `m4ig_native_vehicle_links` records any existing Garage↔native vehicle mapping.

## Scenario A — Admin deletes the car only from `player_vehicles`

Example: the Garage has a Sultan registered to the player in `m4ig_vehicles`, but an administrator deletes the matching `player_vehicles` row using phpMyAdmin.

- **Current default, `NativeVehicleCompatibility.Enabled=false`:** the native row disappears, but the Garage's authoritative record remains. If otherwise eligible, the player can still see, Store and Retrieve that Garage-owned car. An older QB Phone, Housing, Dealership or Keys system that reads only `player_vehicles` may instead show the car missing.
- **When `Enabled=true` and an old native link exists:** the next Garage projection detects the previously linked native row is gone and returns **`PREVIOUS_NATIVE_ROW_MISSING`**. It **does not blindly recreate the deleted native vehicle**. The Garage-owned `m4ig_vehicles` row still remains.
- **When `Enabled=true` but no previous native link exists:** a projection may **create a native row** if it can validate the owner, plate, model and destination table schema. Therefore do not assume that every native-table deletion will stay deleted.
- **External SQL DELETE is not a Garage-owned delete event.** Garage has no reason to treat an unrelated native row removal as authority to remove an owner's registered Garage vehicle.

**Observed code:** `server/native_vehicle_compat.lua` checks `m4ig_native_vehicle_links` before creating a missing native row. If a prior link exists, it returns `PREVIOUS_NATIVE_ROW_MISSING` rather than resurrecting the row.

## Scenario B — Admin deletes the car only from `m4ig_vehicles`

This is **dangerous** and is **not** the supported administrative deletion workflow.

- Garage may no longer find the authoritative owner/plate/condition record. Player-facing Garage vehicle lists and Store/Retrieve will no longer treat that deleted record as a normal Garage-owned car.
- The original native `player_vehicles` / `owned_vehicles` row may **still exist**. The compatibility layer is **one-way from Garage to native**, and is not a guaranteed synchronized-delete mechanism.
- Related rows may exist in `m4ig_access`, `m4ig_temp_keys`, `m4ig_cases`, `m4ig_audit`, `m4ig_native_vehicle_links` and other installed modules. Deleting only the Garage row can leave inconsistent references or historical records. Whether database foreign keys cascade depends on the installed schema.
- An actively spawned vehicle could still exist in the GTA world or another resource's state. A bare SQL DELETE does not perform safe entity removal.

**Never instruct customers to run an unreviewed manual DELETE on a live server.** Back up the DB, inspect legal holds and active world entities, and perform any migration or cleanup through a documented, audited, server-authoritative process.

## Scenario C — Admin wants to delete a vehicle permanently everywhere

As of this documented Garage release, **there is no public `DeleteOwnedVehicle` / `RemoveOwnedVehicle` server export in the shipped Garage API**. Do not pretend an in-game button or API already implements complete deletion.

A future safe admin-only deletion flow would need to:

1. Authenticate the admin on the **server**; confirm intended vehicle ID, owner, plate and reason.
2. Check ownership, legal/seized/impound state, active temporary access, any pending transfer or claim and whether the vehicle currently exists in-world or has occupants.
3. Take a transactionally consistent snapshot/backup; record an audit entry with who initiated the action.
4. Safely remove the live entity **after** occupants and outstanding actions are handled; prevent duplicate Store/Spawn operations.
5. Update/remove the **authoritative `m4ig_vehicles` record and related access/keys/native-link records** according to a documented deletion/retention policy, in a controlled DB transaction wherever possible.
6. Update the native projection target (`player_vehicles` / `owned_vehicles`) **only if the installed integration owns that native record**, while respecting other resources' dependencies.
7. Check vehicle lists, keys, phone apps, police/impound cases and concurrent player sessions afterward.

**This is a design/implementation checklist, not a claim that the current release already has the feature.** Until that workflow is implemented and tested, do not promise customers a fully synchronized cross-framework Delete button.

## How to inspect a car safely in phpMyAdmin (read-only)

Always select the **correct framework database** first, and take a backup before changing anything.

```sql
-- Change the example plate to your real normalized plate.
SELECT id, character_id, plate, model, garage_id, physical_status
FROM m4ig_vehicles
WHERE plate = 'ABC123';

-- QBCore/Qbox only:
SELECT id, citizenid, plate, vehicle, garage, state
FROM player_vehicles
WHERE plate = 'ABC123';

-- ESX only (run in ESX database, not in QB database):
SELECT owner, plate, vehicle, stored, parking
FROM owned_vehicles
WHERE plate = 'ABC123';

-- Optional native compatibility link (when table is installed):
SELECT *
FROM m4ig_native_vehicle_links
WHERE native_plate = 'ABC123';
```

These are **diagnostic SELECT statements only**; they do not delete, revive or migrate the vehicle. If a query fails with "unknown table" or "unknown column", inspect that particular framework/schema release instead of copying another framework's SQL.

## Changing synchronization mode

The installed Garage configuration uses:

```lua
-- m4i_garage/config.lua
Config.NativeVehicleCompatibility = {
    Enabled = false,
    SyncIntervalMs = 0,
    QbPhoneCallback = true,
}
```

When **false**, there is no automatic native table projection. When **true** on QBCore/Qbox/ESX, Garage performs one validated startup projection and event-driven updates at `SyncIntervalMs=0`; a positive interval enables periodic checks. It **does not import legacy native cars into Garage**, automatically delete all native rows when an M4I Garage car disappears or replace all old Garage/Phone/Housing exports.

**For developers:** [Server API](server-exports.md) · [External Integrations](integrations.md) · [Updating / Native Migration](updating.md) · [Troubleshooting](troubleshooting.md) · [Installation](installation.md).