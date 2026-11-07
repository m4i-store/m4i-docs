# Install M4I Garage on QBCore

**Framework ID:** `qbcore` · **Framework resource:** `qb-core` · **Typical native table:** `player_vehicles`.

This is a **QBCore server**, not a replacement QBCore package. Keep your real framework, player login, inventory, fuel, keys, phone and banking resources, choosing only supported providers in Bridge.

## 1. Files and startup segment

After backing up your SQL and old Garage config, place the inner `m4i_bridge` and `m4i_garage` folders under `resources/[m4i]/`. Make sure the installed QBCore resources start before the Garage:

```cfg
# Add missing lines into your EXISTING server.cfg; don't duplicate ensure [qb].
ensure oxmysql
ensure qb-core
# If already started by ensure [qb], do not start them again:
# ensure qb-inventory
# ensure qb-target
# ensure qb-radialmenu

ensure m4i_bridge
ensure m4i_garage
add_ace group.admin m4i.garage.admin allow
```

If your server uses `ensure [qb]`, it may already start the actual inventory, radial, target and vehicle keys. **Verify their started state** instead of pasting `ensure` lines for resources you do not have. It is okay to use Garage `keys` mode without radial.

## 2. Exact configuration

In `m4i_bridge/config.lua` choose:

```lua
Framework = 'qbcore',
Inventory = 'framework',  -- qb_inventory, if qb-inventory is installed
UI = 'framework',         -- qb_textui if that API exists
Radial = 'framework',     -- qb_radialmenu when installed
Target = 'framework',     -- qb_target when installed
Keys = 'framework',       -- verify qb-vehiclekeys adapter
Banking = 'framework'     -- must charge actual PERSONAL player account
```

Edit **values inside `M4IBridgeConfig`**, not as independent global variables. The QBCore profile names an adapter ID; if you use Ox Inventory or Ox Target instead, choose the matching registered Bridge adapter explicitly and verify the real resource is started.

In `m4i_garage/config.lua` use `Config.InteractionMode='radial'` only if the QBCore radial actually registers its items; otherwise use `'keys'`. Select your own police jobs/grades. Set `Config.DeliveryEnabled=false` unless the paid-valet schema/recovery integration is fixed and tested.

## 3. SQL and existing player vehicles

Import **only `m4i_garage/sql/install.sql`** into the existing QBCore database, after a backup. It creates separate `m4ig_*` tables. **Do not drop, recreate, or overwrite `player_vehicles`.**

`Config.NativeVehicleCompatibility.Enabled` is **false** by default. Setting it true projects Garage-owned vehicles to compatible QBCore read tables and may enable a narrow QB Phone garage callback. **It does NOT import all rows from `player_vehicles` into Garage.** Do not run `qb-garages` and M4I Garage as simultaneous authorities for the same cars. Build/verify a safe ownership migration plan first: [Updating and Migration](../updating.md).

## 4. Inventory, keys, phone and other required edits

- **If using Cover:** define `vehicle_cover` inside your real `qb-core/shared/items.lua` or vendor item registry, with no automatic consumption and a trusted Use event. Match the installed Inventory's actual API. [Exact item recipe](../vehicle-cover-item.md).
- **If using QB keys:** `qb-vehiclekeys` keys are typically plate-based; Bridge's QB keys adapter must match your actual installed version. They are **not** interchangeable with Qbox's network-entity keys.
- **If using QB Phone:** the optional `qb-garages:server:GetPlayerVehicles` callback is a narrow compatibility path; it is not a complete replacement for every QB Phone/house garage call. Audit your version's actual callbacks and housing scripts before disabling the old Garage resource.
- **If using a dealership:** call Garage's trusted `RegisterOwnedVehicle` **from the dealership SERVER**, with `GetGarageCharacterId(source)` rather than passing raw QBCore `citizenid`.
- **If using ox_inventory / ox_target instead of QB variants:** select those adapters in Bridge and follow the Cover item use hook appropriate to Ox Inventory.

## 5. First launch test

Run `m4ig_doctor` **in server console**. Use `/garagecreator` as admin, create a public Land zone and safe spawn, and test one newly Garage-registered car: Store, Retrieve, payment, keys, restarts. Test with two users and an actual QB-native owned vehicle **separately** to avoid mistaking legacy ownership for imported Garage ownership.

**Related:** [Full install](../installation.md) · [QBCore external edits](../integrations.md) · [Troubleshooting](../troubleshooting.md) · [Server Exports](../server-exports.md).