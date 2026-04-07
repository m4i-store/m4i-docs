# Integration

This page defines the only approved way for other M4I scripts to consume identity data.

## Core Rule

Use `m4i_identity` read-only exports for identity state access.

Do not:

- query `m4i_identities` directly from other scripts
- create/update identities outside `m4i_identity`
- copy identity resolution logic into gameplay scripts

## Read-Only Access Model

Allowed integration pattern:

1. Script gets server `source`.
2. Script reads identity state via export.
3. Script uses read data for business decisions.

Identity writes remain internal to `m4i_identity` lifecycle.

## Safe Consumption Example

```lua
local state = exports.m4i_identity:GetIdentityState(source)
if not state then
    return
end

local language = state.language
local discordId = state.discord_id
```

Use `GetIdentityLanguage` / `GetIdentityDiscordId` / `GetIdentityLicense` when only one field is needed.

## Bridge-Compatible Guidance

If `m4i_bridge` consumes identity:

- consume only `m4i_identity` read exports
- cache minimally where needed
- never treat bridge as identity write owner
- never mirror identity table writes in bridge

## Intentionally Not Exposed

Not exposed for external write access:

- identity create
- identity update
- identity delete
- direct store-level DB helpers

This is intentional and required for platform consistency.
