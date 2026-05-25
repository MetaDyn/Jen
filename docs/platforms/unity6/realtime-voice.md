# Unity 6 Realtime Voice And Media

This document captures the current MetaDyn Unity 6 voice architecture across both major audio paths: AI push-to-talk and player-to-player realtime voice.

## Executive Summary

Voice is one of MetaDyn’s biggest differentiators and one of its most important technical constraints.

The current Unity platform has **two distinct voice systems**:
- **AI voice interaction** — user records speech, audio is transcribed, language model responds, TTS is played back, and avatar/AI embodiment systems react
- **player-to-player realtime voice** — browser-native WebRTC enables live spatial voice chat between users in the same space

These should be documented separately but understood together, because they shape the same platform experience: embodied, social, browser-delivered presence.

## Current Production Direction Note

As of the 2026-05-25 UGS production sprint milestone, the active UGS Starter branch treats **Vivox** as the production player voice/text direction, while AI voice remains its own separate pipeline. Older WebRTC descriptions in this doc remain useful for historical context, specialized browser-media work, and legacy/reference understanding, but should not be mistaken for the declared active UGS baseline.

## Why Voice Matters In MetaDyn

MetaDyn is not aiming to be a static 3D web viewer.
It is aiming to support:
- embodied AI interactions
- social spaces with natural conversation
- persistent avatars and presence
- creator and enterprise experiences that feel alive in-world

That makes voice a core platform system rather than a feature add-on.

## The Two Voice Paths

## 1. AI Voice Interaction Path

This is the user-to-AI conversation loop.

Documented components include:
- microphone capture
- WAV encoding
- Whisper transcription
- LLM response generation through model providers
- ElevenLabs TTS playback
- animation and lip-sync triggers
- embodied AI systems that use environmental context and multimodal perception

### Important Files

Documented AI/audio files include:
- `Assets/MetaDyn/Audio/MicrophoneRecorder.cs`
- `Assets/MetaDyn/Audio/AudioUtils.cs`
- `Assets/Plugins/WebGL/MicrophonePlugin.jslib`
- `Assets/StreamingAssets/microphone-processor.js`
- `Assets/MetaDyn/AI/MetaDynVoiceController.cs`
- `Assets/MetaDyn/AI/AIPerceptionManager.cs`
- `Assets/MetaDyn/AI/AIEye.cs`
- `Assets/MetaDyn/AI/HeadLookController.cs`

### Current Behavior

The imported docs describe a push-to-talk model where the user intentionally records audio, which is then processed into the AI pipeline.

Important documented behaviors include:
- user-triggered recording flow
- browser/WebGL microphone bridge
- conversion to WAV payloads
- environmental/perception context injection
- streamed or staged TTS response playback
- avatar and head/gaze behavior that makes the AI feel embodied rather than disembodied

### Why It Matters

This is one of the clearest platform differentiators for MetaDyn. The value is not just speech recognition. It is the combination of voice, perception, embodiment, and in-world response.

## 2. Player-To-Player Realtime Voice Path

This is the user-to-user voice system.

Documented components include:
- browser-native WebRTC
- per-player WebRTC manager instances
- Fusion-backed signaling for SDP/ICE exchange
- spatial audio
- lip sync from audio levels
- async signaling queues to handle browser/mic init timing

### Important Files

Current documented files include:
- `Assets/MetaDyn/Managers/WebRTCManager.cs`
- `Assets/MetaDyn/Managers/WebRTCAudioReceiver.cs`
- `Assets/MetaDyn/Managers/WebRTCJSMessageForwarder.cs`
- `Assets/Plugins/WebGL/WebRTCVoice.jslib`
- `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`
- `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`

### Current Behavior

For the active migrated UGS branch, the current production direction is Vivox-backed player voice/text integrated with the session/user-list flow.

The imported docs also describe an earlier/current-adjacent realtime voice system that is:
- browser-native WebRTC based
- spatially aware
- integrated with avatar lip sync
- using mesh topology rather than SFU routing

That reference implementation remains important context for browser-media work and embodiment features, but the active UGS baseline should now be documented primarily through the Vivox path.

## AI Voice And Social Voice Must Be Kept Conceptually Separate

These systems share some media infrastructure concerns, but they serve different jobs.

### AI Voice
- usually intentional, interaction-driven, request/response-oriented
- tied to recording, transcription, model inference, TTS, and embodiment
- can tolerate a different latency profile than live social voice

### Social Voice
- continuous realtime conversation
- must feel immediate
- depends on network/media topology and browser constraints
- scales differently and breaks differently

Keeping these distinct in the docs prevents architecture confusion.

## WebGL Constraints

Because Unity WebGL is the primary delivery target, the voice stack must respect browser realities.

Important documented constraints include:
- user-triggered permission requirements for mic access
- `.jslib` bridge requirements for browser APIs
- performance sensitivity in the audio path
- the need for worklet/processor support in the active microphone path

A particularly important current fact from the imported docs:
- `Assets/StreamingAssets/microphone-processor.js` is required by the active microphone worklet pipeline

That file should be treated as platform-critical rather than incidental.

## Current Realtime Voice Scale Model

### What Exists Today
The current player voice system uses WebRTC mesh/P2P behavior.

### Practical Implication
This works for current room sizes, but it means each participant effectively scales their media connections with other participants. That becomes the bottleneck before the rest of the platform necessarily does.

### Current Documented Target
The imported docs repeatedly reference a current target of roughly:
- up to 50 concurrent users per session

That should be documented carefully as a current design target, not as an infinitely safe guarantee under all voice/network conditions.

## Future Scale Direction

The imported docs already identify the next scaling step for voice:
- migrate large-room voice from mesh WebRTC to an SFU-based architecture

Documented candidates include:
- LiveKit
- Cloudflare-based realtime/SFU infrastructure

### Practical Product Framing
- **short term:** current WebRTC path is appropriate for today’s product maturity and room targets
- **medium term:** larger room ambitions require an SFU
- **long term:** voice routing, moderation, permissions, and observability likely become more platformized and less scene-local

## Voice And Identity

Voice is not only a transport problem.
It also interacts with:
- authenticated identity
- player/avatar representation
- moderation permissions
- session topology
- future account-level communication and presence expectations

This is why voice docs should stay connected to auth and multiplayer docs rather than living as a purely media-layer appendix.

## What Is Already Strong

### Dual-Path Voice Architecture
MetaDyn is already thinking in terms of two separate voice products instead of forcing one stack to do everything.

### Embodied AI Integration
The AI path is not just “record audio, get text back.” It is attached to a broader embodiment system.

### Real Browser-Native Realtime Voice
The social path is concrete enough to shape scale planning and product expectations.

### Lip Sync And Presence
Voice is tied back into avatars, which matters a lot for immersion and perceived quality.

## What Still Needs Sharper Documentation Or Hardening

1. explicit operational guidance on verified room-size expectations under real network conditions
2. clearer documentation for voice moderation and mute/admin behaviors in relation to account identity
3. a future migration plan document for SFU adoption once room sizes or event use cases demand it
4. sharper documentation of browser support edges and fallback behavior
5. observability guidance for voice failures in production deployments

## Recommended Documentation Position

The curated docs should describe current voice status as:
- already one of MetaDyn’s defining platform strengths
- real enough to be architecturally important today
- not yet the final scale architecture for very large spaces

That is the accurate middle ground.

## Source Basis

Primary imported sources used in this synthesis:
- `import/unity6-docs/.claude/Quick Reference/INFRASTRUCTURE.md`
- `import/unity6-docs/.claude/Quick Reference/QUICK_REFERENCE.md`
- `import/unity6-docs/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`
- `import/unity6-docs/.claude/Planning/WebRTC_Scaling_Options.md`
- `import/unity6-docs/.claude/Planning/MetaDyn_Platform_PRD_v1.0.md`
TOOLKIT_INVENTORY.md`
- `import/unity6-docs/.claude/Planning/WebRTC_Scaling_Options.md`
- `import/unity6-docs/.claude/Planning/MetaDyn_Platform_PRD_v1.0.md`
