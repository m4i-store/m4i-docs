# Script Template: Integration

Document how the script integrates with:

- `m4i_bridge` framework/provider exports
- Universal Core Contract v4 capabilities used by the script
- callbacks
- permissions/security checks
- script-owned persistence
- logs/trace IDs
- webhooks where operationally required

## Mandatory integration rules

- use bridge exports instead of direct QBCore/Qbox/ESX/Ox Core calls
- do not call `m4i_core` directly from gameplay business logic when bridge abstraction exists
- do not mutate core/framework-owned player data with direct SQL
- keep script-owned SQL inside a dedicated data/repository service
- validate all external input before side effects
- handle callback timeout/error branches
- handle unsupported provider capabilities explicitly
- avoid polling unchanged player/framework state
- use bridge logging for operational visibility

Read:

- [Universal M4I Architecture](../../core/universal-architecture.md)
- [Universal Core Contract v4](../../core/m4i_bridge/universal-core-contract-v4.md)
- [Script Development Guide](../../core/m4i_bridge/script-development-guide.md)
- [M4I Data Access Policy](../../shared/data-access-policy.md)

## Required documentation sections

Every released script should document:

- server flow
- client flow
- bridge exports/capabilities used
- callback contract(s)
- dependency/provider matrix
- persistent tables owned by the script
- failure behavior when a provider capability is unavailable
- restart/recovery expectations
- security-sensitive actions

## Webhook rules

For important scripts:

- use a dedicated `server/services/webhook_service.lua`
- keep endpoints in configuration
- route by category/key with default fallback
- never scatter raw webhook HTTP calls in gameplay handlers
- webhook failures must not crash gameplay/runtime

## Data ownership statement

The integration page must state what the script owns.

Example:

```text
Framework/player identity: m4i_bridge / selected framework
Money/job/groups: m4i_bridge / selected framework
Script tables: my_script_* only
Inventory: m4i_bridge inventory provider
```

This prevents future maintainers from adding duplicate framework state or unsafe SQL shortcuts.

## Localization reference requirement

Before implementing localization, use the current M4I language integration playbook for that resource.
