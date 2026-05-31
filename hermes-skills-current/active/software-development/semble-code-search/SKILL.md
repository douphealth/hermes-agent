---
name: semble-code-search
description: Use Semble for ultra-low-token semantic/lexical code search across local WordPress/plugin/theme/snippet/automation repos. Load when investigating codebases, WordPress technical SEO code, schema/canonical/redirect logic, REST scripts, plugins, themes, snippets, or when user requests token-efficient code inspection.
version: 1.0.0
metadata:
  hermes:
    tags: [semble, code-search, mcp, wordpress, seo, token-efficiency]
    related_skills: [graphify-superpowers, wp-rest-cloudflare, authority-engine, native-mcp]
---

# Semble Code Search

Semble is installed locally for fast, CPU-only code retrieval with hybrid semantic + BM25 search. It is a code retrieval accelerator, not an SEO crawler or content optimizer.

## Local installation

- CLI: `/home/hermes/.local/bin/semble`
- MCP server config: `~/.hermes/config.yaml` under `mcp_servers.semble`
- MCP tools become available after Hermes/gateway restart as `mcp_semble_search` and `mcp_semble_find_related`.

## Use first for code questions

Before using broad `search_files` + `read_file` across large codebases, run Semble:

```bash
/home/hermes/.local/bin/semble search "schema Article JSON-LD" /path/to/repo -k 5
/home/hermes/.local/bin/semble search "canonical URL output" /path/to/wp-content -k 5
/home/hermes/.local/bin/semble search "redirect old slug to new slug" /path/to/repo -k 5
/home/hermes/.local/bin/semble search "newsletter REST endpoint" /path/to/repo -k 5
/home/hermes/.local/bin/semble find-related path/from/result.php 42 /path/to/repo -k 5
```

For remote public repos:

```bash
/home/hermes/.local/bin/semble search "rank math schema filters" https://github.com/vendor/repo -k 5
```

## WordPress / SEO query patterns

Use Semble for:

- custom theme/plugin code
- Code Snippets exports
- `mu-plugins`
- REST automation scripts
- schema generators
- canonical/noindex logic
- redirect maps
- internal-link automation
- cache purge hooks
- sitemap/robots handlers
- newsletter/form endpoints
- Cloudflare/LiteSpeed integration code

High-signal queries:

```bash
semble search "wp_head canonical noindex robots meta" ./wp-content
semble search "Article schema JSON-LD author dateModified" ./wp-content
semble search "redirect_canonical template_redirect 301" ./wp-content
semble search "Rank Math schema filter" ./wp-content
semble search "Yoast wpseo_schema_graph" ./wp-content
semble search "REST route register_rest_route subscribe" ./wp-content
semble search "LiteSpeed purge post save_post" ./wp-content
```

## MCP usage

Hermes config contains:

```yaml
mcp_servers:
  semble:
    command: /home/hermes/.local/bin/semble
    args: []
    timeout: 180
    connect_timeout: 120
    sampling:
      enabled: false
```

Restart Hermes/gateway before expecting MCP tools to appear in the active tool list. Current sessions may not hot-load new MCP tools.

## Workflow

1. Identify repo/path to inspect.
2. Run Semble search with a natural-language or symbol query.
3. Use returned exact file paths + line numbers.
4. Read only the relevant snippets/files with `read_file`.
5. Patch surgically.
6. Verify with tests, public crawl, REST checks, or targeted command.

## Pitfalls

- Do not install Semble on production WordPress servers; keep it on Hermes/local side.
- Semble indexes code, not live WordPress database content unless exported to files.
- For tiny codebases, normal file search may be faster.
- For secrets, avoid printing full files; Semble should point to locations, then inspect minimal snippets.
- MCP config changes require restart; CLI works immediately.
- First run may download the small code embedding model from Hugging Face. If a transient `RemoteProtocolError`/disconnect occurs during model download, rerun once; the retry succeeded during installation verification.
