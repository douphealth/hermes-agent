# OpenRouter `:free` Model Slug Safety

## Trigger

Use this reference when configuring or debugging Hermes model routing, delegation, auxiliary models, or provider overrides through OpenRouter where the user requests a `:free` model slug.

## Durable lesson

On OpenRouter, `:free` is part of the actual model identifier, not cosmetic metadata. For example:

- Free route: `deepseek/deepseek-v4-flash:free`
- Paid sibling: `deepseek/deepseek-v4-flash`

Dropping `:free` can route to the paid model and charge the account. Treat suffix preservation as cost/security-critical.

## Required workflow

1. **Stop paid route first.** If a user reports unexpected billing, immediately clear or disable the suspected delegation/auxiliary route before investigating further.
2. **Inspect exact active config values.** Check the precise provider/model values that will be used by the runtime, not just the intended command.
3. **Preserve `:free` exactly.** Do not normalize, trim, display-normalize, or compare in a way that removes the suffix for OpenRouter calls.
4. **Guard against paid siblings.** If `delegation.provider` is `openrouter`, refuse `deepseek/deepseek-v4-flash` when the intended/requested model is the free route; require `deepseek/deepseek-v4-flash:free` exactly.
5. **Verify without billing.** Prefer static/config checks, catalog pricing checks, unit tests/mocks, or request construction inspection. Avoid smoke tests that make actual model calls until the user explicitly accepts the possibility of a charge.
6. **Restart and re-check.** After config/code changes, restart the gateway and verify the live config/process state.

## Implementation notes from the incident

Relevant delegation path:

- `tools/delegate_tool.py`
- `_resolve_delegation_credentials(cfg, parent_agent)` reads `delegation.provider` and `delegation.model`.
- `delegate_task(...)` passes `creds["model"]` into `_build_child_agent(...)`.
- `_build_child_agent(...)` constructs `AIAgent(model=effective_model, provider=effective_provider, ...)`.

A robust local guard belongs near `_resolve_delegation_credentials(...)` because that is the handoff from persisted delegation config into child runtime construction.

Suggested guard behavior:

- If provider is `openrouter` and model is exactly `deepseek/deepseek-v4-flash`, raise a refusal explaining it is the paid sibling and requiring `deepseek/deepseek-v4-flash:free`.
- If model ends in `:free` but provider is not `openrouter`, raise a refusal explaining OpenRouter free-tier slugs must be sent via `delegation.provider: openrouter`.

## User-facing response pattern

Be blunt and action-first:

- Acknowledge the billing risk/error directly.
- State the immediate safety action taken.
- State the exact guard added or config corrected.
- State what remains unverified if tool/runtime limits interrupt the work.

Avoid framing OpenRouter display normalization as proof of safety. The only safe assertion is the exact request/config model string that will be sent.