# Overview

`m4i-docs` organizes M4I knowledge in four sections:

- Introduction: onboarding and documentation model
- Core Systems: platform-level architecture, `m4i_core`, and `m4i_bridge`
- Scripts: script-level documentation and templates
- Shared Standards: cross-project rules, including integration and data-access policy

## Platform model

M4I separates portability from native runtime implementation.

- `m4i_bridge`: universal compatibility/integration boundary
- `m4i_core`: native M4I framework and data runtime
- M4I gameplay scripts: depend on the bridge, not on a concrete framework

When another framework is selected, `m4i_bridge` translates the M4I contract to that provider. M4I does not place a second Data Proxy over QBCore/Qbox/ESX/Ox Core; those frameworks own their own data architecture.

When `m4i_core` is selected, the M4I Data Layer provides server-authoritative state, memory-backed hot-path reads, strong financial persistence, and controlled ordinary-state persistence.

## Documentation model

- Central hub first: full docs live here.
- Resource repos second: short README + link to official docs page.
- One change path: canonical docs changes are made in this repository and synchronized to GitBook.
- Implemented vs planned: roadmap features must be labeled clearly until shipped and validated.

## Scale strategy

As M4I grows, this structure avoids documentation and integration sprawl by keeping:

- one canonical documentation location
- one navigation tree
- one shared platform contract
- one framework boundary for M4I scripts
- one data-access policy
- provider-specific logic isolated in adapters

The goal is an ecosystem of scripts that behaves like one platform rather than a collection of unrelated resources.
