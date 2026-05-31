# Lovable project chat / upgrade automation pattern

Use when the user wants Hermes to operate Lovable projects, improve an existing Lovable app, or create new Lovable apps from a spec.

## What worked

Authenticated Cookie-Editor exports can be used not only for inventory but also for Lovable's project APIs. After extracting `lovable-session-id-v2` without printing it, authenticated requests use:

```http
Authorization=[REDACTED] <lovable-session-id-v2>
Origin: https://lovable.dev
Referer: https://lovable.dev/projects/<project_id>
Content-Type: application/json
```

Observed endpoint for sending a prompt into an existing project:

```http
POST https://api.lovable.dev/projects/{project_id}/chat
```

Body shape observed from Lovable frontend:

```json
{
  "id": "umsg_<unique-id>",
  "message": "<full Lovable prompt>",
  "thread_id": "main",
  "model": "auto",
  "current_viewport_width": 1440,
  "current_viewport_height": 1000,
  "current_viewport_dpr": 1
}
```

Observed endpoint for project creation from the frontend bundle:

```http
POST https://api.lovable.dev/workspaces/{workspace_id}/projects
```

Relevant body fields from the frontend include `description`, `tech_stack`, `visibility`, `project_type`, `initial_message`, `metadata`, and optional `source_repo_url`, `env_vars`, `deployment_target`, `supabase_project_config`, etc. Prefer creating/upgrading through the UI/API only after identifying the correct workspace/project from inventory.

## CAPTCHA blocker pattern

Lovable may return:

```json
{
  "type": "captcha_required",
  "message": "Additional verification is required. Please complete the captcha and try again."
}
```

This means access and endpoint discovery were valid, but generation needs human browser verification. Do **not** claim the prompt was submitted. Save the exact prompt as an artifact and give the user one concrete next step: open the Lovable project, paste the saved prompt, complete CAPTCHA, then send the result/screenshot so Hermes can QA and iterate.

## Best-practice flow for upgrade requests

1. Identify the correct target app from the Lovable inventory using project name, display name, published URL, workspace, and project ID.
2. Save a rich, reusable prompt artifact under the portfolio working directory before attempting submission.
3. Attempt `POST /projects/{project_id}/chat` only with redacted logging. Save response status/body to a local artifact.
4. If blocked by CAPTCHA, stop automation and give the user the exact project URL and saved prompt path/text.
5. After the user submits in Lovable, QA the published app URL and send follow-up Lovable prompts until the app is actually better.

## User-facing tone

For this user, be direct and evidence-first. Say exactly what was done, what is blocked, and the next action. Do not bury the CAPTCHA blocker under long explanations.
