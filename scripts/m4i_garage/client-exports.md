# Client Exports — M4I Garage

**Current code:** `m4i_garage 0.1.140-alpha` · implementation files `client/exports.lua` and `client/vehicle_condition.lua` verified on 7 November 2026.

These functions are called from a **client Lua script running on the player's machine**. They are intended for read-only location/UI status and controlled Garage UI requests. **Client exports do not grant keys, ownership, money or permissions.**

## Quick reference

| Client export | Input | Return | Why use it |
| --- | --- | --- | --- |
| `GetGarages()` | None | Array of public Garage snapshots | Show the locally synchronized Garage catalogue |
| `GetGarage(garageId)` | String Garage ID | Garage snapshot or `nil` | Lookup one local garage |
| `GetCurrentGarage()` | None | Garage snapshot or `nil` | Which normal Garage the player is inside |
| `IsPlayerInGarage(garageId?)` | Optional string ID | Boolean | Check polygon membership |
| `IsGarageUIOpen()` | None | Boolean | Prevent your own UI from competing with Garage |
| `OpenGarage(garageId?)` | Optional string ID | `boolean, reason?` | Ask the real Garage UI to open near the player |
| `GetVehicleCondition(vehicle)` | Client vehicle **entity handle** | `condition, error?` | Read hydrated Garage car fuel/engine/body |
| `NotifyVehicleRepaired(vehicle, scope)` | Client vehicle handle and `'partial'`/`'full'` | `boolean, error?` | Notify Garage's repair observation about an external repair |

**Always** call these from client Lua:

```lua
-- my_resource/client.lua
local garage = exports['m4i_garage']:GetCurrentGarage()
if garage then
    print('Inside Garage',garage.id,garage.label)
end
```

Do **not** copy the call into your server script. For server usage read [Server Exports](server-exports.md).

## Garage snapshot schema

The public client snapshot contains:

```lua
{
    id = 'public_legion', -- example
    label = 'Legion Square Parking',
    kind = 'public',
    category = 'land',
    storageMode = 'locked',
    networkId = nil,
    priority = 0,
    zone = {...},
    spawns = {...}
}
```

The returned table is a **detached copy**. Editing its `label` or `spawns` does **not** edit Garage or persist changes. The client catalogue may be empty until synchronization completes. Don't assume the list includes a server-side permission to store vehicles.

## GetGarages()

```lua
local list = exports['m4i_garage']:GetGarages()
for _, garage in ipairs(list) do
    print(garage.id, garage.kind, garage.category)
end
```

Use it to display locations or build a local indicator, not to reimplement server custody/permissions. Vehicle details, balances and sensitive owner IDs are not returned.

## GetGarage(garageId)

```lua
local garage = exports['m4i_garage']:GetGarage('public_legion')
if garage then
    print(garage.label, #garage.spawns)
end
```

`garageId` must be a non-empty string up to 128 characters. Returns `nil` if invalid or not in the client's synced catalogue.

## GetCurrentGarage() / IsPlayerInGarage()

```lua
local here = exports['m4i_garage']:GetCurrentGarage()
if here and exports['m4i_garage']:IsPlayerInGarage(here.id) then
    print('Player is in a normal Garage polygon', here.id)
end
```

`GetCurrentGarage` selects the current normal garage zone using the client-side zone logic. Cover-only and special NPC/custody contexts are not general parking. `IsPlayerInGarage()` without an ID checks whether the player is in a compatible Garage polygon. These are **position checks**, not authority to spawn or seize a vehicle.

## IsGarageUIOpen()

```lua
if exports['m4i_garage']:IsGarageUIOpen() then
    print('Garage NUI is already active; avoid opening an overlapping menu')
end
```

Useful if your custom radial/quick menu wants to defer when Garage owns focus.

## OpenGarage(garageId?)

```lua
-- my_resource/client.lua
RegisterCommand('mygarage', function()
    local here = exports['m4i_garage']:GetCurrentGarage()
    if not here then return print('Stand at a Garage first') end

    local requested, reason = exports['m4i_garage']:OpenGarage(here.id)
    if not requested then
        print('Unable to request Garage UI:', reason)
        return
    end

    print('Garage UI request sent; wait for server authorization')
end, false)
```

A `true` return indicates **a request was sent**, **not** final approval. Garage still checks the true position, framework identity, access, enabled state and server-controlled vehicle catalogue. This export is not a remote “open any Garage from anywhere” bypass.

## GetVehicleCondition(vehicle)

```lua
local vehicle = GetVehiclePedIsIn(PlayerPedId(), false)
local state, reason = exports['m4i_garage']:GetVehicleCondition(vehicle)

if not state then
    print('Condition unavailable:', reason)
else
    print('Garage vehicle:', state.vehicleId)
    print('Fuel:', state.fuel, 'Engine:', state.engine, 'Body:', state.body)
end
```

Returns `{ vehicleId, fuel, engine, body, hydrated = true }` only when the local **network entity is a Garage-signed, hydrated car**. Errors may include `INVALID_VEHICLE`, `NOT_REGISTERED`, `NOT_HYDRATED`, `CONDITION_UNAVAILABLE`.

**Note:** the client's live readings can differ briefly from the persisted SQL value. For the authoritative stored snapshot, use the [server's `GetVehicleCondition(vehicleId)`](server-exports.md#getvehicleconditionvehicleid).

## NotifyVehicleRepaired(vehicle, scope)

This is a **client observation hint**, not a server-certified payment or full SQL reset.

```lua
-- In a real external mechanic CLIENT script, after the physical
-- repair native/actions have successfully completed:
local vehicle = GetVehiclePedIsIn(PlayerPedId(), false)
local ok, reason = exports['m4i_garage']:NotifyVehicleRepaired(vehicle, 'partial')

if not ok then
    print('Garage did not accept repair observation:', reason)
end
```

Supported scopes are `partial` and `full`. The vehicle must be a signed hydrated Garage car, and the local client must own its network control. Errors: `NOT_REGISTERED`, `NOT_HYDRATED`, `NOT_NETWORK_OWNER`, `INVALID_SCOPE`.

**Full repair requires trusted server authorization or independently verified physical evidence**; simply sending `'full'` from a client cannot erase old damage in SQL. See [Vehicle Damage & Repairs](damage-persistence.md) and [Server Permit API](server-exports.md#authorizefullrepair--beginfullrepair).

## Integrating in your own client resource

In the dependent resource's `fxmanifest.lua`, add this dependency when required:

```lua
dependency 'm4i_garage'
client_scripts { 'client.lua' }
```

Adjust to your existing manifest instead of replacing it. Wait until Garage is started and the local player/session has synchronized before interpreting a missing snapshot as a permanent missing garage. **Never edit `m4i_garage/client/exports.lua` to add a custom menu**; call the stable API from your own script.

**Next:** [Server Exports](server-exports.md) · [Garage Integrations](integrations.md) · [Commands](commands.md).