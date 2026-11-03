# m4i_garage — Client and Server Exports

**Source:** TEST VPS `m4i_garage v0.1.121-alpha` (3 November 2026). The public API below is implemented and validated with automated Lua tests. A real in-game integration acceptance test is still required. This page is not a claim that the older public GitHub source repository contains this code.

`m4i_garage` owns vehicle storage, damage snapshots, keys, cover, seizure and garage records. Use `m4i_bridge` for framework identity, jobs, groups, player/financial operations. Use the Garage exports below for **Garage-specific** operations only; never write directly to Garage's SQL tables from other scripts.

## Client exports

Client exports work on the **local player's FiveM client**. They do not grant storage, ownership, keys or police permissions.

| Export | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `GetGarages` | `GetGarages()` | `garage[]` | Copy of client-synced visible catalogue; may be empty before sync |
| `GetGarage` | `GetGarage(garageId: string)` | `garage?` | No mutable reference to internal state |
| `GetCurrentGarage` | `GetCurrentGarage()` | `garage?` | Highest-priority normal Garage zone containing the player; excludes Impound/Seized/Cover-only zones |
| `IsPlayerInGarage` | `IsPlayerInGarage(garageId?: string)` | `boolean` | With ID: polygon membership; without ID: normal Garage zone |
| `IsGarageUIOpen` | `IsGarageUIOpen()` | `boolean` | Current M4I Garage NUI state |
| `OpenGarage` | `OpenGarage(garageId?: string)` | `boolean, reason` | Requires player inside a normal Garage polygon. Success `true, "REQUESTED"` means the request was sent, **not** server approval |
| `GetVehicleCondition` | `GetVehicleCondition(vehicleHandle: number)` | `condition?, reason?` | Signed, already hydrated Garage vehicle only; local live fuel/engine/body |
| `NotifyVehicleRepaired` | `NotifyVehicleRepaired(vehicleHandle, scope)` | Existing repair API | Legacy client export. Use `"partial"` or `"full"` only after the actual corresponding repair; see repair contract below |

Public Garage fields: `id`, `label`, `kind`, `category`, `storageMode`, `networkId`, `priority`, `zone`, `spawns`. This is a detached table; changing it does not edit Garage Creator or persist anything. `GetVehicleCondition` returns `{ vehicleId, fuel, engine, body, hydrated }`.

### Client example: open at the current zone

```lua
local here = exports['m4i_garage']:GetCurrentGarage()

if here and exports['m4i_garage']:IsPlayerInGarage(here.id) then
    local requested, reason = exports['m4i_garage']:OpenGarage(here.id)

    if not requested then
        print(('Garage rejected UI request: %s'):format(reason))
    end
end
```
Final access and proximity checks remain on the server. `OpenGarage` does not bypass police NPC interaction, garage job requirements, vehicle keys, or the asynchronous `vehicles` callback. It returns `false` with a reason such as `UNKNOWN_GARAGE`, `UI_ALREADY_OPEN`, `NOT_AT_GARAGE`, `USE_GARAGE_SERVICE` or `INVALID_GARAGE_ID` for client-side validation errors.

### Client example: local, hydrated condition

```lua
local veh = GetVehiclePedIsIn(PlayerPedId(), false)
local condition, err = exports['m4i_garage']:GetVehicleCondition(veh)

if condition then
    print('Garage ID', condition.vehicleId)
    print('Fuel', condition.fuel, 'Engine', condition.engine, 'Body', condition.body)
else
    print('No signed, ready Garage vehicle:', err)
end
```
Possible failures: `INVALID_VEHICLE`, `NOT_REGISTERED`, `NOT_HYDRATED` or `CONDITION_UNAVAILABLE`. Local health is a *live native reading*, not a confirmed database write.

## Server exports

All new server exports require a real **invoking server resource**; invalid calls are rejected before database access.

| Export | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `GetGarage` | `GetGarage(garageId: string)` | `garage?, reason?` | Detached public catalogue snapshot |
| `CanPlayerAccessGarage` | `CanPlayerAccessGarage(playerSource: number, garageId: string)` | `boolean, reason?` | Bridge-backed access check only; **not** location/keys/storage authorization |
| `HasVehicleAccess` | `HasVehicleAccess(playerSource: number, vehicleId: number, includeTemporary?: boolean)` | `boolean, accessTypeOrReason` | Values when allowed: `owner`, `shared`, `temporary` |
| `GetVehicleByPlate` | `GetVehicleByPlate(plate: string)` | `vehicle?, reason?` | Normalizes uppercase, supports 1–8 alphanumeric/space/hyphen characters; parameterized SQL; no owner/props |
| `GetVehicleCondition` | `GetVehicleCondition(vehicleId: number)` | `condition?, reason?` | **Persisted** snapshot; may lag live physics until autosave/Store |
| `IsVehicleStored` | `IsVehicleStored(vehicleId: number)` | `boolean, reason?` | Only true for exact `physical_status == "stored"` |
| `GetVehicleEntity` | `GetVehicleEntity(vehicleId: number)` | `entity?, netIdOrReason?` | Currently live signed network entity only |

`GetVehicleByPlate` returns `{ id, plate, model, category, physicalStatus, garageId, legalHold }`. `GetVehicleCondition` returns `{ vehicleId, physicalStatus, garageId, fuel, engine, body }`. Both omit owner identity and raw properties. The entity returned by `GetVehicleEntity` is a **server-side entity handle**; use its Network ID to communicate with clients and revalidate state before performing mutations.

### Existing server exports (backward compatible)

| Export | Signature | Behavior |
| --- | --- | --- |
| `GetGarages` | `GetGarages()` | Existing catalogue snapshot; treat returned nested values as read-only |
| `GetVehicleStatus` | `GetVehicleStatus(vehicleId)` | Existing SQL status row. May include `character_id`; **never forward its raw result to untrusted clients** |
| `PlayerHasVehicleKey` | `PlayerHasVehicleKey(playerSource, vehicleId)` | Existing read-only key/access check |
| `RegisterOwnedVehicle` | `RegisterOwnedVehicle(characterId, plate, model, category, properties, garageId, spawnType, verifiedVehicleClass)` | Returns `true, vehicleId` or `false, reason`. Requires `Config.TrustedVehicleRegistrars[GetInvokingResource()] == true` and validated model/category/class/garage |
| `AuthorizeFullRepair` | `AuthorizeFullRepair(playerSource, netId)` | Trusted server resource only; returns authorization outcome |
| `BeginFullRepair` | `BeginFullRepair(playerSource, netId)` | Alias of `AuthorizeFullRepair` |

`RegisterOwnedVehicle` is intentionally **not** a general-purpose player-triggered export. Default registrar allowlist is empty. Do not expose it through client events or unsecured server callbacks.

### Server example: inspect a stored vehicle

```lua
local record, err = exports['m4i_garage']:GetVehicleByPlate('M4I 88')

if record then
    local persisted = exports['m4i_garage']:GetVehicleCondition(record.id)
    local stored = exports['m4i_garage']:IsVehicleStored(record.id)

    print(record.id, record.physicalStatus, stored, persisted and persisted.fuel)
else
    print('Garage lookup failed:', err)
end
```
### Server example: check access before integration

```lua
local canAccess, kind = exports['m4i_garage']:HasVehicleAccess(source, 88, true)

if canAccess then
    print('Access type:', kind) -- owner / shared / temporary
end

local canUseGarage = exports['m4i_garage']:CanPlayerAccessGarage(source, 'public_1')
```
Access results are advisory for third-party UI; **Garage itself always revalidates** signed entity, plate/model, real physical zone, player identity, SQL custody, legal hold and money before any Store/Spawn/Seize action.

## Repair integration (security boundary)

A trusted mechanic/server script should first request a permit **on the server**, perform its actual repair on the client, then report success via the existing verified repair flow; do not send `vehicleFullyRepaired` or `trustedRepairApplied` from unrelated client scripts just to erase old dents.

```lua
-- server.lua, in a resource explicitly allowed by Config.RepairTrustedResources
local permitted, reason = exports['m4i_garage']:BeginFullRepair(playerSource, vehicleNetId)

if not permitted then
    return print('Repair not authorized:', reason)
end

-- Your own verified mechanic flow now performs the physical repair.
-- After success use m4i_garage's documented trusted-repair notification.
```
Client `NotifyVehicleRepaired(vehicle, 'partial')` must not be used to claim a full repair. Damage resurrection prevention relies on signed repair evidence.

## Errors and operational notes

- `nil, "RESOURCE_ONLY"` (or `false`) means a new server export was called without an invoking resource.
- `nil, "INVALID_VEHICLE_ID"`, `nil, "INVALID_PLATE"`, `nil, "VEHICLE_NOT_FOUND"` or `nil, "NOT_IN_WORLD"` are normal lookup failures.
- `false, "NO_ACCESS"` is expected for unauthorized players. Do not treat false as a database error.
- Any export backed by oxmysql may yield. Keep it outside per-frame client/server loops, and cache or subscribe when appropriate.
- These exports do **not** offer unchecked direct SQL writes, forced Spawn/Store, money transfers, police Seize, damage resetting or forced vehicle deletion.
- The interface is covered by `tests/public_exports_contract_v0221.lua` and `tests/manifest_exports_escrow_v0221.lua` on the TEST VPS.

See [Integration](integration.md), [Installation](installation.md), and [Configuration](configuration.md).
