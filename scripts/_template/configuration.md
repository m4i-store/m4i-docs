# Script Template: Configuration

Document all script config keys with:

- type
- default value
- valid range/options
- production recommendation

## Bridge alignment requirement

If a script config overlaps with bridge capabilities (callbacks, security, logging), reference bridge behavior instead of redefining conflicting rules.

## Webhook standard requirement

Important scripts must include:

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

Add script-specific webhook keys as needed and route them by event key/category.

## Localization reference requirement

Before implementing localization, refer to:

- `M4I_LANGUAGE_INTEGRATION_PLAYBOOK.md`
