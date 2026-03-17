# Perlin Noise Embodiment Enhancement Plan

## Goal

Use low-amplitude Perlin noise in the AI embodiment stack to create more natural, less robotic real-time engagement without compromising perception accuracy, navigation correctness, or user trust.

This is not a randomness plan.
It is a subtle motion-and-attention plan for making AI presence feel more alive.

---

## Why Perlin Noise Makes Sense Here

Perlin noise is useful because it produces:
- smooth continuous motion
- natural variation without sharp jitter
- repeatable behavior when seeded
- low-cost runtime modulation

For embodiment, this is better than raw random values because:
- random values create twitchy or mechanical changes
- Perlin noise creates drift, sway, and soft re-weighting that feel organic

The right use is:
- micro-movement
- attention biasing
- timing variation
- low-level modulation of already-valid behaviors

The wrong use is:
- changing correctness-critical logic
- making detection unreliable
- introducing gameplay inconsistency

---

## Core Principle

Use Perlin noise only to influence:
- how something feels
- not whether it fundamentally works

That means:
- OK: gaze drift, idle sway, soft scan bias, timing softness
- Not OK: random missed detections, unstable target lock, inconsistent auth logic, memory corruption, navigation failure

---

## Best Integration Targets

### 1. HeadLookController

**File:** `/Assets/MetaDyn/AI/HeadLookController.cs`

This is the strongest first target because head and eye behavior are where “robotic” embodiment is most obvious.

#### Good Uses

- subtle idle drift when no explicit look target is active
- tiny modulation of look position while tracking a target
- slight look-weight breathing
- minor body yaw sway while idle
- natural-feeling glance settle rather than hard-lock targeting

#### Recommended Effects

**Neutral Look Drift**
- Add slow Perlin offset to the neutral forward look point
- Makes the AI feel like it is softly surveying rather than freezing in place

**Tracking Softness**
- When tracking a user/object, apply a very small offset so the eyes/head don’t feel perfectly locked to a single point forever
- Should look like natural micro-adjustment, not distraction

**Look Weight Variation**
- Slightly modulate `_currentWeight` or target weight
- Gives a subtle feeling of changing focus intensity

**Idle Body Sway**
- If `enableBodyRotation` is active and there is no hard target, introduce a small yaw drift
- This should be extremely subtle

#### Safe Ranges

- neutral position drift: `0.02m - 0.08m`
- target tracking offset: `0.01m - 0.04m`
- look weight modulation: `+/- 0.02 - 0.05`
- idle yaw sway: `+/- 1 - 2 degrees`
- noise speed: low frequency only

#### Why This Works

- most believable embodiment gains come from head/eye motion
- small continuous motion prevents mannequin-like stillness
- can be added without changing the public API of the component

#### Risks

- too much offset makes the AI look unfocused
- too much weight modulation can feel “floaty”
- body sway during active attention can look indecisive

#### Recommendation

Start here first.
This is the highest-return, lowest-risk Perlin integration point.

---

### 2. AIPerceptionManager

**File:** `/Assets/MetaDyn/AI/AIPerceptionManager.cs`

Perlin noise makes sense here only for prioritization and cadence, not for raw detection correctness.

#### Good Uses

- slight scan cadence variation
- soft attention bias toward one nearby object/user over another
- natural alternation in which equally relevant object becomes “salient”
- subtle weighting of front/left/right preference over time

#### Good Pattern

Keep detection deterministic:
- still scan everything in radius
- still gather the same object set

Then use Perlin noise to influence:
- ranking
- salience
- which object gets surfaced as primary focus

#### Recommended Effects

**Scan Cadence Drift**
- If perception refresh ever moves to scheduled intervals, vary by small amounts
- Prevents perfectly machine-like timing patterns

**Object Interest Bias**
- Apply a temporary Perlin-based score bias to perceived objects
- Especially useful when several targets are equally close

**Directional Curiosity**
- Slightly favor objects/users in a drifting direction field
- Feels like shifting awareness rather than omniscient lock-on

#### Safe Ranges

- scan interval offset: `+/- 0.1s - 0.4s`
- salience bias: very small additive score only
- front/side bias: enough to break ties, not enough to override explicit logic

#### Important Constraint

Do **not** use Perlin noise to:
- shrink or expand perception radius dynamically in a way that changes correctness
- randomly skip users
- randomly miss objects
- suppress `OnUserDetected` events

#### Recommendation

Use Perlin noise only as a tie-breaker / attention shaper.
Never as a truth source.

---

### 3. MetaDynVoiceController

**File:** `/Assets/MetaDyn/AI/MetaDynVoiceController.cs`

This is the right place for behavioral pacing modulation after perception detects a user and before/after speech.

#### Good Uses

- slight variation in return-to-idle timing
- occasional low-priority glance triggers while waiting
- soft engagement-state modulation during silence
- tiny offsets in when the avatar re-centers after interaction

#### Recommended Effects

**Idle Engagement Drift**
- While waiting for user input, vary how “alert” the AI feels
- Can influence glance frequency or look-weight floor

**Return-to-Neutral Softness**
- Instead of always returning to neutral on the same timing, add a smooth modulation

**Conversation Attention Rhythm**
- After speaking, let the embodiment hold attention briefly or ease out based on low-frequency noise

#### Safe Ranges

- delay variation: `+/- 0.1s - 0.5s`
- glance chance modulation: low amplitude only
- idle engagement scalar: subtle, slow-moving

#### Risks

- too much modulation can make response timing feel inconsistent
- should not interfere with actual speech, capture, or command execution

#### Recommendation

Add only after `HeadLookController` changes are working well.

---

### 4. AIEye

**File:** `/Assets/MetaDyn/AI/AIEye.cs`

This is a weaker candidate because it touches actual sensing reliability.
Use Perlin noise here only very lightly.

#### Good Uses

- slight variation in capture cooldown
- tiny pre-capture settle timing
- naturalized “blink-like” wait before certain scans

#### Safe Uses

- small offsets to visual cadence
- presentation-like timing softness

#### Unsafe Uses

- anything that reduces reliable capture when vision is explicitly requested
- anything that makes user-facing “look” commands inconsistent

#### Recommendation

Treat this as optional and conservative.
Do not prioritize it early.

---

## Where Not To Use Perlin Noise

Perlin noise should **not** drive:

- authentication logic
- memory writes
- tool/function execution
- actual movement destinations
- object detection truth
- user detection events
- navigation/pathfinding correctness
- moderation logic
- permissions
- networked identity state

These systems must remain deterministic and trustworthy.

---

## Suggested Rollout Order

### Phase 1: Head and Gaze Naturalization

Target:
- `HeadLookController`

Add:
- idle neutral drift
- micro target offset
- subtle look-weight breathing

Expected outcome:
- biggest visible embodiment improvement
- lowest risk to logic

### Phase 2: Attention Prioritization Softness

Target:
- `AIPerceptionManager`

Add:
- salience biasing
- slight scan cadence variation
- directional curiosity drift

Expected outcome:
- more natural focus switching
- less deterministic object prioritization

### Phase 3: Conversational Timing Texture

Target:
- `MetaDynVoiceController`

Add:
- return-to-neutral timing drift
- engagement-state variation
- subtle glance pacing

Expected outcome:
- more human-feeling conversational presence

### Phase 4: Optional Vision Cadence Softening

Target:
- `AIEye`

Add:
- tiny cooldown variation
- very small pre-capture settle

Expected outcome:
- slight realism gain
- low priority compared with other phases

---

## Proposed Shared Noise Parameters

If implemented cleanly, use a shared conceptual pattern:

```csharp
[Header("Perlin Noise")]
public bool enablePerlinNoise = true;
public float noiseSpeed = 0.2f;
public float noiseAmplitude = 0.05f;
public float noiseSeed = 0.0f;
```

Possible per-system variants:

### HeadLookController
- `idleNoiseAmplitude`
- `trackingNoiseAmplitude`
- `weightNoiseAmplitude`
- `yawNoiseAmplitude`

### AIPerceptionManager
- `salienceNoiseAmplitude`
- `scanIntervalNoiseAmplitude`
- `directionBiasNoiseAmplitude`

### MetaDynVoiceController
- `idleEngagementNoiseAmplitude`
- `timingNoiseAmplitude`

### AIEye
- `cooldownNoiseAmplitude`
- `captureSettleNoiseAmplitude`

---

## Implementation Pattern Recommendation

Use time-based Perlin sampling with stable offsets:

```csharp
float t = Time.time * noiseSpeed;
float n = Mathf.PerlinNoise(noiseSeed, t);
float centered = (n * 2f) - 1f; // Convert 0..1 to -1..1
```

For multiple independent channels:
- use different seed offsets
- example:
  - `noiseSeed + 10`
  - `noiseSeed + 20`
  - `noiseSeed + 30`

This avoids correlated motion on every axis.

---

## Specific Recommendations By File

### `/Assets/MetaDyn/AI/HeadLookController.cs`

Add:
- `enableIdleNoise`
- `idleNoiseAmplitude`
- `trackingNoiseAmplitude`
- `weightNoiseAmplitude`
- `noiseSpeed`
- seeded X/Z offsets for neutral and tracking states

Best place to apply:
- inside `OnAnimatorIK()` before final `SetLookAtPosition`
- optionally in `Update()` for idle body yaw offset

### `/Assets/MetaDyn/AI/AIPerceptionManager.cs`

Add:
- per-object salience bias method
- optional scan cadence timer if moving away from fully on-demand scans
- directional curiosity value derived from Perlin noise

Best place to apply:
- after `ScanEnvironment()` has collected objects
- before final sorting/selection of highest-interest items

### `/Assets/MetaDyn/AI/MetaDynVoiceController.cs`

Add:
- engagement drift scalar
- soft return timing modulation
- optional idle glance timing helper

Best place to apply:
- idle state transitions
- post-response settle behavior
- non-critical gaze timing behavior

### `/Assets/MetaDyn/AI/AIEye.cs`

Add:
- tiny cooldown jitter
- optional settle-before-capture timer

Best place to apply:
- cooldown logic
- pre-capture timing only

---

## Design Guardrails

To keep this feeling good:

- low amplitude
- low frequency
- deterministic seeds per agent
- explicit disable toggle in inspector
- no effect on correctness-critical paths
- easy rollback by disabling one bool

If the user can consciously notice the noise most of the time, it is probably too strong.

---

## Success Criteria

This enhancement is successful if:

- the AI feels less frozen when idle
- gaze feels less perfectly robotic
- attention changes feel less binary
- embodiment feels more present without becoming distracting
- no gameplay/system correctness regresses

---

## Recommended First Implementation

If only one change is made first:

**Implement Perlin-driven idle and target micro-drift in `HeadLookController`.**

That gives the highest visible quality improvement with the lowest system risk.

After that:
- add perception salience biasing
- then conversational timing modulation

---

## Summary

Best places for Perlin noise:
1. `HeadLookController` — highest value
2. `AIPerceptionManager` — attention shaping, not detection truth
3. `MetaDynVoiceController` — conversational pacing texture
4. `AIEye` — optional, conservative only

Avoid using Perlin noise anywhere that affects truth, authority, permissions, or reliability.
