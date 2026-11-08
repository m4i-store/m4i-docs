# Vehicle SQL Ownership, Native Synchronization and Deletion

**M4I Garage `0.1.140-alpha`** · Source: `server/native_vehicle_compat.lua`, `server/native_vehicle_deletion.lua`, `config.lua` and `sql/install.sql` · Updated 8 November 2026.

**Core principle:** `m4ig_vehicles` is always Garage's authoritative vehicle table. QB/Qbox `player_vehicles` and ESX `owned_vehicles` are optional native compatibility tables; M4I Garage does not blindly import old framework cars.

## 1 — Which table holds vehicles?

| Framework | Garage authoritative table | Optional native read-compatible table | Native deletion mirror? |
| --- | --- | --- | --- |
| M4I Core | `m4ig_vehicles` | None from this module | Not applicable |
| QBCore | **`m4ig_vehicles`** | `player_vehicles` | Supported, opt-in |
| Qbox / QBX | **`m4ig_vehicles`** | `player_vehicles` | Supported, opt-in |
| ESX Legacy | **`m4ig_vehicles`** | `owned_vehicles` | Supported, opt-in |
| Ox Core | `m4ig_vehicles` | No native projection in reviewed module | Not applicable |

The existing `m4ig_native_vehicle_links` associates each Garage-owned vehicle with a **specific previously verified native row**. `m4ig_identity_map` maps QB/ESX/Qbox string character IDs into Garage's persistent numeric ID.

## 2 — Customer config: TRUE / FALSE

Open **`m4i_garage/config.lua`**, find the existing `Config.NativeVehicleCompatibility` table and edit its values. Do not create a second table or put this snippet in your Framework Core.

```lua
Config.NativeVehicleCompatibility = {
    Enabled = true,  -- REQUIRED to create and check native-linked records

    -- FALSE (default): deleting player_vehicles / owned_vehicles
    -- does NOT delete the matching m4ig_vehicles record.
    -- TRUE: after verified native deletion, automatically delete
    -- the eligible stored Garage record, with SQL archive + audit.
    DeleteOnNativeRowMissing = false,

    SyncIntervalMs = 0,
    QbPhoneCallback = true,
}
```

**Both `Enabled` and `DeleteOnNativeRowMissing` must be `true`** for this feature to run. If `Enabled=false`, toggling only `DeleteOnNativeRowMissing=true` does nothing. Do not enable native projection before migrating or auditing any existing framework ownership rows, phone/housing scripts and original Garage controller.

### Choose the behavior

| `Enabled` | `DeleteOnNativeRowMissing` | Result |
| --- | --- | --- |
| `false` | `false` or `true` | No native projection/deletion mirror; Garage's own records remain authoritative |
| `true` | **`false` (default)** | Native projection works; a native-row deletion is logged as missing/linked, but Garage-owned car stays |
| `true` | **`true` (optional)** | Verified loss of a *previously linked* native row schedules protected deletion of an eligible **normally stored** Garage record |

**Only QBCore, Qbox and ESX support this mirror**. The file still contains the setting on M4I/Ox Core, but those profiles have no relevant native table to monitor. Changes require a safe restart of `m4i_garage`; they are not a live Confige toggle.

## 3 — What exactly happens when TRUE?

Example: an administrator deletes `ABC123` from QBCore `player_vehicles` using phpMyAdmin. The car has an existing verified `m4ig_native_vehicle_links` entry.

1. Garage's independent native-row monitor checks previously linked, missing records **every 60 seconds**, even when `SyncIntervalMs = 0`.
2. The native row must remain absent for at least **180 seconds (3 minutes)** over repeated successful checks. If the row returns or the database check fails, the pending deletion is cancelled/reset.
3. Garage revalidates the correct framework, owner/character identity, native row ID, **normalized plate**, Garage location/status, police legal holds, active cases, live entity and pending operations. An unrelated duplicate native plate or a reassigned native row stops deletion.
4. Only a **normal `physical_status='stored'` vehicle with `legal_hold=0`**, no Cover metadata and no world/valet activity is eligible. `out`, `covered`, `impounded`, `seized`, `delivering` or active police cases are explicitly protected. If it becomes normally stored later while still truly missing, it can become eligible then.
5. Before removal, the server writes the vehicle's row snapshot to `m4ig_native_delete_archive`. Its controlled **SQL transaction** deletes the eligible `m4ig_vehicles` row and dependent temporary-key/shared-access/native-link rows, plus present optional reminder/snapshot rows, and inserts a `native_delete_sync` audit entry.
6. The default limit is **five deletions per 60-second pass** to avoid a large unexpected cascade. Player UI reflects the loss when it next requests the Garage list.

**The archive is a backup, not a public Restore button.** The removed vehicle can be investigated in the SQL archive, but restoration requires an administrator to reconcile the native owner, link and Garage record from a tested backup or controlled restoration process. No customer-facing automatic restore export is provided.

### Safeguards

- No previous native link → **never delete** based on a native row not being found.
- Native row reappeared, even under a new native ID with the **same normalized plate** → **do not delete**.
- Legal hold, Police Seize, Impound, world vehicle, cover, active valet/charge → **do not delete**.
- Missing native table / SQL error / interrupted database query → fail closed; the pending timer resets.
- Manual `DELETE FROM m4ig_vehicles` does **not** delete the native table automatically. This option is deliberately **one-way** from a missing **linked native row** to a safe stored Garage car.
- False by default for customer safety. It does not operate on native records from M4I Core or Ox Core.

## 4 — Check the archive, linkage and audit in phpMyAdmin

Use the correct QB/ESX/Qbox database. The following **SELECT** queries are safe and do not change player data.

```sql
-- Garage authoritative record:
SELECT id, character_id, plate, model, garage_id, physical_status, legal_hold
FROM m4ig_vehicles WHERE plate='ABC123';

-- Previously linked native record, if any:
SELECT *
FROM m4ig_native_vehicle_links WHERE native_plate='ABC123';

-- Archived records deleted by the optional monitor:
SELECT m4ig_vehicle_id, framework, native_vehicle_id, native_owner,
       plate, deleted_at
FROM m4ig_native_delete_archive
WHERE plate='ABC123';

-- Who/what removed the car (system actor is NULL):
SELECT vehicle_id, action, detail, created_at
FROM m4ig_audit
WHERE action='native_delete_sync'
ORDER BY id DESC LIMIT 20;
```

For **QBCore/Qbox** also inspect `player_vehicles`; for **ESX** inspect `owned_vehicles` using that installed vendor's actual column names. Do **not** copy a native vendor's column names into another framework or attempt to repair a missing row by inserting fake Garage ownership SQL.

## 5 — What if an Admin manually deletes from `m4ig_vehicles` instead?

That is **not the same direction as this toggle**. It can leave native rows, orphaned access, case history and spawned world entities. Deleting an authoritative Garage row directly can break custody. This optional monitor does **not** propagate SQL deletions from Garage back to QB/ESX.

There remains **no public `DeleteOwnedVehicle` / `RemoveOwnedVehicle` Server Export** or one-click admin GUI Delete workflow for arbitrary cars in this Garage release. The new feature is a bounded, automated reconciliation of a **previously linked native-row deletion**, not an unrestricted vehicle deletion API.

## 6 — Before setting TRUE in production

1. Take a **full SQL backup** of `m4ig_*` and native player vehicles, and back up your current `config.lua`.
2. Confirm `NativeVehicleCompatibility.Enabled=true` is already safely in use and that the native Garage resource is not simultaneously controlling stored cars.
3. Inspect `m4ig_native_vehicle_links` for actual verified associations, and resolve old missing native records before enabling. The 3-minute grace gives a warning window; it does not automatically make a contaminated migration safe.
4. Change **only** `DeleteOnNativeRowMissing` to `true`, restart `m4i_garage` in a maintenance window, run console `m4ig_doctor`.
5. Test **one disposable Garage-owned car**: delete its linked QB/ESX native row in the staging database; check log, archive, Garage vehicle absence and link cleanup after the verified grace.
6. Also test that a currently `out`, covered, impounded or seized car is protected, and that restoring a native row before grace expiry cancels deletion.
7. If behavior is unwanted, set **`DeleteOnNativeRowMissing=false`** and restart; this **stops future automatic deletions**, but does not resurrect previously deleted vehicles. Restore those from the archive/backup with an approved recovery workflow.

**Source QA status:** The `0.1.140-alpha` implementation was validated with isolated MariaDB transaction cases (QB/ESX record missing/present, reassigned ID, legal hold, covered/out, active case) and Lua scheduler/grace tests. **Real multiplayer production deletion tests were not performed**, and customers should stage-test before enabling `true`.

**Related:** [Full Installation](installation.md) · [Every Config Setting](customization-reference.md) · [Framework-Specific Installers](framework-installation.md) · [Server Exports](server-exports.md) · [Updating](updating.md) · [Troubleshooting](troubleshooting.md).