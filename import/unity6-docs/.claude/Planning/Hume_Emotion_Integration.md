# Hume Emotion + Blendshape Integration Plan

## Goal
Add emotion-driven facial animation for NPCs by integrating Hume AI sentiment/emotion detection with the existing lip sync and blendshape system, completing the embodied AI stack.

## Current Stack (Assumed)
- Voice capture → STT → LLM response → TTS audio output
- Lip sync already implemented (viseme/blendshape driven)
- Orchestration via `MetaDynVoiceController` and avatar face/blendshape systems

## Proposed Architecture
### 1) Emotion Inference Layer (Hume)
- Feed audio stream or buffered chunks (250–500ms windows).
- Receive emotion scores (e.g., joy, sadness, anger, fear, surprise, neutral).
- Normalize and time-stamp results.

### 2) Blendshape Mixer
- **Two channels:**
  - Lip sync (viseme/phoneme driven)
  - Emotion (Hume driven)
- Apply **weighted blending** so visemes dominate mouth region while emotion affects brow/eyes/cheeks.
- Add smoothing and decay to avoid snapping.

### 3) Avatar Controller Integration
- Map Hume emotions to a small set of stable blendshapes:
  - Joy → smile, cheek raise, eye squint
  - Sadness → brow down, mouth corners down
  - Anger → brow lower, lip tight
  - Surprise → brow up, jaw open (capped)
- Clamp or reduce weights on jaw/mouth when lip sync is active.

## Implementation Steps
1. **Audio Tap:** Add a hook to feed mic/TTS audio to Hume (stream or chunked).
2. **Emotion Service:** Build a small client wrapper to call Hume and parse scores.
3. **Emotion State:** Maintain current emotion with decay/smoothing.
4. **Blendshape Mixer:** Layer emotion weights over lip sync weights.
5. **Avatar Hook:** Apply final weights per frame to the avatar renderer.
6. **Fallback:** Default to neutral when Hume unavailable.

## Performance + UX Considerations
- Use 250–500ms windows to balance latency and accuracy.
- Smooth transitions (0.2–0.5s) to avoid popping.
- Limit to 3–5 core blendshapes for natural results.
- Provide a toggle to disable emotion in low-end WebGL.

## Open Questions
- Should emotion be inferred from **user voice**, **NPC voice**, or **both**?
- Do we want emotion to be influenced by **text sentiment** as a fallback?
- Which avatar systems (RPM, Avatar SDK) expose the needed blendshapes?

## Success Criteria
- Emotion feels natural and does not interfere with lip sync.
- Latency is not noticeable to users.
- Works in WebGL at stable frame rates.

