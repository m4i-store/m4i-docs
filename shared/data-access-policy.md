# M4I Data Access Policy

This policy is mandatory for new M4I-owned gameplay resources.

## 1. Core/framework data goes through `m4i_bridge`

Do not read or mutate player/framework state through direct framework imports.

Forbidden in M4I business logic:

```lua
exports['qb-core']:GetCoreObject()
exports.qbx_core:GetPlayer(source)
exports.es_extended:getSharedObject()
exports.m4i_core:GetMoney(source, 'cash')
```

Preferred:

```lua
local balance = exports.m4i_bridge:GetMoney(source, 'cash')
local job = exports.m4i_bridge:GetJob(source)
```

The bridge is the portability boundary.

## 2. Never write core-owned framework tables directly

M4I scripts must not issue SQL that changes core-owned:

- player identity
- framework balances
- jobs/groups/duty
- core metadata/status
- provider identity links

Direct SQL can desynchronize the authoritative in-memory framework state from persistence.

Use bridge/core contracts that preserve validation, locks, events, idempotency, and synchronization.

## 3. Script-owned tables are allowed

An M4I script may own dedicated tables for its domain when persistence is necessary.

Examples:

- restaurant recipes/orders
- custom race history
- script-specific settings
- domain audit records

Use the approved bridge database exports/service instead of importing `oxmysql` directly into random gameplay files.

Keep schema and SQL inside a clear repository/service layer for that resource.

## 4. Do not duplicate framework state

Do not create a private copy of money/job/player identity in a script table simply to avoid using the bridge.

If the script needs a stable M4I relational key, use canonical `characterId` where the contract provides it.

## 5. Avoid polling

Do not poll unchanged player data on short loops.

Bad:

```lua
while true do
    Wait(100)
    local money = exports.m4i_bridge:GetMoney(source, 'cash')
end
```

Prefer:

- initial read
- authoritative change event/subscription
- explicit refresh only when needed

If several M4I scripts need the same change signal, extend the shared platform contract instead of implementing duplicate polling loops.

## 6. Prefer bounded snapshots for bulk reads

When a feature needs many fields or many players, prefer a bounded snapshot/bulk API rather than hundreds of repeated fine-grained calls.

If the required snapshot API does not exist yet, propose it in the platform layer.

## 7. Critical and ordinary writes are different

Critical state such as money, purchases, and ownership must use strong transactional semantics.

Ordinary state such as non-critical metadata/status may use dirty tracking and controlled persistence when the provider supports it.

A gameplay script must not weaken critical durability merely to reduce database writes.

## 8. Other frameworks own their data architecture

When `m4i_bridge` is configured for QBCore, Qbox, ESX, or Ox Core:

- M4I calls are translated to that provider
- that provider owns its cache/persistence/schema
- M4I does not add a second Data Proxy/source of truth on top

Performance behavior outside the bridge boundary belongs to the selected framework and its third-party resources.

## 9. Database driver is infrastructure

Current native M4I infrastructure uses `oxmysql`.

M4I gameplay scripts should not couple their core/framework behavior to the driver. This keeps the platform free to change internal storage infrastructure later without rewriting every script.

## 10. Measure before optimizing

Performance work must use metrics/benchmarks.

Track logical requests, actual DB operations, transaction latency, slow operations, retries/conflicts, queue depth (when implemented), and persistence latency.

Do not claim performance superiority without representative measurements.
