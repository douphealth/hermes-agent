# XML-RPC Content Editing for gearuptofit.com

## When to Use
When REST API content sanitizer strips `<style>` tags, `@media` queries, or custom HTML from post content. XML-RPC preserves ALL HTML.

## Authentication
- **Username:** `admin`  
- **Password:** Use the WP-ADMIN password from credentials file (NOT the application password)  
- Application passwords DO NOT work with XML-RPC (returns "Incorrect username or password")

## Quick Reference

### Read Post Content
```xml
<?xml version="1.0"?>
<methodCall>
  <methodName>metaWeblog.getPost</methodName>
  <params>
    <param><value><string>POST_ID</string></value></param>
    <param><value><string>admin</string></value></param>
    <param><value><string>ADMIN_PASSWORD</string></value></param>
  </params>
</methodCall>
```
Send: `curl -s -H "Host: gearuptofit.com" -H "Content-Type: text/xml" -d @file.xml "http://104.168.100.41/xmlrpc.php"`

### Edit Post Content (Preserves ALL HTML)
```xml
<?xml version="1.0"?>
<methodCall>
  <methodName>metaWeblog.editPost</methodName>
  <params>
    <param><value><string>POST_ID</string></value></param>
    <param><value><string>admin</string></value></param>
    <param><value><string>ADMIN_PASSWORD</string></value></param>
    <param><value><struct>
      <member>
        <name>description</name>
        <value><string><![CDATA[FULL_HTML_CONTENT]]></string></value>
      </member>
    </struct></value></param>
    <param><value><boolean>1</boolean></value></param>
  </params>
</methodCall>
```

## Known Working Methods
| Method | Works? | Notes |
|--------|--------|-------|
| `metaWeblog.getPost` | ✅ | Returns full post content in `<description>` field |
| `metaWeblog.editPost` | ✅ | Preserves `<style>`, `@media`, `<script>` |
| `metaWeblog.newPost` | ✅ | Creates new posts |
| `wp.getPosts` | ✅ | Post type `post` only |
| `wp.getOptions` | ✅ | Core options only |
| `wp.setOptions` | ✅ | Core options only |

## NOT Working Methods
| Method | Error | Notes |
|--------|-------|-------|
| `wp.getPosts` (elementor_css) | "Invalid post type" | Can't read Elementor CPTs |
| Application passwords | "Incorrect username or password" | App passwords not supported by XML-RPC |

## CSS Injection Pattern
When injecting responsive CSS into a post:

1. Place the `<style>` block at the TOP of `entry-content` (right before the article content)
2. Include ALL CSS inside a single `<style>` block
3. Include `@media` queries for mobile breakpoints (768px, 480px)
4. Use CDATA wrapping for the full HTML content
5. Verify with `metaWeblog.getPost` that the content was saved correctly

## Troubleshooting
- **Empty response or `parse error`:** Check XML is well-formed. Use CDATA for content with special chars.
- **Not well formed:** Ensure password doesn't contain `&`, `<`, `>` without CDATA/escaping
- **Post content empty after edit:** Check the `lastEdited` response — if `<boolean>1</boolean>`, the edit succeeded
- **Style tags stripped:** Only happens via REST API (Gutenberg sanitizer). XML-RPC preserves them.
