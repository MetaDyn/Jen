# AI Embodiment System: Current State And Improvement Plan

**Project:** MetaDyn Pavilion  
**Date:** 2026-03-04  
**Scope:** Current implementation in this codebase + proposed improvement roadmap

---

## 1. Current State (As Implemented In Code)

The AI embodiment stack is orchestrated by `MetaDynVoiceController` and composed of:

- Perception: `AIPerceptionManager`
- Vision: `AIEye`
- Movement: `AIMovementController`
- Head/eye/body orientation: `HeadLookController`
- Long-term memory: `AIMemoryManager`
- Voice input: `MicrophoneRecorder` (+ `MicrophonePlugin.jslib` on WebGL)

### 1.1 Runtime Wiring

The active Pavilion scene instantiates `--AIAgent--.prefab` (variant chain over `AI.prefab`) and wires key references through prefab + scene overrides, including:

- Chat UI references (panel, bubble, input, send button)
- `MicrophoneRecorder`
- `HeadLookController`
- `AIMovementController`
- `Animator`
- `AIEye` camera override

### 1.2 End-To-End Behavior Flow

1. **User detection and social targeting**
   - `AIPerceptionManager` continuously finds the local input-authority player and sets/updates `activeUser`.
   - On user detection change, `OnUserDetected` fires.
   - `MetaDynVoiceController` consumes this event and sets the look target on `HeadLookController`.

2. **Conversation entry**
   - User can type or push-to-talk.
   - Voice path: `MicrophoneRecorder` emits WAV bytes to `OnRecordingCompleted`, then `MetaDynVoiceController.ProcessVoiceInput()` transcribes via Whisper.

3. **Context assembly**
   - Conversation turn is added to `_conversationHistory`.
   - First turn per interaction triggers memory recall (`AIMemoryManager.RecallMemories`).
   - Spatial context is generated live from nearby user/object/player scan (compact `[SPATIAL: ...]` string).
   - Optional vision capture (`AIEye`) is attached when vision-intent keywords are detected.

4. **Reasoning and response**
   - LLM request is sent to OpenRouter with streaming enabled.
   - Dynamic context (`[MEMORY]`, `[SPATIAL]`) is injected as system message for each request.
   - Streaming chunks render into chat bubble incrementally.

5. **Speech and animation**
   - Response text is sentence-split and sent to ElevenLabs TTS sentence-by-sentence.
   - Clips are queued in order and played via `AudioSource`.
   - Talking/idle animation triggers are driven by voice controller state.

6. **Embodied movement actions**
   - Action tags in LLM output are parsed:
     - `*walk_to:objectName*`
     - `*follow_user*`
     - `*stop_walking*`
   - Tags invoke `AIMovementController` (NavMesh-based movement).
   - While moving, `HeadLookController` is disabled; re-enabled on idle.

7. **Memory writeback**
   - User encounter is recorded on detection.
   - Auto-save can periodically summarize/store conversation.
   - On player leave, conversation is analyzed (topics/sentiment) and persisted through memory API.

### 1.3 Strengths In Current Implementation

- Clear modular components with practical separation of concerns.
- Real streaming pipeline (STT -> LLM stream -> sentence TTS queue) with interrupt support.
- Dynamic context injection avoids stale baked context.
- Embodiment loop includes perception, gaze, locomotion, and memory.
- WebGL microphone path is optimized and operational.

### 1.4 Current Gaps / Risks

1. **Security / secrets**
   - API keys are currently serialized in prefab data (high risk).

2. **Identity fidelity**
   - Memory user IDs are derived from display names, not stable auth UUIDs.

3. **Perception fragmentation**
   - `AIPerceptionManager.GetPerceptionContext()` exists but main prompt path uses a separate compact builder in `MetaDynVoiceController`.
   - This duplicates context logic and can drift.

4. **Action execution reliability**
   - Object resolution for `walk_to` is broad and name-match based; no canonical object registry.

5. **Operational resilience**
   - External services (OpenRouter, Whisper, ElevenLabs, memory API) lack centralized retry/circuit-breaker strategy.

6. **Observability**
   - No unified metrics layer for latency, fail rates, token/voice cost per session, or action execution success.

7. **Scene/prefab coupling**
   - Significant wiring is done by prefab/scene overrides, increasing fragility when duplicating scenes or prefabs.

---

## 2. Comprehensive Improvement Plan

## 2.1 Goals

1. Make AI embodiment production-safe (security + reliability).
2. Improve behavioral consistency (context, memory, movement grounding).
3. Improve maintainability (clear contracts, less duplication, fewer fragile references).
4. Improve observability and tuning speed.

## 2.2 Architecture Direction

Adopt a strict pipeline with explicit interfaces:

1. **Input Layer**
   - Text input + voice input standardized into `UserTurn`.
2. **Context Layer**
   - Single context builder service producing `ContextEnvelope` (memory + spatial + vision metadata).
3. **Reasoning Layer**
   - LLM adapter (OpenRouter provider interface, model routing policy).
4. **Embodiment Action Layer**
   - Action parser -> validated action commands -> action executor.
5. **Output Layer**
   - Speech synthesis + animation + UI feedback.
6. **Persistence/Telemetry Layer**
   - Memory storage, conversation events, metrics, traces.

---

## 2.3 Phased Delivery Plan

## Phase 0: Security And Configuration Hardening (Immediate)

**Objective:** Remove critical risk before feature expansion.

Tasks:
- Remove all hardcoded API keys from prefabs/assets.
- Introduce environment-specific config source:
  - local dev config asset (gitignored) or encrypted runtime fetch.
- Add startup validation for missing credentials with clear non-crashing error states.

Acceptance:
- No secrets in tracked prefabs/scenes.
- AI agent degrades gracefully when a provider key is absent.

## Phase 1: Identity + Memory Contract Stabilization

**Objective:** Make memory consistent across sessions/platforms.

Tasks:
- Replace display-name-based IDs with canonical auth UUID (`auth.users.id`).
- Add memory schema versioning and typed memory categories.
- Persist explicit interaction/session IDs.
- Add memory quality filters (dedupe, confidence tagging, max store frequency).

Acceptance:
- Same user is recognized across renames/devices.
- Memory recall precision improves and duplicate memories are reduced.

## Phase 2: Unified Context Engine

**Objective:** Eliminate context drift and duplicated logic.

Tasks:
- Create a dedicated `AIContextBuilder` used by voice controller.
- Consolidate spatial context into one canonical representation.
- Keep both compact context and detailed context modes (switchable by model/policy).
- Add context budget manager (token-aware truncation and priority ordering).

Acceptance:
- One source of truth for memory/spatial context.
- Stable prompt size under configurable thresholds.

## Phase 3: Action System Reliability Upgrade

**Objective:** Increase movement/action correctness and reduce hallucinated commands.

Tasks:
- Move from freeform tag parsing to structured action schema:
  - e.g., JSON command block or strict mini-language.
- Add object registry (`AIEmbodimentTargetRegistry`) for canonical target IDs/aliases.
- Add action validation and user-safe fallback responses when target not found.
- Add execution result feedback loop into next-turn context.

Acceptance:
- `walk_to` success rate is measurable and materially improved.
- Unknown targets no longer silently fail.

## Phase 4: Voice + Turn Management Robustness

**Objective:** Make conversations resilient under real WebGL/mobile conditions.

Tasks:
- Add explicit turn state machine (`Idle`, `Listening`, `Transcribing`, `Thinking`, `Speaking`, `Interrupted`, `Error`).
- Add provider fallback policy:
  - STT fallback, LLM fallback model, TTS fallback voice/provider.
- Add timeout/retry with backoff per provider adapter.
- Add explicit barge-in policy and cancellation tokens across all async tasks.

Acceptance:
- Agent recovers from transient provider failures without deadlocking conversation.
- Interrupt behavior is deterministic under rapid user input.

## Phase 5: Embodiment Quality Pass (Gaze, Movement, Social Behavior)

**Objective:** Improve believability and comfort.

Tasks:
- Smooth look-target arbitration:
  - user priority > active conversational object > neutral scan.
- Add movement constraints:
  - min personal space around user, no oscillation near stopping distance.
- Add social micro-behaviors:
  - glance, acknowledgement nod timing, idle stance variation triggers.
- Add path failure handling with alternate routes and verbal fallback.

Acceptance:
- Movement/gaze feel intentional and non-jittery.
- Fewer awkward stop/start loops near targets.

## Phase 6: Observability, Cost, And Performance

**Objective:** Operate and tune with real data.

Tasks:
- Instrument end-to-end latency segments:
  - capture, STT, LLM first token, full response, TTS first audio, action execution.
- Track provider errors, retries, and per-session cost estimates.
- Add debug HUD toggle for embodiment diagnostics (dev only).
- Add structured logs for action parse/validation/execution outcomes.

Acceptance:
- Team can identify bottlenecks and failures without deep manual log scraping.
- Cost and latency are measurable per session.

## Phase 7: Test Strategy And Production Gates

**Objective:** Prevent regressions while improving rapidly.

Tasks:
- Unit tests for:
  - context builder
  - action parsing/validation
  - memory formatting and trimming logic
- Integration tests for:
  - end-to-end turn pipeline with mocked providers
- Manual test matrix:
  - Desktop WebGL + Mobile WebGL for voice interruption/lifecycle edge cases
- Release checklist:
  - secret scan, fallback verification, metrics smoke test.

Acceptance:
- Repeated deployments with low regression rate in AI behavior pipeline.

---

## 2.4 Priority Order (Recommended)

1. Phase 0 (security/config)  
2. Phase 1 (identity/memory)  
3. Phase 2 (context unification)  
4. Phase 3 (action reliability)  
5. Phase 4 (turn robustness)  
6. Phase 6 (observability)  
7. Phase 5 (behavior polish)  
8. Phase 7 (ongoing hard gate)

---

## 2.5 Concrete Near-Term Backlog (Next 2 Sprints)

### Sprint A (Safety + Data Integrity)
- Secret removal and secure runtime config loading.
- Canonical user ID integration from auth pipeline.
- Memory write/read schema upgrade.
- Basic provider timeout/retry wrappers.

### Sprint B (Reliability + Embodiment)
- Unified context builder introduced and adopted.
- Structured action schema + target registry.
- Turn state machine and robust cancellation.
- Initial telemetry events + action success metrics.

---

## 2.6 Definition Of Done For “Embodiment vNext”

Embodiment vNext is complete when:

1. No secrets are committed in project assets.
2. Memory identity is stable and auth-backed.
3. Context injection is unified, bounded, and observable.
4. Movement actions are validated and reliably executed with clear failure handling.
5. Voice turn pipeline handles interruption and provider errors gracefully.
6. Latency/failure/cost metrics are available per session.
7. Regression tests cover core pipeline behaviors.

---

## 3. Suggested Follow-Up Documents

If desired, split this into implementation artifacts:

1. `AI_Embodiment_vNext_Technical_Design.md` (interfaces, sequence diagrams)
2. `AI_Embodiment_vNext_Task_Breakdown.md` (ticket-ready tasks with estimates)
3. `AI_Embodiment_Test_Plan.md` (automated + manual matrix)

