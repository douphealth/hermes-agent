# Hermes provider fallback recovery

Use this reference when gateway chat returns a sanitized warning like:

`⚠️ The model provider failed after retries. I kept raw provider details out of chat; check gateway logs for diagnostics.`

## Fast diagnosis

1. Inspect the live gateway service logs, not just chat output:
   - `journalctl --user -u hermes-gateway.service --since '15 minutes ago' --no-pager -o cat`
   - or `~/.hermes/logs/gateway.log` if systemd logs are insufficient.
2. Look for the exact tuple in provider failure lines:
   - `provider=...`
   - `base_url=...`
   - `model=...`
   - HTTP status / timeout summary.
3. Inspect config provider and fallback sections:
   - `model`
   - `fallback_providers`
   - `fallback_chain`
   - `fallback_model`
4. If a fallback is nonsensical or explicitly unwanted, remove the fallback entry instead of trying to make it work.

## Broken combo observed

A failure path showed:

- primary: `provider=openai-codex`, `base_url=https://chatgpt.com/backend-api/codex`, `model=gpt-5.5`
- primary failure: non-streaming Codex request stale for 300s / timeout
- fallback attempted: `provider=azure-foundry`, `model=gpt-5.5`
- broken request tuple in logs: `provider=azure-foundry base_url=https://chatgpt.com/backend-api/codex`
- result: HTTP 404 `{'detail': 'Not Found'}`

That tuple is invalid. Azure Foundry must not be sent to the ChatGPT Codex backend URL. If the user's intent is “delete it,” remove the Azure fallback from config immediately.

## Safe removal workflow

Use a YAML-preserving script or targeted edit to remove Azure fallback entries from `~/.hermes/config.yaml`:

- remove `fallback_providers` entries where `provider: azure-foundry`
- remove `fallback_chain` entries where `provider: azure-foundry`
- remove `fallback_model` if it is an Azure Foundry dict
- preserve the primary `model` block unless the user asks to change it
- write a timestamped or descriptive backup before saving

Example verification after removal:

```bash
python3 - <<'PY'
import yaml, pathlib
p = pathlib.Path('/home/hermes/.hermes/config.yaml')
c = yaml.safe_load(p.read_text()) or {}
print('model:', c.get('model'))
for k in ['fallback_providers', 'fallback_chain', 'fallback_model']:
    print(k, '=', c.get(k, '<absent>'))
print('azure-foundry-in-config:', 'azure-foundry' in p.read_text())
PY
```

Expected result when deleted:

- fallback keys absent or no Azure entries remain
- `azure-foundry-in-config: False`

## Restart and verify

After editing config, restart the gateway so the running process cannot keep stale fallback state:

```bash
systemctl --user restart hermes-gateway.service
sleep 5
systemctl --user status hermes-gateway.service --no-pager -l | head -60
journalctl --user -u hermes-gateway.service --since '1 minute ago' --no-pager -o cat | tail -120
```

If the user is angry and asks to delete a fallback, prioritize the destructive-but-scoped config removal and verification over extended explanation. Report only: removed entry, backup path, active current provider/model, gateway restart status, and any unrelated residual warnings.

## Pitfalls

- Do not assume the sanitized chat warning is a Telegram/platform failure. It often means the LLM provider failed inside the gateway session.
- Do not keep retrying a fallback tuple that combines one provider with another provider's base URL.
- Do not edit bundled `hermes-agent` skill for this operational pattern; store the runtime playbook in this umbrella skill.
- Do not remove the primary provider/model unless the user explicitly asks. In the observed case, only the Azure fallback was unwanted; `openai-codex/gpt-5.5` remained the intended primary.
