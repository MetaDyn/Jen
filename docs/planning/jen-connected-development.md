# Jen-Connected Development — Implementation Plan and Punch List

**Date:** 2026-09-15  
**Status:** Planning; transport and integration not yet selected or implemented.

## Objective

Enable Jen to coordinate approved development work through Codex or similar coding agents running in developer environments, progressing from bounded assignments to verified implementation outcomes.

Josh's environment is the initial pilot, not the limit of the design. Approved developers outside his machine must also be able to collaborate with Jen, with project-specific permissions and their own approved execution environments.

## Confirmed Starting Context

- Jen runs OpenClaw in an Ubuntu VM on Josh's Windows host. The gateway is intended to remain LAN-only, without public inbound exposure.
- Josh runs VS Code on Windows and the coding CLI inside WSL.
- WSL and the OpenClaw VM are separate execution environments. Exact routing and installed tooling have not yet been inspected for this integration.
- Existing remote-subagent architecture and API documents are drafts, not proof of a deployed transport.
- Stock Codex CLI does not automatically register with Jen or retrieve assignments. A supported integration or explicit wrapper is required.
- The intended experience is an opt-in **Jen-connected coding session**. Ordinary CLI sessions remain independent.

## User Experience Target

An approved developer starts a connected session for a permitted project. The integration authenticates the developer and worker, announces availability, and retrieves or accepts authorized assignments. Codex performs the coding work; the integration handles task delivery, status, approvals, and results.

Jen frames assignments, supplies only relevant context, reviews evidence, requests corrections within the authorized scope, and reports outcomes. Remote agents do not inherit Jen's full memory or authority.

The integration should wait efficiently using an established connection or bounded polling with backoff. Idle checks should not require model calls. Do not assume an existing interactive CLI session can be attached or resumed until that behavior is verified.

## Architecture Decisions to Verify First

### Existing Integration Assessment

Inspect installed OpenClaw documentation and configuration capabilities for ACP/coding-agent integration, supported harnesses, session lifecycle, approvals, and local versus remote execution. Inspect the actual Codex CLI version and supported interfaces in WSL.

Determine separately:

- How Jen starts or addresses an agent session.
- How execution reaches WSL or an external developer host.
- How developer identity and project authorization are established.
- How results and approval requests are delivered without an inbound public gateway.

Do not assume ACP alone provides remote transport, multi-user authorization, or a task broker.

### Candidate Transport Models

| Model | Appropriate when | Boundary to preserve |
| --- | --- | --- |
| Direct outbound dispatch from Jen to an approved worker | The worker is reachable over an approved private connection | No public gateway exposure; narrow worker endpoint and authenticated access. |
| Outbound broker connection from both Jen and workers | Distributed workers cannot accept inbound connections | Broker authenticates and isolates participants; it does not expose the gateway or become an unrestricted command relay. |

The broker model is a candidate for distributed development, not an approved implementation decision. Prefer existing supported components where they meet requirements. Any new service, endpoint, network configuration, or installation requires explicit approval.

A developer-facing request channel is a separate decision from worker transport. An authenticated chat or UI request must still be mapped to project permissions; worker enrollment alone does not authorize a person to direct Jen.

## Identity and Authority

Keep three identities distinct:

1. **Developer:** the person requesting work and the actions they may authorize.
2. **Worker:** the enrolled machine/runtime and its available tools.
3. **Project:** the repository, environment, data boundaries, and approval policy.

An approved developer must not automatically gain access to Josh's workstation, other developers' machines, unrelated client data, or Jen's private conversations.

Minimum controls:

- Explicit enrollment, ownership, scoped credentials, expiry/rotation, and revocation.
- Server-side project authorization and worker eligibility checks.
- Host/tool enforcement of repository paths, executable actions, and resource limits.
- Secrets kept in appropriate local stores; no credentials in prompts, task payloads, or repository docs.
- Approvals verified against an authorized human and bound to the exact task, action, target, and expiry—not accepted as self-declared fields from an agent.
- Cancellation and revocation enforced by the execution controller, with truthful acknowledgement of what has actually stopped.
- Remote output treated as untrusted evidence, never authority to expand permissions.

Initial policy: read-only work first, then scoped edits/tests. No automatic merging, publishing, production deployment, credential changes, or destructive actions. Routine actions may be preapproved within an agreed scope, but approval to edit/test does not grant unrestricted shell or network access.

## Task and Result Contract

Build on the existing remote-subagent contract rather than creating an unrelated protocol.

A task should identify:

- Unique task ID, requesting developer, project, eligible worker, and approved objective.
- Repository and base revision, allowed checkout/path, and permitted actions.
- Minimal context, input artifact references/checksums, and expected output.
- Acceptance criteria, time/resource limits, expiry, and approval requirements.

Lifecycle should cover queued, claimed, running, blocked/awaiting approval, completed, failed, cancelled, and expired. Claims need leases or equivalent ownership semantics so retries and disconnects do not cause concurrent duplicate execution.

Results should include summary, base/result revision where applicable, diff/artifacts, commands and test evidence, limitations, and remaining blockers. Keep worker completion distinct from Jen's review and human acceptance.

Controls to specify during design:

- Idempotency and retry behavior; no promise of exactly-once execution.
- Reconnect and task reconciliation; no blind rerun of partially completed writes.
- Cancellation acknowledgement and termination of child processes where supported.
- Artifact access restrictions, retention/deletion, and redacted audit records.
- Concurrent-work protection and isolated checkouts for agent edits.

## Phased Punch List

### Phase 0 — Verify and Select

- [ ] Inspect installed OpenClaw ACP/coding-agent documentation and available integration points.
- [ ] Confirm Codex CLI version, authentication mode, non-interactive/session interfaces, and approval behavior in WSL.
- [ ] Confirm host/VM/WSL routing without altering gateway exposure.
- [ ] Identify one development repository and its data classification.
- [ ] Compare direct dispatch and outbound broker options against external-developer requirements.
- [ ] Document selected components, missing functionality, credential flow, and operational ownership.
- [ ] Obtain Josh's approval before installations, new services, endpoints, or network/config changes.

**Exit criterion:** a verified connection design and explicitly approved pilot scope.

### Phase 1 — One Read-Only WSL Assignment

- [ ] Enroll Josh and one WSL worker with project-specific access.
- [ ] Establish the opt-in connected-session startup process.
- [ ] Submit one bounded repository inspection task.
- [ ] Return status and file-referenced findings to Jen for review.
- [ ] Verify denial of unauthorized paths/actions and invalid credentials.
- [ ] Test disconnect, timeout, cancellation, and duplicate delivery behavior.
- [ ] Confirm no public inbound OpenClaw access was introduced.

**Exit criterion:** Josh starts a connected session, receives an authorized task, and Jen obtains a verifiable result without modifying project or production files.

### Phase 2 — Bounded Coding

- [ ] Use an approved isolated checkout/worktree, preserving the developer's active checkout.
- [ ] Enable narrowly scoped edits and approved test commands.
- [ ] Define network/package-install approval behavior and command sandboxing.
- [ ] Exercise progress, blockers, and action-specific approval requests.
- [ ] Return diffs, revisions, and actual test results.
- [ ] Have Jen review results and request one correction within the same authorization scope.
- [ ] Test interrupted writes/reconnect without duplicate changes.
- [ ] Keep merge, push/publishing, and deployment permissions explicit and separate.

**Exit criterion:** a bounded change is implemented and reviewed with evidence, without modifying unrelated work or exceeding authority.

### Phase 3 — External Developer

- [ ] Enroll one explicitly approved external developer and their worker.
- [ ] Select and authorize their request channel.
- [ ] Verify project-specific task visibility and routing.
- [ ] Test denial of cross-project tasks, artifacts, and private Jen context.
- [ ] Verify they cannot route work to Josh's workstation without separate permission.
- [ ] Test developer and worker revocation, including active-task handling.
- [ ] Complete one authorized task end to end.

**Exit criterion:** external collaboration works with demonstrated identity, project, and worker separation.

### Phase 4 — Operational Readiness

- [ ] Define service/worker ownership, updates, monitoring, and incident procedures.
- [ ] Set concurrency, cost, runtime, and storage limits.
- [ ] Define task/log/artifact retention and deletion.
- [ ] Test recovery and reconciliation after controller/worker outages.
- [ ] Document onboarding, offboarding, approval, and stop procedures.
- [ ] Assess broader autonomy only after reviewing pilot evidence and explicit authorization.

## Data and Enterprise Security Boundaries

Private gateway hosting does not imply private inference. Inventory which prompts, source files, results, and logs reach model providers or any broker. Send only approved context and respect each project's data restrictions.

For a broker, assess hosting location, encryption, tenant isolation, operator access, retention, and compromise impact. Outbound-only connectivity reduces inbound exposure but does not make returned content trusted or eliminate supply-chain and credential risks.

For development workers, prefer least-privileged execution and isolated workspaces. An agent running under a developer's unrestricted account must not be presented as strongly sandboxed merely because its task prompt is narrow.

## Open Decisions

- Which repository anchors the pilot?
- Which supported coding-agent interface will be used, and where does its controller run?
- Is private direct dispatch sufficient initially, or is a broker required for the first external developer?
- Which existing service, if any, can safely provide the required coordination?
- Which developer-facing channel should accept authorized requests?
- Who may approve each action category beyond Josh?
- Which project data may be sent to each model/provider?

## Scope and Non-Goals

This document authorizes no deployment or access change. It does not open the gateway, create accounts/services, install workers, or enroll external developers.

The first release is not an unrestricted remote shell, autonomous production operator, public Jen chat endpoint, or shared access to all MetaDyn repositories. The objective is reliable, accountable development execution within agreed boundaries.

## References

- [Agent orchestration and remote subagents](../ai-systems/agent-orchestration-and-remote-subagents.md)
- [Remote subagent API layer](../ai-systems/remote-subagent-api-layer.md) — illustrative draft code requires security and lifecycle review before reuse; it is not production-ready.
- Discussion with Josh, 2026-09-15: private Ubuntu VM, Windows/WSL coding environment, approved external developers, opt-in connected sessions, and phased agentic execution.
