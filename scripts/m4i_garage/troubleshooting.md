# Troubleshooting — Garage Errors and Fixes


> **Admin deleted a native SQL car?** Set `DeleteOnNativeRowMissing=false` to keep Garage custody unchanged, or set it `true` alongside `Enabled=true` to archive and remove a safely stored, previously linked Garage vehicle after at least 3 minutes. Check `m4ig_native_delete_archive` and audit action `native_delete_sync`. No automatic deletion for `out`, seized, covered, impounded or delivering cars. [Full diagnosis](sql-ownership-and-deletion.md).


> **Admin deleted a car in phpMyAdmin?** Start at [SQL Ownership and Admin Deletion](sql-ownership-and-deletion.md). Native QB/ESX rows and Garage-owned rows have separate authority; never blindly delete both.

**Current source:** `m4i_garage 0.1.140-alpha` · M4I Bridge `1.5.19-rc.1`. Troubleshoot **the failing layer** before changing code or deleting SQL.

## First diagnosis in 60 seconds

1. Check resource names and states: `oxmysql`, your one chosen framework, `m4i_bridge` and `m4i_garage`. Do not leave an old garage controlling the same vehicles.
2. Run **`m4ig_doctor` in FXServer console**, not in game chat. It prints framework/inventory/target/radial readiness and Garage `ready`.
3. Check actual selected provider IDs in `m4i_bridge/config.lua` and legacy `setr m4i_bridge_profile` overrides.
4. Check **F8** and FXServer console for the exact error or request rejection.
5. Open `/garagecreator` with admin rights; confirm at least one **enabled zone with valid spawn bay**, and test the easiest `InteractionMode='keys'` baseline.
6. Make one change at a time and retry with an authorized Garage-owned test vehicle. Avoid production SQL resets.

## Installation and provider problems

| Symptom | Most likely cause / what to do |
| --- | --- |
| **Could not find resource `m4i_garage`** | ZIP wrapper nested incorrectly or folder renamed. Need `resources/[m4i]/m4i_garage/fxmanifest.lua`. |
| **Missing `@m4i_bridge/shared/zones.lua`** | Bridge resource missing, renamed, old release, or started after Garage; install real Bridge and use correct name. |
| **Database setup missing** | `oxmysql` wrong DB connection, Garage `sql/install.sql` not imported, table permission/migration issue. |
| **Doctor: Bridge not ready** | Wrong framework, missing resource or provider adapter. Check Bridge config and startup states, not Garage HTML. |
| **Doctor says radial missing** | In `radial` mode start the selected real radial; alternatively use `Config.InteractionMode='keys'` with E/H. |
| **Selected framework not what expected** | Legacy `setr m4i_bridge_profile` may override `M4IBridgeConfig.Framework`. Qbox ID is `qbox` not `qbx`. |
| **ESX has no `esx_inventory` resource** | Do not ensure a fictitious inventory; select actual Ox Inventory or installed ESX provider in Bridge. |
| **Ox Core reports startup but gameplay fails** | Ox Core live end-to-end tests are not completed; verify identity/jobs/bank/inventory or do not declare certified support. |

## UI, zoning, radial, target

| Problem | How to isolate / fix |
| --- | --- |
| **Garage radial menu absent on Qbox** | Check `qbx_radialmenu` **actual resource and adapter ID**, icon schema and add/remove methods. Switch to keys mode to prove Garage works; fix Bridge adapter only after. |
| **QB radial icon appears but clicking does nothing** | Wrong selected provider, export callback signature, or action removed outside zone. Verify `qb-radialmenu` API version and Garage near saved bay. |
| **E/H prompt missing** | Must use keys mode, be inside valid PolyZone and close to bay; TextUI provider must actually be running and not hidden by overlapping cover/target overlay. |
| **Open/Store no action** | Garage disabled or no valid spawn bay, category mismatch, permission denied, unregistered car, player too far, passenger in vehicle, or NUI callback rejected. |
| **Target NPC not clickable** | Target adapter add/remove entity callback mismatch, NPC not streamed, `Config.NpcModel` invalid or player outside allowed range. |
| **Garage Creator does not open** | Missing `m4i.garage.admin` ACE or Bridge IsAdmin false; use `/garagecreator` in game, not FXServer console. |
| **Can't save Garage zone** | Check min 3 polygon points, non-self-intersecting geometry, valid minZ/maxZ, enabled status, spawn count and overlapping invalid area; inspect server rejection. |
| **Zone visible on wrong height** | Free Cam Z/minZ/maxZ or incorrect terrain/raycast. Test in actual GTA world, not just flat 2D map. |
| **Blip wrong color/icon or missing** | Individual garage blip visibility, sprite/color/scale, job access and category. Public garages can share legend while having individual map pins. |
| **Creator says stale revision** | Another admin/refresh updated authoritative record. Reload latest version, reapply only intended changes and save. |

## Cars, ownership and spawning

| Problem | Check |
| --- | --- |
| **My old QB/ESX vehicles don't appear** | They exist in original `player_vehicles`/`owned_vehicles`, not Garage's `m4ig_vehicles`. Separate migration required. |
| **GetGarageCharacterId returns nil** | Framework character not loaded; source ID invalid; Bridge framework mapping not ready. Use trusted server export after login. |
| **Dealer registration fails UNTRUSTED_RESOURCE** | Exact dealership resource name missing from `Config.TrustedVehicleRegistrars`; do not use a client direct call. |
| **Dealer says INVALID_GARAGE / class mismatch** | Destination Garage category/vehicle group does not match real GTA class, `spawnType`, model or legal kind. |
| **Two cars spawn / duplicate after relog** | Both old and M4I Garage controllers own same vehicle, or duplicate callback/repair of a failed spawn. Stop conflicting controller after migration verification. |
| **Can't retrieve due to spawn clearance** | Every configured bay is too close to another vehicle/person/cover or has invalid Z. Add safe bays/change live spawn policy via Creator. |
| **Passenger car disappears when storing** | Critical safety failure; verify passenger exit logic, server occupied-state checks and installed build; do not use unsafe manual delete script. |
| **Keys work in QB but not Qbox** | Plate-based QB keys API differs from entity/network-based Qbox keys contract; use a matching provider. |
| **Car condition resets to 0 / old dents return** | Hydration, tank and deformation observation, or full repair permit didn't persist; follow [Damage Guide](damage-persistence.md). |

## Covers, police, insurance and money

| Problem | Check |
| --- | --- |
| **Cover item does nothing in Ox Inventory** | Define client Use event + companion resource; `consume=0`, correct slot ID; [Cover Item Recipe](vehicle-cover-item.md). |
| **Cover item disappears after click** | Vendor inventory auto-consumption or wrong metadata receipt integration; don't deduct immediately on Use. |
| **Cover disappears a moment after spawn** | Cover Allow/Deny zones, 3D ground and saved rules, visibility streaming and restart policy; confirm prop exists. |
| **Can't immediately re-cover same car** | Server-enforced **15s cooldown** on success; edit `Config.CoverActionCooldownSeconds` only if desired. |
| **Solid Cover prop launches car** | Verify early collision disable, prop removal order and vehicle freeze; use Pass-through while debugging. |
| **Seize menu empty** | Stand near a valid eligible car (~3m), use Refresh Nearby Vehicles, ensure police job/grade and Seized facility. |
| **Police can't release despite paying** | Check legal hold vs Impound state; seizure requires authenticated release, not ordinary owner pickup. |
| **Insurance claim fails** | Must have current policy, valid out/occupied status, safe removal, sufficient real money; cannot bypass Police legal hold. |
| **Money refused despite adequate player cash/bank** | Selected Bridge Banking adapter reading wrong framework account or a society balance; test personal bank get/debit/refund. |
| **Phone Garage app missing** | LB/QS actual custom-app API mismatch, wrong Bridge Phone adapter or no `phone` inventory item. QB Phone/NPWD need dedicated adapter. |
| **AI Delivery fails/payments table missing** | Optional feature currently has source-known schema/ledger portability issues; set `Config.DeliveryEnabled=false` until fixed/verified. |

## Key source-verified errors

| Code | Meaning / expected correction |
| --- | --- |
| `UNTRUSTED_RESOURCE` | Dealership registrar isn't explicitly allowed by trusted server resource name |
| `INVALID_GARAGE` | Destination ID missing, wrong type/category/class or disallowed kind |
| `VEHICLE_GTA_CLASS_REQUIRED` | Addon vehicle class unknown or doesn't match garage category |
| `NOT_HYDRATED` | Client attempted to inspect/repair signed car before damage state loaded |
| `RESOURCE_NOT_ALLOWED` | Mechanic server resource absent from `RepairTrustedResources` |
| `NOT_SIGNED` | Wrong physical vehicle/network ID, owner access or distance in repair permit |
| `PLAYER_NOT_LOADED` | Trusted identity mapping request before framework character ready |
| `NOT_IN_WORLD` | `GetVehicleEntity` requested stored/unspawned car |
| `NO_ACCESS` | No Garage-owned vehicle/garage access, even if client UI renders an option |
| `STALE_REVISION` | Admin saved against an old Garage Creator revision |

## Safe evidence to collect in a support ticket

Send **resource versions**, selected framework and adapter IDs, which feature fails, the relevant F8/FXServer errors, an image of the current Garage Creator tab and steps to reproduce on a test car. **Do not send DB passwords, license tokens, OAuth credentials or private player identifiers.**

**Related:** [Installation](installation.md) · [Configuration](customization-reference.md) · [Five Frameworks](framework-installation.md) · [Verification](verification.md) · [Known Limitations](../../shared/fivem-install-known-limitations.md).