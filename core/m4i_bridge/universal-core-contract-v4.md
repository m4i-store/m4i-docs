# Universal Core Contract v4

Status: **alpha / additive**

Contract version:

```text
4.0.0-alpha.1
```

The Universal Core Contract is the framework portability boundary for M4I-owned gameplay resources.

It is additive to the existing bridge API; existing v3 consumers do not have to be rewritten merely because v4 exists.

## Non-negotiable invariant

M4I gameplay resources depend on `m4i_bridge`, never on a concrete framework.

Allowed:

```lua
local balance = exports.m4i_bridge:GetMoney(source, "bank")
local ok, err = exports.m4i_bridge:AddMoney(source, "bank", 500, "mission_reward", operationId)
local job = exports.m4i_bridge:GetJob(source)
```

Forbidden in M4I business logic:

```lua
exports["qb-core"]:GetCoreObject()
exports.qbx_core:GetPlayer(source)
exports.es_extended:getSharedObject()
exports.m4i_core:GetMoney(source, "bank")
```

Provider-specific calls belong in bridge adapters.

## Supported framework providers

The current bridge has v4 framework adapters for:

- `m4i` (`m4i_core` resource)
- `qbox`
- `qbcore`
- `esx`
- `ox_core`

The contract normalizes M4I script behavior; it does not claim all providers have identical underlying semantics.

## Server exports

```lua
exports.m4i_bridge:GetFrameworkContractVersion()
exports.m4i_bridge:GetFrameworkCapabilities()

exports.m4i_bridge:GetCharacterId(sourceId)

exports.m4i_bridge:GetMoney(sourceId, account)
exports.m4i_bridge:AddMoney(sourceId, account, amount, reason, operationId?)
exports.m4i_bridge:RemoveMoney(sourceId, account, amount, reason, operationId?)
exports.m4i_bridge:SetMoney(sourceId, account, amount, reason, operationId?)

exports.m4i_bridge:GetJob(sourceId)
exports.m4i_bridge:SetJob(sourceId, jobName, grade)
exports.m4i_bridge:SetDuty(sourceId, onDuty)

exports.m4i_bridge:GetMetadata(sourceId, key)
exports.m4i_bridge:SetMetadata(sourceId, key, value)
exports.m4i_bridge:GetGroups(sourceId)
```

## Canonical job shape

A normalized job is expected to look conceptually like:

```lua
{
    name = "police",
    label = "Police",
    grade = 2,
    onDuty = true, -- may be nil when the provider has no universal duty primitive
    type = "leo"  -- optional/provider-dependent
}
```

Optional values must be treated as optional.

## Capability reporting

Before relying on provider-dependent behavior:

```lua
local info = exports.m4i_bridge:GetFrameworkCapabilities()
```

The response includes:

- contract version
- selected provider
- readiness
- provider capability metadata

Unsupported semantics must be reported rather than silently emulated incorrectly.

### Idempotent money

`capabilities.idempotentMoney = true` means the provider durably deduplicates money operation IDs.

If an operation ID is supplied to a provider that cannot safely provide that guarantee, the operation must fail explicitly instead of discarding the ID and pretending it was idempotent.

Provider `m4i`, implemented by the `m4i_core` resource, supports durable money operation IDs.

## Money semantics

Named accounts are normalized at the bridge boundary, but availability is provider-dependent.

Typical examples:

- QBCore/Qbox: `cash`, `bank`, `crypto`
- ESX: canonical `cash` maps to ESX money; account support depends on configured ESX accounts
- Ox Core: current normalized account behavior differs and intentionally does not pretend unsupported cash/crypto semantics exist
- provider `m4i` / `m4i_core`: named accounts are native to the M4I account model

Scripts should check capabilities when portability depends on a specific account semantic.

## Duty semantics

QBCore/Qbox expose a direct duty concept. ESX/Ox Core do not have one universal primitive that is safe to assume across every server.

Therefore:

- use `SetDuty` where supported
- handle explicit unsupported errors
- do not add provider-specific duty hacks to M4I gameplay code

## Canonical identity

M4I-owned relational data should prefer canonical M4I `characterId` where available.

Provider IDs are integration/migration aliases, not a reason for M4I scripts to hard-code provider identity formats.

The native core maintains provider identity links so external/provider identifiers can map to canonical M4I users/characters.

## Framework switching

Framework switching is an offline deployment/migration operation.

It may require:

- clean server stop
- database backup
- canonical identity mapping
- money/job/group/ownership migration
- configuration change
- provider restart ordering
- capability validation
- rollback

The Universal Core Contract makes M4I script source portable; it does not magically migrate arbitrary persistent data or in-memory state between frameworks.

## Third-party scripts

The portability guarantee applies to M4I-owned scripts that obey the bridge boundary.

Framework-native third-party resources may require reverse-compatibility shims or source patches.

A future shim can translate public framework exports/events, but cannot guarantee arbitrary compatibility for resources that hard-code private framework internals or database schemas.

## Data ownership

The contract does not create an M4I Data Proxy over non-M4I frameworks.

- if provider = `m4i`, the `m4i_core` resource owns the native M4I data architecture
- if provider = QBCore/Qbox/ESX/Ox, that provider owns its data architecture

`m4i_bridge` remains the API compatibility layer in both cases.
