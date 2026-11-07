# Vehicle Cover Item — Add It to Your Existing Inventory

> **VISUAL LOCATION OF COVER CONFIG:** Open `/garagecreator` → **Vehicle Covers**. See the [actual Garage Creator screenshots and Cover explanation](visual-setup-guide.md), plus the [complete editable options reference](customization-reference.md). The Ox client Use adapter below remains required where the inventory does not register the item event itself.


**Applies to** M4I Garage 0.1.139-alpha + M4I Bridge 1.5.19-rc.1. These instructions apply to the optional **Vehicle Cover** feature. No vehicle-cover item is required merely to install and use the ordinary Open/Store Garage feature.

## Do customers need to create an item?

**Yes, when they want to use physical Vehicle Covers.** The item must exist in the actual inventory system configured in `m4i_bridge/config.lua`, with the exact **name `vehicle_cover`**. Bridge does not automatically inject item definitions into third-party inventory databases or item files. If the item is already defined, **do not define it a second time**.

**Do not automatically consume an item on initial Use.** M4I Garage checks vehicle ownership, proximity, safe zone, cooldown and item slot before charging a successful cover action. Each physical cover has **five successful uses**, then disappears. External Ox/QB inventories keep per-unit remaining uses in metadata; stacks with an exhausted unit need to be split into individual slots. Default ESX inventory cannot store slot metadata, so Bridge uses a separate per-character SQL ledger and should not allow transfer/drop of a partially used cover.

| Framework and inventory actually installed | Item definition location | Is a usable-item callback created automatically? |
| --- | --- | --- |
| M4I + `m4i_inventory` | `m4i_inventory/shared/items.lua` | Yes, native M4I Inventory Use event; current M4I test build already defines `vehicle_cover` |
| QBCore + `qb-inventory` | `qb-core/shared/items.lua` | Yes: M4I Garage requests Bridge registration via `QBCore.Functions.CreateUseableItem`, *after* you define the item |
| Qbox / ESX + `ox_inventory` | `ox_inventory/data/items.lua` | **No automatic Ox item-use event registration** in the current Bridge: define an Ox client event adapter described below |
| ESX + `esx_inventory` | ESX `items` SQL table and/or vendor item definition, per installed version | Yes: Garage/Bridge registers `ESX.RegisterUsableItem` for its shipped `esx_inventory` provider, *after* the item exists |

**Important:** choose the *inventory*, not just the framework. For example, ESX with `ox_inventory` follows the Ox recipe, not the ESX default recipe.

## M4I Inventory — already included in current M4I source

Check `m4i_inventory/shared/items.lua` for:

```lua
M4IItems.vehicle_cover = {
    label = 'Vehicle Cover',
    description = 'Five successful cover actions per physical item.',
    image = 'vehicle_cover',
    weight = 1000,
    stack = true, maxStack = 5,
    category = 'equipment',
    usable = true,
    use = { consume = 0, cooldownMs = 1000 }
}
```

If it is already present, **do not add it again**. The referenced image is a global M4I image ID, not necessarily a local file. Use the existing Inventory item-use event—do not add a duplicate callback.

## QBCore / qb-inventory

Open `resources/[qb]/qb-core/shared/items.lua` and place the entry **inside** `QBCore.Shared.Items = { ... }`, if it does not already exist:

```lua
['vehicle_cover'] = {
    name = 'vehicle_cover',
    label = 'Vehicle Cover',
    weight = 1500,
    type = 'item',
    image = 'vehicle_cover.png',
    unique = true,
    useable = true,
    shouldClose = true,
    description = 'Reusable vehicle cover (5 successful uses)'
},
```

Keep **`unique=true`** so each item has its own slot/metadata. `vehicle_cover.png` must exist in this vendor inventory's image path if its UI requires local images; otherwise use a valid existing placeholder or integrate its UI with M4I Upload. The global Upload ID alone does **not** inject a PNG into every third-party inventory.

**Do not create a second `CreateUseableItem` registration.** Once `qb-core`, `qb-inventory`, Bridge and Garage start in order, Garage calls `RegisterGarageCoverUsable` and Bridge registers the real QBCore Use handler. A successful console message contains `usable item registered via Bridge provider=qb_inventory`.

## Qbox / QBX and other bases running ox_inventory

Open `ox_inventory/data/items.lua`, inside its `return { ... }` table, and add one definition:

```lua
['vehicle_cover'] = {
    label = 'Vehicle Cover',
    weight = 1500,
    stack = false, -- one physical cover per slot: metadata safety
    close = true,
    consume = 0, -- NEVER consume immediately; Garage handles 5-use charge
    client = {
        event = 'm4i_cover_ox_adapter:use'
    }
},
```

In this build the shipped Ox inventory provider handles item ownership, slot metadata and charging but **does not automatically register the Use UI callback**. Add a small independent client adapter resource (rather than editing protected Garage code or copying the TEST-ONLY `m4i_test_compat` event):

```text
resources/[m4i]/m4i_cover_ox_adapter/
  fxmanifest.lua
  client.lua
```

**fxmanifest.lua**

```lua
fx_version 'cerulean'
game 'gta5'
lua54 'yes'
dependencies { 'ox_inventory', 'm4i_garage' }
client_script 'client.lua'
```

**client.lua**

```lua
-- Ox inventory emits its chosen item and slot on client-side Use.
-- This is an entry point only; M4I Garage rechecks the actual item,
-- selected slot and vehicle authorization on the server.
AddEventHandler('m4i_cover_ox_adapter:use', function(item, slot)
    if type(item) ~= 'table' or item.name ~= 'vehicle_cover' then return end
    local slotId = type(slot) == 'table' and slot.slot or slot
    slotId = tonumber(slotId)
    if not slotId or slotId < 1 or slotId % 1 ~= 0 then return end
    TriggerEvent('m4i_garage:useCoverItem', slotId)
end)
```

**server.cfg** after Garage:

```cfg
ensure ox_inventory
# ensure your framework + m4i_bridge before m4i_garage
ensure m4i_garage
ensure m4i_cover_ox_adapter
```

Never use `m4i_test:oxCoverUsed` or `m4i_test_compat` in a customer's production item definition. Those names belong to an internal testing helper, not the delivery package. Test the selected Ox version's client-event argument shape and `consume=0` behaviour before releasing to players.

## ESX Legacy + ESX default inventory

ESX Legacy item schemas vary across versions and installed inventory resources. **First** inspect the `items` table's columns (with a database backup):

```sql
SHOW COLUMNS FROM items;
SELECT name, label FROM items WHERE name = 'vehicle_cover';
```

If the installation has `name`, `label` and `weight` and there is no existing row, an example for that schema is:

```sql
INSERT INTO items (name, label, weight)
VALUES ('vehicle_cover', 'Vehicle Cover', 1500);
```

Adapt the statement for any required vendor columns; **do not run the example blindly on a different schema**. If ESX is using a separate `esx_inventory` definition file, register the item there according to that installed version as well. The Bridge ESX usable-item adapter calls `ESX.RegisterUsableItem` during Garage startup, so do not register the same callback again. The server should log `usable item registered via Bridge provider=esx_inventory`.

**Special ESX constraint:** no per-slot item metadata in this shipped adapter; a separate Garage/Bridge ledger tracks five uses per owner. Restrict trades/drops of partially used covers unless your ESX inventory implementation provides a tested transfer-safe adapter.

## Restart and test

1. Back up the modified inventory item definition/SQL, then change only the selected inventory's item registry.
2. Restart the relevant framework/inventory as required by its docs, then `m4i_bridge` and `m4i_garage` in proper dependency order. Avoid hot-restarting another player's active vehicle during production.
3. For Ox, start/restart the companion `m4i_cover_ox_adapter` after Garage.
4. Grant one cover using your inventory/admin's **normal trusted item grant** mechanism. Never let a client directly request items.
5. Use next to your **own registered stationary car in an allowed Cover zone**. Verify no item disappears immediately on click. After a valid covering, remaining uses decrease by one; after the fifth successful covering the physical item disappears.
6. Test failed cover attempts (out of zone, wrong owner, moving car), cooldown, disconnect/reconnect, restart and final-use depletion.
7. Check both FXServer console and F8 on the client. For QB/ESX, check the `usable item registered via Bridge` log; for Ox, verify the companion event runs and the Garage still revalidates the slot server-side.

**If you do not want Vehicle Cover at all:** you do not need to add `vehicle_cover` to install and use ordinary Garage storage. Do not interpret absence of the optional item as a Garage installation failure.

See also [Five-Framework Installation](framework-installation.md), [Third-party Integration Recipes](integration-recipes.md), and [QA Checklist](../../shared/fivem-qa-checklist.md).