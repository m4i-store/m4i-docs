# Install M4I Garage on Qbox / QBX

**Framework ID in Bridge:** **`qbox`** (not `qbx`) · **Core resource:** `qbx_core` · **Common addons:** `ox_lib`, `ox_inventory`, `ox_target`, `qbx_radialmenu`.

## 1. Dependencies and server.cfg

Retain your current Qbox/Overextended base; do not install `qb-core` as a second core. Its optional QB compatibility bridge is not the same as the Garage Bridge's actual framework provider.

```cfg
# In your existing Qbox server.cfg. Do not duplicate [ox]/[qbx] resources.
ensure oxmysql
ensure ox_lib
ensure qbx_core
# Already loaded by your existing groups or add as actual resources:
# ensure ox_inventory
# ensure ox_target
# ensure qbx_radialmenu

ensure m4i_bridge
ensure m4i_garage
add_ace group.admin m4i.garage.admin allow
```

Make sure Ox Inventory is configured to the correct Qbox framework and started. If the Qbox resource bundle already ensures these scripts with `ensure [ox]` / `ensure [qbx]`, **do not ensure them twice**.

## 2. Exact selection and required changes

In the existing `m4i_bridge/config.lua` table:

```lua
Framework = 'qbox',
Inventory = 'ox_inventory',   -- if installed
UI = 'ox_lib',
Target = 'ox_target',
Radial = 'qbx_radialmenu',    -- only if the exact adapter is installed
Keys = 'qbx_vehiclekeys',    -- only if the exact keys resource is installed
Banking = 'framework'
```

These are **individual values** to edit inside the already existing table; do not paste this partial fragment outside `M4IBridgeConfig`. The actual Qbox resources sometimes use different forked radial/keys APIs. Confirm exports and signatures with the installed vendor; if unmatched, implement a Bridge adapter instead of modifying Garage security modules.

**Most robust initial workaround for incompatible Qbox radial:** set **`Config.InteractionMode='keys'`** in `m4i_garage/config.lua`, then use E/H near an authorized Garage spawn bay. This avoids radial while NPC functions may still use Ox Target.

## 3. Database ownership and compatibility

After a backup, import `m4i_garage/sql/install.sql` into the same Qbox database configured for `oxmysql`. This creates `m4ig_*` Garage tables and a numeric framework-qualified `m4ig_identity_map` surrogate.

**Never give `RegisterOwnedVehicle` the raw `citizenid`/Ox identifier**. Use `exports['m4i_garage']:GetGarageCharacterId(playerSource)` on the trusted server after Qbox character load.

Optional `NativeVehicleCompatibility.Enabled=true` projects **already Garage-owned** cars into framework-readable vehicle rows. It does **not** implement the complete **`qbx_garages` server exports** or automatically migrate pre-existing Qbox garage ownership. NPWD apps and external houses may call those missing exports. Inventory which ones are needed and write a verified companion adapter before disabling their original garage resource.

## 4. Cover, keys, phone and payment

- **Cover with Ox Inventory:** define item `vehicle_cover` with `consume=0` and configure a **client Use adapter** that calls Garage's validated use action. Ox Inventory's server-only Bridge item adapter does not magically register this client Use behavior. [Cover item guide](../vehicle-cover-item.md).
- **Qbox keys:** use `qbx_vehiclekeys` only if installed, and test its entity-based grant/HasKeys behavior. It's different from QB's plate-based keys.
- **TextUI:** `ox_lib` must actually be running for the Garage prompt. A broken UI provider can make E/H actions appear absent even if the zone is present.
- **Phone:** NPWD is **not** automatically an LB/QS `AddCustomApp` provider. A companion app/API may be needed; a real `phone` inventory item is also required for Garage phone/valet actions.
- **Payments:** Impound/GPS/transfer fees must debit **the player's personal bank account** via a working framework adapter, not a society/job account.

## 5. Verification

1. Run `m4ig_doctor` from **server console**; confirm `qbox`, Ox Inventory/Target and keys-mode or radial readiness.
2. Create a Garage with `/garagecreator`, add clear spawn bays and save.
3. Verify a newly registered Garage vehicle appears and can Store/Retrieve.
4. Test Cover, keys, Impound bank charges and Qbox phone **individually**. Don't assume passing one flow proves all addon forks compatible.

**Related:** [Complete install](../installation.md) · [Integrations](../integrations.md) · [Known limitations](../../../shared/fivem-install-known-limitations.md) · [Developer Server Exports](../server-exports.md).