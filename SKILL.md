---
name: line-docs-skill
description: Use when building on the LINE Platform or troubleshooting Messaging API, LIFF, LINE Login, channel access tokens, webhook verification, and LINE Mini App workflows.
---

# LINE Developers Skill

Use this skill for any LINE Platform task: Messaging API bots, LIFF apps, LINE Login, channel access tokens, webhook verification, rich menus, and LINE Mini App integration.

## Refresh Boundary

1. If the installed skill is a git checkout, try:
   ```bash
   git -C <skill-directory> pull origin main --ff-only
   ```
2. After pulling, load references from `references/`.
3. Do not run repo-maintenance scripts such as `scripts/sync-docs.sh` or `scripts/generate_index.py` during normal skill usage.
4. If refresh fails, continue with the local files and do not block the user.

## Required Entry Point

Always consult `references/INDEX.md` first to locate the correct documentation.

For setup or debugging questions, do not answer from one page alone. Read the task-specific guides and the related reference pages together.

## Core Lookup Map

| Task | Start Here |
| --- | --- |
| Find the right doc | `references/INDEX.md` |
| Messaging API overview | `references/docs/messaging-api/overview/index.html.md` |
| Messaging API getting started | `references/docs/messaging-api/getting-started/index.html.md` |
| Receiving webhooks | `references/docs/messaging-api/receiving-messages/index.html.md` |
| Verify webhook URL | `references/docs/messaging-api/verify-webhook-url/index.html.md` |
| Verify webhook signature | `references/docs/messaging-api/verify-webhook-signature/index.html.md` |
| Sending messages | `references/docs/messaging-api/sending-messages/index.html.md` |
| Rich menus | `references/docs/messaging-api/rich-menus-overview/index.html.md`, `references/docs/messaging-api/using-rich-menus/index.html.md` |
| Channel access tokens | `references/docs/basics/channel-access-token/index.html.md` |
| LIFF overview | `references/docs/liff/overview/index.html.md` |
| LIFF app setup | `references/docs/liff/getting-started/index.html.md`, `references/docs/liff/registering-liff-apps/index.html.md` |
| LIFF development | `references/docs/liff/developing-liff-apps/index.html.md` |
| LINE Login | `references/docs/line-login/getting-started/index.html.md`, `references/docs/line-login/integrate-line-login/index.html.md` |
| LINE Login security / PKCE | `references/docs/line-login/security-checklist/index.html.md`, `references/docs/line-login/integrate-pkce/index.html.md` |
| LINE Mini App | files under `references/docs/line-mini-app/` |
| Exact endpoint schema | `references/reference/messaging-api/index.html.md` and other `references/reference/` pages |

## Working Rules

1. Prefer local docs over memory for token types, flow steps, and API behavior.
2. Distinguish clearly between:
   - channel access token
   - channel secret
   - LIFF ID
   - LINE Login channel settings
3. When a question is about HTTP or webhook behavior, combine the guide page with the relevant reference page.
4. When the docs are browser-context-specific, state whether the behavior is for LIFF browser or external browser.
5. When troubleshooting, give the user a validation order.

## Workflow For LINE Tasks

Use this flow for questions like "build a LINE bot", "webhook doesn't fire", "LIFF init fails", "LINE Login callback error", or "how do I set up a LINE Mini App".

1. Identify the feature area first:
   - Messaging API
   - LIFF
   - LINE Login
   - LINE Mini App
2. Read `references/INDEX.md`.
3. Read the relevant overview or getting-started guide.
4. Read the exact reference page if the question involves an endpoint, payload, token, or parameter.
5. Answer in this order:
   - channel or app type required
   - required credentials or identifiers
   - platform-specific constraints
   - implementation or debugging steps
   - next verification step

## Mandatory Feature Branches

### Messaging API Branch

- Use `references/docs/messaging-api/overview/index.html.md`.
- For setup, also read `references/docs/messaging-api/getting-started/index.html.md`.
- For webhook issues, read:
  - `references/docs/messaging-api/receiving-messages/index.html.md`
  - `references/docs/messaging-api/verify-webhook-url/index.html.md`
  - `references/docs/messaging-api/verify-webhook-signature/index.html.md`
- For exact endpoint behavior, also read `references/reference/messaging-api/index.html.md`.

### LIFF Branch

- Use `references/docs/liff/overview/index.html.md`.
- For creating or registering the app, read `references/docs/liff/getting-started/index.html.md` and `references/docs/liff/registering-liff-apps/index.html.md`.
- If behavior differs by environment, state whether the app opens in LIFF browser or external browser.
- If `liff.init()` or device features fail, check environment constraints before suggesting code changes.

### LINE Login Branch

- Use `references/docs/line-login/getting-started/index.html.md`.
- For web login flow, also read `references/docs/line-login/integrate-line-login/index.html.md`.
- For secure flow details, use `references/docs/line-login/security-checklist/index.html.md` and `references/docs/line-login/integrate-pkce/index.html.md`.
- Always verify:
  - correct channel type
  - app type
  - callback URL
  - channel ID / channel secret usage

### LINE Mini App Branch

- Use `references/docs/line-mini-app/` via `references/INDEX.md`.
- Treat LINE Mini App questions as LIFF-based unless the docs for that feature say otherwise.
- Call out when the behavior depends on verification status, supported region, or in-app capabilities.

## Troubleshooting Order

When the user reports a broken setup, check these in order:

1. Wrong channel type or app type.
2. Wrong credential type:
   - channel access token for API calls
   - channel secret for webhook signature validation
3. Webhook URL, HTTPS, certificate, or callback URL mismatch.
4. LIFF ID, endpoint URL, or browser-context mismatch.
5. Payload or endpoint mismatch against the official reference.
6. Only then investigate SDK or application code.

## Fast Failure Hints

- HTTP `401`: verify the channel access token type, validity, and channel match.
- HTTP `403`: verify channel permissions or feature availability.
- HTTP `400`: verify request body, parameters, and endpoint contract against the reference.
- Webhook signature failure: use the channel secret, not the access token.
- LIFF behavior mismatch: check whether the app is in LIFF browser or an external browser.

## Minimum Questions To Ask When Context Is Missing

- Which LINE feature are you using?
- What channel type did you create?
- Are you debugging API calls, webhook delivery, LIFF behavior, or login redirect?
- What exact HTTP status or error text are you seeing?
- Are you testing in LIFF browser, LINE app, or an external browser?

## Output Style

1. Start with a short diagnosis.
2. Provide an ordered workflow.
3. Name the local docs used.
4. Explicitly call out token or environment distinctions.
5. End with the next concrete check in console, request log, or API call.
