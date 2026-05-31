<!-- Consolidated from skill: hermes-telegram-gateway-recovery; original path: /home/hermes/.hermes/skills/devops/hermes-telegram-gateway-recovery -->

---
name: hermes-telegram-gateway-recovery
description: Recover Hermes Telegram bots when they stop responding due to duplicate gateway processes, split HERMES_HOME instances, or startup/import crashes. Covers main + secondary bot setups under /home/hermes/.hermes and /home/hermes/.hermes-alex.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [telegram, hermes, gateway, bot, recovery, troubleshooting]
---

# Hermes Telegram Gateway Recovery

Use when a Hermes Telegram bot is not replying, especially in Alexiios's setup with multiple bot instances.

## Environment facts
- Main bot uses `HERMES_HOME=/home/hermes/.hermes`
- Secondary bot uses `HERMES_HOME=/home/hermes/.hermes-alex`
- Secondary launcher often lives at `/home/hermes/.hermes-alex/start.sh`
- Only one bot token can be active per `HERMES_HOME`
- Main failure modes seen in practice:
  1. Multiple `gateway run --replace` processes fighting each other
  2. Secondary/numbered `.env` missing the model/provider credentials required by that home's `config.yaml` (for example `OPENROUTER_API_KEY` for OpenRouter or `AZURE_FOUNDRY_API_KEY` for Azure Foundry)
  3. Per-home model/provider config drift: Telegram connects, but agent replies fail because the isolated home still points at an unsupported provider/model pair (example: `openai-codex` + an unsupported Codex model slug such as `gpt-5.2-codex` can return HTTP 400 even when another Codex slug like `gpt-5.5` works). Live-probe candidate model slugs under the same `HERMES_HOME` instead of trusting model-list output alone.
  4. Provider capacity/billing/model availability failures after the gateway is live: HTTP 429/`Too Many Requests` from an otherwise valid provider, HTTP 402 from OpenRouter credit/max_tokens limits, or HTTP 404 `No endpoints found` after choosing a model slug that OpenRouter no longer serves. Treat these as provider/model routing issues, not Telegram failures.
  5. OpenAI Codex Responses session-state corruption after a provider/model swap: HTTP 400 `invalid_encrypted_content` / `The encrypted content gAAA... could not be verified` means the active Telegram conversation is reusing Codex encrypted reasoning/content that the current provider/account cannot decrypt. Treat this as stale session history, not a Telegram token failure.
  6. Azure OpenAI content-management false positives after the user pastes Azure's own error JSON: HTTP 400 `content_filter` / `ResponsibleAIPolicyViolation` with the `jailbreak` detector can be triggered by the diagnostic text itself. Treat this as prompt/session hygiene and gateway sanitization, not a bad Telegram token.
  7. Gateway starts but agent crashes on import/tool registration
  8. Telegram network fallback/reconnect noise that is not the real root cause

## Fast recovery workflow
1. Check for duplicate gateway processes:
   - `ps -ef | grep -E "gateway run|hermes_cli.main gateway run" | grep -v grep`
2. Kill all existing gateway runners before restarting:
   - `pkill -f "gateway run" || true`
   - Re-check process list to confirm they are gone.
3. Inspect all known bot homes without dumping secrets:
   - `/home/hermes/.hermes/.env`
   - `/home/hermes/.hermes-alex/.env`
   - `/home/hermes/.hermes-*` homes such as `.hermes-001` and `.hermes-003`
   Verify presence of:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENROUTER_API_KEY`
4. For a named bot outage, map bot username → `HERMES_HOME` before restarting by calling Telegram `getMe` for each home token. Example controlled check:
   - Python/read `.env` tokens locally, then `curl -sS https://api.telegram.org/bot$TOKEN/getMe`
   - Match the returned `result.username` to the target bot, e.g. `@myHermes03_bot` has been observed under `/home/hermes/.hermes-003`.
5. If secondary/numbered bot has auth/model issues, sync both the model config and matching credentials from a known-good home. Do not only copy `OPENROUTER_API_KEY` unless the target home actually uses OpenRouter.
   - Compare `config.yaml` model blocks across homes: provider, base_url, default model, api_mode.
   - Compare required env presence/length without dumping secret values (for example `AZURE_FOUNDRY_API_KEY`, `OPENROUTER_API_KEY`).
   - If logs show `The '<model>' model is not supported when using Codex with a ChatGPT account`, treat it as provider/model drift: live-probe available Codex slugs under the same `HERMES_HOME` with `hermes_cli.main chat --provider openai-codex -m <slug> -q 'Reply exactly OK' --toolsets '' --quiet`; use the first slug that returns `OK`.
   - If OpenAI/Codex HTTP 400 `invalid_encrypted_content` or `The encrypted content gAAA... could not be verified`, first run a fresh same-home CLI smoke test (`HERMES_HOME=<home> ./venv/bin/python -m hermes_cli.main chat -q 'Reply exactly OK' --toolsets '' --quiet`). If the fresh smoke test returns `OK`, the provider works and only the Telegram DM session is poisoned. Mark that session entry suspended in `<home>/sessions/sessions.json` (for Alexiios main DM key: `agent:main:telegram:dm:6143186756`) or otherwise force a new session, then restart only that home's gateway. Do not keep changing tokens/keys when the smoke test passes.
   - If Azure OpenAI returns HTTP 400 `content_filter` with `ResponsibleAIPolicyViolation` / `content_filter_result` / `jailbreak` after the user pasted Azure's own error payload, sanitize the inbound diagnostic before it reaches the LLM (for example redact/rename the `jailbreak` field and `ResponsibleAIPolicyViolation` label while preserving that an Azure policy-filter event occurred). Then reset/suspend the affected Telegram DM session and restart the target home's gateway. Do not switch away from Azure if a same-home `gpt-5.5` smoke test returns `OK`.
   - For Azure Foundry `gpt-5.5`, ensure the target home uses `provider: azure-foundry`, `default: gpt-5.5`, `api_mode: chat_completions`, and non-empty Azure `base_url`/`api_key` values. If the home drifted back to `openai-codex` / `codex_responses`, copy the working Azure model block/credentials from a known-good home without printing secrets, then smoke-test before restarting Telegram.
   - For snappier Telegram recovery after provider/session failures, reduce stale context pressure rather than increasing retries: keep `agent.api_max_retries: 1`, lower compression threshold/protected tail for that home, and keep exactly one live gateway process for the target bot.
   - If logs or background process notifications show repeated `Too Many Requests` / HTTP 429 from the LLM provider after inbound messages, keep Telegram running but reroute that home's model config to a non-rate-limited provider/model with matching credentials. In this environment, switching a numbered bot home from Azure Foundry `gpt-5.5` to OpenRouter can clear Azure capacity failures; for the main Hermes02 home (`/home/hermes/.hermes`), switching primary from Azure Foundry `gpt-5.5` to OpenAI Codex `gpt-5.5` cleared repeated Azure 429s when a same-home smoke test passed. Reduce `agent.api_max_retries` to `1` when using fallbacks so Hermes stops burning minutes on retry spam before failover.

   - If an attempted OpenRouter fallback returns HTTP 404 `No endpoints found for <model>`, the model slug is unavailable even if credentials are valid. Choose a known-good OpenRouter model from another working home, live-probe it with a tiny `max_tokens` request, and immediately run a same-home smoke test.
   - After editing config/env, restart only the affected bot home unless a global duplicate-process cleanup is needed.
6. Check logs for real crash cause before blaming Telegram networking:
   - `/home/hermes/.hermes/logs/errors.log`
   - `/home/hermes/.hermes/logs/gateway.log`
   - `/tmp/gw-alex.log` if secondary launcher writes there.
7. If logs show import/startup crash (example: `ToolRegistry.register() got an unexpected keyword argument 'max_result_size_chars'`), verify from the project venv whether the broken import still reproduces:
   - `cd /home/hermes/.hermes/hermes-agent && source venv/bin/activate`
   - import `tools.registry`, `hermes_cli.auth`, and the failing tool module directly.
   This separates stale running processes from current code on disk.
8. Restart cleanly with explicit `HERMES_HOME` values:
   - Main:
     `cd /home/hermes/.hermes/hermes-agent && source venv/bin/activate && HERMES_HOME=/home/hermes/.hermes python -m hermes_cli.main gateway run --replace`
   - Secondary:
     `HERMES_HOME=/home/hermes/.hermes-alex /home/hermes/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace`
   - Named numbered home:
     `HERMES_HOME=/home/hermes/.hermes-003 /home/hermes/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace`
   Prefer Hermes `terminal(background=true)` if available so the process survives the turn and can be polled.
9. Verify recovery with evidence:
   - Process list shows exactly the intended gateway processes
   - For multi-bot setups, verify each process is bound to the correct `HERMES_HOME` by inspecting `/proc/<pid>/environ` (for example `tr '\0' '\n' < /proc/<pid>/environ | grep '^HERMES_HOME='`). A running `gateway run` process can belong to the wrong bot home.
   - `gateway.log` or `agent.log` shows `Connected to Telegram (polling mode)` and `Gateway running`
   - If temporary `httpx.ConnectError` appears, wait for reconnect and look for `Telegram polling resumed after network error`
   - If a parent/background wrapper reports exit but the child gateway PID is still alive and logs continue with inbound messages and sent responses, treat it as a wrapper exit rather than a bot outage.
   - For end-to-end Telegram API verification, use `sendMessage` to the approved owner chat ID after restart and confirm `ok: true`; this proves Telegram can deliver even before the gateway agent processes a fresh user message.
   - For model/provider verification, run a one-shot CLI smoke test under the same home, e.g. `HERMES_HOME=/home/hermes/.hermes-003 /home/hermes/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main chat -q 'Reply with exactly: OK' --toolsets '' --quiet`, and require an `OK` response before claiming the bot can answer. If the smoke test fails with 429, reroute provider/model; if it fails with OpenRouter 404, pick a different served model slug and re-test. For Codex specifically, do not rely only on `get_codex_model_ids()`; probe the exact slug because listed slugs can still be rejected by the account/backend.
   - Background watch alerts can be stale: a previous background session may keep reporting `Error`/`Too Many Requests` after its process has been killed and replaced. Verify current state by checking the live PID's `HERMES_HOME`, the target home's current `config.yaml`, recent log timestamps, and a fresh same-home smoke test before reacting.
   - If the gateway warns that no allowlists are configured, add the owner chat/user ID to the target home's `TELEGRAM_ALLOWED_USERS` (or explicitly opt into allow-all) and restart that home; a connected bot can still deny unauthorized users.
   - If `/start` appears as `Unrecognized slash command` in logs but the gateway sends an unknown-command notice, do not treat that as an outage; it means polling and outbound sending are working.

## Additional field notes from multi-bot recovery
- In this environment, a background launch may spawn a child `gateway run` process that keeps serving Telegram even after the original wrapper/background process reports completion. Always verify the child PID and recent log activity before declaring the bot down.
- If a bot is still silent, do not trust a generic running `gateway run` process alone. Confirm the target bot's own `HERMES_HOME` and restart explicitly with that home if needed:
  - `HERMES_HOME=/home/hermes/.hermes-001 /home/hermes/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace`
  - `HERMES_HOME=/home/hermes/.hermes-003 /home/hermes/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace`
- A `token already in use` startup error immediately after restart often means the fresh instance already grabbed the token and a duplicate second launch lost the race. Check logs for a successful `Connected to Telegram` / `Gateway running` entry before taking destructive action.
- After a Hermes code update, do NOT relaunch all Telegram gateways in parallel. In this environment, concurrent restarts of multiple `HERMES_HOME` bot instances can trigger `Received SIGTERM/SIGINT` shutdown cascades and leave only one survivor. Restart each bot sequentially, verifying `Connected to Telegram` and `Gateway running` in that bot's own `agent.log` before starting the next one.
- Old background `process` notifications can keep firing after a successful recovery because they belong to superseded wrapper launches, not the surviving child gateway. If a completion/error alert arrives for an old session ID, verify the current live bot by checking the latest `gateway run` PID, confirming its `HERMES_HOME` via `/proc/<pid>/environ`, and reading the target bot's own `agent.log` before taking any action.
- When verifying an update, do not trust the CLI line `Update available: ... commits behind` by itself. Confirm real git state with `git rev-list --left-right --count HEAD...origin/main`; if it returns `0 0`, the checkout is current even if the version command still prints a stale behind notice.

## Important interpretation notes
- Do not assume the Telegram API token is bad just because the bot is silent.
- If logs show a Python import/type error during agent startup, fix/restart that first; Telegram can still appear connected while message handling fails.
- If logs show HTTP 400/401/403 from the LLM provider after inbound messages, treat it as model/provider/session failure, not a Telegram token failure. Sync the target home's `config.yaml` model block and matching `.env` keys from a known-good home, then restart and smoke-test under that same `HERMES_HOME`.
- If the HTTP 400 is `invalid_encrypted_content` / `The encrypted content gAAA... could not be verified`, do not assume the configured model is broken. This can be a poisoned OpenAI Codex Responses conversation history after switching providers/models. A fresh same-home CLI smoke test can pass while the Telegram DM keeps failing; in that case force a fresh gateway session by marking the Telegram `sessions.json` entry `suspended: true` (or otherwise resetting the specific session) and restart that home.
- If the HTTP 400 is Azure `content_filter` / `ResponsibleAIPolicyViolation` and the pasted prompt contains Azure's own error JSON, the error text can be the trigger. Preserve the diagnostic meaning but redact trigger labels like `jailbreak`, `ResponsibleAIPolicyViolation`, and `content_filter_result` before passing the message to Azure; reset the affected Telegram session if the bad diagnostic is already in history.
- If the target bot must use Azure Foundry `gpt-5.5`, verify the exact model block under the target `HERMES_HOME`: `provider: azure-foundry`, `default: gpt-5.5`, `api_mode: chat_completions`, non-empty Azure base URL/key. A Telegram token can map correctly while the home has silently drifted back to `openai-codex`.
- If logs show HTTP 429 `Too Many Requests`, treat it as provider capacity/quota saturation, not a Telegram failure. Switch only that bot home's `model` block to another provider/model with valid credentials, restart, and smoke-test. Do not declare fixed until the smoke test passes under the same `HERMES_HOME`. If fallback providers are configured, set `agent.api_max_retries: 1` for the affected home to avoid repeated `Rate limited. Waiting...` messages before failover.
- If logs show OpenRouter HTTP 402 `requires more credits, or fewer max_tokens`, treat it as a billing/max-output-token routing failure, not a Telegram failure. Prefer a cheaper known-served model (for example `google/gemini-2.5-flash-lite` on OpenRouter when live probe returns 200) or cap max output tokens if the config path supports it. Restart the target home and run a same-home `hermes chat -Q -q 'Reply with exactly OK.' --toolsets ''` smoke test before notifying the user.
- If a replacement provider returns HTTP 404 `No endpoints found`, the chosen model slug is not currently served; change the model slug rather than chasing credentials.
- `Connected to Telegram` plus `Gateway running` is necessary but not sufficient; verify there is no immediate `Agent error in session ...` crash after inbound messages.
- In this environment, stale duplicate gateway processes are common and should be killed first.

## Minimal success criteria
- No duplicate stale gateway processes remain
- Main and/or secondary target process is running under the correct `HERMES_HOME`
- Latest logs no longer show the startup TypeError/import crash
- Telegram polling has resumed successfully
