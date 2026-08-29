# Integration Rules

These rules are mandatory for M4I-owned script development.

## Platform boundary

- integrate framework/provider behavior through `m4i_bridge`
- do not call QBCore/Qbox/ESX/Ox Core directly from M4I gameplay business logic
- do not call `m4i_core` directly when a bridge contract exists
- if a required capability is missing, extend the bridge/adapter contract first

## Data boundary

- never mutate core/framework-owned player state through direct SQL
- never maintain a duplicate private source of truth for balances/jobs/player identity
- use canonical bridge identity (`characterId`) for M4I-owned relational data where appropriate
- use bridge DB exports/service only for approved script-owned persistence
- isolate script SQL/schema logic in a dedicated data/repository service
- avoid polling unchanged player data; use events/subscriptions or explicit refresh

Read the full [M4I Data Access Policy](data-access-policy.md).

## Provider responsibility

When `m4i_core` is selected, the native M4I Data Layer owns M4I framework persistence/state behavior.

When another framework is selected, that framework owns its own data architecture. `m4i_bridge` translates APIs but does not create a second Data Proxy/cache source of truth over it.

## Security / callback rules

- follow bridge callback, logging, and security patterns
- validate all client/external input server-side
- protect financial/ownership/admin flows with server authority
- never expose raw DB mutation through unsecured client events
- use cooldown/rate-limit controls for spam-sensitive actions

## Resource packaging

- include `escrow_ignore` for intentionally editable config/shared/docs/sql files
- keep configuration explicit and documented
- include a dedicated `server/services/webhook_service.lua` in important scripts that emit operational webhooks
- keep webhook URLs in configuration (`Config.Webhooks`)
- route webhook events by category/key with a `Default` fallback
- never scatter raw webhook HTTP calls across gameplay files
- webhook failures must be non-breaking and must never crash gameplay runtime

Recommended minimum:

```lua
escrow_ignore {
    "config.lua",
    "shared/*.lua",
    "README.md",
    "sql/*.sql"
}
```

Webhook minimum:

```lua
Config.Webhooks = {
    Enabled = true,
    Default = "",
    Important = "",
    Security = "",
    Admin = "",
    Audit = ""
}
```

## Compatibility claims

A script may claim support for a framework provider only after the required bridge capabilities have been tested on that provider.

Framework-native third-party resources are not automatically portable. Hard-coded provider schemas/private internals require a shim, patch, or migration review.

## Release rule

Before a production release:

- integration path reviewed
- data ownership reviewed
- critical callbacks/security reviewed
- restart/provider-unavailable behavior tested
- provider compatibility claims validated
- docs updated in `m4i-docs`
