# Vehicle Damage, Save/Restore and Repair Integration

M4I Garage is built around **server-owned, persistent vehicle custody**. When a signed vehicle is stored, retrieved or observed, its actual physical state matters. A client visually repairing the car does **not automatically clear all persisted damage**.

**Validated against:** `m4i_garage 0.1.140-alpha` including `client/vehicle_condition.lua`, `server/repair.lua`, `shared/damage_persistence.lua`, and the embedded vehicle deformation code.

## 1. What Garage preserves

| State | Persisted / observed behavior |
| --- | --- |
| **Fuel** | Remaining fuel value; a body repair does not grant free fuel |
| **Engine** | Health, damage changes, authorized full repair |
| **Body** | GTA body health; can differ from visible mesh dents |
| **Petrol tank** | Tank health and relevant leak/damage recovery handling |
| **Doors / hood / trunk** | Detached, damaged and open-state observations, when supported by GTA model |
| **Windows** | Broken/intact glass with per-model native support calibration |
| **Tyres / bumpers** | Burst/broken physical elements |
| **Deformation** | Native/embedded saved body-mesh deformation history and validated rehydration |
| **License plate, paint, mods** | Garage-owned vehicle properties where supported by snapshot/persistence |

The exact amount of mesh deformation a GTA model exposes can vary. Do not promise that every custom streamed car supports identical damage points or full native repair readback.

## 2. Normal vehicle lifecycle

```text
Signed registered car
  → Retrieve from permitted Garage
  → Server creates/tracks correct network entity
  → Client hydrates saved props and physical damage
  → Player drives / impacts / repairs vehicle
  → Garage observes eligible owned car with bounded polling
  → Safe Store transaction saves latest verified state
  → Next Retrieve restores saved condition (no phantom free repair)
```

The server is authoritative for `m4ig_vehicles`, physical status and assigned vehicle identity. **A car spawned by a random script without Garage registration does not become a Garage-owned car merely by having the same plate.**

## 3. Three repair types — behavior and expected persistence

| Case | What should be saved |
| --- | --- |
| **Still damaged** | Save current body/engine/tank, broken components and deformation; restore them after relog/retrieve |
| **Fully repaired** | Save a clean physical repair, clear old signed damage evidence **only after verified full repair**, preserve fuel and legitimate customization |
| **Partially repaired** | Save only components genuinely repaired, **keep the remaining unrepaired damage**; do not reset every window/door/dent |

A full repair that occurs only visually, without a trusted permit or physical proof, can leave old damage in Garage's SQL state. After the next Store/Retrieve, the visible dents or missing components may reappear; this is a **repair integration issue**, not proof Garage always ignores repairs.

## 4. Default persistence controls

In `m4i_garage/config.lua`:

```lua
Config.RepairObservationTickMs = 2000
Config.ConditionAutoSaveTickMs = 30000
Config.ConditionAutoSaveNearMeters = 12.0
Config.ConditionAutoSaveHeartbeatMs = 120000
Config.ConditionAutoSaveDbCooldownMs = 25000
Config.RepairVerificationMaxStoreWaitMs = 22000
Config.DebugVehicleDamagePersistence = false -- recommended after testing
```

These values coordinate the observation cadence, nearby checks, changed-only DB writes, and a bounded wait for a repair candidate when storing. The installed testing config may ship `DebugVehicleDamagePersistence=true` for diagnostics; disable excessive logging for live players after verification.

Too-aggressive polling reduces scalability, especially around crowded, 200-player Garage zones. Do not set every poll to 0 or run an external tight-loop damage sync.

## 5. Recommended external full repair integration (SERVER + CLIENT)

When a trusted mechanic resource performs a legitimate full paid/admin repair:

**Part A — trusted SERVER resource requests a permit**

In `m4i_garage/config.lua` list the exact trusted mechanic resource name:

```lua
Config.RepairTrustedResources = {
    ['my_mechanic'] = true,
    m4i_mechanic = true
}
```

Then in **`my_mechanic/server.lua`**, only **after the mechanic's own server confirms permission, payment and correct target**:

```lua
local allowed, reason = exports['m4i_garage']:BeginFullRepair(
    customerSource, vehicleNetworkId
)
if not allowed then
    print('[my_mechanic] Garage repair permit rejected:', reason)
    return
end

-- Send your verified repair request to the real controlling client,
-- preserving the network vehicle identity and your own paid service ID.
```

Garage checks the actual invoking resource, server-signed owned/accessible Garage car, hydrated live entity, nearby player and 30-second permit expiry.

**Part B — the actual CLIENT performs the GTA repair**, checks the same vehicle is the network entity expected by the server, and only then informs Garage's observation:

```lua
-- Example inside my_mechanic/client.lua after a real valid repair.
local ok, reason = exports['m4i_garage']:NotifyVehicleRepaired(
    actualVehicleHandle, 'full'
)
if not ok then
    print('[my_mechanic] Garage repair observation:', reason)
end
```

The client export is **not** the permission or SQL settlement; the server still validates the trusted signed permit and commits the appropriate Garage state. For safety never accept a user-supplied string `my_mechanic` as equivalent to `GetInvokingResource()`.

**Stock third-party mechanic scripts** that cannot create a trusted server permit may still be recognized conservatively by Garage's **genuine physical damaged → clean observation**. This requires independent evidence over time on the same hydrated car and must not be treated as guaranteed for every GTA model/vendor fork.

## 6. Partial repair integration

If the mechanic actually repairs only tyres, glass, oil or one body component:

```lua
-- client.lua, after real partial repair:
exports['m4i_garage']:NotifyVehicleRepaired(
    actualVehicleHandle, 'partial'
)
```

Do **not** use `scope='full'` to make a button or animation look successful. Partial operations must preserve remaining door, mesh, bumper and tank damage. Oil service is not a complete GTA body restoration; the inventory/catalog of services belongs to the actual mechanic resource.

## 7. Embedded deformation and outside scripts

Garage includes integrated deformation logic for signed vehicles. Avoid running a second uncontrolled deformation resource over the same Garage-owned car if it repeatedly overwrites `Entity(vehicle).state.deformation` or reapplies body repair at spawn.

Exceptions configured in `Config.VehicleDeformation` include excluded types such as bikes/boats/helis/planes and exact model/plate blacklists. Check real vehicle class, streaming and customization before adding broad exclusions.

The actual Gear/Engine/Tank/Body behavior must be tested on a car with **real visible dents**, detached parts, broken glass and a partially repaired state, not merely changing numeric `engine` to 1000 in SQL.

## 8. Acceptance steps to prove repair persistence

1. Register a signed, Garage-owned eligible car and retrieve it.
2. Inflict **real body mesh dents**, break a window, damage a door/tyre and verify body/engine/tank.
3. Store; retrieve; verify damage persists.
4. Execute **only a partial repair**. Store; retrieve; confirm unrepaired parts remain damaged.
5. Execute a genuine **full repair** through trusted server permit and actual physical repair.
6. Store again; retrieve; confirm detached components and dents **do not reappear**.
7. Check fuel wasn't magically filled by body repair; petrol tank health and leak state are clean.
8. Repeat with two connected players and after a controlled resource restart, to catch duplicated server-owned entities and observer ordering.

If the full repair fails to persist, inspect `[m4i_garage][repair]` console diagnostics and `repairCommitted` state/revision. Do not forcibly delete stored damage JSON to conceal failed permit logic.

## 9. Common errors

| Error/behavior | What to inspect |
| --- | --- |
| `RESOURCE_NOT_ALLOWED` | Exact server resource missing from `Config.RepairTrustedResources` |
| `NOT_SIGNED` | Not a Garage-owned, hydrated, nearby valid vehicle, or wrong network ID |
| `NOT_REGISTERED`, `NOT_HYDRATED` on client | Wrong local vehicle handle or state not yet loaded |
| `NOT_NETWORK_OWNER` | Calling client does not control the target vehicle |
| Old damage returns after /fix | No authorized full repair permit or insufficient physical full-repair proof |
| Full repair clears all fuel | External mechanic erroneously resets fuel; Garage full repair is not refueling |
| Tank seems leak-proof forever | Investigate leak-suppression grace/actual new impact; do not disable genuine damage |
| Only some custom models deform | GTA model-native support and deformation blacklist |

**Related:** [Server Repair Exports](server-exports.md#8-repair-integration--authorizefullrepair--beginfullrepair) · [Client Observation Export](client-exports.md#notifyvehiclerepairedvehicle-scope) · [Configuration](customization-reference.md) · [Troubleshooting](troubleshooting.md).