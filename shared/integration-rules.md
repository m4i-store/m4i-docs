# Integration Rules

These rules are mandatory for M4I script development.

- integrate through `m4i_bridge` where abstraction exists
- do not bypass bridge for framework/inventory calls in business logic
- follow bridge callback, logging, and security patterns
- document integrations and failure behavior
- include `escrow_ignore` in every script `fxmanifest.lua` to keep config/shared/docs/sql editable

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
