# Troubleshooting

## Startup fails with configuration validation errors

### Symptoms

- kernel startup aborted
- console shows configuration validation messages

### Checks

1. verify field types in `config/default.lua`
2. verify `providers.selected.<domain>` values are non-empty strings
3. verify boolean flags are booleans (not strings)
4. verify numeric limits are positive where required

## Provider not found or unavailable

### Symptoms

- domain disabled or provider resolution errors
- bridge starts with soft-disabled domains

### Checks

1. confirm selected provider name matches config and adapter naming
2. confirm dependency resource is started (`ox_lib`, `qbx_core`, etc.)
3. inspect `/m4i:debug` provider and disabled-domain sections
4. review `providers.priority` fallback order

## Unexpected fallback provider selected

### Symptoms

- selected provider differs from runtime provider

### Causes

- selected provider failed dependency/health/validation checks
- fallback list selected a healthy alternative

### Actions

1. inspect resolver logs with `debug.providerResolution = true`
2. check provider health thresholds in `providers.health`
3. verify selected provider dependencies and versions

## Plugin registration fails

### Symptoms

- `RegisterPlugin` returns `false` with validation error

### Checks

1. plugin `name` is present and unique
2. lifecycle handlers are functions if defined
3. hooks/middleware definitions are valid tables/functions
4. if source enforcement is enabled, plugin name matches resource name

## Hook issues

### Symptoms

- hooks not firing, or flow cancelled unexpectedly

### Checks

1. verify event name (`before:*` / `after:*`)
2. verify hook priority ordering
3. inspect return shape (`false`, `{ cancel = true }`, payload mutation)
4. check `hooks.failHard` impact on handler errors

## Middleware issues

### Symptoms

- action stops unexpectedly or errors in chain

### Checks

1. ensure `next()` is called at most once
2. verify cancellation is intentional (`return false, "reason"`)
3. check middleware scope name accuracy
4. inspect `middleware.failHard` behavior for handler errors

## Callback timeout or token errors

### Symptoms

- callback returns `timeout`, `invalid_token`, or `token_not_ready`

### Checks

1. confirm callback handler is registered on destination side
2. increase timeout for heavy operations
3. if token mode enabled, ensure token sync occurs before sensitive calls
4. inspect security warnings and trace IDs

## High suspicion scores / blocked source

### Symptoms

- actions rejected due to suspicious behavior

### Checks

1. inspect security logs for triggering action keys
2. review `security.suspicionWeights` and thresholds
3. confirm no duplicate callback request pattern in script logic
4. if needed, tune anomaly threshold/window for your traffic profile

## Collecting diagnostics for support

When reporting issues, include:

- selected providers (`config/providers.lua`)
- production flags (`config/default.lua`)
- `/m4i:debug` output
- related trace IDs
- full error message and structured error code if available
