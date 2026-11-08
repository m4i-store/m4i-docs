# Updating and Migrating Without Losing Vehicles


> **0.1.140-alpha optional feature:** `NativeVehicleCompatibility.DeleteOnNativeRowMissing` defaults to `false`. Once native projection is verified and enabled on QB/Qbox/ESX, a customer may choose `true` to archive+remove a previously linked normal stored car only after repeated absence checks. Existing or historical missing native rows can become eligible after the grace period, so **audit missing links before enabling and take a full SQL backup**. [Complete safety guide](sql-ownership-and-deletion.md).


> **Deleting a vehicle from `player_vehicles` or `owned_vehicles` is not the same as deleting it from Garage.** Read [SQL Ownership and Admin Deletion](sql-ownership-and-deletion.md), including `PREVIOUS_NATIVE_ROW_MISSING` and the missing public Delete export.

**For:** `m4i_garage 0.1.140-alpha` and compatible Bridge. Production users must upgrade deliberately: vehicle custody is valuable persistent state, not disposable UI cache.

## Upgrade checklist

1. Announce a controlled maintenance window; **stop new garage/vehicle/cover actions** in game.
2. Back up **the entire database**, including all `m4ig_*` and optional runtime-created tables. Also preserve existing `player_vehicles` (QB/QBX), `owned_vehicles` (ESX) and inventory item definitions.
3. Back up **the resource directories**, `config.lua`, `server.cfg`, local data/assets and custom adapters; if using Upload, back up its own persistent data separately.
4. Record the actual version from `m4i_garage/fxmanifest.lua`; verify the new ZIP really contains the intended release.
5. Compare the old and new `config.lua`, `sql/install.sql`, `fxmanifest.lua`, docs and supported exports. Preserve customer choices and new defaults. **Do not blindly overwrite a customized config**.
6. Run required SQL migrations against a **staging copy** first. `install.sql` creates the base Garage tables using `CREATE TABLE IF NOT EXISTS`; it does not guarantee every table/column needed by every optional runtime module.
7. Update the inner `m4i_garage` resource folder, preserving approved config and persistent data. Ensure `m4i_bridge` is a compatible version.
8. Restart dependencies only where necessary and during the maintenance window. Do not restart a Garage while players are retrieving/storing cars.
9. Run `m4ig_doctor` in the server console, then validate the full QA checklist with **two real clients** before reopening.
10. Keep both DB and resource backups until the new release proves Store/Retrieve, damage, legal holds, money and restarts safe.

## Migrating from QB/ESX/Qbox garage systems

**Never confuse read compatibility with ownership migration.**

Garage stores its own rows in `m4ig_vehicles` with stable numeric Garage character IDs. An existing QB/ESX/Qbox server may have many cars in other tables. `Config.NativeVehicleCompatibility.Enabled=true` does **not import** those cars into Garage. It projects **already Garage-owned** vehicles into selected framework-readable SQL, with event-driven synchronization when `SyncIntervalMs=0`.

Before deactivating `qb-garages`, `qbx_garages`, `esx_garage` or any other vendor:

| Audit item | What to verify |
| --- | --- |
| Owner mapping | Raw ESX/QB string ID → correct connected/mapped Garage numeric character |
| Plate uniqueness | Collisions across existing player rows, NPC/test cars and Garage rows |
| Model/category | GTA class and Land/Water/Air target Garage |
| Vehicle props | Mods, plate, livery, fuel, engine, tank, windows, doors, deformation |
| Status | Stored, out, impounded, seized, legal hold and current location |
| Keys | Permanent, shared and temporary permissions versus external keys resource |
| Phone/house | Every old vehicle-list/status/garage export/event still called |
| Payments | Outstanding impound/insurance/GPS charges and refund state |
| Rollback | How to restore previous authoritative Garage without creating duplicate cars |

**Safe staged approach:** export only verified source rows, create a one-time **trusted migration program** that maps each original owner and vehicle to Garage's normalized model/category, then reconcile counts, plates, status and permissions. Store a migration log/idempotency key. Do not use a public command that blindly registers cars from client-submitted plate/model.

The shipped `RegisterOwnedVehicle` export is intended for **trusted server-side ownership registration**, not a turnkey bulk importer for every vendor. It rejects duplicates and mismatched class/category; verify any migration adapter against its contract.

## Native read compatibility

```lua
-- m4i_garage/config.lua
Config.NativeVehicleCompatibility = {
    Enabled = false,
    SyncIntervalMs = 0,
    QbPhoneCallback = true
}
```

Only enable after verifying what the current provider actually projects, that **Garage alone controls spawning and storage**, and that native table values reflect an existing Garage-owned car rather than overwriting someone else's legacy row.

It does not automatically recreate Qbox `qbx_garages` exports, every QB Phone callback, a housing garage API or third-party vehicle spawn behavior. Implement those missing calls through a validated server companion if customers need them.

## SQL schema risks

The base installer creates eight Garage-owned tables. Some optional support modules create additional tables automatically; an SQL account without DDL privileges may be unable to initialize them. A controlled migration account can pre-apply exact versioned table definitions.

**Known optional blocker:** Paid AI Valet currently references a payment table not created by the reviewed installer, plus an M4I-specific ledger in its recovery path. Keep `Config.DeliveryEnabled=false` on unverified builds. Read [Known Limitations](../../shared/fivem-install-known-limitations.md).

## How to roll back correctly

If a release fails:

1. Stop the new Garage and prevent simultaneous use of the previous Garage.
2. Restore the **matching resource code, configuration and required database state** from the snapshot taken before upgrade.
3. Reconcile cars touched after backup; **never overwrite all live player vehicles with a stale old DB** without explicitly accounting for new legitimate transactions.
4. Restore vendor compatibility shims and chosen provider selection.
5. Run server doctor and two-client Store/Retrieve on staging.
6. Only reopen to players once duplicate/ghost vehicle and legal-hold counts have been reviewed.

**Don't reset `m4ig_identity_map`** casually: its numeric surrogate references are used by Garage-owned vehicles. And do not delete the Upload resource's persistent `data/` to “fix” an image loading problem.

**Next:** [Installation](installation.md) · [Integrations](integrations.md) · [Go-Live Verification](verification.md) · [Troubleshooting](troubleshooting.md).