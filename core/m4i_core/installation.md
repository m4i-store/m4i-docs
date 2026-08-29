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

## Start order

When `m4i_core` is the selected framework provider:

```cfg
ensure oxmysql
ensure m4i_core
ensure m4i_bridge

# M4I gameplay resources after the bridge
ensure m4i_example
```

`m4i_core` does not depend on `m4i_bridge`; the bridge consumes the core provider.

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

## Staging without framework cutover

Installing the resource files is different from selecting the provider.

The current `m4i_bridge` default selected framework is `qbox`, and autodetect is disabled. If Qbox is healthy, simply having M4I code available does not make M4I the selected framework.

For maximum cutover safety, keep `m4i_core` stopped until its database/config preflight is complete. Remember that the framework fallback priority can consider M4I if the selected provider becomes unavailable and `m4i_core` is running.

## First isolated boot

Recommended sequence:

1. use a dedicated test database
2. start `oxmysql`
3. start `m4i_core`
4. verify migrations versions
5. verify `exports.m4i_core:IsReady()` returns `true`
6. start `m4i_bridge` with framework provider `m4i` only in the test profile
7. verify `GetFrameworkCapabilities()`
8. connect a test client
9. test load/reconnect/resource restart
10. test money idempotency and persistence
11. stop and restart the profile
12. verify database invariants again

## Production migration

Do not remove QBCore/Qbox/ESX/Ox Core merely because `m4i_core` starts successfully.

Production cutover requires resource compatibility and persistent-data migration. Follow [Production Rollout](production-rollout.md).
