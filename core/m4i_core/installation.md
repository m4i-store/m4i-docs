# m4i_core Installation

## Requirements

- FiveM server artifact with Lua 5.4 support
- MariaDB/MySQL connection supported by `oxmysql`
- `oxmysql` installed and started before `m4i_core`
- database credentials with permission to create/update the M4I schema when automatic migrations are enabled

The FiveM resource folder name must be exactly:

```text
m4i_core
```

No QBCore, Qbox, ESX, or Ox Core resource is required for the native M4I framework path.

## Start order

Native M4I is now the default framework mode in `m4i_bridge`.

Use:

```cfg
ensure oxmysql
ensure m4i_core
ensure m4i_bridge

# M4I gameplay resources after the bridge
ensure m4i_example
```

`m4i_core` does not depend on `m4i_bridge`; the bridge consumes provider `m4i` through the native core adapter.

Other bridge domains may still use separate providers such as `ox_inventory`, `ox_lib`, or `ox_target`. Those are not framework cores.

## Runtime verification

After `m4i_core` starts, verify the native runtime identity:

```lua
local info = exports.m4i_core:GetRuntimeInfo()
```

Expected architecture fields include:

```text
mode = primary
externalFrameworkRequired = false
databaseDriver = oxmysql
```

`exports.m4i_core:IsReady()` must become `true` after database preflight/migrations complete.

## Automatic migrations

Current default:

```lua
database = {
    autoMigrate = true
}
```

On first start, the core can create/update its own `m4i_*` schema, including the migration table, user/character tables, accounts/ledger, groups/memberships, and provider-link tables.

**Do not first-start `m4i_core` against an important production database without a verified database backup and rollback plan.**

The migrations are designed to be idempotent, but production discipline still requires a backup before schema changes.

## Bridge primary/default behavior

The shipped bridge defaults are now:

```lua
selected = {
    framework = "m4i"
}

priority = {
    framework = { "m4i" }
}
```

Autodetect remains disabled by default.

Therefore an unhealthy/late `m4i_core` does **not** silently turn the server into QBCore/Qbox/ESX/Ox Core. The framework domain can soft-disable temporarily and recover on Core readiness/resource restart.

External framework adapters still exist for explicit compatibility mode when an operator deliberately selects one.

## First isolated boot

Recommended sequence:

1. use a dedicated test database
2. start `oxmysql`
3. start `m4i_core`
4. verify migration versions
5. verify `GetRuntimeInfo()` reports primary standalone mode
6. verify `exports.m4i_core:IsReady()` returns `true`
7. start `m4i_bridge`
8. verify `GetFrameworkCapabilities()` reports provider `m4i`
9. connect a test client
10. test load/reconnect/resource restart
11. test snapshots/subscriptions and source/session reuse protection
12. test money operation-ID replay/conflict and persistence
13. stop/restart Core and Bridge while connected
14. restart the isolated profile
15. verify database invariants again

## Production migration

The native M4I stack no longer requires another framework core. However, **do not delete an existing production QBCore/Qbox/ESX/Ox Core immediately** merely because the native M4I runtime starts successfully.

Existing third-party resources and persistent data may still be tied to that framework. Production cutover therefore requires:

- resource compatibility audit
- database backup
- data migration where required
- controlled provider cutover
- smoke/reconnect/restart tests
- rollback validation

Only after that cutover is proven should the old production framework resources be removed. Follow [Production Rollout](production-rollout.md).
