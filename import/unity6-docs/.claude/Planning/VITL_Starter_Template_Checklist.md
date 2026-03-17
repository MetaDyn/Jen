# VITL Starter Template Checklist

Basic checklist for using the current Pavilion + MetaDyn SDK codebase as the starter template for a new client project under `vitl.world`.

**Date:** 2026-03-12
**Status:** Working checklist

---

## Goal

Use the existing Pavilion project as the baseline Unity/WebGL starter, keep the reusable MetaDyn platform layer intact, and stand up a branded VITL world with the minimum required changes to:

- scene/content
- runtime config
- auth/dashboard wiring
- deployment
- domain routing

This is a migration checklist, not a full product spec.

---

## Important Current Constraint

The current auth implementation is designed around shared-cookie SSO on `*.metadyn.xyz`.

That means:

- `dashboard.metadyn.xyz` can authenticate users for `pavilion.metadyn.xyz`
- the current cookie pattern does **not** automatically work on `vitl.world`
- a custom-domain auth handoff flow is required if VITL must authenticate directly on `vitl.world`

Recommended rollout:

1. Launch the VITL space first on a MetaDyn-controlled hostname
2. Confirm branding, deployment, and space configuration work
3. Add `vitl.world` routing after deciding whether it is:
   - a public alias only, or
   - a fully authenticated custom domain with token handoff

---

## Template Boundary

Treat these areas as the reusable starter platform:

- `Assets/MetaDyn/`
  - SDK/runtime/editor/auth/deployment systems
- `Assets/Pavilion/Scripts/`
  - baseline player/session/game flow
- `Assets/Common/`
  - shared UI such as launcher/menu flow
- `Assets/Plugins/WebGL/`
  - browser integration such as auth bridge and WebRTC bridge

Treat these areas as project/client-specific and expected to change:

- `Assets/Pavilion/MetaDynPavilion.unity`
- environment art, branding, media, lighting, skybox
- avatar curation
- runtime config assets
- deployment profile assets

---

## Phase 1: Create VITL Project Baseline

- [ ] Create a dedicated VITL branch or repo from the current Pavilion codebase
- [ ] Keep `Assets/MetaDyn/` intact as the shared platform layer
- [ ] Duplicate the Pavilion scene and rename it for VITL
- [ ] Decide whether VITL remains inside this repo short-term or becomes its own project repo
- [ ] Preserve the current Unity/URP/Fusion versions unless there is a specific reason to change them

Recommended naming:

- Scene: `VITLWorld.unity`
- Runtime config: `VITL_Prod.asset` and `VITL_Dev.asset`
- Server profiles: `VITL Production Server` and `VITL Development Server`

---

## Phase 2: Rebrand the Starter Experience

- [ ] Replace Pavilion naming in visible UI with VITL naming
- [ ] Replace logos, splash assets, icons, and any MetaDyn/Pavilion client-facing media that should be white-labeled
- [ ] Set `worldDisplayName` for the VITL runtime config
- [ ] Review default scene objects for Pavilion-specific signage or environment references
- [ ] Decide whether MetaDyn branding stays as “powered by” or is hidden from the client-facing scene

Likely touch points:

- `Assets/MetaDyn/Media/`
- `Assets/Common/`
- scene objects in `Assets/Pavilion/MetaDynPavilion.unity`
- `MetaDynRuntimeConfig.worldDisplayName`

---

## Phase 3: Create VITL Runtime Config

Create dedicated runtime config assets instead of reusing Pavilion values.

- [ ] Create a VITL production runtime config
- [ ] Create a VITL development runtime config
- [ ] Set a unique `spaceId` for each environment
- [ ] Set the correct `ownerId` for the VITL space owner/admin account
- [ ] Set `roomName` values that are stable and environment-specific
- [ ] Set `worldDisplayName` to the public-facing VITL world name
- [ ] Set `maxPlayers` to the intended session cap for launch
- [ ] Verify the runtime config asset is the one selected during build/deploy

Suggested initial values:

- Production `roomName`: `VITLProd`
- Development `roomName`: `VITLDev`
- Production hostname target: `vitl.metadyn.xyz` or similar MetaDyn-controlled host before custom domain cutover

Relevant code:

- `Assets/MetaDyn/Core/Runtime/MetaDynRuntimeConfig.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`

---

## Phase 4: Auth and Dashboard Wiring

Decide which of these two launch modes applies.

### Option A: Fastest Path, MetaDyn-Hosted Auth First

- [ ] Keep dashboard login on `dashboard.metadyn.xyz`
- [ ] Launch VITL first on a MetaDyn subdomain
- [ ] Point the Unity build’s `WebAuthBridge.dashboardUrl` to the MetaDyn dashboard
- [ ] Keep shared-cookie SSO as-is
- [ ] Verify VITL users can authenticate and return into the VITL world

Use this option if the priority is fast launch with minimal auth engineering.

### Option B: Direct Authenticated Launch on `vitl.world`

- [ ] Define the auth handoff flow from MetaDyn dashboard to `vitl.world`
- [ ] Decide whether the return mechanism uses:
  - short-lived signed token, or
  - short-lived exchange code
- [ ] Update dashboard login flow to redirect back to `https://vitl.world/...`
- [ ] Add client-domain token consumption logic on the Unity/web shell side
- [ ] Update logout behavior because current cookie clearing logic is hardcoded for `.metadyn.xyz`
- [ ] Validate that unauthenticated visits to `vitl.world` can complete login and return successfully

Use this option only if VITL must use the custom domain for authenticated sessions immediately.

Current code/docs that matter:

- `Assets/MetaDyn/Dashboard/WebAuthBridge.cs`
- `Assets/Plugins/WebGL/AuthBridge.jslib`
- `.claude/Quick Reference/AUTH_SYSTEM.md`

---

## Phase 5: Deployment Setup

- [ ] Create a VITL production server profile asset
- [ ] Create a VITL development server profile asset
- [ ] Set unique remote paths so VITL deployments do not mix with Pavilion files
- [ ] Set `deployedURL` values for both environments
- [ ] Confirm the final URL pattern includes `/{roomName}-{spaceId}/`
- [ ] Configure nginx roots to point at the actual deployed subfolder
- [ ] Configure Cloudflare DNS/proxy for the chosen VITL hostnames
- [ ] Run the first deployment from the selected runtime config + server profile pair

Suggested initial host split:

- Development: `dev-vitl.metadyn.xyz`
- Production: `vitl.metadyn.xyz`
- Later custom domain alias: `vitl.world`

Suggested remote paths:

- `/var/www/unity-webgl/dev-vitl`
- `/var/www/unity-webgl/vitl`

Relevant docs:

- `.claude/Quick Reference/DEPLOYMENT_ARCHITECTURE.md`
- `.claude/Quick Reference/INFRASTRUCTURE.md`

---

## Phase 6: Scene and Content Conversion

- [ ] Remove Pavilion-specific environment elements that do not belong in the VITL world
- [ ] Replace hero environment assets with VITL-approved art/content
- [ ] Rebuild lighting if scene materials or skybox change significantly
- [ ] Re-bake NavMesh if geometry changes affect walkable space
- [ ] Review spawn points and entrance flow
- [ ] Review interactables, projection surfaces, and any demo props left from Pavilion
- [ ] Curate the avatar list for the VITL experience
- [ ] Remove unused test assets from the client-facing build path where practical

Minimum scene review areas:

- player spawn flow
- UI visibility on WebGL/mobile
- audio/video surfaces
- AI agent presence, if not part of VITL scope

---

## Phase 7: Platform Feature Selection

Decide what VITL actually inherits from the platform on day one.

- [ ] Authentication
- [ ] User list / moderation
- [ ] Voice chat / WebRTC
- [ ] AI embodiment features
- [ ] Dashboard-managed space metadata
- [ ] Projection surfaces / media screens
- [ ] Avatar persistence

Recommended launch posture for a first client migration:

- Keep auth
- Keep runtime config + deployment tooling
- Keep user/session basics
- Enable voice only if the VITL use case clearly needs it
- Disable AI-specific features unless they are part of the sold scope

This reduces client complexity and avoids dragging in every Pavilion demo feature by default.

---

## Phase 8: Domain Cutover Plan for `vitl.world`

Only do this after the MetaDyn-hosted VITL environment is stable.

- [ ] Decide whether `vitl.world` is:
  - primary launch domain, or
  - branded alias to a MetaDyn-hosted canonical URL
- [ ] Add DNS records for `vitl.world` and any needed `www` or subdomain entries
- [ ] Provision SSL for the VITL domain on the target host/proxy
- [ ] Add nginx routing for the VITL domain
- [ ] Decide whether the canonical authenticated URL remains under `*.metadyn.xyz`
- [ ] If direct auth is required on `vitl.world`, implement custom-domain auth handoff before launch
- [ ] Verify redirects, caching headers, and asset loading under the new host

Recommended near-term pattern:

- Canonical authenticated app: `vitl.metadyn.xyz`
- Custom brand domain: `vitl.world`
- Promote `vitl.world` publicly only after auth behavior is fully defined

---

## Phase 9: Launch Readiness Checklist

- [ ] VITL runtime config is using correct `spaceId`, `ownerId`, and `roomName`
- [ ] Production build deploys to the intended VITL URL
- [ ] Login flow works for the chosen domain strategy
- [ ] VITL branding is visible and Pavilion branding is removed where required
- [ ] Spawn flow and avatar selection work in WebGL
- [ ] Voice/auth/AI features match the actual client scope
- [ ] Basic moderation/admin ownership is assigned correctly
- [ ] Production URL, owner account, and deployment path are documented

---

## Recommended First Implementation Order

1. Fork/branch the Pavilion starter into a VITL working line
2. Create VITL runtime config assets
3. Create VITL server profile assets
4. Rebrand the scene/UI
5. Deploy to `dev-vitl.metadyn.xyz`
6. Validate auth and launch flow on the MetaDyn domain
7. Convert the scene/content for VITL
8. Deploy production to `vitl.metadyn.xyz`
9. Decide whether `vitl.world` is an alias or a full custom-domain auth surface

---

## Open Decisions

- [ ] Will VITL have its own dashboard experience, or reuse the current MetaDyn dashboard?
- [ ] Is `vitl.world` required for authenticated launch on day one?
- [ ] Does VITL need voice/chat/AI in v1, or just the core world shell?
- [ ] Does VITL need a separate repo/package boundary from Pavilion immediately?
- [ ] Is the deliverable a one-off client world or a repeatable white-label starter model?

