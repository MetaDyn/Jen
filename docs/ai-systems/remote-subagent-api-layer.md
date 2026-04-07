# Remote Subagent API Layer

**Status:** Planning / implementation specification draft
**Date:** 2026-04-07
**Related:** `agent-orchestration-and-remote-subagents.md`

## Purpose

This document specifies the API layer for remote MetaDyn subagents that run on other machines and receive bounded delegated work from Jen.

The API layer is intentionally small:
- discover agent capabilities
- submit a task
- poll task status/result
- cancel a task
- expose health information

It should be implemented behind authenticated service-to-service access and should not be exposed as a public chat API.

## Design Goals

- Keep Jen as the central orchestrator and final synthesizer.
- Keep each remote subagent bounded to its approved domain.
- Make task packets explicit, auditable, and replay-resistant.
- Avoid sending raw secrets or unnecessary private context.
- Support both synchronous quick checks and asynchronous longer work.
- Allow future OpenClaw plugin/tool integration without tying the contract to one implementation language.

## Non-Goals

- This is not a public user-facing API.
- This is not a full agent marketplace.
- This is not a replacement for OpenClaw's gateway.
- This does not grant subagents authority to create services, deploy production changes, or perform destructive actions without explicit approval.
- This does not define the final secret-storage mechanism.

## Base URL

Each remote subagent host exposes a base URL from an approved registry.

Example:

```text
https://unity-architect.internal.metadyn.xyz
```

All API paths are versioned:

```text
/agent/v1/...
```

## Authentication

Recommended initial model:
- HTTPS for all non-localhost traffic
- static service token or short-lived bearer token for V1
- later migration to mTLS or signed service tokens if needed

Every request from Jen or the OpenClaw plugin wrapper should include:

```http
Authorization: Bearer <service-token>
X-MetaDyn-Caller: jen
X-MetaDyn-Request-Id: 01HVEXAMPLEULID000000000
```

Optional but recommended for replay protection:

```http
X-MetaDyn-Timestamp: 2026-04-07T00:00:00Z
X-MetaDyn-Signature: v1=<hmac-sha256-signature>
```

Do not put the service token or signing secret in this docs tree.

## Status Codes

Use normal HTTP status semantics:

- `200 OK`: request succeeded
- `202 Accepted`: task accepted for asynchronous processing
- `400 Bad Request`: schema or validation error
- `401 Unauthorized`: missing or invalid auth
- `403 Forbidden`: caller authenticated but not allowed for this operation/domain
- `404 Not Found`: task or endpoint does not exist
- `409 Conflict`: task already exists or cannot transition state
- `422 Unprocessable Entity`: request is well-formed but violates task constraints
- `429 Too Many Requests`: rate limit or concurrency limit hit
- `500 Internal Server Error`: unexpected agent host failure
- `503 Service Unavailable`: agent unavailable or draining

## Common Error Shape

```json
{
  "error": {
    "code": "domain_not_allowed",
    "message": "This agent does not accept tasks in the requested domain.",
    "request_id": "01HVEXAMPLEULID000000000",
    "retryable": false,
    "details": {
      "requested_domain": "cloudflare",
      "allowed_domains": ["unity", "webgl", "sdk"]
    }
  }
}
```

## Task Lifecycle

Allowed task statuses:

- `queued`
- `running`
- `blocked`
- `completed`
- `failed`
- `cancelled`
- `expired`

Normal flow:

```text
POST /agent/v1/tasks -> 202 accepted
GET /agent/v1/tasks/{task_id} -> queued/running
GET /agent/v1/tasks/{task_id} -> completed/failed/blocked
```

Cancellation flow:

```text
POST /agent/v1/tasks/{task_id}/cancel -> 200 cancelled
```

Blocked tasks should include `requires_human_approval=true` and explain what approval is needed.

## Endpoint Summary

```text
GET  /agent/v1/health
GET  /agent/v1/capabilities
POST /agent/v1/tasks
GET  /agent/v1/tasks/{task_id}
POST /agent/v1/tasks/{task_id}/cancel
```

## Health Check

Request:

```http
GET /agent/v1/health HTTP/1.1
Host: unity-architect.internal.metadyn.xyz
Authorization: Bearer <service-token>
X-MetaDyn-Caller: jen
X-MetaDyn-Request-Id: 01HVHEALTH000000000000
```

Response:

```json
{
  "status": "ok",
  "agent_id": "metadyn-unity-architect",
  "version": "0.1.0",
  "time": "2026-04-07T00:00:00Z",
  "queue": {
    "running": 1,
    "queued": 2,
    "max_concurrent": 3
  }
}
```

## Capability Discovery

Request:

```http
GET /agent/v1/capabilities HTTP/1.1
Host: unity-architect.internal.metadyn.xyz
Authorization: Bearer <service-token>
X-MetaDyn-Caller: jen
X-MetaDyn-Request-Id: 01HVCAPS0000000000000
```

Response:

```json
{
  "agent_id": "metadyn-unity-architect",
  "display_name": "Unity Architect",
  "version": "0.1.0",
  "description": "Reviews Unity 6, WebGL, SDK, avatar runtime, and deployment-adjacent Unity implementation work.",
  "domains": ["unity", "webgl", "sdk", "avatar-runtime"],
  "tools": ["repo_read", "plan_review", "diff_review", "test_runner"],
  "can_modify_files": false,
  "can_execute_commands": true,
  "approval_required_for": [
    "network",
    "deployment",
    "destructive_fs",
    "external_messages",
    "production_config"
  ],
  "max_task_seconds": 900,
  "max_context_bytes": 250000,
  "supports_streaming": false,
  "supports_artifacts": true
}
```

## Task Submission

Request:

```http
POST /agent/v1/tasks HTTP/1.1
Host: unity-architect.internal.metadyn.xyz
Content-Type: application/json
Authorization: Bearer <service-token>
X-MetaDyn-Caller: jen
X-MetaDyn-Request-Id: 01HVTASK0000000000000
```

Body:

```json
{
  "task_id": "01HVTASK0000000000000",
  "requested_by": "jen",
  "conversation_ref": "openclaw-session-opaque-ref",
  "priority": "normal",
  "domain": "unity",
  "objective": "Review the avatar upload implementation guide for Unity runtime and WebGL risks.",
  "constraints": [
    "Do not modify files.",
    "Do not run deployment commands.",
    "Do not access external services.",
    "Return findings with file references when possible."
  ],
  "context_refs": [
    {
      "type": "workspace_file",
      "path": "docs/planning/metadyn-vrm-and-glb-upload-implementation-guide-2026-04-06.md",
      "sha256": null
    }
  ],
  "inline_context": [
    {
      "label": "User request",
      "content_type": "text/plain",
      "content": "Please review this plan for implementation blockers."
    }
  ],
  "artifacts": [],
  "approval": {
    "approval_id": null,
    "approved_actions": []
  },
  "return_format": {
    "type": "review_findings",
    "include_summary": true,
    "include_next_actions": true
  },
  "timeout_seconds": 600
}
```

Accepted response:

```json
{
  "task_id": "01HVTASK0000000000000",
  "status": "queued",
  "result_url": "/agent/v1/tasks/01HVTASK0000000000000",
  "accepted_at": "2026-04-07T00:00:00Z",
  "estimated_seconds": 180
}
```

Rejected response:

```json
{
  "error": {
    "code": "approval_required",
    "message": "The task requested command execution requiring network access, but no approval was provided.",
    "request_id": "01HVTASK0000000000000",
    "retryable": true,
    "details": {
      "required_approval": "network"
    }
  }
}
```

## Task Result

Request:

```http
GET /agent/v1/tasks/01HVTASK0000000000000 HTTP/1.1
Host: unity-architect.internal.metadyn.xyz
Authorization: Bearer <service-token>
X-MetaDyn-Caller: jen
X-MetaDyn-Request-Id: 01HVRESULT00000000000
```

Running response:

```json
{
  "task_id": "01HVTASK0000000000000",
  "status": "running",
  "started_at": "2026-04-07T00:00:15Z",
  "updated_at": "2026-04-07T00:01:00Z",
  "progress": {
    "message": "Reading referenced Unity plan and checking WebGL constraints.",
    "percent": 45
  }
}
```

Completed response:

```json
{
  "task_id": "01HVTASK0000000000000",
  "status": "completed",
  "started_at": "2026-04-07T00:00:15Z",
  "completed_at": "2026-04-07T00:03:12Z",
  "summary": "Found two implementation risks and one missing verification step.",
  "findings": [
    {
      "severity": "high",
      "title": "Runtime import path needs WebGL-specific memory validation.",
      "evidence": {
        "type": "file",
        "path": "docs/planning/metadyn-vrm-and-glb-upload-implementation-guide-2026-04-06.md",
        "line": 570
      },
      "recommendation": "Add explicit browser memory and model-size test cases before implementation."
    },
    {
      "severity": "medium",
      "title": "Avatar normalization pipeline should define failure behavior.",
      "evidence": {
        "type": "file",
        "path": "docs/planning/metadyn-avatar-normalization-pipeline-2026-04-06.md",
        "line": 1
      },
      "recommendation": "Define whether failed normalization blocks upload or falls back to a pending moderation state."
    }
  ],
  "artifacts": [],
  "requires_human_approval": false,
  "next_actions": [
    "Add WebGL memory test cases to the implementation guide.",
    "Define avatar normalization failure handling before code work begins."
  ]
}
```

Blocked response:

```json
{
  "task_id": "01HVTASK0000000000000",
  "status": "blocked",
  "summary": "The requested test requires network access to download Unity packages.",
  "requires_human_approval": true,
  "required_approval": {
    "actions": ["network"],
    "reason": "Package restore needs access to Unity package registries."
  },
  "next_actions": [
    "Ask Josh for approval before running package restore.",
    "Alternatively continue with static review only."
  ]
}
```

Failed response:

```json
{
  "task_id": "01HVTASK0000000000000",
  "status": "failed",
  "summary": "The task failed during local repository inspection.",
  "error": {
    "code": "workspace_not_found",
    "message": "The referenced workspace path was not mounted on this subagent host.",
    "retryable": false
  },
  "artifacts": [],
  "requires_human_approval": false,
  "next_actions": [
    "Mount the relevant repository on the subagent host or send the needed file content inline."
  ]
}
```

## Cancellation

Request:

```http
POST /agent/v1/tasks/01HVTASK0000000000000/cancel HTTP/1.1
Host: unity-architect.internal.metadyn.xyz
Content-Type: application/json
Authorization: Bearer <service-token>
X-MetaDyn-Caller: jen
X-MetaDyn-Request-Id: 01HVCANCEL0000000000
```

Body:

```json
{
  "reason": "User changed scope before the task completed."
}
```

Response:

```json
{
  "task_id": "01HVTASK0000000000000",
  "status": "cancelled",
  "cancelled_at": "2026-04-07T00:04:00Z"
}
```

## Curl Examples

Capability discovery:

```bash
curl -sS \
  -H "Authorization: Bearer $METADYN_SUBAGENT_TOKEN" \
  -H "X-MetaDyn-Caller: jen" \
  -H "X-MetaDyn-Request-Id: 01HVCAPS0000000000000" \
  https://unity-architect.internal.metadyn.xyz/agent/v1/capabilities
```

Submit task:

```bash
curl -sS \
  -X POST \
  -H "Authorization: Bearer $METADYN_SUBAGENT_TOKEN" \
  -H "X-MetaDyn-Caller: jen" \
  -H "X-MetaDyn-Request-Id: 01HVTASK0000000000000" \
  -H "Content-Type: application/json" \
  --data @task.json \
  https://unity-architect.internal.metadyn.xyz/agent/v1/tasks
```

Poll task:

```bash
curl -sS \
  -H "Authorization: Bearer $METADYN_SUBAGENT_TOKEN" \
  -H "X-MetaDyn-Caller: jen" \
  -H "X-MetaDyn-Request-Id: 01HVRESULT00000000000" \
  https://unity-architect.internal.metadyn.xyz/agent/v1/tasks/01HVTASK0000000000000
```

## Reference Python Server Example

This is a deliberately small FastAPI-style example to illustrate the contract. It is not production-ready.

```python
from datetime import datetime, timezone
import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="MetaDyn Remote Subagent API")

AGENT_ID = "metadyn-unity-architect"
SERVICE_TOKEN = os.environ.get("METADYN_SUBAGENT_TOKEN")
TASKS: dict[str, dict[str, Any]] = {}


class ContextRef(BaseModel):
    type: str
    path: str | None = None
    sha256: str | None = None


class Approval(BaseModel):
    approval_id: str | None = None
    approved_actions: list[str] = Field(default_factory=list)


class ReturnFormat(BaseModel):
    type: str = "review_findings"
    include_summary: bool = True
    include_next_actions: bool = True


class TaskRequest(BaseModel):
    task_id: str
    requested_by: str
    conversation_ref: str
    priority: str = "normal"
    domain: str
    objective: str
    constraints: list[str] = Field(default_factory=list)
    context_refs: list[ContextRef] = Field(default_factory=list)
    inline_context: list[dict[str, str]] = Field(default_factory=list)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    approval: Approval = Field(default_factory=Approval)
    return_format: ReturnFormat = Field(default_factory=ReturnFormat)
    timeout_seconds: int = 600


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def require_auth(authorization: str | None) -> None:
    if not SERVICE_TOKEN:
        raise HTTPException(status_code=503, detail="Service token is not configured.")
    if authorization != f"Bearer {SERVICE_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized.")


@app.get("/agent/v1/health")
def health(authorization: str | None = Header(default=None)):
    require_auth(authorization)
    return {
        "status": "ok",
        "agent_id": AGENT_ID,
        "version": "0.1.0",
        "time": utc_now(),
        "queue": {"running": 0, "queued": 0, "max_concurrent": 3},
    }


@app.get("/agent/v1/capabilities")
def capabilities(authorization: str | None = Header(default=None)):
    require_auth(authorization)
    return {
        "agent_id": AGENT_ID,
        "display_name": "Unity Architect",
        "version": "0.1.0",
        "domains": ["unity", "webgl", "sdk", "avatar-runtime"],
        "tools": ["repo_read", "plan_review", "diff_review", "test_runner"],
        "can_modify_files": False,
        "can_execute_commands": True,
        "approval_required_for": ["network", "deployment", "destructive_fs"],
        "max_task_seconds": 900,
        "max_context_bytes": 250000,
        "supports_streaming": False,
        "supports_artifacts": True,
    }


@app.post("/agent/v1/tasks", status_code=202)
def create_task(task: TaskRequest, authorization: str | None = Header(default=None)):
    require_auth(authorization)
    if task.domain not in {"unity", "webgl", "sdk", "avatar-runtime"}:
        raise HTTPException(status_code=403, detail="Domain is not allowed for this agent.")
    if task.task_id in TASKS:
        raise HTTPException(status_code=409, detail="Task already exists.")

    TASKS[task.task_id] = {
        "task_id": task.task_id,
        "status": "queued",
        "accepted_at": utc_now(),
        "request": task.model_dump(),
    }
    return {
        "task_id": task.task_id,
        "status": "queued",
        "result_url": f"/agent/v1/tasks/{task.task_id}",
        "accepted_at": TASKS[task.task_id]["accepted_at"],
        "estimated_seconds": 180,
    }


@app.get("/agent/v1/tasks/{task_id}")
def get_task(task_id: str, authorization: str | None = Header(default=None)):
    require_auth(authorization)
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found.")

    task = TASKS[task_id]
    if task["status"] == "queued":
        # Real implementation would dispatch background work instead of faking completion here.
        task["status"] = "completed"
        task["completed_at"] = utc_now()
        task["summary"] = "Static review completed."
        task["findings"] = []
        task["artifacts"] = []
        task["requires_human_approval"] = False
        task["next_actions"] = []
    return task


@app.post("/agent/v1/tasks/{task_id}/cancel")
def cancel_task(task_id: str, authorization: str | None = Header(default=None)):
    require_auth(authorization)
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found.")
    TASKS[task_id]["status"] = "cancelled"
    TASKS[task_id]["cancelled_at"] = utc_now()
    return {
        "task_id": task_id,
        "status": "cancelled",
        "cancelled_at": TASKS[task_id]["cancelled_at"],
    }
```

## Reference TypeScript Client Example

This illustrates how an OpenClaw plugin or local wrapper could call a subagent. It is not final plugin code.

```ts
type SubagentTaskRequest = {
  task_id: string;
  requested_by: "jen";
  conversation_ref: string;
  priority: "low" | "normal" | "high";
  domain: string;
  objective: string;
  constraints: string[];
  context_refs: Array<{ type: string; path?: string; sha256?: string | null }>;
  inline_context: Array<{ label: string; content_type: string; content: string }>;
  artifacts: Array<Record<string, unknown>>;
  approval: { approval_id: string | null; approved_actions: string[] };
  return_format: {
    type: string;
    include_summary: boolean;
    include_next_actions: boolean;
  };
  timeout_seconds: number;
};

type SubagentTaskResult = {
  task_id: string;
  status: "queued" | "running" | "blocked" | "completed" | "failed" | "cancelled" | "expired";
  summary?: string;
  findings?: Array<Record<string, unknown>>;
  artifacts?: Array<Record<string, unknown>>;
  requires_human_approval?: boolean;
  next_actions?: string[];
};

async function subagentFetch<T>(
  baseUrl: string,
  token: string,
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      "X-MetaDyn-Caller": "jen",
      "X-MetaDyn-Request-Id": crypto.randomUUID(),
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Subagent request failed: ${response.status} ${body}`);
  }

  return response.json() as Promise<T>;
}

export async function delegateToSubagent(
  baseUrl: string,
  token: string,
  task: SubagentTaskRequest,
): Promise<SubagentTaskResult> {
  const accepted = await subagentFetch<{ result_url: string }>(baseUrl, token, "/agent/v1/tasks", {
    method: "POST",
    body: JSON.stringify(task),
  });

  for (let attempt = 0; attempt < 60; attempt += 1) {
    const result = await subagentFetch<SubagentTaskResult>(baseUrl, token, accepted.result_url);
    if (["completed", "failed", "blocked", "cancelled", "expired"].includes(result.status)) {
      return result;
    }
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }

  throw new Error(`Subagent task timed out: ${task.task_id}`);
}
```

## Registry Example

The registry should contain connection metadata but no secrets.

```json
{
  "subagents": [
    {
      "agent_id": "metadyn-unity-architect",
      "display_name": "Unity Architect",
      "owner": "MetaDyn",
      "host_label": "unity-agent-vps-01",
      "base_url": "https://unity-architect.internal.metadyn.xyz",
      "auth_ref": "secret://metadyn/subagents/unity-architect/token",
      "allowed_domains": ["unity", "webgl", "sdk", "avatar-runtime"],
      "denied_domains": ["dns", "billing", "external-messaging"],
      "approval_required_for": ["network", "deployment", "destructive_fs", "production_config"],
      "last_verified": "2026-04-07",
      "status": "planned"
    }
  ]
}
```

## OpenClaw Tool Wrapper Shape

The OpenClaw-facing tool should accept a smaller input than the raw HTTP API and fill standard fields itself.

Tool input:

```json
{
  "agent_id": "metadyn-unity-architect",
  "domain": "unity",
  "objective": "Review this Unity implementation plan for WebGL blockers.",
  "context_refs": [
    "docs/planning/metadyn-vrm-and-glb-upload-implementation-guide-2026-04-06.md"
  ],
  "constraints": [
    "Do not modify files.",
    "Return findings with file references."
  ]
}
```

Tool behavior:
- look up the agent in the registry
- validate the requested domain
- load only approved context references
- redact secrets before sending context
- submit the task
- poll for completion
- return structured findings to Jen

## Minimal Implementation Sequence

1. Confirm which host will run the first remote subagent.
2. Create the secret outside the docs tree.
3. Stand up the health and capabilities endpoints.
4. Add task submission and polling with in-memory storage for local testing.
5. Replace in-memory task storage with durable host-local task state if needed.
6. Add audit logging.
7. Wrap the API from an OpenClaw plugin/tool.
8. Run one read-only pilot delegation.

## Open Questions

- Should task IDs be generated by Jen or by the subagent host?
- Should task results allow patches, or only review findings, for V1?
- Should a remote subagent receive raw file content or only workspace-relative references?
- Should this use HMAC request signing immediately, or start with bearer tokens behind private ingress?
- Should OpenClaw nodes be the transport instead of HTTP for some trusted local machines?
