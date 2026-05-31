# CSS Injection Priority Chain for Elementor WordPress Sites

When you need CSS but theme files aren't writable and REST API has limitations:

## Quick Decision Tree

```
Can edit theme style.css?
  ├─ YES → Edit directly (child theme only!)
  └─ NO (file_not_writable) →
      ├─ Is WPCode installed? → Create CSS snippet (DB-backed, no file perms)
      ├─ Is Elementor Pro? → Try per-page custom CSS via _elementor_page_settings meta
      ├─ Has hosting panel? → Use panel file manager (HestiaCP:8090, cPanel:2083)
      └─ None of the above → Upload CSS to wp-content/uploads + WPCode PHP enqueue
```

## Critical Nuances

### Theme File Editor Reports Success on Failure
The Theme File Editor always returns HTTP 200, even when the file save fails. The `file_not_writable` error is hidden in a Mustache/JS template string (`<# } else if ( 'file_not_writable' === data.code ) { #>`) — invisible to curl/browser users.

**Always verify the save** by re-reading the file content from the textarea after submission.

### Post Content `<style>` is Stripped
When updating `wp/v2/posts/{ID}` via REST, WordPress applies `wp_kses_post()` which strips `<style>` tags. CSS rules appear as visible plain text on the frontend.

### `custom_css` Not in REST Settings
The `PUT /wp/v2/settings` endpoint does NOT expose `custom_css`. The field is silently ignored.

### Elementor Snippet Conditions are Brittle
Creating CSS via `elementor_snippet` and setting `_elementor_location: elementor_head` does NOT guarantee the CSS appears. Conditions must be set through the native Elementor admin UI — REST meta updates are frequently silently discarded.

## Recommended Path: WPCode CSS Snippet

```bash
# Navigate to: /wp-admin/admin.php?page=wpcode-snippet-manager
# Snippet type: CSS
# Code: paste your CSS
# Insert Method: Auto Insert (site-wide)
# Status: Active
```

WPCode stores in DB — no file permissions needed. Use browser-based edit only (see wpcode-safe-editing.md for why REST edits corrupt encoding).
