# m4i_core Installation

## Requirements

- FiveM server artifact with Lua 5.4 support
- MariaDB/MySQL supported by `oxmysql`
- `oxmysql` installed
- `m4i_registry` installed
- database credentials with permission to create/update M4I schema when automatic migrations are enabled

Resource folder names must remain exact:

```text
m4i_registry
m4i_core
m4i_bridge
m4i_admin
```

No QBCore, Qbox, ESX, or Ox Core resource is required for the native M4I framework path.

## Native start order

Core 0.3 requires canonical registry definitions before Core membership migration/player load.

Use:

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
ensure m4i_bridge
ensure m4i_admin

# M4I gameplay resources after the bridge
ensure m4i_example
```

`m4i_core` does not depend on `m4i_bridge`; Bridge consumes provider `m4i` through the native Core adapter. Core accesses `m4i_registry` directly for canonical job/gang/group definitions.

Other bridge domains may still use separate providers such as `ox_inventory`, `ox_lib`, or `ox_target`. Those are not framework cores.

## Runtime verification

After Registry/Core start:

```lua
local registryReady = exports.m4i_registry:IsReady()
local info = exports.m4i_core:GetRuntimeInfo()
local coreReady = exports.m4i_core:IsReady()
```

Expected Core architecture fields include:

```text
mode = primary
externalFrameworkRequired = false
databaseDriver = oxmysql
definitionRegistry = m4i_registry
definitionRegistryRequired = true
```

Core readiness should remain false if the required definition registry cannot become ready.

## Automatic migrations

Both Registry and Core currently ship automatic migrations enabled by default.

Registry must migrate first. Registry schema v2 prepares canonical definition/history state and group-name uniqueness, then imports legacy Core group definitions if present. Core schema v3 then upgrades group membership rows to domain-aware membership state.

**Do not first-start these releases against an important production database without a verified database backup and rollback plan.**

### Legacy group migration ordering

For an upgraded native M4I database:

1. `m4i_registry` starts;
2. Registry creates/updates its own schema;
3. Registry imports missing legacy `m4i_groups` definitions without overwriting existing Registry definitions;
4. Registry seeds canonical `unemployed` if missing;
5. Registry publishes ready;
6. `m4i_core` starts/migrates membership rows to `group_domain`;
7. Core runtime uses Registry definitions from that point forward.

The old `m4i_groups` table is not automatically dropped in these releases.

## Bridge primary/default behavior

Shipped bridge defaults remain:

```lua
selected = {
    framework = "m4i"
}

priority = {
    framework = { "m4i" }
}
```

Autodetect remains disabled by default. Native M4I therefore does not silently fall back to QBCore/Qbox/ESX/Ox Core.

External framework adapters remain explicit compatibility choices.

## First isolated boot

Use a dedicated profile and database clone. Recommended gate:

1. back up/clone the isolated database
2. start only `oxmysql`
3. start `m4i_registry`
4. verify Registry v2 migration and canonical definitions
5. verify legacy group import/default seeding if legacy test rows exist
6. start `m4i_core`
7. verify Core v3 membership migration
8. verify `GetRuntimeInfo()` and `IsReady()`
9. start `m4i_bridge`
10. verify framework provider `m4i` and definition read exports
11. start `m4i_admin`
12. connect a real test client
13. test player load/reconnect/source reuse
14. test money operation-ID replay/conflict and persistence
15. test job grade validation
16. edit job/gang/group definitions live and verify Core refresh without restart
17. verify job/gang/group canonical duplicate rejection
18. verify Smart Import and namespace-conflict UX
19. restart Registry/Core/Bridge in controlled order while connected
20. restart the isolated profile and re-check database/runtime invariants

Binary image upload/materialization is not yet part of this runtime gate because it is not shipped.

## Production migration

The native stack does not require another framework core. However, do **not** delete an existing production QBCore/Qbox/ESX/Ox Core merely because Registry/Core start successfully.

Existing third-party resources and persistent data may still be framework-specific. Production cutover requires:

- direct dependency audit
- framework-schema SQL audit
- database/file backup
- data migration where required
- controlled provider/config cutover
- smoke/reconnect/restart tests
- rollback validation

Only after that cutover is proven should obsolete old-framework resources be removed. Follow [Production Rollout](production-rollout.md).
