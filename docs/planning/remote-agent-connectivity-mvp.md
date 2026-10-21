# Remote Subagent API MVP — Codex Build Handoff

**Updated:** 2026-10-20
**Status:** Source implemented for the current MVP; deployment acceptance remains unverified.

## Implementation progress (2026-10-21)

- Source: [MetaDyn/MetaDynRemoteSubagent](https://github.com/MetaDyn/MetaDynRemoteSubagent), `main` through `cd9dcfc`. The shared Node handler, Node HTTP server, thin Netlify entry point, bearer auth, bounded tasks, telemetry, OpenAI-compatible model adapter, and read-only Codex workspace review are implemented. The core is JavaScript ES modules; the original TypeScript preference was not followed.
- Automated verification: 17 tests passed for the supported contract, both entry points, error handling, and configured adapters. Codex itself was mocked in those tests.
- Observed local inference: a MetaDyn-network Ollama model returned a basic answer through the model adapter. The strict API connectivity request reached the model but returned HTTP 502 because it answered `OK.` rather than exact `OK`; the shorter example prompt returned `OK` through the adapter. No exact-`OK` API success is claimed.
- Remaining acceptance: deploy the selected Netlify site, configure its secrets and model endpoint, verify an exact-`OK` response at the deployed URL, and verify a call from Jen's host. A live Codex workspace review is also unverified. Future text/audio/video capability routing and long media jobs are outside this MVP.

## Immediate assignment

Build a small remote subagent application with an authenticated HTTP API. Send it a message and receive an actual model-generated `OK` response. Deploy this application to Josh's selected Netlify site. Keep its core portable for later deployment on ordinary servers, AWS, or Azure.

**FastAPI is NOT a requirement or dependency of this application. Do not provision a separate Python host, build an orchestration service, or block this MVP on FastAPI.** A future/existing FastAPI orchestration layer can call this API like any other HTTP client. It is outside this assignment.

This section supersedes prior versions of this document that required a FastAPI deployment or a separate backend before the first test.

## Build one application, not provider-specific systems

Use a framework-independent TypeScript core for validation, bounded model execution, normalized results, and errors.

Provide thin HTTP entry points around that SAME core:

- A Netlify-compatible entry point for the immediate deployment. Use Netlify's supported server-side execution mechanism; any function wrapper is packaging only, not another agent implementation.
- A standard Node HTTP server entry point for local use and portable server/container deployment.

No provider event objects, Netlify imports, or host-specific request logic in the core. Both entry points call the same handler and expose the same contract. Select the model/provider through server-side configuration. Use available approved credentials; do not assume Netlify supplies a persistent agent or that its AI Gateway is enabled.

First working path:

`Jen or test HTTP client -> deployed subagent API -> configured model -> OK response`

No intermediary orchestration app is needed to prove this path. Later:

`Jen -> FastAPI orchestration -> this same subagent API`

## Existing plans and narrow MVP scope

Read for architectural context:

- [Agent orchestration and remote subagents](../ai-systems/agent-orchestration-and-remote-subagents.md)
- [Remote subagent API layer](../ai-systems/remote-subagent-api-layer.md)

Keep their versioned API, bounded delegation, authentication, task IDs, and error conventions. Those documents describe the larger target, not a requirement to build all endpoints now. This document scopes the immediate MVP.

## API contract

Implement:

- `GET /agent/v1/health` — basic application liveness, not a claim that a model call succeeded.
- `POST /agent/v1/tasks` — synchronous, authenticated connectivity task.

Use a small validated subset of the existing task envelope:

```json
{
  "task_id": "client-generated-unique-id",
  "requested_by": "jen",
  "domain": "connectivity",
  "objective": "Reply with exactly: OK.",
  "constraints": [],
  "timeout_seconds": 20
}
```

Require `Authorization: Bearer <service-token>`. Accept/generate `X-MetaDyn-Request-Id` and return it for correlation. Caller headers are metadata, not authentication.

The initial supported operation is the bounded connectivity check, not arbitrary prompts or tool execution. Reject unsupported domains/objectives rather than silently ignoring them. Extend supported operations later through the same task contract and handler interface.

Call the real configured model with `Reply with exactly: OK.` Return HTTP 200 only when the call succeeds and its trimmed text equals `OK`:

```json
{
  "task_id": "client-generated-unique-id",
  "status": "completed",
  "summary": "OK",
  "metadata": {
    "request_id": "correlation-id",
    "duration_ms": 123
  }
}
```

Return safe structured errors using the existing `error.code`, `error.message`, `error.request_id`, and `error.retryable` conventions. Invalid authentication, malformed input, unsupported work, provider failure, timeout, and unexpected model output must not become success responses. Do not replace failed or unexpected model output with hardcoded `OK`.

Synchronous only: no 202 acceptance response, polling, durable task storage, or cancellation claims. Task IDs correlate work; they are not durable idempotency guarantees.

## Minimum security and telemetry

- HTTPS for deployed calls; server-side bearer-token validation before model execution.
- Store service token and provider credentials in environment/hosting secret settings. Never place them in browser bundles, source, logs, or docs.
- Enforce bounded body size, output tokens, and execution deadline compatible with the deployed runtime. Use provider cancellation where supported.
- No automatic retries, arbitrary downstream URLs, commands, tools, or uncontrolled model proxying.
- Log structured request-received, model-call-started, completed, and failed events with UTC timestamp, request ID, task ID, local elapsed duration, and safe outcome/error code.
- Do not log credentials, private context, raw prompts, or raw provider exception traces by default.
- Do not build a telemetry service, UI, broker, or database for this test.

## Implementation sequence

1. Inspect the approved repository and Netlify site conventions. Obtain the intended site/repository and credential configuration if not already supplied; do not invent targets.
2. Implement the generic handler and injectable model adapter; test using a fake model adapter.
3. Add the standard Node server entry point and verify a local HTTP round trip.
4. Add the thin Netlify entry point using the same handler; configure API routing and server-side secrets.
5. Deploy to the approved Netlify site and test the real model-backed API.
6. Provide the URL and secure credential-setup instructions so Jen can test from her host. Do not publish secret values in handoff messages.

## Acceptance criteria

- An HTTP client can submit the task to the deployed Netlify URL and receive actual model-generated `OK` in the normalized result.
- The same core passes contract tests through the standard Node server and Netlify entry point. No duplicated agent logic.
- Missing/invalid auth never triggers inference.
- Tests cover bad input, unsupported work, provider failure, timeout, and unexpected output. Default automated tests do not require paid calls.
- Correlated logs identify the request and outcome without exposing secrets.
- Provide one copy-paste HTTP example using an environment variable for the bearer token.
- Distinguish local/mock results from deployed live-model evidence. Jen-host verification is a separate reported gate if Codex cannot access that host; do not block deployment on building an intermediary.

## Deliverables and extension boundaries

Deliver source, tests, secret-free environment example, standard Node startup instructions, Netlify deployment instructions, supported API contract, deployed endpoint URL, and verification results.

No FastAPI service in this assignment. No new database, agent registry, memory system, dashboard, broker, streaming, asynchronous jobs, or autonomous tools. Preserve extensibility through the shared handler, model adapter, HTTP contract, and thin hosting entry points—not speculative infrastructure.
