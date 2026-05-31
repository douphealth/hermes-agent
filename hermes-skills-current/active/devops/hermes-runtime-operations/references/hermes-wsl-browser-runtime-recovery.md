<!-- Consolidated from skill: hermes-wsl-browser-runtime-recovery; original path: /home/hermes/.hermes/skills/devops/hermes-wsl-browser-runtime-recovery -->

---
name: hermes-wsl-browser-runtime-recovery
description: Recover Hermes browser automation in WSL when browser tools fail because Node, agent-browser dependencies, or Playwright browsers are missing. Includes Telegram-session fallback checks on Windows-side paths.
tags: [hermes, wsl, browser, playwright, node, telegram]
---

# Hermes WSL Browser Runtime Recovery

Use this when Hermes browser tools fail in WSL with errors like:
- `agent-browser: exec: node: not found`
- `Cannot find module .../node_modules/agent-browser/bin/agent-browser.js`
- `Executable doesn't exist at ~/.cache/ms-playwright/...`

## Goal
Restore working browser automation before telling the user the browser is unavailable.

## Recovery flow

1. **Check Node/npm first**
   ```bash
   node -v
   npm -v
   npx -v
   ```
   If missing, install Node in user space by the environment's approved method, then re-check versions.

2. **Restore Hermes JS dependencies**
   ```bash
   cd ~/.hermes/hermes-agent
   npm install
   ```

3. **Install Playwright Chromium runtime**
   ```bash
   cd ~/.hermes/hermes-agent
   npx playwright install chromium
   ```

4. **Verify with a real browser tool call**
   Do not stop at version checks. Run an actual browser action such as navigating to `https://example.com` and confirm success.

## Failure chain mapping
- `node: not found` → Node runtime missing in WSL
- `Cannot find module ...agent-browser...` → repo `npm install` missing/broken
- `Executable doesn't exist at ~/.cache/ms-playwright/...` → Playwright browser payload missing

## Telegram / BotFather fallback checks from WSL
Before claiming there is no usable Telegram path from WSL, check:
1. browser automation against Telegram Web
2. Windows-side Telegram Desktop data under `/mnt/c/Users/<username>/AppData/Roaming/Telegram Desktop`
3. Windows app-local Telegram state under `/mnt/c/Users/<username>/AppData/Local/Packages/...`

If a Windows Telegram Desktop path exists, treat that as evidence that local recovery/session options may still exist and investigate before declaring a blocker.

## Verification checklist
- `node -v` works
- `npm install` completed in `~/.hermes/hermes-agent`
- `npx playwright install chromium` completed
- browser navigation succeeds through Hermes browser tools
- Telegram fallback paths were checked if the task involves BotFather or Telegram account-side actions

## Production lesson
For Hermes itself, if future agents keep giving lazy environment excuses, patch `agent/prompt_builder.py` so the WSL environment hint explicitly requires browser-runtime repair and Windows-side Telegram checks before reporting blockers.
