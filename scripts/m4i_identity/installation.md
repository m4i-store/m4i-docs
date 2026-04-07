# Installation

## Requirements

- FiveM server (Lua 5.4 enabled)
- `oxmysql` started and operational
- `m4i_identity` resource files installed
- `m4i_bridge` optional for logging fallback/integration patterns

## SQL Import

Import:

- `m4i_identity/sql/m4i_identity.sql`

This creates the `m4i_identities` table used by identity persistence.

## Start Order Guidance

Recommended order:

1. `oxmysql`
2. `m4i_bridge` (optional but recommended)
3. `m4i_identity`
4. M4I gameplay/business scripts

`m4i_identity` must start before scripts that read identity state.

## First Setup Checklist

1. Confirm `oxmysql` is started.
2. Import SQL schema.
3. Configure `m4i_identity/config.lua`.
4. Ensure `RequirePreRegisteredDiscord`, `AutoCreatePlayer`, and language settings match your policy.
5. Restart server and validate join flow with test accounts.
6. Validate read-only exports from a test script.

## Common Mistakes

- SQL schema not imported.
- Starting scripts that depend on identity before `m4i_identity`.
- Expecting `m4i_bridge` to own identity writes.
- Enabling strict allowlist mode without allowlisting Discord IDs first.
