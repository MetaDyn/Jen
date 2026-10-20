# Remote Agent Connectivity MVP — Provider-Neutral First

**Status:** Approved planning direction; implementation and deployment not yet verified.
**Date:** 2026-10-20
**Audience:** Josh, Jen, and the manually started Codex implementation session.

## Goal

Jen submits a task through a portable FastAPI application to a provider-neutral remote agent handler and receives a real model-generated `OK`. Build the generic handler first. Netlify is one possible deployment adapter, not the application architecture or a required first deployment. Begin with one observable round trip while preserving the existing remote-subagent architecture.

## Required reading

- [Agent orchestration and remote subagents](../ai-systems/agent-orchestration-and-remote-subagents.md)
- [Remote subagent API layer](../ai-systems/remote-subagent-api-layer.md)
- [Jen connected development](jen-connected-development.md)

Those documents describe broader plans, not proof that services already exist. This MVP implements only the synchronous subset below. Inspect the selected repository and existing deployment configuration before editing; reuse established structures.

## Architecture and deployment boundaries

Request path:

`Jen -> FastAPI -> generic remote agent handler -> configured model -> response`

- **FastAPI:** common Python API and orchestration boundary, packaged as a portable container. Run on an approved Python/container-capable host. Do not attempt to deploy the Python container to Netlify.
- **Generic agent core:** provider-neutral task validation, bounded execution, normalized results/errors, and correlation metadata. No Netlify imports, event objects, environment assumptions, or deployment URLs in the core contract.
- **HTTP transport:** FastAPI calls a configured remote HTTPS endpoint implementing the shared contract. It must not require a Netlify-specific adapter or URL shape.
- **Deployment wrappers:** expose the same core behavior on a conventional server/container first. A thin Netlify wrapper may expose the same contract later; AWS/Azure wrappers must not change the contract either.
- **Netlify compatibility:** Netlify's runtime may require a JavaScript/TypeScript HTTP wrapper rather than running the Python server. Keep that packaging concern outside the agent contract and business logic. Do not claim identical Python binaries run on every host. Before implementation, select a portable execution-core runtime supported by intended deployment targets; a framework-independent TypeScript core with thin HTTP wrappers is a recommended starting point, with FastAPI remaining the common Python orchestration layer.
- A model call proves remote inference execution, not a persistent autonomous agent with memory/tools.

Build and test the generic core and standard HTTP endpoint before provider-specific packaging. Obtain approved repository, deployment target, and model/provider configuration before deployment. Do not create another service/site to resolve missing information.

## MVP API

Expose on FastAPI:

- `GET /agent/v1/health`
- `GET /agent/v1/capabilities`
- `POST /agent/v1/tasks`

Reuse the envelope and error conventions from the existing remote-subagent API document. The first supported domain is a bounded connectivity check. Accept the relevant existing fields including `task_id`, `requested_by`, `domain`, `objective`, `constraints`, and `timeout_seconds`. Validate supported values; do not silently accept unsupported actions or permissions.

Carry `X-MetaDyn-Request-Id` through both hops. Keep this request/correlation ID distinct from the task ID, even when initially generated together.

**Explicit synchronous subset:** return HTTP 200 with a completed task result directly, or an appropriate structured failure. Do not return HTTP 202, advertise asynchronous processing, or provide pretend task-status/cancellation endpoints. Durable jobs, polling, and cancellation are later extensions of the existing specification.

Completed results should use the existing conventions: `task_id`, `status: completed`, timestamps, and `summary: OK`. Preserve the actual model output; unexpected output must fail the connectivity check rather than be replaced with a success string. Include request correlation and elapsed timing in an explicitly documented compatible metadata extension.

Capabilities must accurately report the narrow MVP: no file modifications, commands, tools, memory, streaming, or autonomous actions.

## Implementation steps

1. Inspect existing code and deployment conventions; identify the approved targets and dependencies.
2. Implement validated request/result models and the synchronous FastAPI endpoints.
3. Separate endpoint handling from execution through a small adapter interface. Add one generic HTTP execution adapter; no provider-specific adapter is required.
4. Implement a framework-independent agent handler that invokes the configured model with the bounded instruction `Reply with exactly: OK.` Expose it through a minimal standard HTTP server wrapper. Return actual model output and safe errors. Keep Netlify support to a thin optional deployment wrapper after the generic path works.
5. Propagate correlation IDs, enforce timeouts, and add structured logs on both sides.
6. Add automated tests with a mocked provider plus an explicitly enabled live integration test.
7. Provide local/container startup and deployment instructions. Deploy only to authorized targets, then test the actual deployed path from Jen's host.

## Security and operational bounds

- HTTPS for non-localhost calls.
- Separate bearer secrets for Jen-to-FastAPI and FastAPI-to-remote-agent; validate both hops.
- Secrets remain in environment/provider secret settings, never source, client bundles, logs, or this repo.
- Use a configured, allowlisted execution URL; never accept arbitrary downstream URLs from task input.
- Bound input size, model output, concurrent work, and execution time within deployed platform limits.
- No automatic retries in the MVP, preventing inadvertent duplicate model calls. Durable idempotency/replay protection is a later gate before enabling retries or side-effecting tasks; do not claim it is solved by a correlation ID.
- Treat caller metadata headers as metadata, not authentication.
- Do not expose an unauthenticated general-purpose model proxy or arbitrary prompt/tool execution.
- Failure responses must not disclose tokens, provider credentials, or raw internal exception traces.

## Minimum telemetry

Structured logs only; no separate telemetry service or dashboard.

Record at the appropriate boundary: `request.sent`, `request.received`, `response.sent`, `response.received`, and failures/timeouts. Include UTC timestamp, request ID, task ID, emitting component, event, outcome, duration, and safe error code where applicable.

Use locally measured elapsed durations; do not rely on cross-host clock subtraction for latency. Correlation must let an operator distinguish requests not observed at the receiver from received requests that failed to answer. Logs alone do not prove why a missing event is absent.

Do not log raw prompts, private context, or credentials by default.

## Acceptance gates

- A request originating on Jen's host passes through deployed FastAPI and the deployed generic agent endpoint, invokes the configured model, and returns exactly `OK` as the task summary.
- Structured logs correlate the full round trip with the same request/task IDs.
- Both hops reject missing/invalid authentication; unauthorized requests never trigger model calls.
- Invalid input, unexpected model output, downstream errors, and timeouts produce explicit failures rather than false success.
- Automated tests cover those paths without requiring paid live calls by default.
- FastAPI runs locally and in its container using configuration-only host/provider differences.
- Deployment documentation clearly distinguishes the remote agent endpoint from separately hosted FastAPI.

A hardcoded `OK` is permitted only as a labeled connectivity fixture, never as evidence that the model/agent round trip passed.

## Out of scope

No broker, new database, UI/dashboard, persistent agent memory, autonomous workflows, tools, streaming, callbacks, durable task queue, or full registry. No required cloud-specific implementation in the first generic milestone. Netlify compatibility must be preserved without making Netlify a dependency. No production changes outside the authorized deployment scope.

## Codex handoff deliverables

- Source and tests using the selected repository's conventions.
- Secret-free environment configuration example and portable FastAPI container configuration.
- Setup/deployment instructions for both components and secret configuration.
- Exact supported request/result/error contract and telemetry fields.
- Test results distinguishing mocked, local, deployed connectivity, and actual model execution evidence.
- Deployed remote agent URL and approved FastAPI URL, or explicit blockers if either is unavailable.

Do not report end-to-end completion after testing only the remote agent endpoint. A full pass requires the actual Jen-host-to-FastAPI-to-remote-agent-to-model return path.
