# Integration Rules

These rules are mandatory for M4I script development.

- integrate through `m4i_bridge` where abstraction exists
- do not bypass bridge for framework/inventory calls in business logic
- follow bridge callback, logging, and security patterns
- document integrations and failure behavior
- include `escrow_ignore` in every script `fxmanifest.lua` to keep config/shared/docs/sql editable
- include a dedicated `server/services/webhook_service.lua` in important scripts
- keep webhook URLs in `config.lua` (`Config.Webhooks`)
- route webhooks by category/key with `Default` fallback
- never scatter raw webhook HTTP calls across business files
- webhook send failures must be non-breaking (never crash script runtime)

If a required bridge abstraction is missing, propose bridge extension first.

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

## Webhook Standard

- Every important script must own a dedicated webhook service.
- Webhook endpoints must be configured in `Config.Webhooks`, not hardcoded.
- Webhook sends must route by event key/category and fallback to `Default` when needed.
- Raw webhook HTTP calls must not be scattered across random script files.
- Webhook failures are operational signals only and must never break gameplay/runtime flow.
