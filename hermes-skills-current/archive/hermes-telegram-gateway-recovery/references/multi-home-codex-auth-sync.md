# Multi-home Codex auth sync during Telegram recovery

Session-derived pattern from a multi-bot recovery involving `/home/hermes/.hermes`, `/home/hermes/.hermes-alex`, `/home/hermes/.hermes-001`, and `/home/hermes/.hermes-003`.

## Symptom
- Telegram gateways connect and poll successfully, but agent replies fail because Azure Foundry returns 401 invalid subscription key/wrong endpoint.
- Switching a secondary/numbered home to `provider: openai-codex` and `model: gpt-5.5` can make the main home smoke test pass while other homes fail with:
  - `No Codex credentials stored. Run hermes auth...`
  - `Codex refresh token was already consumed by another client...`
- A smoke test that prints only `session_id` and no expected `OK` is not success.

## Fix pattern
1. Back up target `config.yaml`.
2. Change target home's model block to the same known-good Codex block as main:
   - `provider: openai-codex`
   - `default: gpt-5.5`
   - Codex backend base URL
   - explicit context length if used by the known-good home
3. Set `agent.api_max_retries: 1` during recovery to avoid slow retry spam.
4. Copy known-good Codex auth into each target home:
   - `cp -p /home/hermes/.hermes/auth.json <target-home>/auth.json`
   - `chmod 600 <target-home>/auth.json`
5. Run same-home smoke tests and require literal `OK` before restarting Telegram:
   - `HERMES_HOME=<target-home> /home/hermes/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main chat -q 'Reply exactly OK' --toolsets '' --quiet`
6. Kill stale gateway processes, then restart homes sequentially, verifying each home logs `Connected to Telegram (polling mode)` and `Gateway running with 1 platform(s)`.

## Pitfalls
- Codex credentials live in `<HERMES_HOME>/auth.json`, not `.env`; copying `.env` keys is insufficient.
- Do not dump `auth.json`, Telegram tokens, or provider keys into logs or replies.
- Do not restart all homes in parallel; sequential restart avoids shutdown cascades.
