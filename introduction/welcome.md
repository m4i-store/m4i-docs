# Welcome

Welcome to `m4i-docs`, the official M4I documentation hub and Git source for the M4I GitBook site.

This documentation is designed for:

- server owners
- M4I developers
- script maintainers
- integration partners

If you are new, follow this path:

1. [Overview](overview.md)
2. [Standards](standards.md)
3. [Universal M4I Architecture](../core/universal-architecture.md)
4. [m4i_core](../core/m4i_core/introduction.md)
5. [m4i_bridge](../core/m4i_bridge/introduction.md)
6. [Script Development Guide](../core/m4i_bridge/script-development-guide.md)
7. [M4I Data Access Policy](../shared/data-access-policy.md)
8. Script Template and product-specific docs

## The core rule

M4I-owned gameplay scripts integrate through `m4i_bridge`.

`m4i_core` is the native M4I framework/runtime, but M4I gameplay scripts should not bind directly to it. This keeps scripts portable across supported framework providers.

All production-facing M4I documentation should be published in this hub so GitBook and the repository stay synchronized.
