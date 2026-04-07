# Integration Rules

These rules are mandatory for M4I script development.

- integrate through `m4i_bridge` where abstraction exists
- do not bypass bridge for framework/inventory calls in business logic
- follow bridge callback, logging, and security patterns
- document integrations and failure behavior

If a required bridge abstraction is missing, propose bridge extension first.
