# Server Exports — M4I Garage


> **New optional SQL deletion mirror is a CONFIG setting, not a Server Export:** `DeleteOnNativeRowMissing=true` opt-in checks previously linked QB/Qbox/ESX records and removes only safe normally stored cars after an archive and a 3-minute grace. There is still **no** arbitrary public `DeleteOwnedVehicle` export. [Read the feature's contract](sql-ownership-and-deletion.md).


> **No public vehicle deletion export:** See [SQL Ownership, Native Sync and Admin Deletion](sql-ownership-and-deletion.md). `RegisterOwnedVehicle` cannot be used to remove a registered car.

**Documented source:** `m4i_garage 0.1.140-alpha`, `server/exports.lua`, `server/registry.lua`, `server/keys.lua`, `server/repair.lua` (7 November 2026).

These functions must be called from the **SERVER Lua of another genuine FiveM resource**. Most validate `GetInvokingResource()`; vehicle mutations use additional **strict allowlists**. Do not invoke them from browser JavaScript or an untrusted client event.

For functions running **on the player's client**, go to the separate [Client Exports](client-exports.md).

## API at a glance

| Server export | Parameters | Returns | Typical use |
| --- | --- | --- | --- |
| `GetGarage` | `garageId: string` | `garage? , reason?` | Read public metadata for a garage |
| `CanPlayerAccessGarage` | `playerSource, garageId` | `boolean, reason?` | Verify job/group/access to location |
| `HasVehicleAccess` | `playerSource, vehicleId, includeTemporary?` | `boolean, kindOrReason` | Owner/shared/temporary authorization |
| `GetVehicleByPlate` | `plate: string` | `vehicle? , reason?` | Lookup Garage-owned car (sanitized) |
| `GetVehicleCondition` | `vehicleId: number` | `condition? , reason?` | Persisted fuel, engine, body |
| `IsVehicleStored` | `vehicleId: number` | `boolean, reason?` | Check `physical_status='stored'` |
| `GetVehicleEntity` | `vehicleId: number` | `serverEntityHandle? , netIdOrReason` | Locate signed car in live world |
| `GetGarageCharacterId` | `playerSource: number` | `numericId? , reason?` | Map QBCore/Qbox/ESX/Ox player to Garage ID |
| `RegisterOwnedVehicle` | `characterId, plate, model, category, properties, garageId, spawnType, vehicleClass` | `boolean, insertedIdOrReason` | Register paid owned vehicle from a trusted dealership |
| `GetVehicleStatus` | `vehicleId` | Selected DB status row or `nil` | Legacy server information |
| `GetGarages` | None | Snapshot array | Legacy server catalogue |
| `PlayerHasVehicleKey` | `playerSource, vehicleId` | `boolean` | Check owner/shared/temporary Garage key |
| `AuthorizeFullRepair` | `playerSource, networkId` | `boolean, reason?` | Server-signed full repair permit |
| `BeginFullRepair` | `playerSource, networkId` | `boolean, reason?` | Alias to AuthorizeFullRepair |

**No public export allows bypassing Garage custody to create/delete arbitrary cars, release a legal hold, or debit money without checks.** A successful read-only check does not grant permission to perform an unrelated action.

## 1. Read one Garage — GetGarage(garageId)

```lua
-- trusted server script
local garage, reason = exports['m4i_garage']:GetGarage('public_legion')
if garage then
    print(garage.id, garage.label, garage.kind, garage.category)
else
    print('Garage not available', reason)
end
```

Returns a **detached public snapshot**; modifying it does not edit saved Garage locations. Unknown or malformed ID may return `nil`.

## 2. Check permissions — CanPlayerAccessGarage / HasVehicleAccess

```lua
local src = source -- source from your own verified server event / command
local canEnter, reason = exports['m4i_garage']:CanPlayerAccessGarage(src, 'job_police')
if not canEnter then return print('No garage access', reason) end

local vehicleId = 42 -- example: obtain from trusted server lookup
local allowed, kind = exports['m4i_garage']:HasVehicleAccess(src, vehicleId, true)
if allowed then
    print('Access kind:', kind) -- owner | shared | temporary
end
```

`CanPlayerAccessGarage` checks whether the player is entitled to **access a particular Garage**. It does **not** verify that the player stands inside its polygon, has a parking bay, owns a vehicle, is allowed to retrieve a seized vehicle, or has sufficient money.

`HasVehicleAccess` checks vehicle-specific owner/shared access; `includeTemporary=true` also admits a temporary key holder. Reasons may include `RESOURCE_ONLY`, `INVALID_INPUT`, `VEHICLE_NOT_FOUND`, `NO_ACCESS`.

## 3. Vehicle lookup — GetVehicleByPlate / GetVehicleCondition

```lua
local vehicle, err = exports['m4i_garage']:GetVehicleByPlate('ABC123')
if not vehicle then return print(err) end

print('Vehicle ID:', vehicle.id)
print('Status:', vehicle.physicalStatus, 'Garage:', vehicle.garageId)
print('Legal hold?', vehicle.legalHold)

local saved, why = exports['m4i_garage']:GetVehicleCondition(vehicle.id)
if saved then
    print('Saved fuel:', saved.fuel, 'engine:', saved.engine, 'body:', saved.body)
end
```

`GetVehicleByPlate` accepts a 1–8 character string using letters/digits/spaces/hyphens and normalizes to uppercase. Returns only:

```lua
{id=42, plate='ABC123', model='sultan', category='land',
 physicalStatus='stored', garageId='public_legion', legalHold=false}
```

No owner identifiers or internal serialized vehicle properties are exposed by this API. `GetVehicleCondition(vehicleId)` returns `{vehicleId, physicalStatus, garageId, fuel, engine, body}` from **stored SQL**; it can lag native physics until observation/Store. For locally hydrated live condition, use the client export.

## 4. Status and entity — IsVehicleStored / GetVehicleEntity

```lua
local vehicleId = 42
local isStored, reason = exports['m4i_garage']:IsVehicleStored(vehicleId)
if isStored then
    print('Vehicle is in Garage storage')
end

local entity, netId = exports['m4i_garage']:GetVehicleEntity(vehicleId)
if entity and DoesEntityExist(entity) then
    print('Server entity handle:', entity, 'Network ID:', netId)
end
```

An `'impound'`/seized/out car is **not** `'stored'`. `GetVehicleEntity` only returns an actively tracked signed **world entity** (and its Network ID), or an error such as `NOT_IN_WORLD`. Server entity handles are not client vehicle handles; use Network IDs and always revalidate after state changes.

## 5. The critical external-framework mapping — GetGarageCharacterId

**Do not pass the framework's raw string ID or the FiveM `source` to `RegisterOwnedVehicle`.** M4I uses numeric native character IDs; QBCore, ESX, Qbox and Ox Core use a **stable provider-qualified numeric Garage surrogate**, mapped in `m4ig_identity_map`.

```lua
-- Example inside your OWN dealership SERVER, after a real character loaded.
local src = 23 -- illustrative connected player source, not an owner ID
local characterId, reason =
    exports['m4i_garage']:GetGarageCharacterId(src)

if not characterId then
    print('Character not ready:', reason)
    return
end
print('Garage numeric character ID:', characterId)
```

Typical errors: `INVALID_PLAYER_SOURCE`, `NOT_READY`, `PLAYER_NOT_LOADED`. This export works only for **a connected, authenticated player**. Persist the Garage-owned vehicle against the returned **numeric ID**. Never infer that number from the public citizen ID displayed in UI.

## 6. Trusted dealership registration — RegisterOwnedVehicle

The server-side signature is:

```lua
exports['m4i_garage']:RegisterOwnedVehicle(
    characterId,           -- stable numeric Garage ID
    plate,                 -- valid unique plate, MAX 8 chars
    model,                 -- trusted GTA spawn model
    category,              -- 'land' | 'water' | 'air'
    properties,            -- validated vehicle properties table
    garageId,              -- existing compatible normal Garage
    spawnType,             -- e.g. 'automobile', 'bike', 'boat', 'heli', 'plane'
    verifiedVehicleClass   -- verified GTA class 0..22, needed if no known registry
)
```

**Security gate:** `server/registry.lua` checks `GetInvokingResource()` against `Config.TrustedVehicleRegistrars`. That setting is in `m4i_garage/config.lua`:

```lua
-- Add ONLY an audited actual dealership server-resource NAME.
Config.TrustedVehicleRegistrars = {
    ['my_dealership'] = true
}
```

**Example from `my_dealership/server.lua`:**

```lua
-- Call only AFTER your real server has:
-- authenticated the player, completed payment, validated model, plate,
-- ownership and permissions, chosen a valid target Garage and vehicle class.
local sourceId = buyerSource
local characterId, idError =
    exports['m4i_garage']:GetGarageCharacterId(sourceId)
if not characterId then
    print('Garage ID unavailable:', idError)
    return
end

-- Fictional example car Sultan, GTA vehicle class 6 (Sports).
local success, vehicleIdOrReason =
    exports['m4i_garage']:RegisterOwnedVehicle(
        characterId, 'ABC123', 'sultan', 'land',
        {}, 'public_legion', 'automobile', 6
    )

if not success then
    print('Garage registration failed:', vehicleIdOrReason)
    -- Your dealership must implement its own payment reversal / retry
    -- policy. Never tell the customer the sale fully succeeded here.
    return
end

print('Registered Garage vehicle ID:', vehicleIdOrReason)
```

**The above is a call example, not a ready-made purchase flow.** Do not paste it into `qb-core`, `ox_inventory`, `m4i_garage` or a new client event. Place it inside your actual **trusted dealership server transaction**. Validate the model's GTA class against Garage category and allowed groups. Duplicate plate, invalid garage, mismatched `spawnType`/`category`, invalid payload, or untrusted calling resource are rejected.

**Important:** `GetGarageCharacterId` is the correct mapping for all external-framework dealers, not a string `citizenid`.

## 7. Native/legacy read methods — GetGarages / GetVehicleStatus / PlayerHasVehicleKey

```lua
local locations = exports['m4i_garage']:GetGarages()
local row = exports['m4i_garage']:GetVehicleStatus(42)
local canUseKey = exports['m4i_garage']:PlayerHasVehicleKey(src, 42)
```

`GetGarages` returns the native Garage snapshot for a **server resource**; treat it as metadata, not a permission grant. `GetVehicleStatus` returns a limited DB row with the vehicle/character IDs, plate, legal/physical hold and location fields; do not expose it directly to public NUI without authorization. `PlayerHasVehicleKey` covers Garage owner/shared/temporary permissions and returns a boolean-compatible result. It does not grant the external vehicle-keys vendor keys automatically.

## 8. Repair integration — AuthorizeFullRepair / BeginFullRepair

These are **SERVER-only** and use the same trusted permit logic. The caller's resource name must exist in **`Config.RepairTrustedResources`**, and the car must be a signed, already hydrated, owned/access-allowed, nearby Garage vehicle. The permit expires in approximately **30 seconds**.

In `m4i_garage/config.lua`:

```lua
Config.RepairTrustedResources = {
    m4i_mechanic = true,
    ['my_mechanic'] = true
}
```

In `my_mechanic/server.lua` **after your own server has validated the actual service/payment/admin authorization**:

```lua
local ok, reason = exports['m4i_garage']:BeginFullRepair(
    customerSource, vehicleNetworkId
)
if not ok then
    print('Garage repair permit denied:', reason)
    return
end

-- Your mechanic must then cause the TRUE GTA full repair to complete
-- on the correct network entity's controlling client.
-- After actual success, that client signals the proper Garage repair
-- observation event/export; the Garage server still verifies/saves the
-- signed vehicle's repair state.
```

The client may use `exports['m4i_garage']:NotifyVehicleRepaired(veh, 'full')` or the documented Garage local fully-repaired event **after** real physical repair. A bare event without this prior server permit (or independently verified two-observation physical recovery) **cannot erase SQL damage**.

**Don't confuse partial with full repair**: changing a tyre should not erase pre-existing broken windows, doors and deformation. Full-repair authority is never granted from a user-controlled source name. [Full repair guide](damage-persistence.md).

## 9. Internal events are not public exports

Do not directly trigger `m4i_garage:server:trustedRepairApplied`, `m4i_garage:server:physicalFullRepairObserved` or internal NUI callbacks as an easy shortcut. Those events have server signature/permission and observation contracts. Use the stable exposed exports above, and integrate paid services through your own trusted backend.

The resource version / payment adapter / license and external scripts may evolve. Verify each invocation on the installed current version. **A source-verified API is not a guarantee that the customer's external vendor is compatible without integration testing.**

**Related:** [Client Exports](client-exports.md) · [Installation](installation.md) · [Garage Integrations](integrations.md) · [Vehicle Persistence](damage-persistence.md) · [Troubleshooting](troubleshooting.md).