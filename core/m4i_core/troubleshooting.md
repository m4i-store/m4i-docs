# m4i_core Troubleshooting

## Core does not become ready

Check:

1. `oxmysql` is started first
2. database connection is valid
3. migrations completed without error
4. resource folder is named exactly `m4i_core`
5. console does not show schema or startup failures
6. `exports.m4i_core:IsReady()` returns `true`
7. `exports.m4i_core:GetRuntimeInfo()` reports `mode = primary` and `externalFrameworkRequired = false`

A failure here does not mean another framework core is missing. Native `m4i_core` does not require QBCore/Qbox/ESX/Ox Core.

## Bridge does not select M4I

The shipped/default framework provider is `m4i` and the default framework priority is M4I-only.

Check:

1. no profile-scoped `m4i_bridge:frameworkProvider` override intentionally selects another framework
2. `m4i_core` is started before or alongside the bridge
3. `GetPlayerData` exists and is functional
4. `IsReady()` becomes `true`
5. `GetFrameworkCapabilities()` reports provider `m4i` once healthy
6. bridge resolver/health logs do not show a permanently disabled M4I provider

A `GetPlayer`-only partial core is intentionally not considered healthy.

If the bridge starts while Core is still completing database/migration readiness, the framework domain may be temporarily soft-disabled. The `m4i_core:server:ready` lifecycle signal should refresh/recover provider `m4i` without selecting another core.

## Unexpected external framework selection

Under the shipped defaults, QBCore/Qbox/ESX/Ox Core are not automatic framework fallback candidates.

If one of them is selected, inspect deliberate configuration changes:

- `providers.selected.framework`
- the `m4i_bridge:frameworkProvider` convar/profile override
- whether framework autodetect was explicitly enabled
- whether framework priority was customized
- whether registered-provider fallback was explicitly enabled

Treat external framework selection as compatibility mode, not native M4I failover.

## Automatic migration errors

Current default is `autoMigrate = true`.

If startup fails during migration:

- stop the core
- do not manually mark the migration as applied
- inspect the exact SQL/database error
- verify the target database/schema
- restore from backup if a production migration partially changed unexpected state
- reproduce in staging before retrying production

## Player loads but data is missing

Inspect:

- canonical user/character resolution
- account/group load results
- provider identity links
- database errors
- whether the player source/identity changed during the load
- session handoff/retry metrics

Do not fix missing runtime state by editing M4I core tables while the player is online.

## Money operation fails

Check:

- account name is allowed
- amount is valid and within max transaction limit
- sufficient balance exists for removals
- a stable operation ID was not reused for a conflicting operation
- transaction/ledger did not report an error
- optimistic conflict did not exceed its bounded retry

Never bypass a failed money mutation with direct SQL while the player is loaded.

## Reconnect or source-reuse issues

Collect:

- old and new source IDs
- character ID
- session generation where relevant
- load/unload timing
- session handoff metrics
- deferred cleanup metrics
- console errors

The current core includes guards for overlapping sessions, delayed cleanup, load retries, queued stale-session deliveries, and terminal unload events against reused source IDs. Any reproduction should be treated as a lifecycle bug and tested before production changes.

## Database pressure

If database activity is unexpectedly high:

- identify the caller/resource
- distinguish core-owned operations from script-owned SQL
- verify gameplay scripts are not polling bridge DB exports
- verify scripts are not bypassing bridge/core APIs
- inspect snapshot/cache/delivery/write-queue metrics
- inspect transaction/save latency
- inspect whether ordinary state is being written unnecessarily often

See [M4I Data Layer](data-layer.md) and [M4I Data Access Policy](../../shared/data-access-policy.md).

## Support evidence

Include:

- `m4i_core` main/release commit
- `m4i_bridge` main/release commit
- `GetRuntimeInfo()` output with secrets excluded
- provider configuration
- migration versions
- relevant metrics snapshot
- exact console error
- minimal reproduction steps
