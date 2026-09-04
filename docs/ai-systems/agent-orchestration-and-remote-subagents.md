# Agent Orchestration And Remote Subagents

**Status:** Planning / architecture draft
**Date:** 2026-04-07

## Purpose

This document defines the working architecture direction for Jen as MetaDyn's orchestration layer and for remote machines that expose API-backed specialist agents as subagents.

It consolidates details currently spread across:
- `docs/ai-systems/jen.md`
- `docs/architecture/overview.md`
- `docs/architecture/collaboration-model.md`
- `docs/infrastructure/topology.md`
- `OPENCLAW_OVERVIEW.md`
- long-term memory notes about subordinate agents and backend channels

## Current Known State

Jen is the main orchestrator for MetaDyn and currently runs through OpenClaw on GPT 6 Astra.

OpenClaw provides the local control plane around the model:
- long-lived gateway
- WebSocket API
- browser control UI
- channel integrations
- node/device pairing
- plugin loading
- local state and configuration management
- support for plugins that can add RPC methods, HTTP handlers, agent tools, CLI commands, background services, and skills

MetaDyn's planned subordinate agent set is:
- Metaverse CTO
- Marketing Strategist
- DevOps Specialist
- Unity Architect
- UX Architect
- Community Manager

Current memory notes indicate that the Metaverse CTO agent is already set up, while the remaining agents are planned.

## Target Mental Model

Jen should be treated as the central control-plane agent, not as one peer among many equal bots.

Remote subagents should be treated as bounded specialist services that Jen can delegate to when their domain, tools, or machine-local context makes them the correct executor.

The clean model is:
- Jen owns user interaction, task framing, policy, memory routing, and final synthesis.
- Subagents own narrow specialist execution within their approved domains.
- Remote machines expose an authenticated backend API to receive tasks and return structured results.
- OpenClaw remains the local gateway and orchestration shell around Jen.
- Remote subagent APIs should not become public chat surfaces unless explicitly approved.

## Control Plane Roles

### Jen

Responsibilities:
- understand Josh's request and project context
- choose whether delegation is needed
- select the appropriate subagent
- send a bounded task packet
- evaluate the returned result
- merge subagent output into the canonical answer or work product
- preserve relevant decisions in docs or memory
- enforce approval boundaries for external actions, destructive operations, production changes, and secrets

### OpenClaw Gateway

Responsibilities:
- host the local orchestration runtime
- expose the browser control surface
- manage channels, sessions, plugins, tools, and nodes
- provide the likely integration point for agent tools or plugin-backed calls into remote subagent APIs

OpenClaw plugin capabilities are relevant here because plugins can add RPC methods, HTTP handlers, agent tools, CLI commands, background services, and skills.

### Remote Subagent Host

Responsibilities:
- run a specialist agent process or service
- expose a small authenticated backend API
- keep machine-local secrets and operational access local to that host
- execute only tasks inside its delegated scope
- return structured results, evidence, logs, diffs, or artifacts
- reject tasks outside its declared capability or authorization boundary

## Remote Subagent API Shape

This is a proposed minimal contract. It should be implemented only after host inventory, security boundaries, and OpenClaw plugin integration are confirmed.

For the detailed API-layer specification, request/response examples, and reference server/client code, see:
- `remote-subagent-api-layer.md`

### Capability Discovery

Endpoint:

```text
GET /agent/v1/capabilities
```

Response shape:

```json
{
  "agent_id": "metadyn-unity-architect",
  "display_name": "Unity Architect",
  "version": "0.1.0",
  "domains": ["unity", "webgl", "sdk", "avatar-runtime"],
  "tools": ["repo_read", "repo_patch", "test_runner"],
  "approval_required_for": ["network", "deployment", "destructive_fs", "external_messages"],
  "max_task_seconds": 900
}
```

### Task Submission

Endpoint:

```text
POST /agent/v1/tasks
```

Request shape:

```json
{
  "task_id": "uuid-or-ulid",
  "requested_by": "jen",
  "conversation_ref": "opaque-session-ref",
  "priority": "normal",
  "domain": "unity",
  "objective": "Review the avatar upload implementation plan for Unity runtime risks.",
  "constraints": [
    "Do not modify production config.",
    "Do not create new services.",
    "Return file and line references for findings."
  ],
  "context_refs": [
    "docs/planning/metadyn-vrm-and-glb-upload-implementation-guide-2026-04-06.md"
  ],
  "artifacts": [],
  "approval_token": null
}
```

Response shape:

```json
{
  "task_id": "uuid-or-ulid",
  "status": "accepted",
  "result_url": "/agent/v1/tasks/uuid-or-ulid",
  "estimated_seconds": 120
}
```

### Task Result

Endpoint:

```text
GET /agent/v1/tasks/{task_id}
```

Response shape:

```json
{
  "task_id": "uuid-or-ulid",
  "status": "completed",
  "summary": "Found two Unity runtime risks and one missing verification step.",
  "findings": [
    {
      "severity": "high",
      "title": "Runtime importer dependency is not pinned in the implementation plan.",
      "evidence": "docs/planning/example.md:42",
      "recommendation": "Pin the package version before implementation."
    }
  ],
  "artifacts": [],
  "requires_human_approval": false,
  "next_actions": []
}
```

### Cancellation

Endpoint:

```text
POST /agent/v1/tasks/{task_id}/cancel
```

Purpose:
- stop long-running work
- prevent stale tasks from producing late writes
- let Jen cancel delegation when the user changes scope

## Security And Trust Boundaries

Remote subagents should default to least privilege.

Baseline requirements:
- TLS for all non-localhost transport
- service-to-service authentication
- per-agent scoped credentials
- no raw long-lived secrets in docs, prompts, task packets, or logs
- explicit allowlist of caller identity, expected source, and permitted methods
- task-level constraints included in every delegation request
- audit log on the remote host for received tasks, executed actions, and returned artifacts
- remote agent must reject tasks outside its declared domain

Approval-sensitive actions:
- production deployment
- destructive filesystem operations
- modifying live gateway/runtime/auth/network config
- sending external messages or posts
- rotating credentials
- changing DNS, SSL, Cloudflare, or ingress
- creating new services, daemons, public endpoints, routes, pages, or background workflows

## Delegation Rules

Jen should delegate when:
- the task maps cleanly to a specialist domain
- the remote host has local context or tools Jen does not have
- parallel specialist review would improve quality
- execution on a remote machine is required to inspect or test the target system

Jen should not delegate when:
- the task is simple enough to handle locally
- the user explicitly asked Jen not to involve other agents
- the subagent would need secrets or production access not already approved
- the task requires a structural change that was not explicitly requested
- the remote agent's authority or identity is ambiguous

## Subagent Registry Direction

Jen needs a small registry of approved subagents before runtime delegation is safe.

Suggested registry fields:
- agent ID
- display name
- owner / responsible human
- host label
- endpoint URL or connection profile
- authentication mechanism
- allowed domains
- denied domains
- available tools
- approval requirements
- logging location
- last verified date
- current status

This registry should avoid secrets. Store credentials in the appropriate secret manager or host-local config, not in the docs tree.

## OpenClaw Integration Direction

The clean integration path is likely an OpenClaw plugin or agent tool that wraps the remote subagent API.

The tool should:
- load the approved subagent registry
- expose a narrow `delegate_to_subagent` capability to Jen
- validate task domain against the registry before sending
- attach standard constraints and session references
- redact secrets and irrelevant private context
- poll or subscribe for task results
- return structured output to Jen for synthesis

Avoid building direct ad hoc HTTP calls from chat context unless there is a clear operational reason.

## Open Questions

- Which remote machines will host each specialist subagent?
- Is the Metaverse CTO agent already reachable by an API, CLI, OpenClaw node, or another mechanism?
- Should subagent communication use HTTP request/response first, WebSocket, queue-based jobs, or OpenClaw-native node/plugin transport?
- Where should the approved subagent registry live?
- What identity provider or service-token mechanism should secure machine-to-machine calls?
- Should remote subagents be allowed to patch files directly, or should they return proposed diffs for Jen to apply?
- What logs are safe to preserve for audit without leaking private user context?

## Immediate Next Steps

1. Inventory the existing Metaverse CTO agent and document how it is reached today.
2. Decide whether the first integration should be an OpenClaw plugin/tool or a simpler internal HTTP client.
3. Draft the subagent registry with no secrets.
4. Define one narrow pilot delegation flow, such as asking the Unity Architect to review a Unity plan and return findings only.
5. Only after that, implement the minimal API wrapper.
