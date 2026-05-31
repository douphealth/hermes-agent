# Lovable cookie export dedupe / identity check

When a user uploads multiple Cookie-Editor JSON exports for Lovable, first prove whether they are genuinely different authenticated Lovable sessions.

## Safe checks

Do not print or persist raw cookie/token values. It is safe to log/report:

- JWT payload `email`, `name`, `sub` / `user_id`.
- `iat` / `exp` timestamps if useful.
- A short SHA-256 prefix of the token for equality checks.
- Counts and ID-set comparisons for workspaces/projects.

## Python snippet

```python
import json, base64, hashlib
from pathlib import Path

def lovable_session_identity(cookie_json_path):
    cookies = json.loads(Path(cookie_json_path).read_text())
    tok = next(c['value'] for c in cookies if c['name'] == 'lovable-session-id-v2')
    payload = tok.split('.')[1]
    payload += '=' * ((4 - len(payload) % 4) % 4)
    claims = json.loads(base64.urlsafe_b64decode(payload))
    return {
        'token_sha_prefix': hashlib.sha256(tok.encode()).hexdigest()[:16],
        'email': claims.get('email'),
        'name': claims.get('name'),
        'sub': claims.get('sub'),
        'user_id': claims.get('user_id'),
        'iat': claims.get('iat'),
        'exp': claims.get('exp'),
    }
```

## Decision rule

- Same `email` + same `sub/user_id` + same token SHA prefix: exact same session. Do not merge as new data.
- Same identity but different token SHA: same account, refreshed session. Compare workspace/project ID sets; merge only if access changed.
- Different identity: fetch inventory and merge with source-session provenance.

## User-facing wording

If duplicate:

> I processed it. It is still logged in as `<email>` and exposes the same N workspaces / M projects as the previous export. No new data was added. To get the other account, switch Lovable/Google accounts in the browser first, then export cookies again.
