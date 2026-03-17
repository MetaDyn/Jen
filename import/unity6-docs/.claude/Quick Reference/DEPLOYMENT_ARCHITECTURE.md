# Deployment Architecture

Comprehensive reference for MetaDyn deployment architecture, hosting models, runtime configuration, and SDK-integrated deployment tooling.

**Status:** Active Planning Reference | **Last Updated:** 2026-03-07

---

## Purpose

This document exists because deployment/infrastructure is now a core part of the MetaDyn platform and SDK story, not just an internal ops concern.

Use this document to align on:
- how MetaDyn spaces are hosted and deployed
- how the Unity SDK participates in deployment
- how self-hosting and shared hosting should coexist
- what is configured in Unity vs dashboard/backend
- how each space/build is isolated

This document complements, but does not replace:
- `INFRASTRUCTURE.md`
- `AUTH_SYSTEM.md`
- `SDK_DEVELOPMENT.md`
- `SDK_UPDATE_MANIFEST.md`

---

## Executive Summary

MetaDyn deployment is currently built around:

- Unity WebGL builds
- Cloudflare-proxied delivery
- SSH/rsync/scp deployment from the Unity Editor
- runtime configuration via `MetaDynRuntimeConfig`
- dashboard-linked metadata and auth

Confirmed planning direction:

- MetaDyn will support **self-hosting** and **shared hosting** models
- each space is deployed as **its own build**
- deployment tooling is an **integral part of the SDK**
- infrastructure should be **partially configurable from the dashboard**

---

## Hosting Models

### 1. Self-Hosted

MetaDyn customers/partners can deploy their own space builds to infrastructure they control.

Expected characteristics:
- custom server profile
- custom remote path / domain routing
- customer-owned or partner-owned hosting environment
- MetaDyn SDK deployment tooling still used where appropriate

Use cases:
- enterprise/private deployments
- white-label environments
- agency-managed client hosting
- custom security/compliance requirements

### 2. Shared Hosting (Spatial-style Platform Model)

MetaDyn also supports a managed/shared hosting model similar in spirit to Spatial.io.

Expected characteristics:
- MetaDyn-managed infrastructure
- shared hosting patterns across many spaces
- dashboard-driven provisioning and metadata
- standardized delivery/runtime behavior

Use cases:
- creators who do not want to manage hosting
- platform-native published spaces
- simpler onboarding and managed deployment

### Planning Implication

The deployment system must support both:
- direct deployment to specific server profiles
- future managed/shared platform deployment flows

This means deployment should be thought of as a **platform capability**, not only a developer utility.

---

## Space Deployment Model

### Canonical Rule

Each MetaDyn space is its **own build**.

This is the current intended model and should be treated as source-of-truth unless deliberately redesigned later.

Implications:
- each space has its own deployable WebGL output
- each space has isolated deployment destination/path
- each space can carry its own runtime config and ownership context
- deployment/update behavior should not assume many spaces share one runtime build

### Current Path Pattern

Documented deployment pattern:

```text
{profile.remotePath}/{roomName}-{spaceId}/
```

Benefits:
- isolated space directories
- stable per-space URLs
- easier rollback and content separation
- closer to production platform expectations

---

## Current Deployment Tooling

### Unity Editor Entry Points

Deployment is currently driven from Unity Editor tools:

- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynServerProfile.cs`

### Current Flow

1. Choose/build WebGL output
2. Select runtime config
3. Select server profile
4. Deploy from Unity Editor
5. Remote directory is created over SSH
6. Files are uploaded via `rsync` or `scp`
7. Space becomes accessible at deployed URL

### Recommended Dev vs Prod Environment Pattern (Current Codebase)

If MetaDyn wants a separate development environment such as `dev.pavilion.metadyn.xyz` while keeping production at `pavilion.metadyn.xyz`, the cleanest approach with the current Unity tooling is:

- separate source-control branches
- separate server profiles
- separate runtime-config values per environment
- separate nginx hostnames pointing at different deployed roots

Recommended branch model:

- `main` or `production`
  - production-ready source
  - deploys to `pavilion.metadyn.xyz`
- `develop`
  - active development/integration source
  - deploys to `dev.pavilion.metadyn.xyz`

Recommended Unity asset/config model:

- **Production server profile**
  - `profileName`: `Production Server`
  - `remotePath`: `/var/www/unity-webgl/pavilion`
  - `deployedURL`: `https://pavilion.metadyn.xyz`

- **Development server profile**
  - `profileName`: `Development Server`
  - `remotePath`: `/var/www/unity-webgl/dev-pavilion`
  - `deployedURL`: `https://dev.pavilion.metadyn.xyz`

- **Production runtime config values**
  - production `spaceId`
  - production `ownerId`
  - production `roomName` (for example `PavilionProd`)

- **Development runtime config values**
  - separate dev `spaceId`
  - same or separate `ownerId` as desired
  - dev `roomName` (for example `PavilionDev`)

Important current-code behavior:

- `MetaDynProjectConfig` clones the selected server profile and appends `/{roomName}-{spaceId}/` to both `remotePath` and `deployedURL` during deployment.
- That means a dev deployment configured with `https://dev.pavilion.metadyn.xyz` becomes:

```text
https://dev.pavilion.metadyn.xyz/{roomName}-{spaceId}/
```

not the bare hostname root, unless the deploy logic is intentionally changed later.

Practical implication:

- if the current code is kept, nginx should point each hostname at the specific deployed subfolder
- if the desired UX is a bare-root environment URL, the deployment/path strategy must be adjusted

### Concrete Example

Production:

```text
Branch: main
Profile remotePath: /var/www/unity-webgl/pavilion
Profile deployedURL: https://pavilion.metadyn.xyz
Runtime roomName: PavilionProd
Runtime spaceId: 11111111-1111-1111-1111-111111111111
Final deployed directory: /var/www/unity-webgl/pavilion/PavilionProd-11111111-1111-1111-1111-111111111111/
Final public URL: https://pavilion.metadyn.xyz/PavilionProd-11111111-1111-1111-1111-111111111111/
```

Development:

```text
Branch: develop
Profile remotePath: /var/www/unity-webgl/dev-pavilion
Profile deployedURL: https://dev.pavilion.metadyn.xyz
Runtime roomName: PavilionDev
Runtime spaceId: 22222222-2222-2222-2222-222222222222
Final deployed directory: /var/www/unity-webgl/dev-pavilion/PavilionDev-22222222-2222-2222-2222-222222222222/
Final public URL: https://dev.pavilion.metadyn.xyz/PavilionDev-22222222-2222-2222-2222-222222222222/
```

### Nginx Host Sketch

Using the existing static Unity hosting template approach, the server can expose both environments with separate hostnames:

```nginx
server_name pavilion.metadyn.xyz;
root /var/www/unity-webgl/pavilion/PavilionProd-11111111-1111-1111-1111-111111111111;
```

```nginx
server_name dev.pavilion.metadyn.xyz;
root /var/www/unity-webgl/dev-pavilion/PavilionDev-22222222-2222-2222-2222-222222222222;
```

Both can sit behind Cloudflare and use the existing `metadyn.xyz` certificate lineage pattern.

### Why Branch Separation Matters

The current project uses a single `MetaDynRuntimeConfig` resource asset at runtime.

That means:

- the values in that asset are effectively environment-specific
- if dev and prod share one branch, the asset would be edited back and forth constantly
- keeping dev values in `develop` and prod values in `main` is the least-friction model with the current implementation

### Recommended Immediate Workflow

1. Create a `develop` branch in UVC / Unity Version Control.
2. Create a `Development Server` profile asset in Unity.
3. Set the dev runtime config values in the `develop` branch.
4. Add `dev.pavilion.metadyn.xyz` in Cloudflare DNS.
5. Add an nginx site for `dev.pavilion.metadyn.xyz` using the Unity static-host pattern.
6. Deploy from the `develop` branch to the dev server profile.
7. Merge to `main` only when ready to deploy production.

### Future Improvement Option

If the desired long-term behavior is:

- production at `https://pavilion.metadyn.xyz`
- development at `https://dev.pavilion.metadyn.xyz`

with no trailing `/{roomName}-{spaceId}/` subpath, then one of these changes should happen later:

1. change deployment logic to support an environment root deployment mode, or
2. generate/update nginx roots automatically to target the latest deployed subfolder for each environment hostname

Until that is implemented, the current deployment system should be treated as **hostname + per-space subfolder**, not bare-host root deployment.

### Transfer Strategy

Current code behavior:
- `rsync` preferred
- `scp` fallback
- SSH used to create remote directories first
- non-interactive mode enforced

Key SSH behavior in current tooling:
- custom key path supported
- `BatchMode=yes`
- `StrictHostKeyChecking=no`
- remote directory is created and verified over SSH before transfer
- deployment aborts before `rsync`/`scp` if directory preflight fails
- Unity shows a blocking error dialog when directory setup cannot be confirmed

### Why This Matters

Deployment is not optional tooling around the SDK. It is a core capability of the platform and should remain part of the MetaDyn SDK experience.

---

## SDK Role In Deployment

### Confirmed Product Decision

Deployment tooling is an **integral part of the SDK**.

That means:
- it belongs in the MetaDyn SDK planning surface
- it should be considered part of the installable/editor experience
- it should evolve with the rest of the SDK, not as a disconnected internal tool

### SDK Deployment Responsibilities

The SDK should eventually be able to:
- validate deployment prerequisites
- know the supported runtime/dependency versions
- package or reference the correct build outputs
- deploy a space to its target environment
- sync runtime metadata where applicable
- report deployment status back to the creator in Unity

---

## Runtime Configuration Model

### Source of Truth

`MetaDynRuntimeConfig` is the current source of truth for space runtime settings.

Primary file:
- `Assets/MetaDyn/Core/Runtime/MetaDynRuntimeConfig.cs`

Current role includes:
- room name
- max player count
- world display name
- owner/admin context
- other per-space deployment/runtime metadata

### Current Behavior

The deployment flow uses runtime config to determine:
- which room/space is being deployed
- how the space should identify itself
- what metadata should be embedded/used by the runtime

---

## Dashboard / Backend Configuration Role

### Confirmed Direction

Infrastructure should be **somewhat configurable from the dashboard**.

This does not mean all infra state moves out of Unity.
It means the system should support a balanced split where selected infra/platform values can be managed through dashboard/backend surfaces.

### Current Examples

Already in place or partially in place:
- world display name sync with Supabase `spaces`
- editor-side auth token copied from dashboard
- metadata pull/push between Unity and dashboard/backend

### Planned Direction

Dashboard/backend should eventually be able to influence selected values such as:
- space metadata
- display name
- hosting/deployment options where appropriate
- ownership/admin context
- possibly managed-hosting deployment metadata

Unity should remain responsible for:
- build generation
- deployment initiation
- local runtime config authoring
- project-side asset references

### Practical Principle

Use the dashboard for:
- metadata
- managed hosting state
- account/space ownership context
- platform-level configuration

Use Unity for:
- build content
- scene/prefab configuration
- runtime asset wiring
- creator-side deployment initiation

---

## Domain and Subdomain Provisioning

### Product Requirement

Each deployed space should have a clear public hostname strategy.

MetaDyn should support:
- auto-generated subdomains
- creator-selected subdomains
- dashboard-managed updates to assigned subdomains

This applies especially to shared hosting.

### Recommended Default Model

When a creator creates or deploys a space:

1. MetaDyn assigns a default generated subdomain
2. The space becomes reachable immediately
3. The creator can later update/change the subdomain in the dashboard
4. Infrastructure updates the DNS + routing configuration accordingly

This gives:
- instant provisioning
- no naming bottleneck
- later customization without blocking initial deployment

### Supported Options

#### Option 1: Auto-Generated Subdomain

MetaDyn generates a unique hostname automatically, for example:

```text
space-8f3k2.metadyn.xyz
aurora-pavilion.metadyn.xyz
world-4b91.metadyn.xyz
```

Best for:
- fast provisioning
- early platform rollout
- avoiding naming collisions
- internal/shared hosting workflows

#### Option 2: Creator-Selected Subdomain

Creator chooses a preferred hostname, for example:

```text
brand-demo.metadyn.xyz
polycount-lab.metadyn.xyz
josh-pavilion.metadyn.xyz
```

Requirements:
- availability check
- reserved word protection
- validation/sanitization rules
- collision handling

Best for:
- creator ownership
- branded identity
- cleaner public-facing URLs

#### Option 3: Unity-Assigned First, Dashboard-Editable Later

This is currently the recommended hybrid product behavior.

Flow:
1. space gets an auto-generated subdomain during provisioning or first deploy
2. creator sees it in Unity/dashboard
3. creator can later replace it in dashboard with a preferred subdomain
4. backend updates DNS and origin routing

Best for:
- least friction
- fast first deployment
- later polish/customization

#### Option 4: Custom Domain (Future)

Longer-term, MetaDyn may also support customer-owned domains such as:

```text
events.customer.com
metaverse.brand.com
portal.partner.org
```

This should be considered future scope, not immediate baseline scope.

### Dashboard Role

Dashboard should eventually allow:
- viewing current assigned subdomain
- seeing whether it is auto-generated or custom-selected
- requesting a new preferred subdomain
- seeing deployment/public URL status
- seeing DNS/routing/provisioning status if relevant

### Unity Role

Unity can:
- show the assigned subdomain after provisioning/deployment
- allow initial assignment if product flow starts in Unity
- pass desired subdomain metadata into deployment/provisioning flow

But longer-term, dashboard is the better system of record for public hostname management.

### Infrastructure Flow After Assignment

Once a subdomain is assigned or changed, the infrastructure flow should handle:

1. create/update Cloudflare DNS record
2. create/update nginx or origin routing config
3. map hostname to the correct space directory/app instance
4. verify Cloudflare proxy/SSL path
5. confirm public resolution and availability

### Cloudflare DNS Model

For a shared-hosted space, typical DNS behavior is:
- create `A` record to the shared host IP
- or create `CNAME` to the managed host target
- usually keep Cloudflare `proxied = true`

This means many different space subdomains can point to the same server, while nginx/origin routing decides which space is served.

### Hardening / Validation Requirements

Subdomain management should include:
- uniqueness checks
- reserved name restrictions
- allowed-character validation
- length limits
- rate limiting for changes
- audit trail of hostname changes
- rollback if a hostname update fails halfway through

### Recommended Product Direction

Best immediate product direction:

1. auto-generate a working subdomain by default
2. show it in Unity and dashboard
3. allow later dashboard-based rename/change
4. automate DNS + proxy/routing updates behind the scenes

This balances:
- speed
- reliability
- creator control
- infrastructure simplicity

---

## Networking and Delivery Architecture

### Current Delivery Stack

- Unity WebGL build
- nginx origin
- Cloudflare proxy/CDN
- Brotli-compressed static build assets
- WebSocket proxying for Fusion and WebRTC signaling

### Current Network Stack

- Photon Fusion Shared Mode
- WebRTC P2P voice
- Supabase-backed auth/profile context
- Cloudflare-backed routing/performance edge

### Current Scale Assumption

Documented current target:
- up to `50` users per session

Important caveat:
- voice scaling remains bandwidth-dependent because current model is WebRTC mesh
- future scale path is LiveKit SFU or similar

---

## Security / Access Considerations

### Current Deployment Access Pattern

Deployment currently relies on:
- SSH key access
- non-interactive transfer commands
- developer token auth for dashboard-backed metadata updates

### Security Considerations To Track

- `StrictHostKeyChecking=no` is convenient but should be treated as an operational tradeoff
- SSH key handling should remain explicit and documented
- dashboard/editor auth tokens stored in `EditorPrefs` should be treated carefully
- managed hosting and self-hosting may require different security expectations over time

---

## Operational Questions Already Resolved

### Hosting model?

Resolved:
- both **self-hosting** and **shared hosting** will be supported

### Is each space its own build?

Resolved:
- yes, each space is its own build

### Is deployment tooling part of the SDK?

Resolved:
- yes, deployment tooling is an integral part of the SDK

### Should infra be configurable from the dashboard?

Resolved:
- yes, at least partially / selectively

---

## Open Planning Work

These areas still need deeper specification later:

1. Managed/shared hosting provisioning flow
2. How dashboard-configurable infra options are modeled
3. How self-hosted deployment differs in UI/permissions from managed deployment
4. Future rollback/versioning strategy for deployed spaces
5. Multi-environment support (`dev`, `staging`, `prod`)
6. Deployment permissions model for teams/orgs
7. Long-term packaging of deployment tooling in the SDK distribution story

---

## Recommended Next Discussion Topics

1. Shared hosting product model
   - what exactly makes a deployment “shared hosted” vs self-hosted
2. Dashboard-configurable infra fields
   - which values live in Unity
   - which values live in dashboard/backend
3. Deployment environments
   - dev/staging/prod support
4. Deployment ownership/permissions
   - who can deploy what space and where
5. Rollback/version history
   - how failed or previous builds are recovered

---

## Related Documentation

- [INFRASTRUCTURE.md](INFRASTRUCTURE.md)
- [AUTH_SYSTEM.md](AUTH_SYSTEM.md)
- [SDK_DEVELOPMENT.md](SDK_DEVELOPMENT.md)
- [SDK_UPDATE_MANIFEST.md](SDK_UPDATE_MANIFEST.md)
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynServerProfile.cs`
- `Assets/MetaDyn/Core/Runtime/MetaDynRuntimeConfig.cs`
