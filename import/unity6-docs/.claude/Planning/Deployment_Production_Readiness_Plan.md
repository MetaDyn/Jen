# Deployment Production Readiness Plan

**Date:** 2026-03-08  
**Status:** Planning  
**Purpose:** Evaluate the current Unity-driven deployment implementation against the documented MetaDyn deployment architecture and define the path to truly one-click, production-ready deployment.

---

## Executive Summary

MetaDyn currently has a functional one-click upload flow from the Unity Editor:
- per-space deployment paths
- SSH preflight for remote directory creation
- `rsync` preferred, `scp` fallback
- runtime config update before deployment

That is useful, but it is not yet a production-grade one-click deployment system.

The main gap is that the current implementation is still a file transfer tool. It does not yet automate:
- release versioning
- rollback
- nginx provisioning
- DNS/subdomain provisioning
- post-deploy public URL verification
- deployment history/auditing
- host-side execution via a deployment API

The documented long-term architecture already points toward a host deployment API and dashboard-backed control plane. That is the correct path.

---

## Current State

### What Exists Today

- Unity Editor deployment UI via `MetaDynProjectConfig`
- server profile configuration via `MetaDynServerProfile`
- SSH-based directory creation and verification
- file transfer via `rsync` or `scp`
- dynamic per-space folder path:

```text
{remotePath}/{roomName}-{spaceId}/
```

- runtime config metadata update before deployment

### What Works Well

- simple deploy flow for internal use
- per-space isolation at the directory level
- explicit server profile model
- non-interactive SSH behavior
- recent hardening now fails fast if remote directory setup cannot be verified

### What It Really Is

Current deployment is best described as:

> Unity-triggered remote file sync to a prepared host

It is not yet:

> production one-click provisioning and release management

---

## Gap Analysis Against The Docs

### 1. Runtime URL Consistency Gap

The runtime config is intended to carry deployment metadata, but the current deployment flow updates `deploymentURL` from the base selected profile before the dynamic per-space URL suffix is applied.

Impact:
- runtime metadata can disagree with the actual deployed public URL
- any downstream system relying on runtime config can become inconsistent

### 2. Provisioning Gap

The docs describe deployment as including host/routing concerns, but the code currently only:
- creates a target directory
- uploads files

It does not:
- generate nginx config
- validate nginx config
- reload nginx safely
- create or update Cloudflare DNS
- assign or validate subdomains
- confirm public availability

### 3. Release Management Gap

The code deploys directly into the live target path. There is no:
- release directory structure
- manifest
- checksum
- atomic activation
- deployment history
- rollback path

This is the largest production-readiness gap after provisioning.

### 4. Verification Gap

The deployer verifies the remote directory exists before transfer, but it does not verify:
- required build files landed correctly
- `index.html` is served publicly
- the final URL resolves through Cloudflare/nginx
- expected cache/compression behavior is present

### 5. UX / Status Gap

The deployment docs call for status visibility and reporting, but the current implementation has only limited local status handling:
- no real transfer progress parsing
- no structured deploy stages
- no deployment logs persisted anywhere
- no history

### 6. Security / Control Plane Gap

The documented long-term model is dashboard -> host deployment API.

Current implementation still relies on:
- editor-held SSH access
- editor-held auth token in `EditorPrefs`
- direct execution from the developer machine

That is workable for internal development, but not the final production operating model.

### 7. Reliability Gap

Production deployment needs:
- atomic releases
- rollback
- environment separation
- auditable deployment records
- safer timeouts and better retry behavior

The current uploader does not provide these yet.

---

## Production Readiness Goals

For MetaDyn deployment to be considered truly one-click and production-ready, it should support all of the following:

1. Build or receive the correct deployable artifact.
2. Create a versioned release on the host.
3. Write or update per-space runtime metadata.
4. Provision or update hostname routing.
5. Validate nginx config and activate it safely.
6. Verify public reachability at the final URL.
7. Record deployment metadata, logs, and status.
8. Support rollback to a prior known-good release.
9. Distinguish `dev`, `staging`, and `prod`.
10. Run through a host-side deployment API rather than depending on direct editor shell access for the long term.

---

## Recommended Phases

## Phase 1: Harden The Existing Unity Deployer

Goal:
Make the current Unity-driven deployment path reliable enough for controlled production use before introducing a host deployment API.

Scope:
- fix runtime deployment URL consistency
- improve SSH/write verification
- add release metadata
- add post-deploy verification
- fix cross-platform path and timeout issues
- make failure reporting clearer

Expected outcome:
- safer and more deterministic deploys
- fewer ambiguous failures
- basic release traceability

## Phase 2: Introduce Host-Side Deployment API

Goal:
Move deployment execution from the editor machine to the host environment.

Responsibilities of the host API:
- authenticate deploy requests
- create or update release directories
- generate runtime config
- generate nginx config from template
- validate nginx config
- reload nginx safely
- activate the correct release
- return deployment logs and final status

Expected outcome:
- true execution-plane separation
- better security
- easier dashboard integration

## Phase 3: Full Platform Deployment Workflow

Goal:
Align the implementation with the full documented platform model.

Scope:
- dashboard-triggered deploys
- subdomain assignment and validation
- Cloudflare DNS automation
- deployment history
- rollback UI
- deployment permissions by org/team/environment

Expected outcome:
- true production one-click deployment
- dashboard as control plane
- repeatable managed hosting experience

---

## Prepare For Phase 1

Before Phase 1 implementation starts, prepare the codebase and operational assumptions so the work lands cleanly.

### 1. Lock The Current Deployment Contract

Agree on the current contract for local Unity deployment:
- Unity remains the trigger surface for Phase 1
- deploy target remains a pre-existing host reachable by SSH
- deployment still targets static WebGL output
- no DNS/nginx automation yet in Phase 1 unless explicitly added

This avoids blending Phase 1 hardening with Phase 2 platform expansion.

### 2. Define The Release Directory Structure

Pick a release layout now so Phase 1 and Phase 2 do not diverge later.

Recommended pattern:

```text
{spaceRoot}/
  current -> releases/{buildId}/
  releases/
    {buildId}/
      index.html
      Build/
      TemplateData/
      manifest.json
```

Required decision:
- whether `{spaceRoot}` remains `{remotePath}/{roomName}-{spaceId}/`
- or whether space root becomes `{remotePath}/{spaceId}/` with room name only in metadata

### 3. Define The Deployment Manifest Schema

Create a minimal manifest format before coding.

Recommended fields:
- `buildId`
- `spaceId`
- `roomName`
- `worldDisplayName`
- `buildVersion`
- `buildTimestamp`
- `publicUrl`
- `sourceMachine`
- `unityVersion`
- `deployMethod`
- `artifactChecksum`

This will become the base for deploy history and rollback later.

### 4. Decide The Post-Deploy Verification Rules

Phase 1 needs a strict success definition.

Recommended checks:
- remote release directory exists
- expected files exist: `index.html`, loader, `.data`, `.wasm`, framework file
- final public URL returns HTTP 200
- optional: verify Cloudflare headers if traffic is expected through proxy

Deployment should not report success unless these checks pass.

### 5. Separate Stage Statuses In Code

Define deployment stages now so the UI and logs can evolve without rework.

Recommended stages:
1. validate local inputs
2. authenticate/connect
3. prepare remote release
4. upload artifact
5. verify remote files
6. activate release
7. verify public URL
8. complete

Even if the first version shows simple text only, the internal stage model should exist.

### 6. Decide Timeout And Retry Policy

The current fixed 30-second transfer timeout is not sufficient for production.

Define:
- SSH command timeout
- transfer timeout
- post-deploy HTTP verification timeout
- whether retries are allowed for transient failures

Recommended policy:
- SSH preflight timeout: short
- transfer timeout: size-aware or profile-configurable
- public verification timeout: medium with a few retries

### 7. Define Environment Support Boundaries

Even if full environment support is Phase 3, Phase 1 should not block it.

Prepare for:
- `dev`
- `staging`
- `prod`

At minimum, ensure deployment metadata and server profiles can represent environment identity cleanly.

### 8. Create A Manual Rollback Runbook First

Even before one-click rollback exists, Phase 1 should produce enough release structure that rollback can be performed manually and safely.

Document:
- where release directories live
- how `current` is switched
- how to restore a previous release
- how to verify restoration

### 9. Define What Stays Editor-Side vs Moves Later

Phase 1 should keep implementation scoped.

Editor-side in Phase 1:
- build selection
- runtime metadata preparation
- upload trigger
- local status display

Deferred to later host API:
- nginx generation
- DNS automation
- secrets vaulting
- org/team deployment authorization

### 10. Identify The Minimum Acceptance Test Matrix

Before coding, define the acceptance matrix.

Minimum cases:
- successful deploy to empty new space path
- successful redeploy to existing space
- SSH auth failure
- remote write permission failure
- partial upload failure
- post-deploy URL verification failure
- manual rollback to previous release

---

## Phase 1 Implementation Tasks

### Core Fixes

- fix runtime config `deploymentURL` to use the final dynamic space URL
- ensure all editor UI calls happen on the main thread
- fix non-Windows `scp` source path behavior
- replace the fixed transfer timeout with configurable stage timeouts

### Release Model

- generate a `buildId`
- upload into `releases/{buildId}/`
- write `manifest.json`
- activate deployment by updating a `current` pointer or equivalent

### Verification

- verify remote expected files exist
- perform final public URL verification
- fail deployment if verification fails

### Logging

- produce structured per-stage log output
- capture deploy summary in a machine-readable form

---

## Proposed Target Architecture

### Phase 1

```text
Unity Editor
  -> SSH preflight
  -> upload versioned release
  -> activate release
  -> verify public URL
```

### Phase 2+

```text
Unity Editor or Dashboard
  -> Deployment API on host
      -> create release
      -> write runtime config
      -> generate nginx config
      -> validate/reload nginx
      -> activate release
      -> verify public URL
      -> return status/logs
```

---

## Recommended Immediate Next Actions

1. Fix the runtime `deploymentURL` inconsistency.
2. Design the release directory layout and manifest schema.
3. Add versioned release deployment instead of syncing directly into the live directory.
4. Add post-deploy file and URL verification.
5. Replace the fixed transfer timeout with a profile-driven policy.
6. Keep nginx/DNS automation out of Phase 1 unless explicitly prioritized.
7. Start Phase 2 design in parallel only after Phase 1 release structure is stable.

---

## Phase 1 Implementation Checklist

This checklist turns Phase 1 into file-level work so implementation can proceed without re-planning the whole deployment surface.

### A. Fix Runtime Metadata Consistency

Goal:
Ensure runtime config always records the actual final deployed URL and release metadata.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- `Assets/MetaDyn/Core/Runtime/MetaDynRuntimeConfig.cs`

Tasks:
- update runtime config after the dynamic per-space URL is computed, not before
- add any missing runtime metadata fields needed for release tracking
- ensure the final deployed URL written to runtime config matches the actual published space path
- decide whether `buildId` belongs in runtime config or only in the deploy manifest

Acceptance:
- deploying a space with subfolder suffix writes the exact final public URL into runtime config
- runtime config metadata matches the deploy result shown in the editor

### B. Introduce Structured Deployment Stages

Goal:
Make deployment status explicit and consistent across UI, logs, and future automation.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`

Tasks:
- define internal deployment stages as named constants or enum values
- emit stage transitions through the existing callback path
- stop passing `null` for deployment progress/status
- ensure all editor-facing state updates are marshaled back to the main thread
- remove any direct editor dialog calls from background worker threads

Acceptance:
- the editor shows stage-based status during deploy
- failures identify the stage that failed
- no Unity editor UI API is called from worker threads

### C. Replace Direct-To-Live Upload With Versioned Releases

Goal:
Deploy into versioned release directories rather than directly into the live path.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynServerProfile.cs`

Tasks:
- generate a `buildId` per deployment
- derive a release path under the space root
- upload into `releases/{buildId}/`
- define how the active release is exposed:
  - `current` symlink preferred on Linux hosts
  - fallback alternative if symlink approach is not acceptable on all targets
- preserve existing space isolation semantics

Acceptance:
- each deployment lands in a unique release directory
- the active/public path can be switched without overwriting prior releases
- the previous release remains available for rollback

### D. Add Deployment Manifest Generation

Goal:
Capture machine-readable deployment metadata for history, debugging, and rollback support.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- optional new file: `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManifest.cs`

Tasks:
- define a serializable manifest model
- generate `manifest.json` before upload or as part of the release payload
- include:
  - `buildId`
  - `spaceId`
  - `roomName`
  - `worldDisplayName`
  - `buildVersion`
  - `buildTimestamp`
  - `publicUrl`
  - `unityVersion`
  - `deployMethod`
- decide whether to include file checksums in Phase 1 or defer to Phase 2

Acceptance:
- every release directory contains a manifest
- manifest values match the actual deploy target and runtime config

### E. Add Remote File Verification

Goal:
Do not mark deployment successful unless the expected files exist on the host after transfer.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`

Tasks:
- define the minimum required file set for a valid Unity WebGL deployment
- add an SSH verification command after transfer completes
- validate presence of:
  - `index.html`
  - `Build/`
  - expected loader/framework/data/wasm files
- fail deploy if the remote release is incomplete

Acceptance:
- partial uploads are detected
- deployment success requires remote file verification to pass

### F. Add Public URL Verification

Goal:
Do not report success until the space is reachable from its final public URL.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- optional new file: `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentVerifier.cs`

Tasks:
- perform an HTTP verification against the final URL after activation
- check for a successful response from `index.html` or another known entry asset
- add retry behavior for short propagation or origin warm-up delays
- produce actionable failure messages when public verification fails

Acceptance:
- successful deployment means the public URL actually responds
- public verification failures are distinguished from SSH/upload failures

### G. Fix Cross-Platform Transfer Edge Cases

Goal:
Make the deployer safe across Windows and non-Windows editor environments.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`

Tasks:
- fix `scp` source path handling for macOS/Linux
- audit path quoting in all SSH/`rsync`/`scp` commands
- standardize path normalization for local and remote paths
- verify command discovery behavior outside Linux shells if relevant

Acceptance:
- fallback `scp` path works on supported editor OSes
- quoted paths do not break deployment when directories contain spaces

### H. Replace Fixed Transfer Timeout Policy

Goal:
Use stage-appropriate timeout settings rather than a single hard-coded transfer timeout.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynServerProfile.cs`

Tasks:
- separate SSH preflight timeout from transfer timeout
- add configurable transfer timeout fields to server profile if needed
- add verification timeout settings for post-deploy checks
- define sensible defaults for internal production use

Acceptance:
- large WebGL uploads do not fail due to an arbitrary fixed timeout
- timeout failures clearly indicate which stage timed out

### I. Improve Connection Test Into A Real Deploy Preflight

Goal:
Turn the current network reachability check into a deploy-relevant validation.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`

Tasks:
- keep port reachability test if useful
- add optional SSH auth validation
- add remote write test for the target root or a disposable temp path
- surface whether the profile is actually deploy-ready, not just reachable

Acceptance:
- “Test Connection” can distinguish:
  - network unreachable
  - SSH auth failure
  - permission denied on target path
  - deploy-ready success

### J. Add Manual Rollback Support Artifacts

Goal:
Make rollback operationally possible even before a one-click rollback UI exists.

Files:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `.claude/Quick Reference/INFRASTRUCTURE.md`
- optional new runbook doc under `.claude/Planning/`

Tasks:
- preserve prior releases on deploy
- define how to determine the currently active release
- document the manual rollback procedure
- ensure deploy logs identify the build ID that was activated

Acceptance:
- an operator can restore the prior release using the documented procedure
- rollback does not require reconstructing lost metadata manually

### K. Add Phase 1 Acceptance Verification

Goal:
Close Phase 1 with explicit validation instead of informal testing.

Files:
- optional new checklist doc under `.claude/Planning/`
- test support may stay manual if no test harness exists yet

Tasks:
- run a successful deploy to a new space path
- run a successful redeploy to an existing space
- verify release directory structure on host
- verify manifest contents
- verify runtime config final URL
- simulate a failed upload and confirm failure behavior
- confirm manual rollback works

Acceptance:
- all defined scenarios pass
- deployment is stable enough to serve as the base for Phase 2

---

## Source References

- `.claude/Quick Reference/DEPLOYMENT_ARCHITECTURE.md`
- `.claude/Quick Reference/INFRASTRUCTURE.md`
- `.claude/Space_URL_Routing_Strategy.md`
- `.claude/Planning/Build_Server_Distribution_Plan.md`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynServerProfile.cs`
- `Assets/MetaDyn/Core/Runtime/MetaDynRuntimeConfig.cs`
