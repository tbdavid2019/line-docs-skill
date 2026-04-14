# LINE Developers Skill

Knowledge and specialized workflows for building on the [LINE Platform](https://developers.line.biz/en/). This skill provides deep access to the LINE Messaging API, LIFF, LINE Login, and related developer tools.

## Mandatory: Always consult [references/INDEX.md](references/INDEX.md) first to locate specific documentation for any LINE task.

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
4.  Consult [references/messaging-api/webhooks.md](references/messaging-api/webhooks.md) for signature validation requirements.

### 2. LIFF App Setup
When creating a LIFF application:
1.  Read [references/liff/overview.md](references/liff/overview.md).
2.  Ensure the LIFF ID is correctly configured for the target environment (Compact, Tall, Full).
3.  Check `liff.init()` error codes if the app fails to load.

### 3. Rich Menu Management
To create or update a rich menu:
1.  Retrieve existing menus via the API.
2.  Validate the image dimensions (see [references/messaging-api/rich-menus.md](references/messaging-api/rich-menus.md)).
3.  Link the rich menu ID to the specific user or set it as default.

## Reference Entry Points

| Reference | Coverage |
|---|---|
| [INDEX.md](references/INDEX.md) | **Comprehensive directory of ALL LINE documentation** |
| [messaging-api/](references/messaging-api/) | Messaging API (Bots, Webhooks, Push/Reply) |
| [liff/](references/liff/) | LINE Front-end Framework (LIFF) |
| [line-login/](references/line-login/) | OAuth and Social Login |
| [line-pay/](references/line-pay/) | Payments and Transactions |
| [social-api/](references/social-api/) | User profiles and social graph |
| [faq/](references/faq/) | Common issues and community solutions |

## Troubleshooting Ladder
- **HTTP 401**: Check Channel Access Token (Is it expired? Is it a Long-lived token?).
- **HTTP 403**: Check if the feature is enabled in the Channel settings.
- **HTTP 400**: Validate the JSON payload against the official schema.
- **Signature Validation Failure**: Ensure you are using the correct Channel Secret (not the Access Token).
