# Immersive Platforms

## Current Platform Stack

MetaDyn currently deploys immersive and interactive experiences across:
- Unity WebGL
- ThreeJS
- Hyperfy

## Platform Role Notes

### Unity WebGL
Used for browser-delivered immersive or interactive 3D experiences built in Unity.

### ThreeJS
Used for flexible web-native 3D environments, interfaces, visual systems, and custom immersive scenes.

### Hyperfy
Used for immersive spaces and metaverse-native world experiences.

## MetaDynAI Web AR Avatar (2026-09-27)

MetaDynAI owns the embodied-avatar product across the Dashboard-managed avatar definitions and client runtimes. The React/Three.js web client now has an additive WebXR AR mode at `/agent/:identifier/ar`; `identifier` is the same Dashboard avatar slug or GUID used by the standard `/agent/:identifier` page. The standard page keeps its existing background and controls. AR is opt-in through an **Enter AR** gesture and reuses the selected avatar profile, voice, memory, animation, and lip-sync services.

On a supported device, the AR mode requests `immersive-ar` camera passthrough, shows a hit-test reticle on a detected surface, and places the avatar for the current session. A DOM overlay keeps the conversation controls available. This is session-based placement; persistent anchors and Unity AR integration have not been established by this web work. It does not create a live Jen/OpenClaw connection.

MetaDynAI commit [`6311b7b`](https://github.com/MetaDyn/MetaDynAI/commit/6311b7b) shipped the initial route and runtime code on 2026-09-27. The user then tested the deployed [Industrial avatar](https://agentai-react1.metadyn.xyz/agent/industrial/ar) in Android Chrome, confirmed the standard Industrial page still worked, and reported successful indoor/outdoor placement, conversation, audio playback, lip sync, and response to device movement. Local screenshots in `Web/AgentAI-React/Screens/` document the permission prompt, passthrough reticle, placed avatar, and speaking UI. This is a user-observed runtime result; Jen's docs have not independently verified Netlify build logs or device behavior.

Next validation: record the device and Chrome versions; check exit/re-entry, QR entry, other avatar identifiers, and stability over longer sessions. iOS web, Meta Quest Browser, and future Meta glasses SDK/device paths need separate capability and interaction testing. The screenshots also show overlap between Send and Stop on a narrow phone layout, a mobile UI polish item. Source detail: [MetaDynAI AR implementation plan](https://github.com/MetaDyn/MetaDynAI/blob/main/Web/AgentAI-React/AR_IMPLEMENTATION_PLAN.md); the first-demo observations above come from the user's 2026-09-27 test report.

## Cross-Platform Concerns

These platforms should eventually be documented against common concerns:
- identity continuity
- presence/state synchronization
- avatar embodiment
- AI agent integration
- memory continuity
- analytics/telemetry
- asset pipelines
- deployment flow
- performance constraints

## To Be Expanded

Future additions should capture:
- what each platform is best used for
- deployment pipeline per platform
- authentication/identity model per platform
- avatar/runtime integration approach
- hosting path and CDN strategy
