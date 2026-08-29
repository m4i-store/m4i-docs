# Troubleshooting

## Startup fails with configuration validation errors

Check:

1. field types in `config/default.lua`
2. `providers.selected.<domain>` values
3. boolean/numeric limits
4. exact provider/resource names

## Provider not found or unavailable

Check:

1. selected provider name matches config/adapter naming
2. dependency resource is started
3. `/m4i:debug` provider/domain state
4. `providers.priority` order
5. provider health failure count

## M4I provider is unavailable

For framework provider `m4i`, verify:

- resource name is exactly `m4i_core`
- `m4i_core` starts before the bridge
- `exports.m4i_core:IsReady()` returns `true`
- normalized `GetPlayerData` is available
- the required v4 surface is present

A partial `GetPlayer`-only core is intentionally rejected as unhealthy.

## Unexpected fallback provider selected

Possible causes:

- selected provider failed dependency/readiness/health checks
- priority fallback selected a healthy alternative
- a provider recovered and runtime switching restored a preferred candidate

Actions:

1. enable provider-resolution diagnostics in staging
2. inspect health thresholds
3. inspect selected + priority configuration together
4. verify which framework resources are currently running

If production is not ready for M4I cutover, remember that a running `m4i_core` can be a configured fallback candidate.

## Server/client provider mismatch

If server behavior uses one framework while client reads appear to use another:

- verify the current bridge build includes M4I client recovery
- restart/reproduce in staging
- inspect provider health/recovery logs
- verify the native core became ready on both sides

Current bridge recovery is designed to reselect a healthy preferred M4I provider on both server and client without requiring a bridge restart.

## v4 capability call fails

Check:

```lua
local info = exports.m4i_bridge:GetFrameworkCapabilities()
```

Verify:

- `ready == true`
- the expected provider is selected
- the requested semantic is advertised as supported

Do not patch M4I gameplay code with a provider-specific call merely because one provider lacks a universal capability.

## Money operation ID error

If a v4 money mutation fails when an `operationId` is supplied:

- verify `capabilities.idempotentMoney`
- verify the ID was not reused for a conflicting operation
- do not remove the ID silently in retryable financial flows

The bridge intentionally refuses to pretend a non-idempotent provider is idempotent.

## Database misuse / high load

The bridge database service is for approved script-owned persistence.

If an M4I script is issuing repeated SQL for framework/player state:

- stop the direct SQL path
- move framework state access to the bridge/core contract
- replace polling with event-driven behavior where possible
- review [M4I Data Access Policy](../../shared/data-access-policy.md)

The bridge is not a Data Proxy/cache source of truth for QBCore/Qbox/ESX/Ox Core.

## Callback timeout or token errors

Check:

1. handler registration on the destination side
2. timeout is appropriate for the operation
3. token synchronization when token mode is enabled
4. duplicate/replayed request behavior
5. trace IDs and security logs

## Plugin/hook/middleware issues

Verify ownership, naming, registration lifecycle, cancellation behavior, `next()` usage, and fail-hard configuration.

## Collecting diagnostics

Include:

- selected/priority providers
- production flags
- `/m4i:debug` output
- `GetFrameworkCapabilities()` result when framework behavior is involved
- trace IDs
- exact error/reason
- bridge/core commit or release version
