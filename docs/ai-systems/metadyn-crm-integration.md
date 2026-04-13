# MetaDyn CRM Integration

## Purpose

This document describes Jen's local integration with `https://crm.metadyn.xyz`, which is currently a Twenty CRM instance.

The integration is designed to give Jen and future MetaDyn agents a reliable, auditable, scriptable way to work with CRM data without embedding raw secrets in docs or chat flows.

## Current State

Jen now has a working local CRM toolkit backed by the Twenty GraphQL API.

Current implementation files:

- `tools/metadyn_crm.py` — primary CLI for CRM operations
- `tools/metadyn_crm_list_companies.py` — compatibility wrapper for simple company listing

Secrets are intentionally kept out of version control.
The CRM API token is stored locally outside the repo in:

- `/home/jza/.openclaw/.secrets/metadyn-crm-api-key`

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

- The integration currently talks directly to Twenty's GraphQL API.
- The helper prefers narrow, task-oriented commands instead of exposing arbitrary raw GraphQL by default.
- Write-paths for company creation, company update, person creation, person update, note creation, task creation, and note/task attachment have been exercised against the live CRM.
- Temporary validation records used during testing were cleaned up after verification.

## Known Limitations

- This is not yet a full long-running MCP server process.
- The current interface is local CLI + JSON operation wrapper.
- Task listing/update is not yet implemented.
- Note update/delete is not exposed through the helper yet.
- Opportunity/deal workflows are not yet exposed.
- Assignee-aware task workflows are not yet implemented.

## Recommended Next Steps

1. Add task listing and task update support.
2. Add note update/delete support.
3. Add company/person search by richer multi-field criteria.
4. Add opportunity/deal operations once MetaDyn defines its pipeline usage.
5. Wrap the `rpc` operation contract in a real MCP server so Jen and subordinate agents can call it as a first-class tool.
6. Add audit-oriented logging around write actions if this becomes a multi-agent shared integration.

## Security Rules

- Never commit API keys, bearer tokens, or raw CRM credentials.
- Never dump broad customer datasets into docs or memory files.
- Prefer targeted queries over large exports.
- Treat CRM writes as production actions.
- For bulk or potentially destructive updates, require explicit human confirmation.
