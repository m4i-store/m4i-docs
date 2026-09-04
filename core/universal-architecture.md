# Universal M4I Architecture

## Purpose

M4I is a platform, not a single monolithic FiveM resource.

The shipped native architecture separates four responsibilities:

- `m4i_registry` — canonical live definitions/catalogs
- `m4i_core` — native player/runtime authority and framework provider `m4i`
- `m4i_bridge` — stable gameplay integration/compatibility boundary
- `m4i_admin` — authorized in-game management of registry definitions

These responsibilities must not become competing sources of truth.

## Native M4I model

```text
                         m4i_admin
                             |
                             v
                        m4i_registry
                         /         \
                        v           v
             m4i_core definitions  m4i_bridge read API
                    |
                    v
                 M4I Core
            player/runtime state
                    |
                    v
                  MySQL

M4I GAMEPLAY SCRIPTS
          |
          v
     m4i_bridge
          |
          v
 provider m4i (m4i_core)
          |
          v
    M4I DATA LAYER
          |
          v
       oxmysql
          |
          v
    MariaDB / MySQL
```

Native startup order is:

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
ensure m4i_bridge
ensure m4i_admin
```

`m4i_core` 0.3 requires `m4i_registry` to be ready before it migrates/loads runtime group memberships.

## Rule 1 — gameplay scripts depend on the bridge

M4I-owned gameplay resources should call `m4i_bridge`, not a framework directly.

For the native framework path:

```text
M4I script -> m4i_bridge -> provider m4i -> m4i_core
```

External framework compatibility remains explicit:

```text
M4I script -> m4i_bridge -> qbcore / qbox / esx / ox_core
```

The shipped default framework provider is `m4i`, default framework priority contains only `m4i`, and framework autodetection remains disabled by default. The bridge does not silently fall back to another framework core in the normal native profile.

## Rule 2 — definitions and player runtime are separate authorities

`m4i_registry` owns canonical definition data such as:

- item definitions
- job definitions and grades
- gang definitions and grades
- generic group definitions and grades
- vehicle catalog definitions
- weapon definitions
- shared locations

`m4i_core` owns native runtime facts such as:

- user/character identity and sessions
- money/accounts
- which groups/jobs a character belongs to
- membership grade, active state and duty state
- metadata/status
- Data Layer runtime state

Example:

```text
m4i_registry:
  police is a job, label = Police, grades = 0..5

m4i_core:
  character 42 has job police, grade 3, onDuty = true
```

The same job definition must not also be authoritative in a Core-owned definition table.

## Rule 3 — job/gang/group keys have one canonical namespace

Jobs, gangs and generic groups are all represented by a name in Core membership state. Therefore the registry enforces one shared canonical key namespace across those domains.

A key such as `police` cannot simultaneously mean both a job and a gang. The rule is enforced by the registry database as well as by runtime/admin preflight logic.

This prevents ambiguous membership records and race-created duplicates.

## Rule 4 — the selected external framework owns its own data

When QBCore, Qbox, ESX, or Ox Core is explicitly selected, that framework remains responsible for its own cache, persistence, schema and runtime behavior.

**There is no M4I Data Proxy over other frameworks.**

`m4i_bridge` translates supported public capabilities. It does not maintain a competing authoritative player cache or write-behind database layer above another framework.

The registry definition service is an M4I catalog service; it does not intercept or rewrite external-framework player persistence.

## Rule 5 — M4I Data Layer is native-core only

The shipped M4I Data Layer belongs to `m4i_core` and includes:

- server-authoritative RAM-backed player state
- revision-aware bounded snapshot micro-cache
- bounded bulk snapshots
- event/subscription delivery
- wildcard subscriptions
- fixed bounded delivery workers
- ordinary dirty-state write-behind
- per-character coalescing and bounded persistence queue
- backpressure and bounded retry/recovery
- session-generation protection against source reuse
- terminal unload identity semantics
- metrics and bounded latency percentiles

Critical money remains on an immediate transactional path. Job/duty mutations remain immediate controlled persistence paths. These native capabilities are not emulated for external frameworks.

## Definition reads for gameplay resources

M4I gameplay resources should normally use the read-only definition surface in `m4i_bridge`:

```lua
exports.m4i_bridge:GetItemDefinition(key)
exports.m4i_bridge:GetJobDefinition(key)
exports.m4i_bridge:GetGangDefinition(key)
exports.m4i_bridge:GetGroupDefinition(key)
exports.m4i_bridge:GetVehicleDefinition(key)
exports.m4i_bridge:GetWeaponDefinition(key)
exports.m4i_bridge:GetLocationDefinition(key)
```

Registry mutations remain in the trusted administration boundary, not gameplay code.

## Live administration

`m4i_admin` manages definitions through an authorized in-game NUI.

Changes can be previewed, saved, soft-deleted and rolled back without restarting `m4i_core` or the server. Smart Import can parse supported JSON/static Lua data without executing pasted Lua.

Binary asset upload/automatic inventory-image materialization is a planned hardened follow-up and is not part of the currently shipped admin/registry contract.

## Third-party scripts

### M4I-native scripts

Use `m4i_bridge` and supported M4I definition/runtime contracts.

### Framework-native third-party scripts

A script that directly imports QBCore, Qbox, ESX, or Ox Core is not automatically portable to native M4I.

Compatibility may require:

- a reverse-compatibility shim
- a bridge-based source patch
- schema/data migration
- replacement with an M4I-native resource

Direct framework SQL/private-internal dependencies cannot be declared compatible merely because public exports look similar.

## Framework switching

Changing framework provider is a controlled deployment operation, not a live gameplay feature.

A production migration may require:

1. dependency/resource audit
2. database and file backup
3. identity/money/membership/ownership migration
4. canonical definition migration/import
5. provider configuration cutover
6. isolated and production smoke tests
7. rollback validation

Do not delete the old production framework until every required third-party resource and persistent-data dependency has a validated M4I or compatibility path.

## Current release policy

The code repositories now ship native `m4i` as the bridge default and registry-backed `m4i_core` as the native framework path. This code state does **not** prove an existing production server has been migrated.

Before deleting an old production framework, run the latest isolated real FiveM gate using `oxmysql + m4i_registry + m4i_core + m4i_bridge + m4i_admin`, then complete the production compatibility/data audit and controlled cutover plan.
