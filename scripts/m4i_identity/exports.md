# Exports

All `m4i_identity` exports are server-side and read-only.

## GetIdentityState

```lua
exports.m4i_identity:GetIdentityState(source)
```

Returns:

```lua
{
    identityId = number,
    discord_id = string or nil,
    license = string or nil,
    language = string
}
```

Returns `nil` when no runtime state exists for the source.

## GetIdentityLanguage

```lua
exports.m4i_identity:GetIdentityLanguage(source)
```

Returns `string|nil`.

## GetIdentityDiscordId

```lua
exports.m4i_identity:GetIdentityDiscordId(source)
```

Returns `string|nil`.

## GetIdentityLicense

```lua
exports.m4i_identity:GetIdentityLicense(source)
```

Returns `string|nil`.

## GetAllIdentityStates

```lua
exports.m4i_identity:GetAllIdentityStates()
```

Returns a map keyed by source containing runtime identity state copies.

Use for diagnostics/internals, not for heavy gameplay loops.

## GetIdentityDebugSnapshot

```lua
exports.m4i_identity:GetIdentityDebugSnapshot()
```

Returns lightweight runtime operational snapshot:

```lua
{
    runtime = {
        activeCount = number
    },
    throttle = {
        enabled = boolean,
        trackedKeys = number,
        coolingDown = number
    },
    queue = {
        enabled = boolean,
        rejectAll = boolean,
        placeholderDelayMs = number
    },
    webhooks = {
        enabled = boolean,
        configuredEndpoints = number,
        hasDefault = boolean,
        hasRoutes = boolean
    },
    timestamp = number
}
```

## Usage Example

```lua
local language = exports.m4i_identity:GetIdentityLanguage(source)
if language == "ar" then
    -- Apply Arabic-side business behavior in your script.
end
```

## Important Boundaries

- No write exports are provided.
- Runtime state is memory-backed and controlled by `m4i_identity`.
- External scripts must not infer DB ownership from exports.
