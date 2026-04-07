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

## Platform Deployment Context

The API layer should support MetaDyn's real deployment model, not just review-style subagent work.

The relevant documented deployment context is:
- dashboard is the control plane for space creation and operator intent
- remote host APIs are the execution plane for filesystem, nginx, process, and verification work
- Cloudflare is the edge layer for DNS, proxying, SSL/TLS, CDN behavior, and WebSocket pass-through
- nginx is the origin router/server
- each space is its own build or own app/runtime instance
- Unity WebGL and ThreeJS/WebXR spaces are normally static file deployments
- Hyperfy and similar Node-backed spaces are normally reverse-proxied local app runtimes
- safe nginx activation is always `nginx -t` first, reload only if the config test succeeds and reload has been explicitly approved/requested

Primary local docs:
- `docs/platforms/unity6/deployment-hosting.md`
- `docs/infrastructure/nginx-ssl-proxy.md`
- `docs/runbooks/ubuntu-server-bootstrap-checklist.md`
- `docs/runbooks/metadyn-unity-webgl-site-deployment.md`
- `docs/runbooks/gitlab-ce-nginx-proxy-handoff.md`
- `docs/runbooks/umami-analytics-nginx-proxy-handoff.md`
- `docs/runbooks/grafana-supabase-monitoring.md`
- `docs/platforms/immersive-spaces.md`
- `import/unity6-docs/.claude/Planning/Build_Server_Distribution_Plan.md`
- `import/unity6-docs/.claude/Planning/Dashboard_Unity_Hyperfy_Flows.md`
- `import/unity6-docs/.claude/Planning/Hyperfy_User_System_Integration.md`
- `import/unity6-docs/.claude/config/unity-proxy-config.md`
- `import/unity6-docs/.claude/config/hyperfy-proxy-config.md`

## Current Hetzner nginx SSL Host Conventions

The current handoff runbooks describe a production-sensitive MetaDyn Hetzner host that acts as an nginx SSL proxy for `*.metadyn.xyz`.

Important conventions:
- Unity WebGL root parent: `/var/www/unity-webgl`
- Unity site root: `/var/www/unity-webgl/<site-slug>`
- nginx site file: `/etc/nginx/sites-available/<full-domain>`
- enabled symlink: `/etc/nginx/sites-enabled/<full-domain>`
- shared certificate: `/etc/letsencrypt/live/metadyn.xyz/fullchain.pem`
- shared private key: `/etc/letsencrypt/live/metadyn.xyz/privkey.pem`
- app-backed services listen on loopback and host nginx terminates public TLS

Important safety rules:
- confirm the exact full domain before writing config
- if the hostname is ambiguous or misspelled, stop and ask
- keep changes minimal and reversible
- do not modify existing live sites while adding a new one
- do not change certificate paths unless explicitly requested
- do not reference `/etc/letsencrypt/options-ssl-nginx.conf` or `/etc/letsencrypt/ssl-dhparams.pem` unless those files are confirmed present on the host
- do not reload or restart nginx unless explicitly requested/approved, even if `nginx -t` passes
- for first Unity build copy, prefer reviewing `rsync --dry-run` output before live sync when practical

Known reverse-proxy app patterns from the runbooks:
- GitLab CE: `gitlab.metadyn.xyz` -> `http://127.0.0.1:8060`
- Umami analytics: `analytics.metadyn.xyz` -> `http://127.0.0.1:3000`
- Grafana monitoring: `monitor.metadyn.xyz` -> `http://127.0.0.1:3001`

These examples matter because Hyperfy and other app-backed immersive runtimes should use the same host principle: local loopback app runtime, public TLS at host nginx, no extra public app port.

GitLab and Umami should not be treated as default workloads that the orchestration API deploys from scratch. They are already native production installs on the host. The API layer may still need to modify or verify their nginx routing, service health, tracking integration, or handoff state when explicitly requested and approved.

The primary deployment use case for this orchestration layer remains MetaDyn's immersive space layers: Unity WebGL, Hyperfy, ThreeJS, WebXR, and related dashboard-created platform spaces.

## Dashboard-To-Remote-Host Deployment Flow

The intended "one click" deployment path should look like this:

```text
operator -> dashboard.metadyn.xyz -> OpenClaw/Jen or backend deploy API -> remote host subagent/deploy service -> Cloudflare/nginx/filesystem/process manager -> public space URL
```

Detailed flow:

1. Operator creates or selects a space in the dashboard.
2. Dashboard validates ownership, organization, and requested space type.
3. Dashboard or Jen submits a deployment task to the approved remote deployment subagent.
4. Remote host validates the task against its allowed domains and deployment templates.
5. Remote host provisions files or an app instance.
6. Remote host writes runtime config and deployment metadata.
7. Remote host creates or verifies the Cloudflare DNS record.
8. Remote host generates nginx config from the appropriate template.
9. Remote host enables the site and runs `nginx -t`.
10. Remote host reloads nginx only if validation succeeds and reload is explicitly approved/requested.
11. Remote host verifies HTTP/HTTPS and WebSocket behavior where relevant.
12. Remote host returns public URL, logs, artifact references, and deployment metadata.
13. Dashboard records the result and exposes the space to the creator/operator.

## Deployment Task Types

Recommended deployment task domains:

- `deploy.unity_webgl`
- `deploy.threejs`
- `deploy.webxr`
- `deploy.hyperfy`
- `deploy.nginx_route`
- `deploy.cloudflare_dns`
- `deploy.verify_space`
- `deploy.proxy_app`

The remote host should reject deployment domains it does not explicitly support.

Deployment tasks should use the same `POST /agent/v1/tasks` endpoint as other subagent tasks, with `domain` set to one of the deployment domains and a structured deployment payload inside `artifacts` or `inline_context`.

Example deployment-host capabilities response:

```json
{
  "agent_id": "metadyn-hetzner-deploy-host",
  "display_name": "MetaDyn Hetzner Deploy Host",
  "version": "0.1.0",
  "description": "Executes approved MetaDyn deployment tasks on the nginx SSL proxy host.",
  "domains": [
    "deploy.unity_webgl",
    "deploy.threejs",
    "deploy.webxr",
    "deploy.hyperfy",
    "deploy.proxy_app",
    "deploy.nginx_route",
    "deploy.cloudflare_dns",
    "deploy.verify_space"
  ],
  "tools": [
    "filesystem_deploy",
    "nginx_site_render",
    "nginx_config_test",
    "nginx_reload_when_approved",
    "loopback_health_check",
    "https_resolve_check"
  ],
  "can_modify_files": true,
  "can_execute_commands": true,
  "approval_required_for": [
    "deployment",
    "nginx_reload",
    "cloudflare_dns",
    "process_start",
    "dependency_install",
    "destructive_fs"
  ],
  "max_task_seconds": 1200,
  "max_context_bytes": 250000,
  "supports_streaming": false,
  "supports_artifacts": true
}
```

## Space Deployment Request Payload

For deployment work, the recommended task body adds a `space_deployment_request` artifact.

```json
{
  "task_id": "01HVDEPLOYUNITY00000000",
  "requested_by": "jen",
  "conversation_ref": "openclaw-session-opaque-ref",
  "priority": "high",
  "domain": "deploy.unity_webgl",
  "objective": "Deploy the Pavilion Unity WebGL build to the selected MetaDyn hostname.",
  "constraints": [
    "Use the static Unity/WebGL nginx template.",
    "Run nginx -t before reload.",
    "Reload nginx only if config validation succeeds.",
    "Do not modify unrelated nginx site configs.",
    "Do not rotate certificates or credentials.",
    "Return public URL, verification results, and logs."
  ],
  "context_refs": [
    {
      "type": "workspace_file",
      "path": "docs/platforms/unity6/deployment-hosting.md",
      "sha256": null
    },
    {
      "type": "workspace_file",
      "path": "docs/infrastructure/nginx-ssl-proxy.md",
      "sha256": null
    }
  ],
  "inline_context": [],
  "artifacts": [
    {
      "type": "space_deployment_request",
      "space": {
        "space_id": "11111111-1111-1111-1111-111111111111",
        "space_name": "PavilionProd",
        "space_type": "unity_webgl",
        "owner_ref": "supabase-user-or-org-ref",
        "environment": "production"
      },
      "routing": {
        "hostname": "pavilion.metadyn.xyz",
        "canonical_url": "https://pavilion.metadyn.xyz/PavilionProd-11111111-1111-1111-1111-111111111111/",
        "cloudflare_zone": "metadyn.xyz",
        "dns_record_mode": "create_or_verify",
        "cloudflare_proxy": true
      },
      "artifact_source": {
        "mode": "remote_path",
        "path": "/tmp/metadyn-builds/01HVDEPLOYUNITY00000000/Build"
      },
      "origin": {
        "mode": "static",
        "root": "/var/www/unity-webgl/pavilion/PavilionProd-11111111-1111-1111-1111-111111111111",
        "cert_name": "metadyn.xyz",
        "nginx_site_name": "pavilion.metadyn.xyz"
      },
      "runtime_config": {
        "room_name": "PavilionProd",
        "max_players": 32,
        "world_display_name": "Pavilion",
        "auth_mode": "metadyn_shared_cookie"
      }
    }
  ],
  "approval": {
    "approval_id": "deploy-approval-opaque-ref",
    "approved_actions": ["network", "deployment", "nginx_reload", "cloudflare_dns"]
  },
  "return_format": {
    "type": "deployment_result",
    "include_summary": true,
    "include_next_actions": true
  },
  "timeout_seconds": 1200
}
```

## Unity WebGL Deployment Example

Unity WebGL deployments should follow the documented per-space static hosting pattern:

```text
{remotePath}/{roomName}-{spaceId}/
```

For the current Hetzner handoff runbook, a simpler site-level root is also documented:

```text
/var/www/unity-webgl/<site-slug>/
```

Use the site-level root when creating a standalone hostname such as `example.metadyn.xyz`. Use the `{roomName}-{spaceId}` subfolder model when the Unity deployment profile or per-space isolation strategy explicitly expects it.

Example task payload excerpt:

```json
{
  "domain": "deploy.unity_webgl",
  "artifacts": [
    {
      "type": "space_deployment_request",
      "space": {
        "space_id": "22222222-2222-2222-2222-222222222222",
        "space_name": "PavilionDev",
        "space_type": "unity_webgl",
        "environment": "development"
      },
      "artifact_source": {
        "mode": "rsync_from_build_server",
        "source_host": "build-worker-01",
        "source_path": "/srv/metadyn/builds/pavilion-dev/Build"
      },
      "origin": {
        "mode": "static",
        "root": "/var/www/unity-webgl/dev-pavilion/PavilionDev-22222222-2222-2222-2222-222222222222",
        "cert_name": "metadyn.xyz",
        "nginx_site_name": "dev.pavilion.metadyn.xyz"
      },
      "routing": {
        "hostname": "dev.pavilion.metadyn.xyz",
        "canonical_url": "https://dev.pavilion.metadyn.xyz/PavilionDev-22222222-2222-2222-2222-222222222222/"
      }
    }
  ]
}
```

Expected remote host operations:

```text
mkdir -p /var/www/unity-webgl/dev-pavilion/PavilionDev-22222222-2222-2222-2222-222222222222
rsync Unity WebGL Build output into that directory
generate nginx static site config for dev.pavilion.metadyn.xyz
ln -s sites-available config into sites-enabled if needed
nginx -t
systemctl reload nginx only after nginx -t succeeds and reload is explicitly approved
curl -I https://dev.pavilion.metadyn.xyz/PavilionDev-22222222-2222-2222-2222-222222222222/
return deployment result
```

## ThreeJS / WebXR Static Deployment Example

ThreeJS and WebXR web apps should use the same static-hosting lane as Unity unless the app has a server runtime.

Example:

```json
{
  "task_id": "01HVDEPLOYWEBXR0000000",
  "requested_by": "jen",
  "conversation_ref": "openclaw-session-opaque-ref",
  "priority": "normal",
  "domain": "deploy.webxr",
  "objective": "Deploy a WebXR/ThreeJS space from a dashboard-created template.",
  "constraints": [
    "Use static nginx hosting.",
    "Run nginx -t before reload.",
    "Do not create new background services.",
    "Return the deployed URL and verification status."
  ],
  "context_refs": [
    {
      "type": "workspace_file",
      "path": "docs/platforms/immersive-spaces.md",
      "sha256": null
    }
  ],
  "inline_context": [],
  "artifacts": [
    {
      "type": "space_deployment_request",
      "space": {
        "space_id": "33333333-3333-3333-3333-333333333333",
        "space_name": "BrandGallery",
        "space_type": "webxr_static",
        "environment": "production"
      },
      "artifact_source": {
        "mode": "dashboard_template",
        "template_id": "threejs-gallery-v1",
        "rendered_artifact_path": "/tmp/metadyn-spaces/brand-gallery/dist"
      },
      "origin": {
        "mode": "static",
        "root": "/var/www/metadyn-spaces/brand-gallery",
        "cert_name": "metadyn.xyz",
        "nginx_site_name": "brand-gallery.metadyn.xyz"
      },
      "routing": {
        "hostname": "brand-gallery.metadyn.xyz",
        "canonical_url": "https://brand-gallery.metadyn.xyz/"
      },
      "runtime_config": {
        "dashboard_space_ref": "dashboard-space-33333333",
        "auth_mode": "metadyn_shared_cookie_optional",
        "webxr_required": false
      }
    }
  ],
  "approval": {
    "approval_id": "deploy-approval-opaque-ref",
    "approved_actions": ["deployment", "nginx_reload", "cloudflare_dns"]
  },
  "return_format": {
    "type": "deployment_result",
    "include_summary": true,
    "include_next_actions": true
  },
  "timeout_seconds": 900
}
```

Expected remote host operations:

```text
copy or render the dashboard-created ThreeJS/WebXR template
write runtime config for the dashboard space reference
copy static app output into /var/www/metadyn-spaces/brand-gallery
generate nginx static site config
nginx -t
reload nginx only if valid and explicitly approved
verify https://brand-gallery.metadyn.xyz/
```

## Hyperfy Deployment Example

Hyperfy deployments should use the reverse-proxy lane because Hyperfy is app/runtime-backed and needs WebSocket support.

Example:

```json
{
  "task_id": "01HVDEPLOYHYPERFY00000",
  "requested_by": "jen",
  "conversation_ref": "openclaw-session-opaque-ref",
  "priority": "high",
  "domain": "deploy.hyperfy",
  "objective": "Provision a new Hyperfy space from a dashboard-created template and expose it on a MetaDyn subdomain.",
  "constraints": [
    "Use the Hyperfy/Node reverse-proxy nginx template.",
    "Use 127.0.0.1 for the upstream host unless the host config says otherwise.",
    "Include WebSocket upgrade headers.",
    "Run nginx -t before reload.",
    "Do not enable legacy local Hyperfy auth fallback.",
    "Return public URL and WebSocket verification status."
  ],
  "context_refs": [
    {
      "type": "workspace_file",
      "path": "docs/infrastructure/nginx-ssl-proxy.md",
      "sha256": null
    }
  ],
  "inline_context": [],
  "artifacts": [
    {
      "type": "space_deployment_request",
      "space": {
        "space_id": "44444444-4444-4444-4444-444444444444",
        "space_name": "HyperfyMuseum",
        "space_type": "hyperfy",
        "environment": "production"
      },
      "artifact_source": {
        "mode": "template_copy",
        "template_id": "hyperfy-default-world-v1",
        "template_path": "/opt/metadyn/templates/hyperfy/default-world"
      },
      "origin": {
        "mode": "reverse_proxy",
        "app_root": "/opt/metadyn/hyperfy-spaces/hyperfy-museum",
        "upstream_url": "http://127.0.0.1:3017",
        "process_name": "hyperfy-museum",
        "cert_name": "metadyn.xyz",
        "nginx_site_name": "hyperfy-museum.metadyn.xyz"
      },
      "routing": {
        "hostname": "hyperfy-museum.metadyn.xyz",
        "canonical_url": "https://hyperfy-museum.metadyn.xyz/"
      },
      "runtime_config": {
        "auth_mode": "metadyn_shared_cookie_required",
        "dashboard_redirect_url": "https://dashboard.metadyn.xyz/login",
        "supabase_profile_sync": "read_on_join",
        "legacy_local_auth_fallback": false
      }
    }
  ],
  "approval": {
    "approval_id": "deploy-approval-opaque-ref",
    "approved_actions": ["network", "deployment", "process_start", "nginx_reload", "cloudflare_dns"]
  },
  "return_format": {
    "type": "deployment_result",
    "include_summary": true,
    "include_next_actions": true
  },
  "timeout_seconds": 1200
}
```

Expected remote host operations:

```text
validate subdomain and reserve hostname
copy Hyperfy template into /opt/metadyn/hyperfy-spaces/hyperfy-museum
write space runtime config and shared-cookie auth settings
install dependencies only if explicitly approved
start or reload the Hyperfy process on its assigned local port
create or verify Cloudflare DNS record
generate nginx reverse-proxy config with WebSocket upgrade headers
nginx -t
systemctl reload nginx only after nginx -t succeeds and reload is explicitly approved
verify HTTPS response
verify WebSocket upgrade path if practical
return deployment result
```

## Connecting A Dashboard-Created Space To A Unity WebGL Build

The dashboard/backend should own metadata and hosting/deployment intent. Unity should own the WebGL build content and project runtime configuration.

Recommended flow:

1. Dashboard creates the canonical `space` record with `space_id`, owner, display name, requested hostname, platform type, and environment.
2. Dashboard returns a deployment descriptor to Unity, Jen, or the build worker.
3. Unity build or build server embeds/selects matching runtime config values.
4. Build server emits WebGL artifacts plus a manifest.
5. Remote deploy subagent receives the descriptor and artifact source.
6. Remote deploy subagent copies the build to the per-space static directory.
7. Remote deploy subagent writes nginx static routing and verifies the public URL.
8. Dashboard updates the space record with deployment status, public URL, artifact checksum, and last deployed time.

Example deployment descriptor:

```json
{
  "space_id": "55555555-5555-5555-5555-555555555555",
  "dashboard_space_ref": "dashboard-space-55555555",
  "platform_type": "unity_webgl",
  "environment": "production",
  "display_name": "Client Demo Pavilion",
  "room_name": "ClientDemoPavilion",
  "hostname": "client-demo.metadyn.xyz",
  "remote_path": "/var/www/unity-webgl/client-demo",
  "final_directory": "/var/www/unity-webgl/client-demo/ClientDemoPavilion-55555555-5555-5555-5555-555555555555",
  "public_url": "https://client-demo.metadyn.xyz/ClientDemoPavilion-55555555-5555-5555-5555-555555555555/",
  "auth_mode": "metadyn_shared_cookie",
  "nginx_mode": "static_unity_webgl",
  "cert_name": "metadyn.xyz"
}
```

## Deployment Result Shape

Deployment task results should be more operational than review task results.

```json
{
  "task_id": "01HVDEPLOYUNITY00000000",
  "status": "completed",
  "started_at": "2026-04-07T00:00:15Z",
  "completed_at": "2026-04-07T00:04:42Z",
  "summary": "Unity WebGL space deployed and verified.",
  "deployment": {
    "deployment_id": "dep_01HVDEPLOYUNITY00000000",
    "space_id": "11111111-1111-1111-1111-111111111111",
    "space_type": "unity_webgl",
    "environment": "production",
    "hostname": "pavilion.metadyn.xyz",
    "public_url": "https://pavilion.metadyn.xyz/PavilionProd-11111111-1111-1111-1111-111111111111/",
    "origin_root": "/var/www/unity-webgl/pavilion/PavilionProd-11111111-1111-1111-1111-111111111111",
    "nginx_site_name": "pavilion.metadyn.xyz",
    "artifact_checksum": "sha256:example"
  },
  "verification": {
    "dns": "passed",
    "nginx_config": "passed",
    "nginx_reload": "passed",
    "https": "passed",
    "websocket": "not_applicable"
  },
  "logs": [
    {
      "level": "info",
      "message": "Created deployment directory."
    },
    {
      "level": "info",
      "message": "nginx -t succeeded; nginx reload was approved and completed."
    }
  ],
  "artifacts": [
    {
      "type": "nginx_site_config",
      "path": "/etc/nginx/sites-available/pavilion.metadyn.xyz",
      "redacted": false
    },
    {
      "type": "deployment_manifest",
      "path": "/var/www/unity-webgl/pavilion/PavilionProd-11111111-1111-1111-1111-111111111111/manifest.json",
      "redacted": false
    }
  ],
  "requires_human_approval": false,
  "next_actions": [
    "Record deployment metadata in the dashboard space record.",
    "Run browser smoke test for auth redirect and WebGL load."
  ]
}
```

## App Reverse-Proxy Handoff Example

The GitLab, Umami, and Grafana runbooks document the same reverse-proxy pattern that should be reused for Hyperfy/Node-style immersive app deployments:

- app listens only on loopback
- host nginx owns public `:80` and `:443`
- shared `metadyn.xyz` certificate is reused
- nginx site is validated with `nginx -t`
- nginx reload is separate and must be approved/requested
- runtime secrets stay out of the docs tree and task packets

This section is not saying GitLab or Umami should normally be provisioned by the immersive-space orchestration API. For those existing production installs, `deploy.proxy_app` is mainly useful for explicit maintenance, routing changes, health verification, or carefully approved handoff updates. New immersive app runtimes, such as Hyperfy-style spaces, are the natural deployment target for this pattern.

Example task for a generic app-backed space or internal app:

```json
{
  "task_id": "01HVPROXYAPP0000000000",
  "requested_by": "jen",
  "conversation_ref": "openclaw-session-opaque-ref",
  "priority": "normal",
  "domain": "deploy.proxy_app",
  "objective": "Create a host-nginx reverse proxy route for an approved loopback app runtime.",
  "constraints": [
    "Use the shared metadyn.xyz certificate paths.",
    "Proxy only to a loopback upstream.",
    "Do not expose the app's internal listener publicly.",
    "Run nginx -t before any reload.",
    "Do not reload nginx unless reload_nginx is true and approved.",
    "Do not include secrets in logs or returned artifacts."
  ],
  "context_refs": [
    {
      "type": "workspace_file",
      "path": "docs/runbooks/gitlab-ce-nginx-proxy-handoff.md",
      "sha256": null
    },
    {
      "type": "workspace_file",
      "path": "docs/runbooks/umami-analytics-nginx-proxy-handoff.md",
      "sha256": null
    }
  ],
  "inline_context": [],
  "artifacts": [
    {
      "type": "reverse_proxy_deployment_request",
      "routing": {
        "hostname": "example-app.metadyn.xyz",
        "canonical_url": "https://example-app.metadyn.xyz/"
      },
      "origin": {
        "mode": "reverse_proxy",
        "upstream_url": "http://127.0.0.1:3020",
        "cert_name": "metadyn.xyz",
        "nginx_site_name": "example-app.metadyn.xyz"
      },
      "activation": {
        "write_site_config": true,
        "enable_site": true,
        "test_nginx": true,
        "reload_nginx": false
      },
      "verification": {
        "loopback_health_url": "http://127.0.0.1:3020/",
        "https_resolve_check": "example-app.metadyn.xyz:443:127.0.0.1"
      }
    }
  ],
  "approval": {
    "approval_id": "proxy-approval-opaque-ref",
    "approved_actions": ["deployment"]
  },
  "return_format": {
    "type": "deployment_result",
    "include_summary": true,
    "include_next_actions": true
  },
  "timeout_seconds": 600
}
```

This can model internal app handoffs like:

```json
[
  {
    "hostname": "gitlab.metadyn.xyz",
    "upstream_url": "http://127.0.0.1:8060",
    "runbook": "docs/runbooks/gitlab-ce-nginx-proxy-handoff.md"
  },
  {
    "hostname": "analytics.metadyn.xyz",
    "upstream_url": "http://127.0.0.1:3000",
    "runbook": "docs/runbooks/umami-analytics-nginx-proxy-handoff.md"
  },
  {
    "hostname": "monitor.metadyn.xyz",
    "upstream_url": "http://127.0.0.1:3001",
    "runbook": "docs/runbooks/grafana-supabase-monitoring.md"
  }
]
```

## Reference Nginx Template Renderer

This is a compact reference helper for a remote deploy service. It is intentionally narrow and should be paired with strict validation before production use.

```python
from dataclasses import dataclass
import re


SAFE_SITE_RE = re.compile(r"^[a-z0-9.-]+$")


@dataclass(frozen=True)
class StaticSiteConfig:
    hostname: str
    app_root: str
    cert_name: str = "metadyn.xyz"


@dataclass(frozen=True)
class ReverseProxyConfig:
    hostname: str
    upstream_url: str
    cert_name: str = "metadyn.xyz"


def validate_hostname(hostname: str) -> None:
    if not SAFE_SITE_RE.fullmatch(hostname):
        raise ValueError(f"Unsafe hostname: {hostname}")
    if ".." in hostname or hostname.startswith(".") or hostname.endswith("."):
        raise ValueError(f"Invalid hostname: {hostname}")


def render_static_unity_site(config: StaticSiteConfig) -> str:
    validate_hostname(config.hostname)
    return f"""# HTTP to HTTPS redirect
server {{
    listen 80;
    server_name {config.hostname};

    return 301 https://$host$request_uri;
}}

# HTTPS - Static Unity WebGL / app host
server {{
    listen 443 ssl http2;
    server_name {config.hostname};

    root {config.app_root};
    index index.html;

    ssl_certificate /etc/letsencrypt/live/{config.cert_name}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{config.cert_name}/privkey.pem;

    location ~* \\.wasm\\.br$ {{
        types {{ }}
        default_type application/wasm;
        add_header Content-Encoding br;
    }}

    location ~* \\.data\\.br$ {{
        types {{ }}
        default_type application/octet-stream;
        add_header Content-Encoding br;
    }}

    location ~* \\.js\\.br$ {{
        types {{ }}
        default_type application/javascript;
        add_header Content-Encoding br;
    }}

    location ~* \\.(data|wasm|symbols\\.json)$ {{
        gzip on;
        gzip_types application/octet-stream application/wasm;
        gzip_vary on;
    }}

    location ~* \\.(jpg|jpeg|png|gif|ico|css|js)$ {{
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}

    location / {{
        try_files $uri $uri/ /index.html;
        add_header Access-Control-Allow-Origin '*' always;
        add_header Access-Control-Allow-Methods 'GET, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Content-Type' always;
    }}

    client_max_body_size 200M;
}}
"""


def render_reverse_proxy_site(config: ReverseProxyConfig) -> str:
    validate_hostname(config.hostname)
    if not config.upstream_url.startswith("http://127.0.0.1:"):
        raise ValueError("Expected local 127.0.0.1 upstream for Hyperfy/Node deployments.")
    return f"""# HTTP to HTTPS redirect
server {{
    listen 80;
    server_name {config.hostname};

    return 301 https://$host$request_uri;
}}

# HTTPS - Reverse proxy to Hyperfy / Node app
server {{
    listen 443 ssl http2;
    server_name {config.hostname};

    ssl_certificate /etc/letsencrypt/live/{config.cert_name}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{config.cert_name}/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {{
        proxy_pass {config.upstream_url};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }}
}}
"""
```

## Reference Deployment Executor Shape

This illustrates the local execution steps a remote deploy subagent would perform after receiving a validated deployment task. It deliberately avoids including Cloudflare token handling or process-manager specifics.

```python
from pathlib import Path
import shutil
import subprocess


def run_checked(command: list[str]) -> None:
    subprocess.run(command, check=True)


def deploy_static_space(
    source_dir: Path,
    target_dir: Path,
    site_name: str,
    nginx_config: str,
    reload_nginx: bool = False,
) -> None:
    if not source_dir.exists():
        raise FileNotFoundError(f"Missing build output: {source_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy static build output into the isolated per-space directory.
    for item in source_dir.iterdir():
        destination = target_dir / item.name
        if item.is_dir():
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)

    available = Path("/etc/nginx/sites-available") / site_name
    enabled = Path("/etc/nginx/sites-enabled") / site_name
    available.write_text(nginx_config, encoding="utf-8")

    if not enabled.exists():
        enabled.symlink_to(available)

    run_checked(["nginx", "-t"])
    if reload_nginx:
        run_checked(["systemctl", "reload", "nginx"])
```

Production implementation notes:
- run the deploy service under a constrained service account
- grant only the minimum sudo privileges needed for nginx validation/reload and site config writes
- store Cloudflare credentials in the host secret store, not in task packets
- use atomic release directories or rollback pointers before enabling broad production use
- write audit logs for task ID, caller, hostname, config path, artifact checksum, and command results
- treat dependency installation, process manager changes, and production route changes as approval-sensitive operations
- make nginx reload an explicit task approval flag, not an automatic side effect of rendering or validating a config

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
