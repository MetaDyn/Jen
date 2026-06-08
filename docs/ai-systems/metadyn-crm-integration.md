# MetaDyn CRM Integration

## Purpose

This document describes Jen's local integration with `https://crm.metadyn.xyz`, which is currently a Twenty CRM instance.

The integration is designed to give Jen and future MetaDyn agents a reliable, auditable, scriptable way to work with CRM data without embedding raw secrets in docs or chat flows.

## Current State

Jen now has a working local CRM toolkit backed by the Twenty GraphQL API.

Current implementation files:

- `tools/metadyn_crm.py` — primary CLI for CRM operations
- `tools/metadyn_crm_list_companies.py` — compatibility wrapper for simple company listing
- `tools/metadyn_calendly.py` — direct Calendly API integration plus CRM bridge flows

Secrets are intentionally kept out of version control.
The API tokens are stored locally outside the repo in:

- `/home/jza/.openclaw/.secrets/metadyn-crm-api-key`
- `/home/jza/.openclaw/.secrets/calendly-api-key`

## Design Goals

- keep the CRM API as the source of truth
- expose a small, practical operational surface for agents
- prefer explicit commands over vague API calls
- support both human CLI usage and future MCP-style tool wrapping
- avoid committing credentials or customer-sensitive dumps into the workspace

## Supported Capabilities

### Company operations

- list companies
- search companies by name/domain
- get one company by id or name filter
- create company
- update company

### Person operations

- list people
- list people scoped to a company
- create person
- update person

### Notes

- create a note
- attach a note to a company
- attach a note to a person
- list notes associated with a company
- list notes associated with a person

### Tasks

- create task
- optionally attach task to a company
- optionally attach task to a person

### Calendly integration layer

Calendly is wired as a direct API integration rather than an MCP auth surface.
That is deliberate: for MetaDyn's workflow automation, the enterprise-ready path is a stable direct API bridge that can:

- read Calendly user/profile state
- list event types
- list scheduled events
- list/create webhook subscriptions
- list/create Calendly contacts
- sync meeting activity into CRM people/companies/notes/tasks
- push CRM people into Calendly contacts when Josh wants contact continuity both ways

The current implementation uses a Calendly personal access token from:

- `/home/jza/.openclaw/.secrets/calendly-api-key`

### Higher-level operation layer

A lightweight MCP-style operation wrapper is included via the `rpc` command.
This allows callers to invoke structured operations such as:

- `company.list`
- `company.search`
- `company.get`
- `company.create`
- `company.update`
- `person.list`
- `person.create`
- `person.update`
- `note.list`
- `note.create`
- `task.create`

This is not a full MCP server yet, but it provides a clean operation contract that can be wrapped by one later with minimal translation.

## CLI Usage

Run from the workspace root:

```bash
./tools/metadyn_crm.py <command> [...args]
```

### List companies

```bash
./tools/metadyn_crm.py list-companies --limit 10
```

### Search companies

```bash
./tools/metadyn_crm.py search-companies Netflix
```

### Get company details

```bash
./tools/metadyn_crm.py get-company --id <company-id>
./tools/metadyn_crm.py get-company --name Netflix
```

### Create a company

```bash
./tools/metadyn_crm.py create-company \
  --name "Acme Studios" \
  --domain-label acmestudios.com \
  --domain-url https://acmestudios.com \
  --employees 45 \
  --icp
```

### Update a company

```bash
./tools/metadyn_crm.py update-company \
  --id <company-id> \
  --name "Acme Studios, Inc." \
  --employees 60
```

### List people

```bash
./tools/metadyn_crm.py list-people
./tools/metadyn_crm.py list-people --company-id <company-id>
```

### Create a person

```bash
./tools/metadyn_crm.py create-person \
  --first-name Jane \
  --last-name Doe \
  --email jane@acmestudios.com \
  --job-title "Partnerships Director" \
  --company-id <company-id>
```

### Update a person

```bash
./tools/metadyn_crm.py update-person \
  --id <person-id> \
  --job-title "VP of Partnerships" \
  --city "Los Angeles"
```

### Create a note

```bash
./tools/metadyn_crm.py create-note \
  --title "Discovery call" \
  --body "Great initial conversation. Interested in immersive brand activations." \
  --company-id <company-id>
```

### List notes for a company or person

```bash
./tools/metadyn_crm.py list-notes --company-id <company-id>
./tools/metadyn_crm.py list-notes --person-id <person-id>
```

### Create a task

```bash
./tools/metadyn_crm.py create-task \
  --title "Follow up on partnership intro" \
  --body "Send recap and next steps." \
  --due-at 2026-04-20T17:00:00Z \
  --status TODO \
  --company-id <company-id>
```

## Calendly CLI Usage

Run from the workspace root:

```bash
./tools/metadyn_calendly.py <command> [...args]
```

### Confirm the Calendly token / account

```bash
./tools/metadyn_calendly.py whoami
```

### List event types

```bash
./tools/metadyn_calendly.py list-event-types --limit 10
```

### List upcoming scheduled events

```bash
./tools/metadyn_calendly.py list-scheduled-events --upcoming --limit 10
```

### List Calendly contacts

```bash
./tools/metadyn_calendly.py list-contacts --limit 25
```

### Create a Calendly contact directly

```bash
./tools/metadyn_calendly.py create-contact \
  --first-name Jane \
  --last-name Doe \
  --email jane@acmestudios.com \
  --company "Acme Studios" \
  --job-title "Partnerships Director"
```

### Push an existing CRM person into Calendly contacts

```bash
./tools/metadyn_calendly.py push-crm-person-to-contact --person-id <person-id>
```

### List webhook subscriptions

```bash
./tools/metadyn_calendly.py list-webhook-subscriptions --limit 10
```

### Create a webhook subscription

Use this when you have a workflow endpoint ready to receive Calendly events.

```bash
./tools/metadyn_calendly.py create-webhook-subscription \
  --callback-url https://example.metadyn.xyz/hooks/calendly \
  --event invitee.created \
  --event invitee.canceled
```

### Sync a scheduled event into CRM

This pulls the scheduled event plus invitees from Calendly, then:

- finds or creates the CRM person by invitee email
- finds or creates the CRM company from the email domain when it looks like a company domain
- creates a CRM note with the meeting summary
- optionally creates a follow-up/prep task

```bash
./tools/metadyn_calendly.py sync-event-to-crm \
  --event-uri https://api.calendly.com/scheduled_events/<event-uuid> \
  --create-task
```

### Sync a webhook payload into CRM

This is the most practical automation path for production workflows.
Feed a saved webhook JSON payload to the bridge:

```bash
./tools/metadyn_calendly.py sync-webhook-to-crm --file /path/to/calendly-webhook.json --create-task
```

Or stream it via stdin from an automation layer:

```bash
cat /path/to/calendly-webhook.json | ./tools/metadyn_calendly.py sync-webhook-to-crm --create-task
```

## MCP-Style Operation Layer

The `rpc` mode accepts a JSON payload with `operation` and `params`.

Example:

```bash
./tools/metadyn_crm.py rpc --json '{
  "operation": "company.list",
  "params": {
    "limit": 5,
    "offset": 0
  }
}'
```

Another example:

```bash
./tools/metadyn_crm.py rpc --json '{
  "operation": "note.create",
  "params": {
    "title": "Met with prospect",
    "body": "Good strategic fit. Wants deck and timelines.",
    "company_id": "<company-id>"
  }
}'
```

## Operational Notes

- The CRM integration talks directly to Twenty's GraphQL API.
- The Calendly integration talks directly to Calendly's REST API using a PAT.
- The helper prefers narrow, task-oriented commands instead of exposing arbitrary raw GraphQL or arbitrary raw Calendly calls by default.
- The Calendly→CRM sync path is intentionally conservative and additive:
  - it does not delete CRM records
  - it only creates companies automatically when the invitee email domain looks like a real company domain
  - it ignores common free-mail domains for company auto-creation
- The clean operational pattern for MetaDyn is:
  1. create a Calendly webhook subscription to a controlled workflow endpoint
  2. let that workflow hand the payload to `sync-webhook-to-crm`
  3. create CRM notes/tasks automatically so Chris and Josh can act on the next step immediately
- The reverse continuity path is `push-crm-person-to-contact`, which lets an important CRM contact be seeded into Calendly's contacts surface.

## Known Limitations

- This is not yet a full long-running MCP server process.
- The current interface is local CLI + JSON operation wrapper on the CRM side, plus local direct REST calls on the Calendly side.
- The Calendly webhook command expects a payload shape compatible with Calendly scheduled-event webhooks and uses defensive fallback fetching when fields are missing.
- There is not yet a dedicated always-on webhook receiver in this workspace; the current bridge assumes an upstream workflow runner or endpoint will pass payloads into the CLI.
- CRM opportunity auto-linking from Calendly meetings is not yet implemented; notes/tasks currently attach to people/companies.
- Assignee-aware task workflows are not yet implemented in the Calendly sync path.

## Recommended MetaDyn Workflow Usage

1. Use Calendly as the scheduling front door.
2. Register webhook subscriptions for at least:
   - `invitee.created`
   - `invitee.canceled`
3. Point those webhooks at a controlled MetaDyn workflow endpoint.
4. Have that workflow call `sync-webhook-to-crm` so every meeting becomes CRM context automatically.
5. For high-value prospects already in CRM, use `push-crm-person-to-contact` so contact context exists in Calendly too.
6. Let Chris/Josh work from CRM notes/tasks instead of manually reconstructing meeting history.

## Recommended Next Steps

1. Add a small receiver/automation endpoint that validates Calendly webhook signatures and forwards payloads into this bridge.
2. Add opportunity matching logic so meetings can automatically attach to the right active opportunity when one clearly exists.
3. Add assignee-aware task workflows and task ownership tooling.
4. Add audit-oriented logging around write actions if this becomes a multi-agent shared integration.
5. Optionally wire the stdio bridge into OpenClaw/ACP-facing tool registration so CRM operations become first-class callable tools.
6. Add approval-aware wrappers for destructive operations so deletion requests can automatically route to Josh for confirmation.

## Approval Rules

For CRM actions that are potentially destructive or materially risky, Jen should seek approval from Josh Garrett before proceeding.

Primary approval contact:

- Josh Garrett — Discord user ID `709916025101090886`

Examples of actions that should require approval before execution:

- deleting a company
- deleting a person
- bulk deletes or bulk updates
- major record merges
- destructive pipeline or ownership changes
- any action that could materially alter customer/prospect history or remove important CRM data

Practical rule:

- low-risk reads and normal additive actions are fine without approval
- destructive or major write actions should pause, reach out to Josh for approval, and then proceed once approved

## Security Rules

- Never commit API keys, bearer tokens, or raw CRM credentials.
- Never dump broad customer datasets into docs or memory files.
- Prefer targeted queries over large exports.
- Treat CRM writes as production actions.
- For bulk or potentially destructive updates, require explicit human confirmation.
ctical rule:

- low-risk reads and normal additive actions are fine without approval
- destructive or major write actions should pause, reach out to Josh for approval, and then proceed once approved

## Security Rules

- Never commit API keys, bearer tokens, or raw CRM credentials.
- Never dump broad customer datasets into docs or memory files.
- Prefer targeted queries over large exports.
- Treat CRM writes as production actions.
- For bulk or potentially destructive updates, require explicit human confirmation.
