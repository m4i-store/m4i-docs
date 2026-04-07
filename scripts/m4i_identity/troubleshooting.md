# Troubleshooting

## Discord Missing Reject

Reason code: `DISCORD_MISSING`

Check:

- player has Discord open and linked
- `RequireDiscord` / `DenyIfDiscordMissing` config values
- server identifier collection logs

## License Missing Reject

Reason code: `LICENSE_MISSING`

Check:

- FiveM startup state for player
- `RequireLicense` / `DenyIfLicenseMissing` config values

## Strict Allowlist Reject

Reason code: `DISCORD_NOT_ALLOWED`

When `RequirePreRegisteredDiscord = true`:

- Discord is mandatory
- identity must already exist by `discord_id`
- no license fallback path is used

## Language Timeout or Invalid Selection

Reason codes:

- `LANGUAGE_TIMEOUT`
- `LANGUAGE_INVALID`

Check:

- `EnableLanguageSelection`
- `ForceLanguageSelection`
- `LanguageSelectionTimeoutMs`
- allowed language values in `shared/languages.lua`

## Throttle Reject

Reason code: `TOO_MANY_ATTEMPTS`

Check:

- reconnect storm from same Discord/license
- throttle config values (`WindowMs`, `MaxAttempts`, `CooldownMs`)
- cooldown timing before retry

## Queue Checkpoint Confusion

If queue is enabled, current flow is a checkpoint contract, not full priority queue.

Check:

- `Queue.Enabled`
- `Queue.PlaceholderDelayMs`
- `Queue.RejectAll`

## Runtime Debug Snapshot

Use:

```lua
local snap = exports.m4i_identity:GetIdentityDebugSnapshot()
print(json.encode(snap))
```

This helps verify current runtime count, throttle load, and queue mode quickly.

## Internal Error Reject

Reason code: `INTERNAL_ERROR`

Check:

- `oxmysql` availability
- server startup logs for pipeline stage crashes
- resource load order
