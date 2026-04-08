# Configuration

`m4i_identity` configuration lives in `m4i_identity/config.lua`.

## Identity Validation Flags

- `RequireDiscord` (`boolean`)
: Requires a Discord identifier in connection identifiers.

- `RequireLicense` (`boolean`)
: Requires a FiveM license identifier.

- `DenyIfDiscordMissing` (`boolean`)
: Rejects the connection if Discord is missing while required.

- `DenyIfLicenseMissing` (`boolean`)
: Rejects the connection if license is missing while required.

## Identity Resolution Policy

- `RequirePreRegisteredDiscord` (`boolean`)
: Strict allowlist mode. Identity must exist by `discord_id`.

- `AutoCreatePlayer` (`boolean`)
: If allowlist is not strict, controls whether missing identities can be created automatically.

- `SyncLicenseWithDiscord` (`boolean`)
: Allows license refresh on connect for matched Discord identities.

## Language Behavior

- `EnableLanguageSelection` (`boolean`)
: Enables pre-join language card flow.

- `ForceLanguageSelection` (`boolean`)
: If true, language card failure/timeouts reject connection.

- `DefaultLanguage` (`string`)
: Default fallback language code.

- `LanguageSelectionTimeoutMs` (`number`)
: Timeout for language card completion.

### Language Policy Rules

- If selection is enabled and forced, timeout/failure => reject (`LANGUAGE_TIMEOUT`).
- If selection is enabled and not forced, timeout/failure => fallback to existing/default language.
- Selected language must match allowed values from `shared/languages.lua`.

## Queue Behavior

`Queue` block:

- `Enabled` (`boolean`)
: Enables queue checkpoint stage.

- `PlaceholderDelayMs` (`number`)
: Optional simulated checkpoint delay.

- `RejectAll` (`boolean`)
: Operational policy switch for rejecting at queue stage.

Queue is checkpoint-ready, not a full priority queue engine.

## Throttle Behavior

`Throttle` block:

- `Enabled` (`boolean`)
- `WindowMs` (`number`)
- `MaxAttempts` (`number`)
- `CooldownMs` (`number`)

Identifier priority for throttle keying is:

1. Discord
2. License
3. Source

Reject reason for threshold/cooldown is `TOO_MANY_ATTEMPTS`.

## Logging

`Logging` block:

- `Debug` (`boolean`)
: Enables debug-level local log output.

- `Category` (`string`)
: Default category for logger fallback formatting.

Bridge logger is used when available; local structured logging is used otherwise.

## Webhooks

`Webhooks` block defines dedicated webhook routing for important identity events.

Minimum categories:

- `Enabled`
- `Default`
- `Important`
- `Security`
- `Admin`
- `Audit`

Script-specific keys used by `m4i_identity`:

- `IdentityCreated`
- `IdentityUpdated`
- `JoinAccepted`
- `JoinRejected`
- `LanguageSelected`
- `ThrottleRejected`

Optional routing table:

- `Webhooks.Routes[eventKey] = "<CategoryName>"`

Routing behavior:

1. direct webhook key (for example `IdentityCreated`) if configured
2. category route via `Webhooks.Routes`
3. fallback to `Default`
4. safe skip when no endpoint is configured

Webhook send failures are always non-breaking.
