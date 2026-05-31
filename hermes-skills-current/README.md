# Hermes Skills Current Snapshot

Portable disaster-recovery snapshot of the local Hermes runtime skill library.

## Restore on a fresh PC

```bash
git clone https://github.com/douphealth/hermes-agent ~/.hermes/hermes-agent
mkdir -p ~/.hermes/skills
rsync -a ~/.hermes/hermes-agent/hermes-skills-current/active/ ~/.hermes/skills/
# Optional archived skills:
# rsync -a ~/.hermes/hermes-agent/hermes-skills-current/archive/ ~/.hermes/skills/.archive/
hermes skills list
```

## Snapshot metadata

- Generated at: `2026-05-31T10:32:22.910032+00:00`
- Active skills: `132`
- Archived skills: `38`
- Files copied: `942`
- Secret redactions: `1188`

## Active skills

- `active/apple/apple-notes` — Manage Apple Notes via memo CLI: create, search, edit.
- `active/apple/apple-reminders` — Apple Reminders via remindctl: add, list, complete.
- `active/apple/findmy` — Track Apple devices/AirTags via FindMy.app on macOS.
- `active/apple/imessage` — Send and receive iMessages/SMS via the imsg CLI on macOS.
- `active/apple/macos-computer-use` — |
- `active/autonomous-ai-agents/claude-code` — Delegate coding to Claude Code CLI (features, PRs).
- `active/autonomous-ai-agents/codex` — Delegate coding to OpenAI Codex CLI (features, PRs).
- `active/autonomous-ai-agents/hermes-agent` — Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and a concise contributor reference. Load this skill when helping users configure Hermes, troubleshoot issues, spawn agent instances, or make code contributions.
- `active/autonomous-ai-agents/kanban-codex-lane` — Use when a Hermes Kanban worker wants to run Codex CLI as an isolated implementation lane while Hermes keeps ownership of task lifecycle, reconciliation, testing, and handoff.
- `active/autonomous-ai-agents/opencode` — Delegate coding to OpenCode CLI (features, PR review).
- `active/creative/architecture-diagram` — Dark-themed SVG architecture/cloud/infra diagrams as HTML.
- `active/creative/ascii-art` — ASCII art: pyfiglet, cowsay, boxes, image-to-ascii.
- `active/creative/ascii-video` — ASCII video: convert video/audio to colored ASCII MP4/GIF.
- `active/creative/baoyu-article-illustrator` — Article illustrations: type × style × palette consistency.
- `active/creative/baoyu-comic` — Knowledge comics (知识漫画): educational, biography, tutorial.
- `active/creative/baoyu-infographic` — Infographics: 21 layouts x 21 styles (信息图, 可视化).
- `active/creative/claude-design` — Design one-off HTML artifacts (landing, deck, prototype).
- `active/creative/comfyui` — Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli for lifecycle and direct REST/WebSocket API for execution.
- `active/creative/creative-ideation` — Generate project ideas via creative constraints.
- `active/creative/design-md` — Author/validate/export Google's DESIGN.md token spec files.
- `active/creative/excalidraw` — Hand-drawn Excalidraw JSON diagrams (arch, flow, seq).
- `active/creative/humanizer` — Humanize text: strip AI-isms and add real voice.
- `active/creative/manim-video` — Manim CE animations: 3Blue1Brown math/algo videos.
- `active/creative/motion-impeccable-taste-design` — Use when upgrading any website, WordPress post, landing page, app UI, or Claude/Hermes-generated frontend to avoid generic AI design. Applies a three-pass system: motion/easing polish, impeccable spacing/typography/layout correction, and taste/reference-driven art direction.
- `active/creative/open-design-superpowers` — Use when the user asks for SOTA design superpowers, Claude Design-like artifacts, landing pages, dashboards, decks, mobile/app prototypes, brand systems, visual redesign, critique, or design-system-driven UI. Routes Hermes through nexu-io/open-design's skills, DESIGN.md systems, craft rules, templates, frames, and anti-AI-slop critique before producing artifacts.
- `active/creative/p5js` — p5.js sketches: gen art, shaders, interactive, 3D.
- `active/creative/pixel-art` — Pixel art w/ era palettes (NES, Game Boy, PICO-8).
- `active/creative/popular-web-designs` — 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS.
- `active/creative/pretext` — Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry games, kinetic typography, and text-powered generative art. Produces single-file HTML demos by default.
- `active/creative/sketch` — Throwaway HTML mockups: 2-3 design variants to compare.
- `active/creative/songwriting-and-ai-music` — Songwriting craft and Suno AI music prompts.
- `active/creative/touchdesigner-mcp` — Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools.
- `active/data-science/jupyter-live-kernel` — Iterative Python via live Jupyter kernel (hamelnb).
- `active/devops/authority-engine` — Unified enterprise SEO execution system for planning, writing, rewriting, clustering, and upgrading content to maximize #1 rankings, topical authority, Featured Snippets, AI Overviews, answer-engine extraction, AI visibility, and conversions. Includes non-plugin AI discovery endpoint patterns in references/ai-discovery-worker-geo-aeo-pattern.md.
- `active/devops/codex-seo-superpowers` — Hermes integration layer for Codex-first SEO/GEO/AEO/AI-visibility superpowers using AgriciDaniel/codex-seo, GEO Optimizer, WordPress llms.txt/plugin patterns, and AI visibility monitoring.
- `active/devops/hermes-runtime-operations` — Use when recovering, provisioning, or troubleshooting Hermes Agent runtime integrations: Telegram gateways, multiple bot homes, split HERMES_HOME processes, WSL browser automation, Playwright/Node dependencies, and BotFather/Telegram Web fallback checks.
- `active/devops/hermes-seo-geo-aeo-supercharger` — Hermes operating mode for WordPress SEO/GEO/AEO Supercharger runs: URL-only intake, evidence-first audits, surgical drafts, Yoast-compatible WordPress draft edits, AI visibility, topical authority, internal links, schema, alt text, trust, and conversion improvements.
- `active/devops/kanban-orchestrator` — Decomposition playbook + anti-temptation rules for an orchestrator profile routing work through Kanban. The "don't do the work yourself" rule and the basic lifecycle are auto-injected into every kanban worker's system prompt; this skill is the deeper playbook when you're specifically playing the orchestrator role.
- `active/devops/kanban-worker` — Pitfalls, examples, and edge cases for Hermes Kanban workers. The lifecycle itself is auto-injected into every worker's system prompt as KANBAN_GUIDANCE (from agent/prompt_builder.py); this skill is what you load when you want deeper detail on specific scenarios.
- `active/devops/redesign` — Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality. Works with any CSS framework or vanilla CSS.
- `active/devops/saas-portfolio-inventory` — Build authenticated enterprise portfolio inventories across GitHub, Cloudflare, Lovable, Supabase, and similar SaaS dashboards; merge data into management workbooks without storing secrets.
- `active/devops/seo-superpowers-public-toolkits` — SOTA SEO/GEO/AEO execution layer distilled from public SEO skills/toolkits: GEO citations, technical audits, SERP crossover, content decay, topical maps, keyword gaps, entity extraction, internal linking.
- `active/devops/webhook-subscriptions` — Webhook subscriptions: event-driven agent runs.
- `active/devops/wordpress-backup-operations` — Use when auditing, repairing, configuring, or verifying WordPress backup systems across MainWP, WPvivid, Google Drive/remote storage, child-site connectivity, schedules, logs, and fleet-wide backup execution.
- `active/devops/wordpress-email-marketing-operations` — Use when auditing, repairing, replacing, or hard-cutting WordPress email marketing systems across FluentCRM, FluentSMTP, FluentForms, MailPoet, Brevo, Kadence/ESP integrations, signup forms, automations, reply paths, and deliverability when wp-admin may be blocked by Cloudflare.
- `active/devops/wordpress-organic-growth-os` — Autonomous enterprise WordPress Organic Growth OS for Alexiios' portfolio. Use when operating managed WordPress sites for SEO/GEO/AEO, topical authority, AI visibility, monetization, conversion, technical QA, and self-improving token-efficient execution.
- `active/devops/wordpress-performance-optimization` — Surgical WordPress performance optimization — PhastPress tuning, Cloudflare caching rules, Elementor-compatible SOTA post meta injection, and speed diagnostics. Zero-breakage priority; never deactivate/overwrite plugins or functions.php handlers.
- `active/dogfood` — Exploratory QA of web apps: find bugs, evidence, reports.
- `active/email/himalaya` — Himalaya CLI: IMAP/SMTP email from terminal.
- `active/gaming/minecraft-modpack-server` — Host modded Minecraft servers (CurseForge, Modrinth).
- `active/gaming/pokemon-player` — Play Pokemon via headless emulator + RAM reads.
- `active/github/codebase-inspection` — Inspect codebases w/ pygount: LOC, languages, ratios.
- `active/github/github-auth` — GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login.
- `active/github/github-code-review` — Review PRs: diffs, inline comments via gh or REST.
- `active/github/github-issues` — Create, triage, label, assign GitHub issues via gh or REST.
- `active/github/github-pr-workflow` — GitHub PR lifecycle: branch, commit, open, CI, merge.
- `active/github/github-repo-management` — Clone, create, fork, configure, and manage GitHub repositories. Manage remotes, secrets, releases, and workflows. Works with gh CLI or falls back to git + GitHub REST API via curl.
- `active/graphify` — any input (code, docs, papers, images) → knowledge graph → clustered communities → HTML + JSON + audit report
- `active/leisure/find-nearby` — Find nearby places (restaurants, cafes, bars, pharmacies, etc.) using OpenStreetMap. Works with coordinates, addresses, cities, zip codes, or Telegram location pins. No API keys needed.
- `active/mcp/mcporter` — Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.
- `active/mcp/native-mcp` — MCP client: connect servers, register tools (stdio/HTTP).
- `active/media/gif-search` — Search/download GIFs from Tenor via curl + jq.
- `active/media/heartmula` — HeartMuLa: Suno-like song generation from lyrics + tags.
- `active/media/songsee` — Audio spectrograms/features (mel, chroma, MFCC) via CLI.
- `active/media/spotify` — Spotify: play, search, queue, manage playlists and devices.
- `active/media/youtube-content` — YouTube transcripts to summaries, threads, blogs.
- `active/mlops/cloud/modal` — Serverless GPU cloud platform for running ML workloads. Use when you need on-demand GPU access without infrastructure management, deploying ML models as APIs, or running batch jobs with automatic scaling.
- `active/mlops/evaluation/lm-evaluation-harness` — lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.).
- `active/mlops/evaluation/weights-and-biases` — W&B: log ML experiments, sweeps, model registry, dashboards.
- `active/mlops/huggingface-hub` — HuggingFace hf CLI: search/download/upload models, datasets.
- `active/mlops/inference/gguf` — GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing flexible quantization from 2-8 bit without GPU requirements.
- `active/mlops/inference/guidance` — Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with Guidance - Microsoft Research's constrained generation framework
- `active/mlops/inference/llama-cpp` — llama.cpp local GGUF inference + HF Hub model discovery.
- `active/mlops/inference/obliteratus` — OBLITERATUS: abliterate LLM refusals (diff-in-means).
- `active/mlops/inference/outlines` — Outlines: structured JSON/regex/Pydantic LLM generation.
- `active/mlops/inference/vllm` — vLLM: high-throughput LLM serving, OpenAI API, quantization.
- `active/mlops/llm-training-operations` — Use when planning or troubleshooting LLM training runs across parameter-efficient fine-tuning, GRPO/RL training, distributed PyTorch/FSDP, memory optimization, checkpoints, evaluation loops, and production training runbooks.
- `active/mlops/models/audiocraft` — AudioCraft: MusicGen text-to-music, AudioGen text-to-sound.
- `active/mlops/models/clip` — OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M image-text pairs. Use for image search, content moderation, or vision-language tasks without fine-tuning. Best for general-purpose image understanding.
- `active/mlops/models/segment-anything` — SAM: zero-shot image segmentation via points, boxes, masks.
- `active/mlops/models/stable-diffusion` — State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, performing image-to-image translation, inpainting, or building custom diffusion pipelines.
- `active/mlops/models/whisper` — OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model sizes from tiny (39M params) to large (1550M params). Use for speech-to-text, podcast transcription, or multilingual audio processing. Best for robust, multilingual ASR.
- `active/mlops/research/dspy` — DSPy: declarative LM programs, auto-optimize prompts, RAG.
- `active/mlops/training/axolotl` — Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO).
- `active/mlops/training/peft` — Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when you need to train <1% of parameters with minimal accuracy loss, or for multi-adapter serving. HuggingFace's official library integrated with transformers ecosystem.
- `active/mlops/training/trl-fine-tuning` — TRL: SFT, DPO, PPO, GRPO, reward modeling for LLM RLHF.
- `active/mlops/training/unsloth` — Unsloth: 2-5x faster LoRA/QLoRA fine-tuning, less VRAM.
- `active/note-taking/obsidian` — Read, search, create, and edit notes in the Obsidian vault.
- `active/productivity/airtable` — Airtable REST API via curl. Records CRUD, filters, upserts.
- `active/productivity/google-workspace` — Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python.
- `active/productivity/linear` — Linear: manage issues, projects, teams via GraphQL + curl.
- `active/productivity/maps` — Geocode, POIs, routes, timezones via OpenStreetMap/OSRM.
- `active/productivity/nano-pdf` — Edit PDF text/typos/titles via nano-pdf CLI (NL prompts).
- `active/productivity/notion` — Notion API + ntn CLI: pages, databases, markdown, Workers.
- `active/productivity/ocr-and-documents` — Extract text from PDFs/scans (pymupdf, marker-pdf).
- `active/productivity/powerpoint` — Create, read, edit .pptx decks, slides, notes, templates.
- `active/productivity/teams-meeting-pipeline` — Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions.
- `active/red-teaming/godmode` — Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN.
- `active/research/arxiv` — Search arXiv papers by keyword, author, category, or ID.
- `active/research/blogwatcher` — Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool.
- `active/research/llm-wiki` — Karpathy's LLM Wiki: build/query interlinked markdown KB.
- `active/research/polymarket` — Query Polymarket: markets, prices, orderbooks, history.
- `active/research/research-paper-writing` — Write ML papers for NeurIPS/ICML/ICLR: design→submit.
- `active/seo/gearuptofit-seo-crawl-triage` — Read-only GearUpToFit.com SEO/GEO/AEO crawl triage workflow before production edits. Captures public-surface audit commands, known URL classes, and recurring pitfalls for category/tool/template checks.
- `active/seo/seo-index-recovery` — Diagnose and recover from Google index drops: GSC API, sitemap audit, noindex checks, Indexing API, Cloudflare bypass
- `active/smart-home/openhue` — Control Philips Hue lights, scenes, rooms via OpenHue CLI.
- `active/social-media/feedhive-sota-social-posting` — Create and schedule SOTA social media posts for all 8 WP sites via FeedHive API
- `active/social-media/social-media-campaigns` — Plan, draft, approve, schedule, and verify social media campaigns across connected schedulers and social accounts.
- `active/social-media/xitter` — Interact with X/Twitter via the x-cli terminal client using official X API credentials. Use for posting, reading timelines, searching tweets, liking, retweeting, bookmarks, mentions, and user lookups.
- `active/social-media/xurl` — X/Twitter via xurl CLI: post, search, DM, media, v2 API.
- `active/software-development/auto-verification` — Verify work with concrete evidence before claiming done. Use for fixes, deployments, code changes, automations, and workflows that need proof, not optimism.
- `active/software-development/code-review` — Guidelines for performing thorough code reviews with security and quality focus
- `active/software-development/codewhale-powercharge` — CodeWhale-inspired Hermes operating mode for SOTA coding/repo work: Fin-style cheap coordination, strict subagent role postures, evidence-first child output, context/cache hygiene, and verification discipline.
- `active/software-development/debugging-hermes-tui-commands` — Debug Hermes TUI slash commands: Python, gateway, Ink UI.
- `active/software-development/graphify-superpowers` — Use the Graphify skills supergraph to route, combine, and query Hermes skills with far fewer tokens. Load when a task may require multiple skills, skill routing, SEO/WordPress workflows, Hermes troubleshooting, or when the user asks for maximum efficiency.
- `active/software-development/hermes-agent-skill-authoring` — Author in-repo SKILL.md: frontmatter, validator, structure.
- `active/software-development/hermes-agent-superpower-compatibility` — Implement SOTA agent-superpower compatibility in Hermes by adapting patterns from external agent frameworks such as OpenHands without bloating runtime or breaking prompt caching.
- `active/software-development/hermes-s6-container-supervision` — Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern.
- `active/software-development/node-inspect-debugger` — Debug Node.js via --inspect + Chrome DevTools Protocol CLI.
- `active/software-development/plan` — Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's `.hermes/plans/` directory, and do not execute the work.
- `active/software-development/python-debugpy` — Debug Python: pdb REPL + debugpy remote (DAP).
- `active/software-development/requesting-code-review` — Use when completing tasks, implementing major features, or before merging. Validates work meets requirements through systematic review process.
- `active/software-development/semble-code-search` — Use Semble for ultra-low-token semantic/lexical code search across local WordPress/plugin/theme/snippet/automation repos. Load when investigating codebases, WordPress technical SEO code, schema/canonical/redirect logic, REST scripts, plugins, themes, snippets, or when user requests token-efficient code inspection.
- `active/software-development/skill-router` — Use first when unsure which skill to load, when a task spans multiple skills, or when you want the smallest effective workflow with minimal token waste.
- `active/software-development/spike` — Throwaway experiments to validate an idea before build.
- `active/software-development/subagent-driven-development` — Use when executing implementation plans with independent tasks. Dispatches fresh delegate_task per task with two-stage review (spec compliance then code quality).
- `active/software-development/systematic-debugging` — 4-phase root cause debugging: understand bugs before fixing.
- `active/software-development/test-driven-development` — TDD: enforce RED-GREEN-REFACTOR, tests before code.
- `active/software-development/workspace-instruction-discovery` — Discover and digest repo-local instruction files before serious code or workspace work so execution follows local rules instead of generic defaults.
- `active/software-development/writing-plans` — Use when you have a spec or requirements for a multi-step task. Creates comprehensive implementation plans with bite-sized tasks, exact file paths, and complete code examples.
- `active/wp-rest-cloudflare` — Patterns for working with WordPress REST API when Cloudflare blocks wp-admin. Covers authentication, content updates with WAF bypass, XML-RPC fallback, Elementor CSS issues, and preventing WordPress auto-wrapping of HTML.
- `active/yuanbao` — Yuanbao (元宝) groups: @mention users, query info/members.

## Archived skills

- `archive/alexiios-seo-domination-system` — Use when Alexiios asks to boost organic traffic, SEO, GEO, AEO, AI visibility, SERP rankings, monetization, keyword/entity rankings, topical authority, competitor outranking, or sitewide growth across his WordPress websites. Operates as the revenue-first SEO/GEO/AEO master workflow.
- `archive/authority-engine-batch-optimizer` — Archive-scale SEO optimization system for auditing, scoring, prioritizing, and batching page upgrades across a WordPress site or content corpus. Designed for maximum ROI, topical authority growth, AEO/GEO gains, and efficient rollout.
- `archive/authority-engine-cluster-factory` — Cluster-building layer for the Authority Engine. Turns one topic or commercial territory into a structured pillar/cluster system with support-page plans, hub maps, internal-link blueprints, and rollout sequencing.
- `archive/authority-engine-command-center` — Master operator workflow for the Authority Engine. Routes intake to the right layer, defines decision trees, standardizes outputs, and manages handoffs across audit, SERP research, batch prioritization, and live execution.
- `archive/authority-engine-memory-and-kpi-loop` — Feedback-loop layer for the Authority Engine. Tracks KPI review cadence, refresh triggers, campaign memory, change logging patterns, and recurring optimization loops so SEO work compounds instead of resetting each cycle.
- `archive/authority-engine-serp-lab` — SERP research and modeling layer for the Authority Engine. Generates query sets, maps winning page types, detects snippet and AI Overview triggers, models competitor patterns, and turns findings into page briefs with information-gain angles.
- `archive/authority-engine-site-audit` — Diagnostic and control-layer SEO audit system for technical SEO, content quality, topical coverage, trust/E-E-A-T, schema, snippet/AIO opportunity, and internal-link architecture. Produces prioritized remediation plans for enterprise SEO execution.
- `archive/authority-engine-snippet-and-ai-overview-strike-system` — Extraction-optimization layer for the Authority Engine. Designs direct-answer blocks, snippet capture patterns, PAA coverage, and AI Overview-ready sections to maximize answer-engine visibility and Position 0 opportunities.
- `archive/authority-engine-trust-and-entity-graph` — Trust and entity-system layer for the Authority Engine. Builds consistent author/brand/entity architecture, strengthens editorial and methodology routing, and improves AI visibility through durable trust-page and entity-graph patterns.
- `archive/authority-engine-wordpress-execution` — Push-button WordPress REST execution layer for the Authority Engine. Publishes and upgrades pages/posts with enterprise-grade SEO, AEO, GEO, trust, internal links, and verification while working around Cloudflare and plugin-layer blockers.
- `archive/enterprise-ai-seo-competitor-mining` — Enterprise-grade SEO opportunity mining using SERP-overlap competitor discovery, AI-assisted brief generation, and revenue-first content clustering. Use to find hidden competitors, prioritize opportunities, and turn insights into pages, internal links, and conversion assets.
- `archive/faq-schema-and-answer-box-optimizer` — Improve WordPress pages for FAQ schema, answer-box extraction, and quick-answer usefulness without adding spammy or fake FAQ sections.
- `archive/fluentcrm-email-audit` — Audit and remediate FluentCRM email marketing setup on WordPress sites via REST API. Covers form repair, sequence audit, deliverability checks, and enterprise-grade configuration when admin UI is blocked by Cloudflare WAF.
- `archive/grpo-rl-training` — Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training
- `archive/hermes-multi-telegram-bot-provisioning` — Run additional Telegram bots concurrently in Hermes by giving each bot its own Hermes home, token, startup process, and DM pairing approval.
- `archive/hermes-telegram-gateway-recovery` — Recover Hermes Telegram bots when they stop responding due to duplicate gateway processes, split HERMES_HOME instances, or startup/import crashes. Covers main + secondary bot setups under /home/hermes/.hermes and /home/hermes/.hermes-alex.
- `archive/hermes-wsl-browser-runtime-recovery` — Recover Hermes browser automation in WSL when browser tools fail because Node, agent-browser dependencies, or Playwright browsers are missing. Includes Telegram-session fallback checks on Windows-side paths.
- `archive/mailpoet-subscribe-fix` — Fix broken MailPoet newsletter subscription forms on WordPress. Covers replacing crashing PHP handlers with REST API AJAX, troubleshooting MailPoet 5.x API crashes, finding correct API methods, and fixing silent email delivery failures caused by broken SMTP plugins.
- `archive/premium-wordpress-html-blocks` — Reusable premium HTML/CSS content blocks for WordPress pages and posts. Focuses on elegant, theme-safe visual modules that improve readability, conversions, and perceived quality without breaking layouts.
- `archive/pytorch-fsdp` — Expert guidance for Fully Sharded Data Parallel training with PyTorch FSDP - parameter sharding, mixed precision, CPU offloading, FSDP2
- `archive/serp-driven-rewrite-playbook` — Rewrite workflow driven by live SERP intent, page-type detection, hidden competitor overlap, and content-gap modeling. Designed for high-ROI SEO rewrites that feel human and rankable.
- `archive/taste-design` — Senior UI/UX Engineer for premium frontend. Configurable design dials (variance 8, motion 6, density 4). Enforces metric-based rules, hardware-accelerated CSS, anti-AI-slop patterns, and balanced design engineering. Works with any CSS framework including vanilla CSS on WordPress sites.
- `archive/wordpress-brevo-sequence-hardcut` — Hard-cut broken WordPress email signup/sequence systems onto direct Brevo delivery, disable legacy automations, and verify branded reply-paths end-to-end.
- `archive/wordpress-category-hub-architecture` — Build and upgrade WordPress category, tag, and hub-page architecture for stronger internal linking, clearer topical authority, and better crawl paths.
- `archive/wordpress-commercial-cluster-builder` — Builds and upgrades commercial SEO clusters on WordPress using parent/child topic architecture, money-page support posts, internal-link systems, trust routing, and conversion next steps.
- `archive/wordpress-eeat-remediation-via-rest` — Upgrade WordPress E-E-A-T / trust signals safely via REST API when Cloudflare blocks wp-admin. Covers author pages, editorial policy, disclosure, methodology, trust blocks, redirects, and careful cleanup of unsupported claims.
- `archive/wordpress-fluentcrm-brevo-cutover-hardcut` — Hard-cut a WordPress email signup flow from legacy FluentCRM/Brevo routes to a new branded delivery path when old welcome emails or reply-to headers keep leaking through.
- `archive/wordpress-fluentcrm-email-audit-fix` — Audit and fix FluentCRM email marketing infrastructure on WordPress sites — form handlers, sequences, cron, delivery, using REST API admin credentials.
- `archive/wordpress-image-alt-caption-snippet-optimizer` — Improve WordPress image alt text, captions, and snippet usefulness for SEO and accessibility without turning images into keyword-stuffed nonsense.
- `archive/wordpress-performance-quick-wins` — Speed up a WordPress site quickly using the strongest low-risk wins first: baseline with short timeouts, check caching, inspect plugins via REST API, activate LiteSpeed Cache if installed but inactive, then verify live improvement.
- `archive/wordpress-rest-commercial-seo-funnel` — Build a commercial SEO cluster and lead funnel on a WordPress site via REST when wp-admin is blocked by Cloudflare. Covers safe page/post creation, Spectra form embedding, thank-you/download flow, and internal-link reinforcement.
- `archive/wordpress-sota-seo-content-system` — SOTA enterprise-grade system for rewriting and upgrading WordPress content via REST with premium human-style copy, visual HTML modules, schema planning, SERP intent matching, duplicate consolidation, and strict verification.
- `archive/wordpress-trust-blocks-and-proof-elements` — Add compact trust blocks, proof elements, methodology notes, and evidence-oriented UI components to WordPress pages without bloating or fabricating authority.
- `archive/wp-email-audit` — Audit WordPress email marketing infrastructure using REST API when wp-admin is Cloudflare-blocked. Covers FluentCRM, FluentSMTP, FluentForms, Kadence ESP integrations, and form connectivity analysis.
- `archive/wp-enterprise-audit` — Comprehensive WordPress site audit and remote remediation using CLI tools and REST API. Covers SEO, security, performance, and indexing when browser tools are unavailable or admin access is restricted.
- `archive/wp-page-content-redesign` — Deploy custom HTML/CSS/JS pages via the WP REST API. Covers theme reset, Cloudflare workarounds, and WordPress auto-tag prevention
- `archive/wp-template-editing` — Edit WordPress block theme templates, template parts (header, footer), and global styles via the WP REST API when browser tools are unavailable.
- `archive/yoast-snippet-layer-remediation` — Diagnose and remediate split-brain WordPress metadata where body content updates succeed but Yoast or plugin-managed public title/meta output remains stale.
