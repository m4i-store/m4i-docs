# FiveM Installation Audit — Actual Limitations and Required Integration Work

**Revalidated from shipped M4I Bridge 1.5.19-rc.1 / M4I Garage 0.1.139-alpha / M4I Upload 0.2.1-alpha (7 November 2026).** This is a **customer-facing release risk checklist**, not a claim that every third-party script is compatible.

## Critical: do not advertise these as automatic

| Scope | Source finding | Required next action before claiming the feature works |
| --- | --- | --- |
| Existing QB/Qbox/ESX owned vehicles | Garage creates its own `m4ig_vehicles`. Opt-in `NativeVehicleCompatibility` projects **Garage-owned** vehicles to framework-readable tables; it is not the reverse migration | Back up/compare native vehicle rows, explicitly plan ownership/plate migration, keep proper Garage controller exclusivity and verify all legacy APIs |
| Qbox `qbx_garages` and NPWD app | Native SQL alone does not reproduce missing `qbx_garages` exports/events or embed a Garage app | Ship/test a companion API adapter before stopping hard-dependent scripts |
| QB Phone | Garage has a narrow `qb-garages:server:GetPlayerVehicles` compatibility callback when configured, not a universal replacement for all QB Phone garage APIs | Inventory which QB Phone callbacks/events are actually used and test in the player's phone |
| Ox Inventory cover Use | Bridge's `ox_inventory` server adapter handles items/slots but doesn't register an automatic client Use event | Define `vehicle_cover` with `consume=0`, implement the client event adapter in [Item Guide](../scripts/m4i_garage/vehicle-cover-item.md); do not ship test-only `m4i_test_compat` |
| Optional Garage Phone/Valet UI | `server/phone.lua` and `server/delivery.lua` check `HasItem(source,'phone',1)` regardless of the phone provider | Ensure a real inventory item literally named `phone`; other names require a tested Garage code/adapter change |
| **AI Valet / Delivery money** | `m4i_garage/server/valet_payment.lua` queries `m4ig_valet_payments`, but its CREATE TABLE statement is **absent** from `m4i_garage/sql/install.sql` and the code reviewed. It also queries `m4i_account_ledger` directly on its recovery/refund path (an M4I-native ledger) | **Do not enable/advertise paid Valet/Delivery on external frameworks until a correct schema, framework-neutral audited payment reference/ledger adapter and crash/restart/refund tests exist.** On a fresh native install confirm the `m4ig_valet_payments` schema exists before testing; do not assume `install.sql` creates it |
| Native Garage/Bridge SQL schemas beyond installer | Garage runtime creates some additional `m4ig_*` support tables; ESX Cover uses `m4i_bridge_esx_cover_uses` per-owner ledger | Apply exact compatible schemas with a migration account, or grant controlled DDL only for the initialization window; keep production runtime privileges least-privilege afterward |
| Unknown commercial Inventory/Keys/Radial/Target/Phone forks | Adapter IDs reference **exact vendor APIs**, not similar names | Implement and test matching adapter, including add/remove and error/permission handling. Some forks may not support the required contract |
| Ox Core framework | Shipped adapter exists but four running test bases were M4I/QBCore/ESX/QBX | Perform real Ox Core runtime/DB/identity/payment/keys test before claiming certified support |
| Asset Escrow | Files called `[escrow]` are ZIP packages; `escrow_ignore` in manifest is not encryption | Publish and verify genuine Cfx Asset Escrow artifact separately |
| Streamed custom vehicle covers | YTYP references may exist while vendor YDR/YTD models are missing | Include permitted model assets or rely on documented safe GTA native fallback; verify F8 and model in live session |

## Feature flags and safe installation defaults

Garage base Open/Store can be configured with a correct framework + Bridge + `oxmysql` + Garage SQL + actual zones. A radial is **optional** if `Config.InteractionMode='keys'`; a Target is still needed for NPC Police/Impound features. `vehicle_cover` is optional unless enabling Cover. `m4i_upload` is optional unless using global images. Phone/AI Valet is optional.

When the money/ledger/schema compatibility for **Delivery** has not been implemented and tested, configure:

```lua
-- m4i_garage/config.lua
Config.DeliveryEnabled = false
```

This avoids advertising a known incomplete optional payment workflow. A 0-fee setting is **not** a substitute for verifying the SQL and recovery code, because some phone/recovery paths still query the payments table. If the customer requires paid Valet on QB/Qbox/ESX/Ox, it needs a proper code and database integration, not merely a `server.cfg` change.

## Schema inventory

`m4i_garage/sql/install.sql` directly creates:
`m4ig_garages`, `m4ig_vehicles`, `m4ig_cases`, `m4ig_audit`, `m4ig_temp_keys`, `m4ig_access`, `m4ig_identity_map`, `m4ig_native_vehicle_links`.

Some runtime modules use `CREATE TABLE IF NOT EXISTS` for:
`m4ig_vehicle_world_snapshots`, `m4ig_insurance_reminders`, `m4ig_seized_checkouts`, `m4ig_seizure_officer_snapshots`, `m4ig_global_settings`, `m4ig_cover_rules`, `m4ig_cover_rule_history`, and the identity/native link tables. ESX Cover module creates `m4i_bridge_esx_cover_uses` on demand. This list is not a replacement for current schema validation: confirm your delivered source and your database structure before go-live.

**If the database runtime user lacks CREATE privileges**, an admin may apply reviewed DDL using a migration account first; do not grant every player script SQL login unrestricted long-term migration rights.

## Sale/hand-off acceptance

- [ ] Required item definitions are in the customer's real inventory files/SQL, including Ox Use event where needed.
- [ ] The selected Framework, Inventory, Radial, Target, UI, Notify, Progress, Keys, Banking, Phone and vehicle classification providers are actual supported adapters; unavailable optional domains have alternatives.
- [ ] Core Garage open/store/take/repair/covers/impound work with **two clients**, reconnect and restart.
- [ ] The selected phone, native garage, police, dealership and mechanic plugins are verified with their exact current versions.
- [ ] No unpaid/charged/refunded Valet task relies on missing schema or the wrong framework account ledger.
- [ ] Package docs, configs, SQL and LICENSE-aware stream assets match deployed release; encrypted Asset Escrow is verified separately.
- [ ] Vendor-dependent features that do not pass are clearly flagged **not supported with this vendor/build**, rather than described as automatic.

**Full guides:** [Garage complete installation](../scripts/m4i_garage/complete-installation.md), [Bridge complete provider setup](../core/m4i_bridge/complete-provider-setup.md), [Upload complete integration](../scripts/m4i_upload/complete-installation.md), [Go-live QA](fivem-qa-checklist.md).