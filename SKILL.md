---
name: line-docs-skill
description: Use when building on the LINE Platform or troubleshooting LINE Developers features such as Messaging API, LIFF, LINE Login, and LINE Mini App workflows
---

# LINE Developers Skill

Knowledge and specialized workflows for building on the [LINE Platform](https://developers.line.biz/en/). This skill provides deep access to the LINE Messaging API, LIFF, LINE Login, and related developer tools.

## Mandatory: Always consult [references/INDEX.md](references/INDEX.md) first to locate specific documentation for any LINE task.

## Installation and Usage Boundary
> Use this boundary:
> 1. **Ensure docs are updated**: Every time you refer to this documentation, do a `git pull` from the documentation area to ensure you have the latest reference:
>    ```bash
>    git -C <skill-directory> pull origin main --ff-only
>    ```
> 2. **After pulling**, load any reference files from the `references/` folder.
> 3. **Do not run repo-maintenance scripts** such as `scripts/sync-docs.sh` or `scripts/generate_index.py` during normal skill usage (these are handled by GitHub Actions).
> 4. If refresh fails, continue with the local files and do not block the user.

## Target Audience
- Developers building LINE Bots (Messaging API)
- Frontend developers building LIFF apps
- System integrators using LINE Login or LINE Pay
- Bot operators managing rich menus and user sessions

## Core Knowledge Areas
- **Messaging API**: Webhooks, message types, rich menus, user ID management, beacons.
- **LIFF (LINE Front-end Framework)**: SDK initialization, OS-specific behavior, QR scanning, profile access.
- **LINE Login**: OAuth 2.0 flow, OpenID Connect, channel secrets.
- **LINE Pay**: Transaction flows, sandbox testing.
- **Social API**: Friend relationship checks, group/room management.

## Operational Workflows

### 1. Webhook Validation & Debugging
If webhooks are not being received or are failing:
1.  Check the "Channel settings" in the LINE Developers Console.
2.  Verify the SSL certificate (LINE requires valid, non-self-signed certificates).
3.  Use the "Verify" button in the console to test the endpoint.
4.  Consult the relevant documents under `references/docs/messaging-api/`, located via [references/INDEX.md](references/INDEX.md), for webhook verification and signature validation requirements.

### 2. LIFF App Setup
When creating a LIFF application:
1.  Read [references/docs/liff/overview/index.html.md](references/docs/liff/overview/index.html.md).
2.  Ensure the LIFF ID is correctly configured for the target environment (Compact, Tall, Full).
3.  Check `liff.init()` error codes if the app fails to load.

### 3. Rich Menu Management
To create or update a rich menu:
1.  Retrieve existing menus via the API.
2.  Validate the image dimensions using the Messaging API documents under `references/docs/messaging-api/`, such as the rich menu overview and related guides listed in [references/INDEX.md](references/INDEX.md).
3.  Link the rich menu ID to the specific user or set it as default.

## Reference Entry Points

| Reference | Coverage |
|---|---|
| [INDEX.md](references/INDEX.md) | **Comprehensive directory of ALL LINE documentation** |
| `references/docs/messaging-api/` | Messaging API guides (Bots, Webhooks, Push/Reply) |
| `references/reference/messaging-api/` | Messaging API reference pages |
| `references/docs/liff/` | LIFF guides |
| `references/reference/liff/` | LIFF reference pages |
| `references/docs/line-login/` | LINE Login guides |
| `references/reference/line-login/` | LINE Login reference pages |
| `references/docs/line-mini-app/` | LINE Mini App guides |
| `references/reference/line-mini-app/` | LINE Mini App reference pages |

## Troubleshooting Ladder
- **HTTP 401**: Check Channel Access Token (Is it expired? Is it a Long-lived token?).
- **HTTP 403**: Check if the feature is enabled in the Channel settings.
- **HTTP 400**: Validate the JSON payload against the official schema.
- **Signature Validation Failure**: Ensure you are using the correct Channel Secret (not the Access Token).
