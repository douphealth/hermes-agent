<!-- Consolidated from skill: hermes-multi-telegram-bot-provisioning; original path: /home/hermes/.hermes/skills/devops/hermes-multi-telegram-bot-provisioning -->

---
name: hermes-multi-telegram-bot-provisioning
description: Run additional Telegram bots concurrently in Hermes by giving each bot its own Hermes home, token, startup process, and DM pairing approval.
version: 1.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [telegram, hermes, gateway, multi-bot, provisioning]
---

# Hermes Multi Telegram Bot Provisioning

Use when the user already has one or more Hermes Telegram bots and wants extra bots live at the same time.

## Core rule
One Hermes home supports one active Telegram bot token. To run multiple bots concurrently, provision one separate Hermes home per bot and start one gateway per home.

## Reusable workflow

1. Verify the new token with Telegram `getMe` before doing any setup.
   Success means the token is valid and returns the bot username.

2. Create a new dedicated Hermes home for the new bot.
   Recommended suffix pattern:
   - `.hermes-001`
   - `.hermes-002`
   - `.hermes-003`

3. In the new bot home, create the normal runtime directories:
   - `logs/`
   - `sessions/`
   - `cron/`

4. Seed the new bot home from an already-working Hermes home by copying only the baseline runtime configuration and auth artifacts.
   This avoids re-running interactive setup for every additional bot.

5. Write a fresh `.env` in the new bot home containing:
   - `HERMES_MAX_ITERATIONS`
   - the new `TELEGRAM_BOT_TOKEN`
   - the model/provider keys required for replies (for this environment, especially `OPENROUTER_API_KEY`)
   - any other shared keys the existing working bot home needs

6. Create a tiny launcher script for that bot home that:
   - changes into the bot home
   - exports `HERMES_HOME` to that bot home
   - runs `python -m hermes_cli.main gateway run --replace`
   - redirects stdout/stderr to a per-bot temp log

7. Start the gateway with explicit `HERMES_HOME` and keep it as a background process.

8. Verify success in `logs/agent.log`.
   Required lines:
   - `Connected to Telegram (polling mode)`
   - `Gateway running with 1 platform(s)`

9. If the owner DMs the bot and gets blocked, approve DM pairing for that specific bot home using:
   - `pairing approve telegram <CODE>`
   Then confirm with:
   - `pairing list`

## Recommended Hermes tool pattern
- Use `execute_code` for the setup phase when you need to parse an existing env file, create the new bot home, copy baseline config/auth, and write new files in one controlled flow.
- Use `terminal` to call Telegram `getMe` for token validation.
- Use `terminal(background=true)` to launch the gateway.
- Use `read_file` on `logs/agent.log` and `logs/errors.log` for verification.
- Use `terminal` again for `pairing approve` and `pairing list`.

## Observed behavior worth remembering
- A bot can be successfully connected to Telegram yet still reject the owner until DM pairing is approved.
- The warning about missing allowlists is expected when relying on DM pairing instead of a static allowlist.
- Additional bots should be isolated by Hermes home rather than by rewriting one shared `.env`.
- In this environment, `terminal(background=true)` may track a wrapper/parent process that later exits with code 1 while the real gateway child keeps running. Do not assume the bot is down just because the background session completed.
- When a background process reports shutdown diagnostics or exits unexpectedly, immediately verify the real state with both:
  - `ps -ef | grep 'hermes_cli.main gateway run'`
  - the bot home's `logs/agent.log`
  If recent lines still show `Connected to Telegram`, `Gateway running with 1 platform(s)`, inbound messages, or sent responses, the child gateway is still healthy.
- If you restart too quickly after a wrapper exit, a duplicate launch may fail with `Telegram bot token already in use (PID ...)`. That usually means the real gateway instance is already alive under the same Hermes home. Confirm the surviving PID before taking action.
- After a restart race, prefer the child process and verify the latest log tail instead of killing everything blindly.

## Minimal success criteria
- Token validates via Telegram `getMe`
- New Hermes home exists and has its own `.env`
- Gateway is running under that home
- Agent log confirms Telegram connection and active gateway
- Owner is approved or visible in the approved-pairing list
