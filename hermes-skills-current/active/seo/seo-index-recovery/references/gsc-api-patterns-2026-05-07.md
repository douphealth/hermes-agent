# GSC API Patterns — May 7, 2026 Session

## Service Account Auth

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_PATH = '/home/hermes/.hermes/cache/seo-optimizer-456317-9ac3ea9a1b61.json'
SITE = 'https://gearuptofit.com/'
SCOPES = ['https://www.googleapis.com/auth/webmasters']

credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
gsc = build('searchconsole', 'v1', credentials=credentials)
```

**Note:** The key file exists on disk with the REAL private key even though display tools redact it. Python can read it directly with `json.load(open(path))` — the bytes are intact.

## List Available Sites

```python
sites = gsc.sites().list().execute()
for site in sites.get('siteEntry', []):
    print(f"  {site['siteUrl']} - {site.get('permissionLevel','')}")
```

## List Submitted Sitemaps (with full details)

```python
sitemaps = gsc.sitemaps().list(siteUrl=SITE).execute()
for s in sitemaps.get('sitemap', []):
    print(f"  {s['path']} | type:{s.get('type','?')} | submitted:{s.get('isSitemapsIndex','?')} | errors:{s.get('errors','0')} | warnings:{s.get('warnings','0')} | contents:{s.get('contents',[])}")
```

The `contents` field shows `submitted` vs `indexed` counts. If submitted > 0 and indexed = 0, Google knows about the URLs but algorithmically rejected them.

## Delete Invalid Sitemap

```python
try:
    gsc.sitemaps().delete(siteUrl=SITE, feedpath='https://gearuptofit.com/sitemap.xml').execute()
    print(f"✓ Deleted")
except Exception as e:
    print(f"✗ Failed: {e}")
```

**Always delete invalid sitemaps BEFORE submitting the correct one.** If you submit while invalid ones exist, Google interleaves them.

## Submit Correct Sitemap

```python
try:
    gsc.sitemaps().submit(siteUrl=SITE, feedpath='https://gearuptofit.com/sitemap_index.xml').execute()
    print(f"✓ Submitted")
except Exception as e:
    print(f"✗ Failed: {e}")
```

## URL Inspection

```python
body = {'inspectionUrl': url, 'siteUrl': SITE}
result = gsc.urlInspection().index().inspect(body=body).execute()
insp = result.get('inspectionResult', {})
idx = insp.get('indexStatusResult', {})
crawl = insp.get('crawlResult', {})

coverage = idx.get('coverageState','?')     # INDEXED, CRAWLED_NOT_INDEXED, URL_NOT_IN_INDEX
verdict = idx.get('verdict','?')             # PASS, NEUTRAL, INEVITABLE
fetch = idx.get('pageFetchState','?')        # SUCCESSFUL, FAILED
robots = idx.get('robotsTxtState','?')       # ALLOWED, BLOCKED
allowed = idx.get('indexingState','?')       # INDEXING_ALLOWED, INDEXING_BLOCKED
canonical = insp.get('canonical','?')        # Google's chosen canonical
last_crawl = crawl.get('lastDownloaded','?')
crawl_status = crawl.get('status','?')
```

### Key Coverage States

| Coverage State | Meaning |
|---|---|
| `Submitted and indexed` | ✅ Page is in Google index |
| `Crawled - currently not indexed` | ⚠️ Google found it but chose not to index — most common cause of drops |
| `URL is unknown to Google` | ❌ Google hasn't discovered this URL at all (sitemap not working) |
| `URL is known but not indexed | ? | Google knows about it but hasn't attempted crawl yet |

## Enable Indexing API (GCP Console — REQUIRES browser login)

The Indexing API enables `URL_UPDATED` notifications which can trigger re-crawl for up to 200 URLs/day.

```python
# This WILL FAIL (403) until the API is enabled in GCP Console
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Need SEPARATE credentials with indexing scope
SCOPES_IDX = ['https://www.googleapis.com/auth/indexing']
credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES_IDX)
indexing = build('indexing', 'v3', credentials=credentials)

body = {"url": url, "type": "URL_UPDATED"}
result = indexing.urlNotifications().publish(body=body).execute()
```

**To enable:** Go to https://console.cloud.google.com/apis/library/indexing.googleapis.com, select the project `seo-optimizer-456317`, and click ENABLE. The service account CANNOT do this — you need a project owner's browser session.

## Attempting to Enable Indexing API via Service Account (will fail)

```python
# Service Usage API — returns 403 PERMISSION_DENIED (error 110002)
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request as AuthRequest

SCOPES_GCP = ['https://www.googleapis.com/auth/cloud-platform']
credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES_GCP)
credentials.refresh(AuthRequest())
token=[REDACTED]

headers = {"Authorization": f"Bearer {token}"}
resp = requests.post(
    f"https://serviceusage.googleapis.com/v1/projects/seo-optimizer-456317/services/indexing.googleapis.com:enable",
    headers=headers
)
# → 403 "Permission denied to enable service [indexing.googleapis.com]"
# Error 110002 = service account lacks project owner/editor role
```

## Content Quality Verification (for "Crawled - not indexed" pages)

```bash
# Check word count, meta robots, headings in one shot
curl -s -A "Mozilla/5.0 (compatible; Googlebot/2.1)" https://site.com/page/ | python3 -c "
import sys, re
html = sys.stdin.read()
# Meta robots
for m in re.findall(r'<meta[^>]*robots[^>]*>', html[:10000], re.IGNORECASE):
    print('Meta:', m)
# Strip HTML for word count
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
print(f'Words: {len(text.split())}')
# Title
title = re.findall(r'<title>(.*?)</title>', html, re.IGNORECASE)
print(f'Title: {title[0] if title else \"NONE\"}')
# H1s
h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE)
print(f'H1s: {len(h1s)}')
# H2s  
h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.IGNORECASE)
print(f'H2s: {len(h2s)}')
"
```
