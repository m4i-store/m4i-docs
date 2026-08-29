# m4i_core Troubleshooting

## Core does not become ready

Check:

1. `oxmysql` is started first
2. database connection is valid
3. migrations completed without error
4. resource folder is named exactly `m4i_core`
5. console does not show schema or startup failures
6. `exports.m4i_core:IsReady()` returns `true`

## Bridge does not select M4I

Check:

1. `m4i_bridge` framework provider is configured as `m4i` for the profile you are testing
2. `m4i_core` is started before the bridge
3. `GetPlayerData` exists and is functional
4. `IsReady()` returns `true`
5. `GetFrameworkCapabilities()` does not report an unavailable native provider
6. bridge resolver/health logs do not show a disabled provider

A `GetPlayer`-only partial core is intentionally not considered healthy.

## Unexpected provider switch

If production is supposed to remain on Qbox/QBCore/ESX/Ox Core but M4I becomes selected after a failure:

- inspect `providers.selected.framework`
- inspect framework priority order
- inspect provider health failures
- verify whether `m4i_core` was running as a fallback candidate

For pre-cutover production staging, keep the active framework plan explicit and do not run unnecessary fallback providers.

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
- operation ID was not reused for a conflicting operation
- transaction/ledger did not report an error
- optimistic conflict did not exceed its bounded retry

Never bypass a failed money mutation with direct SQL while the player is loaded.

## Reconnect or source-reuse issues

Collect:

- old and new source IDs
- character ID
- load/unload timing
- session handoff metrics
- deferred cleanup metrics
- console errors

The current core includes guards for overlapping sessions, delayed cleanup, load retries, and delayed unload events against reused source IDs. Any reproduction should be treated as a lifecycle bug and tested before production changes.

## Database pressure

If database activity is unexpectedly high:

- identify the caller/resource
- distinguish core-owned operations from script-owned SQL
- verify gameplay scripts are not polling bridge DB exports
- verify scripts are not bypassing bridge/core APIs
- inspect transaction/save latency
- inspect whether ordinary state is being written unnecessarily often

See [M4I Data Layer](data-layer.md) and [M4I Data Access Policy](../../shared/data-access-policy.md).

## Support evidence

Include:

- `m4i_core` main/release commit
- `m4i_bridge` main/release commit
- provider configuration
- migration versions
- relevant metrics snapshot
- exact console error
- minimal reproduction steps
