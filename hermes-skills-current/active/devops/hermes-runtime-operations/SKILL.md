---
name: hermes-runtime-operations
description: "Use when recovering, provisioning, or troubleshooting Hermes Agent runtime integrations: Telegram gateways, multiple bot homes, split HERMES_HOME processes, WSL browser automation, Playwright/Node dependencies, and BotFather/Telegram Web fallback checks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes-agent, telegram, gateway, wsl, browser, playwright, recovery]
    related_skills: [hermes-agent]
---

# Hermes Runtime Operations

## Overview

This is the umbrella skill for operational recovery and provisioning of Hermes runtimes, especially Telegram gateway processes, multi-bot setups, split `HERMES_HOME` instances, and WSL browser automation failures. Narrow historical playbooks are preserved in `references/`.

Load `hermes-agent` as well when the task asks about Hermes configuration, CLI, providers, tools, skills, gateway, plugins, or setup.

## When to Use

- Telegram bots stop responding, respond from the wrong home, or conflict through duplicate gateway processes.
- A second or auxiliary Telegram bot must run concurrently with its own token and Hermes home.
- Browser tools fail in WSL because Node, browser dependencies, or Playwright browsers are missing.
- Hermes model routing, delegation, fallback providers, or auxiliary provider setup unexpectedly charges, fails, or must preserve exact OpenRouter `:free` model slugs.
- Gateway chat returns a sanitized provider-failure warning and the raw provider/model/base_url tuple must be diagnosed from logs.
- Hermes Agent itself must be updated safely while preserving local edits, surviving gateway restarts, migrating config, and verifying the updated runtime.
- BotFather, Telegram account-side actions, or Telegram Web fallback checks are needed from WSL/Windows.

## Core Recovery Workflow

1. **Identify the intended home.** Confirm `HERMES_HOME`, config path, token source, process command, and expected bot/account.
2. **List competing processes.** Look for duplicate gateways, stale processes, split homes, or imports crashing at startup.
3. **Stop only the wrong processes.** Preserve active unrelated homes/bots.
4. **Repair prerequisites.** For browser automation, check Node/npm, local agent-browser dependencies, and Playwright browser installs before declaring browser automation unavailable.
5. **Restart with explicit environment.** Launch each gateway with its own home/token and verify logs.
6. **Verify externally.** Send a real message or perform the browser action; do not rely only on process liveness.

## Hermes Agent Safe Update Workflow

Use this when the user asks to update Hermes Agent itself. The update can restart the active gateway and interrupt the conversation, so the workflow must be resumable and evidence-first.

Reference: `references/hermes-safe-update-recovery.md`

Fast checklist:
1. Snapshot version, git HEAD, diffs, and untracked files into a timestamped backup directory.
2. Stash tracked/untracked source changes before running `hermes update`; move any leftover ignored untracked directories into the backup.
3. Run `hermes update`, then verify with `hermes --version`, `git rev-list --left-right --count HEAD...origin/main`, and `git status --short`.
4. Run `hermes config check` / `hermes doctor --fix` for config migrations and safe runtime maintenance.
5. Smoke-test focused areas and verify `hermes gateway status` after the restart.
6. Report any stashed custom patches separately; do not silently reapply them to a clean latest-upstream install.

## Labeled Subsections

### Telegram gateway recovery

Use the detailed reference when a bot stops responding because duplicate gateway processes, split homes, or import crashes are suspected.

Reference: `references/hermes-telegram-gateway-recovery.md`

### Multi-bot provisioning

Use when running an additional Telegram bot concurrently. Each bot needs its own Hermes home, token, startup process, and pairing/approval path.

Reference: `references/hermes-multi-telegram-bot-provisioning.md`

### WSL browser runtime recovery

Use when browser tools fail in WSL. First repair the runtime: check Node/npm, install dependencies, install Playwright browsers, and inspect Windows-side Telegram/session fallback paths where relevant.

Reference: `references/hermes-wsl-browser-runtime-recovery.md`

### OpenRouter free model billing safety

Use when configuring or debugging Hermes delegation/auxiliary/provider routing through OpenRouter with a `:free` model slug. Treat `:free` as part of the billable model ID, disable suspected paid routes first, and verify without making model calls when billing is in question.

Reference: `references/openrouter-free-model-safety.md`

### Provider fallback failure recovery

Use when a gateway chat hides raw provider errors behind a sanitized warning. Check systemd/gateway logs for the exact `provider`, `base_url`, `model`, and HTTP status tuple. If a fallback combines the wrong provider with the wrong base URL, remove the bad fallback entry from config and restart the gateway rather than retrying it.

Reference: `references/hermes-provider-fallback-recovery.md`

### Hermes safe update and post-update recovery

Use when updating Hermes Agent itself. Preserve local source changes first, tolerate gateway-restart interruption by resuming with git/version checks, migrate config, verify focused tests, and repair runtime state only with backed-up, evidence-based steps.

Reference: `references/hermes-safe-update-recovery.md`

## Verification Checklist

- [ ] Correct `HERMES_HOME` and token source identified.
- [ ] Duplicate/stale gateway processes handled safely.
- [ ] Startup logs show the intended bot/home.
- [ ] Provider failure warnings traced to raw `provider` / `base_url` / `model` logs before changing config.
- [ ] Bad fallback entries removed only when scoped to the user's request, with a config backup and restart verification.
- [ ] Browser runtime prerequisites repaired or conclusively checked.
- [ ] External Telegram/browser action verified end-to-end.

## Cloudflared quick tunnel origin-refused triage

When a background `cloudflared`/`trycloudflare.com` tunnel reports `Unable to reach the origin service`, `target machine actively refused it`, or `dial tcp [::1]:PORT`, treat this first as an **origin listener** problem, not a Cloudflare auth problem.

Fast workflow:
1. Poll/log the background process to identify the configured origin URL and port, e.g. `--url http://localhost:10004`.
2. Inspect the tunnel launcher script if available to confirm the exact Windows/WSL origin target.
3. Check listeners on both sides when running under WSL:
   - WSL: `ss -ltnp | grep ':PORT' || true`
   - Windows: `powershell.exe -NoProfile -Command 'Get-NetTCPConnection -LocalPort PORT -State Listen -ErrorAction SilentlyContinue'`
4. If no listener exists, report that the local app/service is stopped or moved; do not keep restarting Cloudflare.
5. Check for duplicate stale Windows `cloudflared.exe` processes with `Get-CimInstance Win32_Process` and stop only the processes targeting the dead origin/port. Preserve unrelated tunnels.
6. Restart the intended local service first, then relaunch `cloudflared tunnel --url http://localhost:PORT --no-autoupdate`.

## Common Pitfalls

1. **Killing every Hermes process.** Multi-bot setups may intentionally run multiple homes.
2. **Trusting process liveness.** A process can be alive but reading the wrong config or token.
3. **Skipping WSL repair.** Do not report browser automation unavailable until Node/npm/dependencies/Playwright paths have actually been checked.
4. **Conflating BotFather with local gateway state.** Account-side configuration and local gateway recovery are separate layers.
5. **Misdiagnosing Cloudflare Tunnel origin failures.** A `trycloudflare.com` URL can be alive while the local origin is dead. When logs show `Unable to reach the origin service` / `connection refused`, inspect the tunnel command for its `--url`, verify a listener on that exact port from the same OS context running `cloudflared` (Windows vs WSL matters), then stop only stale duplicate tunnels pointing at dead origins. Do not kill unrelated tunnels for other ports.
6. **Stale `AUXILIARY_VISION_MODEL` env var breaks browser_vision.**
6. **Stale `AUXILIARY_VISION_MODEL` env var breaks browser_vision.** The `browser_tool.py` reads `AUXILIARY_VISION_MODEL` from the environment (line 207), which overrides the internal vision model resolution. If this env var is set to a deprecated model ID (e.g. `google/gemini-2.0-flash-lite-preview-02-05`), `browser_vision` and `vision_analyze` will fail with "not a valid model ID" errors from OpenRouter. Fix: `unset AUXILIARY_VISION_MODEL` to fall back to the internal `_OPENROUTER_MODEL` default (`google/gemini-3-flash-preview`), or update it to a current model. Check also `AUXILIARY_APPROVAL_MODEL` and `AUXILIARY_WEB_EXTRACT_MODEL` — they may also be stale.

   **Where these vars come from:** They are set at **gateway/CLI startup time** by `hermes_cli/setup.py` (line 968 exports the vision model) and `hermes_cli/tools_config.py` (line 1789 sets a default). They persist in the running process environment — NOT in any shell profile file (`.bashrc`, `.zshrc`, `.profile`). To permanently fix:
   1. Unset in current session: `unset AUXILIARY_VISION_MODEL AUXILIARY_APPROVAL_MODEL AUXILIARY_WEB_EXTRACT_MODEL`
   2. Restart the gateway: `hermes gateway restart`
   3. If still broken, manually set in `~/.hermes/.env`: `AUXILIARY_VISION_MODEL=google/gemini-3.1-flash-lite-preview`
7. **Misreading sanitized provider failures as platform failures.** Gateway chat may hide raw LLM provider details. Before touching Telegram or pairing state, inspect `journalctl --user -u hermes-gateway.service` or gateway logs for the exact provider/base_url/model tuple. If a fallback tuple is invalid (for example `provider=azure-foundry` using the ChatGPT Codex backend URL), remove the bad fallback entry from config and restart the gateway.

   Reference: `references/hermes-provider-fallback-recovery.md`

## Consolidated Reference Index

The following formerly separate narrow skills have been absorbed into this umbrella. Load the listed reference file only when that specific provider, failure mode, or workflow detail is needed.

- `hermes-multi-telegram-bot-provisioning` → `references/hermes-multi-telegram-bot-provisioning.md`
- `hermes-telegram-gateway-recovery` → `references/hermes-telegram-gateway-recovery.md`
- `hermes-wsl-browser-runtime-recovery` → `references/hermes-wsl-browser-runtime-recovery.md`
- OpenRouter `:free` model billing safety → `references/openrouter-free-model-safety.md`
- Gateway provider fallback recovery → `references/hermes-provider-fallback-recovery.md`
- Hermes safe update and post-update runtime recovery → `references/hermes-safe-update-recovery.md`
