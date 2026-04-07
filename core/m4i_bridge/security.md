# Security

## Security model overview

`m4i_bridge` provides centralized security helpers so scripts can inherit safer behavior by default.

Primary controls:

- source validation
- callback token validation (optional)
- callback payload limits
- cooldown and rate limiting
- suspicious scoring and anomaly detection
- optional auto-block and auto-ban hook trigger

## Callback security

Callback service integrates with security checks on server and client flows.

Checks include:

- callback request shape validation
- source identity validation (server-side)
- payload size validation
- cooldown and rate limit checks
- token verification when enabled
- duplicate/replay request blocking

## Token mode

Enable in config:

```lua
callbacks = {
    requireToken = true,
    tokenLength = 40
}
```

Behavior:

- server issues per-source token
- callback envelopes include token
- mismatched/missing token requests are rejected

## Validation and limits

Important settings:

- `security.rejectInvalidSource`
- `security.maxCallbackPayloadBytes`
- `security.callbackCooldownMs`
- `callbacks.serverRateLimit`
- `callbacks.clientRateLimit`

## Suspicious scoring

Security service tracks suspicious events with weighted scoring.

Examples:

- invalid source
- malformed callback request
- token mismatch/missing token
- callback event injection patterns
- duplicate callback requests

Threshold settings:

- `security.suspiciousScoreThreshold`
- `security.suspiciousScoreDecayMs`
- `security.anomalyWindowMs`
- `security.anomalyThreshold`

## Auto-actions

Optional automated responses:

- `security.autoBlockOnThreshold`
- `security.autoBlockDurationMs`
- `security.enableAutoBanHook`
- `security.banHookEvent`

If auto-ban hook is enabled, bridge emits the configured event when threshold is reached. Your server can bind that event to your own ban logic.

## Security best practices

- enable `production.safeMode` on production servers
- enable callback token mode for untrusted environments
- keep payloads small and structured
- never bypass bridge callback channel with ad-hoc net events for sensitive actions
- monitor suspicion scores and blocked source events
- log with trace IDs for incident triage
