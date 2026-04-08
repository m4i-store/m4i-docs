# Script Template: Integration

Document how the script integrates with:

- `m4i_bridge` exports
- callbacks
- permissions/security checks
- logs/trace IDs

## Integration rules

- prefer bridge exports over direct provider APIs
- validate all external input before side effects
- include failure handling for callback timeout/error branches
- use bridge logging for operational visibility
- use a dedicated `server/services/webhook_service.lua` for important events
- never scatter raw webhook HTTP calls in gameplay/business handlers

## Example sections to include

- server flow
- client flow
- callback contract(s)
- dependency map

## Localization reference requirement

Before implementing localization, refer to:

- `M4I_LANGUAGE_INTEGRATION_PLAYBOOK.md`
