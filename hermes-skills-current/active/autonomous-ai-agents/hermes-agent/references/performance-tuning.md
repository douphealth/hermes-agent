# Hermes Performance Tuning — Aggressive Efficiency Config

## Core Principle: Lock Model, Optimize Everything Else

When the user demands a **specific model only** (e.g. deepseek/deepseek-v4-flash for all tasks), do NOT change it. Zero cheap models, zero smart routing. All efficiency gains come from:

1. Squeezing token waste from every system setting
2. Reducing iterations and context bloat
3. Eliminating background/auxiliary overhead

## Config Settings for Max Efficiency (model-locked)

These settings stack. Apply them together for maximum effect.

### Token Waste Reduction

| Setting | Before | After | Why |
|---|---|---|---|
| `agent.max_turns` | 200 | 50 | Fewer wasted tool loops |
| `compression.threshold` | 0.65 | 0.50 | Compress sooner |
| `compression.target_ratio` | 0.15 | 0.10 | Compress harder |
| `compression.protect_last_n` | 8 | 4 | Fewer exempt messages |
| `display.personality` | "kawaii" | `''` | ~200 tokens/turn overhead |
| `display.compact` | false | true | Minimal display token overhead |
| `display.interim_assistant_messages` | true | false | No hidden assistant outputs |
| `display.inline_diffs` | true | false | Saves token overhead |
| `display.tool_progress` | "all" | "minimal" | Less verbose UI |
| `display.busy_input_mode` | "interrupt" | "cancel" | Less UI state |
| `display.resume_display` | "full" | "summary" | Shorter resume |
| `display.tui_status_indicator` | "kaomoji" | "none" | Saves prompt chars |
| `display.user_message_preview.first_lines` | 2 | 1 | Trims preview overhead |
| `display.show_cost` | false | false | Already minimal |
| `display.show_reasoning` | false | false | Already minimal |
| `session.auto_title` | true | false | Saves 1+ LLM calls per session |
| `memory.memory_char_limit` | 1600 | 800 | Half system prompt memory footprint |
| `memory.user_char_limit` | 1000 | 500 | Half user profile footprint |

### Background/Compute Elimination

| Setting | Before | After | Why |
|---|---|---|---|
| `checkpoints.enabled` | true | false | No snapshot writes every N turns |
| `checkpoints.max_snapshots` | 50 | 0 | Eliminates overhead entirely |
| `curator.enabled` | true | false | No weekly background compute |
| `auxiliary_overrides.title_generation.enabled` | true | false | No title gen calls per session |

### Storage & Logging

| Setting | Before | After | Why |
|---|---|---|---|
| `logging.level` | INFO | WARNING | Less disk I/O, fewer log writes |
| `sessions.auto_prune` | false | true | Auto-clean old sessions |
| `sessions.retention_days` | 90 | 14 | Aggressive cleanup |
| `model_catalog.enabled` | true | false | No model catalog fetches |

### Gateway Overhead

| Setting | Before | After | Why |
|---|---|---|---|
| `gateway_platforms.telegram.typing_indicator` | true | false | Saves per-message compute |
| `gateway_platforms.telegram.text_batch_delay` | 0.25 | 0.25 | Keep as-is |

### Context Length

Only reduce if acceptable to the user. The default 128K is overkill for most sessions.

| Setting | Before | After | When |
|---|---|---|---|
| `model.context_length` | 128000 | 64000 | For most sessions, 64K is fine. Reduces prompt processing cost ~50%. |

### Delegation (Subagent) Optimizations

| Setting | Before | After | Why |
|---|---|---|---|
| `delegation.max_iterations` | 50 | 20 | Fewer subagent turns |
| `delegation.child_timeout_seconds` | 600 | 300 | Faster timeout on stuck agents |

### Goals

| Setting | Before | After | Why |
|---|---|---|---|
| `goals.max_turns` | 20 | 10 | Tighter goal-completion budget |

## Smart Routing Alternative (when permitted)

If the user allows model switching for auxiliary/low-priority tasks:

```yaml
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
```

And set ALL auxiliary models to the cheap model (vision, web_extract, compression, session_search, skills_hub, approval, mcp, title_generation, curator).

**WARNING:** Some users are adamant about a single model. Never substitute the model unless explicitly asked or given a "make it cheaper" directive that doesn't specify model locking.

## Expected Impact

- **Token cost:** 75-95% reduction depending on model price delta
- **Response latency:** Faster per-turn because less context to process
- **Session capacity:** More sessions before hitting cost limits
