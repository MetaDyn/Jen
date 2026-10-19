# MetaDyn Unity 6 Platform

This section is the curated documentation set for the current MetaDyn Unity 6 platform and SDK direction.

It is built from the imported source material under `import/unity6-docs/.claude/`, but reorganized to describe the platform in a clearer product shape: what exists now, what is already working, where the architectural seams are, and what still needs productization.

## What This Platform Is

MetaDyn’s Unity 6 work should be understood as a platform stack with several layers:
- a reusable Unity SDK/platform layer
- a starter space/template layer
- a hosted and self-hosted deployment model
- web-first identity and profile continuity
- multiplayer, moderation, and voice systems
- an emerging control-plane relationship with dashboard and backend infrastructure

That means these docs are not just “Unity project notes.” They are platform docs.

## Current Platform Snapshot

**Unity project sync: 2026-10-19.** The platform baseline below comes from the 2026-10-04 Unity documentation and public SDK release. The dated picture-frame update below reflects later Unity source and owner-reported Play Mode behavior; it is not a WebGL build, clean SDK install, or live production check.

- Engine: **Unity 6** (`6000.0.67f1` in the current Unity workspace)
- Rendering: **URP 17.0.4**
- Networking: **UGS Multiplayer Sessions 2.3.0 + NGO 2.7.0 Distributed Authority**, with Relay WSS for WebGL; Photon Fusion is historical for this Starter baseline
- Primary delivery target: **WebGL**; native is secondary
- Auth backend: **Supabase** for MetaDyn accounts and profiles, with UGS Authentication for session participants
- WebGL communication: **NGO DA room text + browser WebRTC spatial voice**; native Vivox remains supported
- SDK release: **v1.4.0 core source**, published 2026-09-26; companion browser bridges, configured player assets, and glTFast Resources materials remain outside the standalone package
- Production readiness: **open**; clean-project install and full WebGL regression gates have not been recorded as passed

## 2026-10-19 Picture Frame And Dashboard Progress

- New `MetaDynEmptyFrame` Unity source and an additive Supabase `space_picture_frames` / private `space-images` contract support images keyed by space and frame ID. The owner reported SQL setup success. The Dashboard Manage Space view supports direct file assignment and signed preview; the owner confirmed that flow works. CSV mapping preview exists, while external-URL import deployment and end-to-end verification remain pending.
- The owner joined a DA session in Unity Play Mode, saw the frame placeholder, corrected a mismatched Unity project space ID, and then saw the Dashboard-assigned image display in world space. The frame reported image revision 1. This verifies the local Editor restore path only.
- During that test, the repository agent's DA implementation had configured the scene transport while Unity Multiplayer Services replaced it with a separate DA transport, causing a WebSockets/UDP mismatch. The agent's first UDP workaround was also wrong because the installed package allows only WSS with a WebGL build target. Corrected source prepares the DA transport for WSS before joining; the owner then joined successfully in Play Mode. A fresh WebGL test is still required.
- The picture-frame MVP punch-list item remains open until browser picker/upload/restore and multiplayer behavior pass. The current public SDK is still v1.4.0 and does not contain the frame feature. If those gates pass and the addition is backward compatible, 1.5.0 is the proposed next release, with the component, storage service, WebGL picker bridge, setup guidance, and clean consumer-project installation included.

Unity implementation authority: `MetaDynStarter-UGS/.claude/SESSION_HANDOFF.md`, `.claude/Planning/Persistent_Picture_Frame_Component_Plan.md`, and `.claude/session_notes/2026-08-20_UGS_DA_MULTIPLAYER_RESTART_HANDOFF.md`.

## Recommended Reading Order

If you want the fastest solid understanding of the platform, read in this order:

1. `platform-overview.md`
2. `system-architecture.md`
3. `auth-identity.md`
4. `multiplayer-social.md`
5. `deployment-hosting.md`
6. `sdk-productization.md`
7. `realtime-voice.md`
8. `platform-deep-dive.md`
9. `import-notes.md`

## Documents In This Section

### Foundation
- `platform-overview.md` — product definition, layers, users, goals, and non-goals
- `system-architecture.md` — major technical systems and how they fit together
- `core-systems.md` — subsystem-level patterns and implementation shape
- `platform-deep-dive.md` — broader strategic reading on strengths, gaps, and long-term direction

### Identity, Presence, And Social Runtime
- `auth-identity.md` — current web-first auth bridge, Supabase-backed identity, and cross-surface continuity direction
- `security-priority-fixes.md` — current trust-boundary flaws, exploit path, and priority remediation sequence for Unity auth/identity
- `multiplayer-social.md` — player/session model, synchronized presence, moderation, and social-runtime architecture
- `realtime-voice.md` — AI voice path, player-to-player voice path, WebGL media constraints, and scale direction

### Deployment And Productization
- `deployment-hosting.md` — per-space deployment, hosting models, Cloudflare/nginx delivery, and deployment architecture
- `sdk-productization.md` — what the SDK currently is, package boundaries, updater direction, and productization gaps
- `ugs-production-sprint-summary-2026-05-25.md` — milestone summary for the completed UGS migration worklist plus mobile/WebGL, Vivox, and SDK-hardening sprint
- `open-sdk-and-hosting-model-2026-05-25.md` — open-source SDK stance, self-host vs MetaDyn-hosted model, optional MetaDyn-connected ecosystem value, and planned platform-site IA direction

### Source Mapping
- `import-notes.md` — mapping from the imported `.claude` material into this normalized doc set
- `platform-capabilities-survey-analysis-2026-01.md` — analysis of early 2026 platform capabilities survey responses, including priority signals and product implications

## What These Docs Try To Do Differently

Compared with the raw imported docs, this section tries to make a few things much clearer:
- what is implemented now versus merely planned
- which systems are platform-critical versus project-local
- where current working reality differs from older planning language
- how Unity, dashboard, identity, hosting, and voice fit together into one product story

## Important Current Reality Checks

A few points are worth keeping explicit throughout this doc set:

- MetaDyn auth is already web-first for Unity, using dashboard login plus a shared `.metadyn.xyz` cookie bridge.
- Hyperfy unified login is no longer just a future aspiration; the next documentation step is profile/data continuity across surfaces, not merely raw login parity.
- Each Unity space is currently treated as its **own build**.
- Deployment tooling is considered part of the SDK/product story, not separate internal ops garnish.
- The SDK v1.4.0 core source is released, while a clean install, companion-asset packaging, and WebGL regression coverage remain open.
- The active Starter runtime uses **UGS/NGO Distributed Authority**. The former Relay listen-server host-migration approach was rejected after runtime testing.
- WebGL room text uses the NGO DA player RPC path and browser spatial voice uses WebRTC. Native Vivox remains supported.
- Mobile browser support is now part of the practical runtime hardening track, not just a distant future aspiration.
- The current social/voice stack is meaningful and usable, but very large-room media scale will require a later SFU path.

## Verified behavior and next gates

Owner-built WebGL tests in August 2026 passed two-client DA join/spawn, roughly five minutes of movement and animation, uninterrupted departure in both directions, and rejoin. A later two-client test passed DA text delivery, bidirectional WebRTC voice, mute/unmute, and speaking indicators. These are bounded runtime observations, not a production-ready declaration.

The exact 2026-08-29 missing-join-code recovery is present in source but awaits an owner-built WebGL test. Three-player reliability, shared-object authority, broader chat/voice/avatar regression, and clean-project package installation remain open. Follow the Unity workspace `.claude/session_notes/2026-08-20_UGS_DA_MULTIPLAYER_RESTART_HANDOFF.md` and `.claude/Planning/SDK_NEXT_RELEASE_PREPARATION.md` for the detailed gates.

## Source Basis

Current sync sources: Unity workspace `.claude/CHANGELOG.md` (2026-09-26 and 2026-08-29), the multiplayer restart handoff, and `SDK_NEXT_RELEASE_PREPARATION.md`. Public SDK release: [MetaDynSDK v1.4.0](https://github.com/MetaDyn/MetaDynSDK/releases/tag/v1.4.0).

Primary source material for this section came from:
- `import/unity6-docs/.claude/Quick Reference/`
- `import/unity6-docs/.claude/Planning/`
- `import/unity6-docs/.claude/README.md`

Use the curated docs first. Drop to the raw import tree when you need exact source phrasing, historical planning context, or details that have not yet been normalized.
