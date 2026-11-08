# m4i_garage — Integration

> **CURRENT GARAGE INTEGRATION GUIDE:** [Required External Script Edits](integrations.md) with real dealership, keys, Cover, phone and mechanic methods; [Client Exports](client-exports.md) and [Server Exports](server-exports.md) for the current `0.1.140-alpha` API. This older page remains for old links.


## Ownership of responsibilities

`m4i_garage` is the authority for Garage-specific parking, car custody, vehicle condition snapshots, temporary/permanent keys, impound, Police Seized, insurance, cover objects and Garage Creator. It is **not** the source of truth for Core player identities, jobs, finances or inventory frameworks.

```text
External script
  |-- Garage-specific read/export --> m4i_garage
  |                                    |
  |                                    +--> signed OneSync vehicle/state
  |                                    +--> garage-owned database
  |                                    +--> m4i_bridge --> selected provider
  |
  +-- general player/job/inventory/money operations --> m4i_bridge
```
Never call QBCore, Qbox, ESX, or Ox Core directly from an M4I gameplay module when a Bridge capability exists. New bridge capabilities should be implemented there rather than building a parallel framework integration.

## Safe integration flow

1. Declare `m4i_garage` as a dependency only if your resource actually invokes it.
2. Use the relevant `server` export for signed IDs, persisted status, garage access or repair authorization; use `client` exports for client zone/UI and locally hydrated condition.
3. Do not grant ownership, create currency transactions or delete vehicles merely because a client says it is inside a Garage. Garage Server remains authoritative.
4. For approved dealership registration, allowlist the exact registrar resource in `Config.TrustedVehicleRegistrars`, validate vehicle class, model, garage category and ownership using Bridge.
5. For mechanic integration, allowlist trusted repair scripts in `Config.RepairTrustedResources` and use the existing verified full-repair permit flow.
6. For custom phone apps or UI, prefer client read-only exports plus verified Garage server actions rather than raw SQL queries.
7. Test with two players, a damaged car, late OneSync stream-in, and full/partial repair before claiming fully identical cosmetic results across clients.

## Client versus server contract

`GetVehicleCondition` is deliberately exported on **both sides**. On the client it receives a local GTA vehicle handle and returns live native readings from a signed, hydrated vehicle. On the server it receives a persistent Garage vehicle ID and returns the last saved SQL snapshot.

```lua
-- client.lua
local live, why = exports['m4i_garage']:GetVehicleCondition(vehicleHandle)

-- server.lua
local saved, why = exports['m4i_garage']:GetVehicleCondition(garageVehicleId)
```
Passing a Network ID as a persistent Garage database ID is incorrect. Use `GetVehicleEntity` server-side to obtain the current entity handle and Network ID for a known Garage ID.

## Security

All write-capable existing exports retain their trust gates. New APIs are read-only except `OpenGarage`, which starts the normal asynchronous, server-validated UI request and cannot open from outside the actual configured polygon.

Never expose `GetVehicleStatus`'s raw SQL result to NUI or a generic client callback without filtering owner/character identity. New `GetVehicleByPlate` does not include that identity.

## Limitations

The source ships a provider-qualified persistent Garage ID for Qbox, QBcore, ESX, and Ox Core, and uses the explicit Bridge target/radial provider selection. See [Five Frameworks and Bridge Providers](framework-compatibility.md). Some optional integrations (notably five-use Cover) remain dependent on specific inventory provider contracts.

The test VPS source is staged at `0.1.121-alpha`. Automated Lua/JavaScript regression tests cover source-level contracts; full real-game provider, Escrow distribution, and 200-client visual consistency remain separate release acceptance steps.
