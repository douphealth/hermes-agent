# Cloudflare Page Rules for WordPress Performance

## Zone-Level Settings

```bash
ZONE_ID="your_zone_id"
CF_TOKEN=[REDACTED]

# Check current settings
curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings" \
  -H "Authorization=[REDACTED] $CF_TOKEN" | jq '.result | .[] | select(.id | IN("minify","brotli","cache_level","polish","always_online","development_mode","ssl","image_resizing","rocket_loader","mirage")) | {id, value}'

# Enable Polish (lossless image optimization)
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/polish" \
  -H "Authorization=[REDACTED] $CF_TOKEN" -d '{"value":"lossless"}'
```

## Page Rules (3 Rules Minimum)

### Priority 1: wp-admin Bypass
Prevents Cloudflare from caching admin pages.

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules" \
  -H "Authorization=[REDACTED] $CF_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "targets": [{"target": "url", "constraint": {"operator": "matches", "value": "*site.com/wp-admin*"}}],
    "actions": [{"id": "cache_level", "value": "bypass"}, {"id": "disable_apps", "value": true}],
    "priority": 1, "status": "active"
  }'
```

### Priority 2: Cache Everything (24h TTL)
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules" \
  -d '{
    "targets": [{"target": "url", "constraint": {"operator": "matches", "value": "*site.com/*"}}],
    "actions": [{"id": "cache_level", "value": "cache_everything"}, {"id": "edge_cache_ttl", "value": 86400}],
    "priority": 2, "status": "active"
  }'
```

### Priority 3: Static Assets Minify + 1yr Cache
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules" \
  -d '{
    "targets": [{"target": "url", "constraint": {"operator": "matches", "value": "*site.com/wp-content/*"}}],
    "actions": [
      {"id": "minify", "value": {"css": "on", "html": "on", "js": "on"}},
      {"id": "browser_cache_ttl", "value": 31536000}
    ],
    "priority": 3, "status": "active"
  }'
```

## Verification

```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules?status=active" \
  -H "Authorization=[REDACTED] $CF_TOKEN" | jq '.result[] | {priority, target: .targets[0].constraint.value, actions: [.actions[] | {id, value}]}'
```
