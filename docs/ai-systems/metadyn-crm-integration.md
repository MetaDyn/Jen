# MetaDyn CRM + Calendly Integration

## Purpose

This document describes MetaDyn's operational CRM and scheduling bridge:

- Twenty CRM at `https://crm.metadyn.xyz`
- Calendly direct API access plus CRM sync flows

The goal is a reliable, auditable operator surface for reading and updating CRM context, then turning scheduled meetings into usable follow-up context instead of scattered chat residue.

## Current Implementation

Primary files:

- `tools/metadyn_crm.py` — main Twenty CRM CLI
- `tools/metadyn_crm_mcp.py` — lightweight stdio MCP-style bridge for the CRM CLI
- `tools/metadyn_crm_list_companies.py` — compatibility wrapper for simple company listing
- `tools/metadyn_calendly.py` — Calendly direct API integration plus CRM bridge flows

Local secrets live outside the repo:

- `/home/jza/.openclaw/.secrets/metadyn-crm-api-key`
- `/home/jza/.openclaw/.secrets/calendly-api-key`

## Design Goals

- keep Twenty as the CRM source of truth
- expose a narrow, practical command surface instead of vague raw API access
- support both direct operator use and future tool wrapping
- keep additive workflows easy and destructive workflows explicit
- avoid committing credentials or broad customer data dumps into the workspace

## What This Tooling Is Good At

### CRM

- companies
- people
- internal team/workspace-member lookup
- notes
- tasks
- opportunities
- structured JSON/RPC-style operations

### Calendly

- account/profile confirmation
- event type listing
- scheduled event listing
- contact listing/creation
- webhook subscription listing/creation
- syncing meetings into CRM people/companies/notes/tasks
- pushing a CRM person into Calendly contacts for continuity

## Command Surface Reference

Run from the workspace root:

```bash
./tools/metadyn_crm.py <command> [...args]
./tools/metadyn_calendly.py <command> [...args]
```

---

## CRM CLI Reference

### Commands

| Command | Purpose |
|---|---|
| `list-companies` | List companies |
| `search-companies` | Search companies by term |
| `get-company` | Get one company by id or name |
| `create-company` | Create company |
| `update-company` | Update company |
| `list-people` | List people, optionally scoped to a company |
| `list-team` | List/search internal Twenty workspace members |
| `create-person` | Create person |
| `update-person` | Update person |
| `list-notes` | List notes linked to a company or person |
| `create-note` | Create note |
| `update-note` | Update note |
| `delete-note` | Delete note |
| `list-tasks` | List tasks, optionally scoped to company/person/opportunity/status |
| `create-task` | Create task |
| `update-task` | Update task |
| `list-opportunities` | List opportunities |
| `create-opportunity` | Create opportunity |
| `update-opportunity` | Update opportunity |
| `rpc` | Structured JSON operation wrapper |

### Companies

#### List companies

```bash
./tools/metadyn_crm.py list-companies --limit 10 --offset 0
```

#### Search companies

```bash
./tools/metadyn_crm.py search-companies Netflix --limit 10
```

#### Get company details

```bash
./tools/metadyn_crm.py get-company --id <company-id>
./tools/metadyn_crm.py get-company --name Netflix
```

#### Create company

```bash
./tools/metadyn_crm.py create-company \
  --name "Acme Studios" \
  --domain-label acmestudios.com \
  --domain-url https://acmestudios.com \
  --linkedin-label "Acme Studios" \
  --linkedin-url https://linkedin.com/company/acme-studios \
  --employees 45 \
  --icp
```

#### Update company

```bash
./tools/metadyn_crm.py update-company \
  --id <company-id> \
  --name "Acme Studios, Inc." \
  --employees 60
```

Supported company fields in create/update flows:

- `--name`
- `--domain-label`
- `--domain-url`
- `--linkedin-label`
- `--linkedin-url`
- `--x-label`
- `--x-url`
- `--employees`
- `--icp`

### People

#### List people

```bash
./tools/metadyn_crm.py list-people
./tools/metadyn_crm.py list-people --company-id <company-id>
```

#### Create person

```bash
./tools/metadyn_crm.py create-person \
  --first-name Jane \
  --last-name Doe \
  --email jane@acmestudios.com \
  --job-title "Partnerships Director" \
  --city "Los Angeles" \
  --company-id <company-id>
```

#### Update person

```bash
./tools/metadyn_crm.py update-person \
  --id <person-id> \
  --job-title "VP of Partnerships" \
  --city "Los Angeles"
```

Supported person fields in create/update flows:

- `--first-name`
- `--last-name`
- `--email`
- `--job-title`
- `--city`
- `--company-id`
- `--linkedin-label`
- `--linkedin-url`
- `--x-label`
- `--x-url`
- `--avatar-url`

### Internal Team / Workspace Members

This is the important distinction inside Twenty:

- **People** = external contacts
- **Team / workspace members** = internal MetaDyn staff

Use `list-team` when you need an internal owner/assignee surface.

```bash
./tools/metadyn_crm.py list-team
./tools/metadyn_crm.py list-team --term Chris --limit 10
```

This is the correct lookup path before assigning opportunity owners with `--owner-id`.

### Notes

#### Create note

```bash
./tools/metadyn_crm.py create-note \
  --title "Discovery call" \
  --body "Great initial conversation. Interested in immersive brand activations." \
  --company-id <company-id>
```

#### List notes

```bash
./tools/metadyn_crm.py list-notes --company-id <company-id>
./tools/metadyn_crm.py list-notes --person-id <person-id>
```

#### Update note

```bash
./tools/metadyn_crm.py update-note \
  --id <note-id> \
  --title "Discovery call - updated" \
  --body "Added recap and next steps."
```

#### Delete note

```bash
./tools/metadyn_crm.py delete-note --id <note-id>
```

### Tasks

#### List tasks

```bash
./tools/metadyn_crm.py list-tasks --status TODO --limit 20
./tools/metadyn_crm.py list-tasks --company-id <company-id>
./tools/metadyn_crm.py list-tasks --person-id <person-id>
./tools/metadyn_crm.py list-tasks --opportunity-id <opportunity-id>
```

Valid task statuses:

- `TODO`
- `IN_PROGRESS`
- `DONE`

#### Create task

```bash
./tools/metadyn_crm.py create-task \
  --title "Follow up on partnership intro" \
  --body "Send recap and next steps." \
  --due-at 2026-04-20T17:00:00Z \
  --status TODO \
  --company-id <company-id>
```

A task can also be attached to a person or opportunity.

#### Update task

```bash
./tools/metadyn_crm.py update-task \
  --id <task-id> \
  --status IN_PROGRESS \
  --assignee-id <workspace-member-id>
```

Supported task update fields:

- `--title`
- `--body`
- `--due-at`
- `--status`
- `--assignee-id`

### Opportunities

#### List opportunities

```bash
./tools/metadyn_crm.py list-opportunities --limit 25
./tools/metadyn_crm.py list-opportunities --term Nelson
./tools/metadyn_crm.py list-opportunities --company-id <company-id>
./tools/metadyn_crm.py list-opportunities --person-id <person-id>
./tools/metadyn_crm.py list-opportunities --stage MEETING
```

Valid opportunity stages:

- `NEW`
- `SCREENING`
- `MEETING`
- `PROPOSAL`
- `CUSTOMER`

#### Create opportunity

```bash
./tools/metadyn_crm.py create-opportunity \
  --name "Acme Spatial Pilot" \
  --stage SCREENING \
  --amount 25000 \
  --currency USD \
  --company-id <company-id> \
  --owner-id <workspace-member-id>
```

#### Update opportunity

```bash
./tools/metadyn_crm.py update-opportunity \
  --id <opportunity-id> \
  --stage MEETING \
  --amount 40000 \
  --owner-id <workspace-member-id>
```

Supported opportunity fields:

- `--name`
- `--close-date`
- `--stage`
- `--amount`
- `--currency`
- `--company-id`
- `--person-id`
- `--owner-id`

---

## Calendly CLI Reference

### Commands

| Command | Purpose |
|---|---|
| `whoami` | Confirm the active Calendly account/token |
| `list-event-types` | List event types |
| `list-contacts` | List contacts |
| `create-contact` | Create a Calendly contact |
| `list-scheduled-events` | List scheduled events |
| `list-webhook-subscriptions` | List webhook subscriptions |
| `create-webhook-subscription` | Create webhook subscription |
| `sync-event-to-crm` | Pull a scheduled event into CRM |
| `sync-webhook-to-crm` | Turn a Calendly webhook payload into CRM context |
| `push-crm-person-to-contact` | Seed a CRM person into Calendly contacts |

### Confirm token / account

```bash
./tools/metadyn_calendly.py whoami
```

### List event types

```bash
./tools/metadyn_calendly.py list-event-types --scope user --limit 10
./tools/metadyn_calendly.py list-event-types --scope organization --limit 10 --json
```

### List scheduled events

```bash
./tools/metadyn_calendly.py list-scheduled-events --upcoming --limit 10
./tools/metadyn_calendly.py list-scheduled-events --invitee-email jane@acmestudios.com
./tools/metadyn_calendly.py list-scheduled-events --status canceled --json
```

Useful filters:

- `--scope user|organization`
- `--status active|canceled`
- `--min-start-time <iso>`
- `--max-start-time <iso>`
- `--invitee-email <email>`
- `--sort <field:dir>`
- `--upcoming`
- `--json`

### List contacts

```bash
./tools/metadyn_calendly.py list-contacts --limit 25
./tools/metadyn_calendly.py list-contacts --json
```

### Create a contact

```bash
./tools/metadyn_calendly.py create-contact \
  --first-name Jane \
  --last-name Doe \
  --email jane@acmestudios.com \
  --phone +18165551234 \
  --job-title "Partnerships Director" \
  --company "Acme Studios" \
  --linkedin https://linkedin.com/in/janedoe \
  --time-zone America/Chicago \
  --city Kansas_City \
  --state Missouri \
  --country US
```

Supported contact fields:

- `--first-name`
- `--last-name`
- `--email`
- `--phone`
- `--job-title`
- `--company`
- `--linkedin`
- `--time-zone`
- `--city`
- `--state`
- `--country`

### Push an existing CRM person into Calendly contacts

```bash
./tools/metadyn_calendly.py push-crm-person-to-contact --person-id <person-id>
```

This is the clean reverse-continuity path when an important CRM contact should also exist in Calendly.

### List webhook subscriptions

```bash
./tools/metadyn_calendly.py list-webhook-subscriptions --limit 10
./tools/metadyn_calendly.py list-webhook-subscriptions --organization <org-uri> --json
```

### Create webhook subscription

Use this once a controlled receiver endpoint exists.

```bash
./tools/metadyn_calendly.py create-webhook-subscription \
  --callback-url https://example.metadyn.xyz/hooks/calendly \
  --event invitee.created \
  --event invitee.canceled
```

Optional fields:

- `--organization <org-uri>`
- `--user <user-uri>`
- `--signing-key <secret>`

### Sync a scheduled event into CRM

This pulls the scheduled event and invitees from Calendly, then:

- finds or creates the CRM person by invitee email
- finds or creates the CRM company from the email domain when it looks like a real company domain
- creates a CRM note with meeting context
- optionally creates a follow-up/prep task

```bash
./tools/metadyn_calendly.py sync-event-to-crm \
  --event-uri https://api.calendly.com/scheduled_events/<event-uuid> \
  --create-task
```

### Sync a webhook payload into CRM

This is the best current automation path.

From file:

```bash
./tools/metadyn_calendly.py sync-webhook-to-crm --file /path/to/calendly-webhook.json --create-task
```

Or via stdin:

```bash
cat /path/to/calendly-webhook.json | ./tools/metadyn_calendly.py sync-webhook-to-crm --create-task
```

Optional fallback fetch support:

```bash
./tools/metadyn_calendly.py sync-webhook-to-crm \
  --file /path/to/calendly-webhook.json \
  --event-uri https://api.calendly.com/scheduled_events/<event-uuid> \
  --create-task
```

---

## RPC / MCP-Style Operation Layer

The CRM CLI includes a structured JSON wrapper through `rpc`.

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

Current operation families include:

- `company.*`
- `person.*`
- `note.*`
- `task.*`
- `opportunity.*`

This is not a full long-running MCP server, but it is a clean structured contract that can be wrapped by one.

---

## Practical Operator Patterns

### 1) Use Calendly as the scheduling front door

- let meetings enter through Calendly
- sync the result into CRM notes/tasks
- work the follow-up from CRM

### 2) Use team lookup before assigning owners

When assigning an opportunity or task owner, use `list-team` first so you are using the internal workspace-member surface, not an external Person record.

### 3) Keep CRM notes pointed at the next move

A good note should usually capture:

- current status
- who owns next action
- next checkpoint
- funding/contact logic if relevant

### 4) Prefer additive writes

The bridge is strongest when it is adding:

- context
- notes
- tasks
- ownership clarity

That fits the intended workflow better than heavy structural mutation.

---

## Known Limitations

- not a full always-on MCP server yet
- no dedicated always-on webhook receiver in this workspace yet
- Calendly webhook automation still assumes an upstream workflow/endpoint hands payloads into the CLI
- Calendly meeting sync does not yet auto-link notes/tasks to an existing opportunity
- Calendly sync does not yet do assignee-aware task routing
- destructive CRM actions are intentionally not the easy/default path

## Recommended Next Steps

1. Add a small receiver endpoint that validates Calendly webhook signatures and forwards payloads into `sync-webhook-to-crm`.
2. Add opportunity matching so meeting activity can attach to the correct live opportunity when the match is clear.
3. Add assignee-aware task routing for Chris/Josh/internal owners.
4. Add audit-oriented logging around write actions if this becomes a heavier shared integration.
5. Optionally expose the CRM operation layer as a first-class registered tool surface.
6. Add approval-aware wrappers for destructive flows.

## Approval Rules

Potentially destructive or materially risky CRM actions should get approval from Josh Garrett before execution.

Primary approval contact:

- Josh Garrett — Discord user ID `709916025101090886`

Examples that should require approval:

- deleting a company
- deleting a person
- bulk deletes or bulk updates
- major merges
- destructive ownership/pipeline changes
- any action that could materially alter prospect/customer history or remove important CRM data

Practical rule:

- normal reads and ordinary additive writes are fine
- destructive or major risky writes should pause for approval

## Security Rules

- Never commit API keys, bearer tokens, or raw CRM credentials.
- Never dump broad customer datasets into docs or memory files.
- Prefer targeted queries over large exports.
- Treat CRM writes as production actions.
- For bulk or destructive updates, require explicit human confirmation.
