# Cost Optimization — Annotated Production Config

This file captures the exact configuration from a production optimization session. Use as a reference when the user demands aggressive cost reduction.

## Before/After Comparison

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Model cost/M tokens | ~$2-8 (deepseek/deepseek-v4-flash) | ~$0.27 (deepseek/deepseek-chat-v3) | ~87-93% |
| Smart routing tasks | n/a (disabled) | ~$0.075/M (gemini-2.0-flash-lite) | 95% on routing tasks |
| Auxiliary tasks | same as primary | ~$0.075/M each | ~95% each |
| Max LLM turns per session | 200 | 50 | 75% fewer |
| Personality overhead | ~200 tokens/turn | 0 (removed) | eliminated |
| Context window | 128K | 64K | 50% less context |
| Checkpoints | on (generates writes every N turns) | off | eliminated |
| Auto-title | on (1 LLM call/session) | off | eliminated |
| Curator background | on (weekly compute) | off | eliminated |
| Session retention | 90 days | 14 days (auto-prune) | 84% less storage |
| Mem limit | 1600 char | 800 char | 50% less overhead |
| Log verbosity | INFO | WARNING | less I/O |

## Full Config (YAML)

```yaml
model:
  default: deepseek/deepseek-chat-v3
  provider: openrouter
  base_url: https://openrouter.ai/api/v1
  context_length: 64000
  api_mode: chat_completions

smart_model_routing:
  enabled: true
  cheap_model: google/gemini-2.0-flash-lite-preview-02-05
  cheap_provider: openrouter
  min_tokens_for_cheap: 200
  max_tokens_for_cheap: 4096
  low_priority_tools:
    - web_search
    - web_extract
    - web_fetch
    - session_search
    - memory

agent:
  max_turns: 50

checkpoints:
  enabled: false

display:
  compact: true
  personality: ''
  interim_assistant_messages: false
  tool_progress: minimal
  inline_diffs: false

compression:
  threshold: 0.50
  target_ratio: 0.10
  protect_last_n: 4

auxiliary:
  vision:     { model: google/gemini-2.0-flash-lite-preview-02-05 }
  web_extract:{ model: google/gemini-2.0-flash-lite-preview-02-05 }
  compression:{ model: google/gemini-2.0-flash-lite-preview-02-05 }
  session_search:{ model: google/gemini-2.0-flash-lite-preview-02-05 }
  title_generation:{ model: google/gemini-2.0-flash-lite-preview-02-05 }
  approval:   { model: google/gemini-2.0-flash-lite-preview-02-05 }
  mcp:        { model: google/gemini-2.0-flash-lite-preview-02-05 }
  skills_hub: { model: google/gemini-2.0-flash-lite-preview-02-05 }
  curator:    { model: google/gemini-2.0-flash-lite-preview-02-05 }

delegation:
  model: google/gemini-2.0-flash-lite-preview-02-05
  max_iterations: 20
  child_timeout_seconds: 300

curator:
  enabled: false

memory:
  memory_char_limit: 800
  user_char_limit: 500

sessions:
  auto_prune: true
  retention_days: 14

logging:
  level: WARNING

model_catalog:
  enabled: false

gateway_platforms:
  telegram:
    typing_indicator: false

session:
  auto_title: false
```

## Update Hermes to Latest

```bash
cd ~/.hermes/hermes-agent
git stash           # save local changes
git pull            # fast-forward to latest
uv sync             # install any new deps
git stash pop       # restore local changes
```

## Restart Gateway

```bash
# Find and kill old gateway
pkill -f "gateway run"
sleep 3
# Start new gateway in background
cd ~/.hermes/hermes-agent && python -m hermes_cli.main gateway run --replace &
```

## Verification

```bash
# Check gateway is running
ps aux | grep "gateway run" | grep -v grep
# Check version
cd ~/.hermes/hermes-agent && git log --oneline -1
# Test config
hermes config check
```
