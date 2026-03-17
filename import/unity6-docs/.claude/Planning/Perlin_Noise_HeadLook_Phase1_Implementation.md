# Perlin Noise HeadLook Phase 1 Implementation

## Goal

Implement a safe first pass of Perlin-noise-driven embodiment enhancement in:

- `/Assets/MetaDyn/AI/HeadLookController.cs`

This phase should:
- make idle embodiment feel more alive
- soften perfect target lock
- preserve the current public behavior of the component
- avoid destabilizing animation, IK, or body orientation

This is the recommended first Perlin-noise implementation because it offers the highest visible quality improvement with the lowest system risk.

---

## Scope

Phase 1 should include only:

1. **Idle neutral drift**
2. **Subtle target micro-drift**
3. **Minor look-weight breathing**

Phase 1 should **not** include:

- aggressive body sway
- perception ranking changes
- conversation timing changes
- blink/capture behavior changes
- movement-controller integration changes beyond preserving existing behavior

---

## Existing File

**Target file:** `/Assets/MetaDyn/AI/HeadLookController.cs`

Current behavior:
- rotates body toward `currentLookTarget` if enabled
- uses IK to smoothly interpolate look position and weight
- looks at a player’s approximate head height
- returns to neutral look when no target is active

Current strengths:
- already smooth
- already inspector-friendly
- already cleanly separated from perception logic

Current weakness:
- neutral and target gaze are still too mechanically exact

---

## Phase 1 Behavior Design

### 1. Idle Neutral Drift

When `currentLookTarget == null`, add a very small Perlin offset to the neutral look point.

Current neutral target:

```csharp
transform.position + transform.forward * 5.0f + eyeOffset
```

New behavior:
- keep this as the base target
- add small Perlin offsets in X/Y/Z
- offsets should move slowly and continuously

Visual result:
- AI feels like it is softly scanning / settling
- AI no longer feels frozen when idle

#### Safe Range

- X drift: `+/- 0.03m`
- Y drift: `+/- 0.015m`
- Z drift: `+/- 0.03m`

Keep Y especially subtle.

---

### 2. Target Micro-Drift

When `currentLookTarget != null`, keep the current exact targeting logic, but add a much smaller Perlin offset.

Purpose:
- avoid perfectly rigid lock
- simulate small eye/head corrections

This must be much weaker than idle drift.

#### Safe Range

- X drift: `+/- 0.01m - 0.02m`
- Y drift: `+/- 0.005m - 0.015m`
- Z drift: near zero or omitted

If tracking a player:
- preserve the existing `+1.5f` head-height bias first
- apply micro-drift after that

---

### 3. Look Weight Breathing

Modulate target look weight slightly with low-frequency Perlin noise.

Current:
- `targetWeight = lookWeight` when active
- `targetWeight = 0f` when neutral

New:
- when active, slightly vary around `lookWeight`
- when neutral, still fade toward zero as today

Purpose:
- creates a subtle sense of changing focus intensity

#### Safe Range

- `lookWeight +/- 0.02f`
- clamp to `[0, 1]`

This should be barely perceptible.

---

## Inspector Fields To Add

Recommended additions:

```csharp
[Header("Perlin Noise")]
[Tooltip("Enable subtle Perlin-noise-based embodiment drift")]
public bool enablePerlinNoise = true;

[Tooltip("Speed of idle drift noise")]
public float idleNoiseSpeed = 0.18f;

[Tooltip("Amplitude of idle drift in meters")]
public float idleNoiseAmplitude = 0.035f;

[Tooltip("Speed of target micro-drift noise")]
public float trackingNoiseSpeed = 0.28f;

[Tooltip("Amplitude of target micro-drift in meters")]
public float trackingNoiseAmplitude = 0.012f;

[Tooltip("Subtle variation applied to active look weight")]
[Range(0f, 0.1f)] public float weightNoiseAmplitude = 0.02f;

[Tooltip("Stable seed offset so each agent can feel slightly different")]
public float noiseSeed = 10f;
```

Optional later:

```csharp
[Tooltip("Enable subtle idle body yaw sway")]
public bool enableIdleBodySway = false;

[Tooltip("Idle body sway in degrees")]
public float idleBodyYawAmplitude = 1.0f;
```

For Phase 1, body sway can remain out of scope.

---

## Internal Helper Functions

Recommended helpers:

```csharp
private float SampleNoise(float channel, float speed)
{
    float n = Mathf.PerlinNoise(noiseSeed + channel, Time.time * speed);
    return (n * 2f) - 1f; // 0..1 -> -1..1
}

private Vector3 GetIdleNoiseOffset()
{
    return new Vector3(
        SampleNoise(10f, idleNoiseSpeed) * idleNoiseAmplitude,
        SampleNoise(20f, idleNoiseSpeed) * (idleNoiseAmplitude * 0.4f),
        SampleNoise(30f, idleNoiseSpeed) * idleNoiseAmplitude
    );
}

private Vector3 GetTrackingNoiseOffset()
{
    return new Vector3(
        SampleNoise(40f, trackingNoiseSpeed) * trackingNoiseAmplitude,
        SampleNoise(50f, trackingNoiseSpeed) * (trackingNoiseAmplitude * 0.75f),
        0f
    );
}

private float GetWeightNoise()
{
    return SampleNoise(60f, trackingNoiseSpeed * 0.5f) * weightNoiseAmplitude;
}
```

Why separate channels:
- avoids correlated movement on all axes
- prevents diagonal or synchronized drift

---

## Implementation Points In Existing File

### In `Awake()`

No major structural changes needed.

Keep:

```csharp
_currentLookPos = transform.position + transform.forward + eyeOffset;
```

Noisy initialization is not necessary.

---

### In `OnAnimatorIK(int layerIndex)`

This is the main implementation site.

Current structure:
1. determine `targetPos`
2. determine `targetWeight`
3. interpolate `_currentLookPos` and `_currentWeight`
4. apply IK

That structure should stay exactly the same.

Only modify target computation.

#### Proposed Logic

Pseudo-implementation:

```csharp
Vector3 targetPos;
float targetWeight;

if (currentLookTarget != null)
{
    targetPos = currentLookTarget.position;

    if (currentLookTarget.CompareTag("Player"))
    {
        targetPos += Vector3.up * 1.5f;
    }

    if (enablePerlinNoise)
    {
        targetPos += GetTrackingNoiseOffset();
    }

    targetWeight = lookWeight;

    if (enablePerlinNoise)
    {
        targetWeight = Mathf.Clamp01(targetWeight + GetWeightNoise());
    }
}
else
{
    targetPos = transform.position + transform.forward * 5.0f + eyeOffset;

    if (enablePerlinNoise)
    {
        targetPos += GetIdleNoiseOffset();
    }

    targetWeight = 0f;
}
```

Then leave the interpolation and IK application unchanged.

This preserves the component’s core architecture.

---

## Optional Body Sway (Not Default For Phase 1)

If added later, do it only in `Update()` and only when:

- `enableBodyRotation == true`
- `currentLookTarget == null`
- `enableIdleBodySway == true`

Use a tiny yaw offset:

```csharp
float yaw = SampleNoise(70f, idleNoiseSpeed * 0.6f) * idleBodyYawAmplitude;
```

Then apply it relative to current facing.

But again:
- this should be Phase 1 optional
- not required for the first implementation pass

---

## Debug / Tuning Recommendations

During implementation, temporarily expose:

- current idle noise vector
- current tracking noise vector
- current noise-adjusted weight

Debug logging should be optional and short-lived.
Inspector tuning is more useful than spammy logs here.

Recommended first tuning pass:

- `idleNoiseAmplitude = 0.03`
- `trackingNoiseAmplitude = 0.01`
- `weightNoiseAmplitude = 0.015`
- `idleNoiseSpeed = 0.15`
- `trackingNoiseSpeed = 0.25`

Then increase carefully if still too static.

---

## Failure Signs

Back off the values if:

- head looks unfocused during conversation
- avatar appears dizzy or distracted
- eyes feel like they are “swimming”
- look target seems inaccurate
- body and head feel disconnected

If users consciously notice the noise immediately, it is likely too strong.

---

## Success Criteria

Phase 1 is successful if:

- idle AI feels less statue-like
- gaze feels less perfectly robotic
- active attention still feels intentional
- no visible jitter appears
- no user interaction becomes less reliable

---

## Minimal Safe Rollout

If you want the lowest-risk first pass:

1. Add idle neutral drift only
2. Test
3. Add tracking micro-drift
4. Test
5. Add weight breathing last

This allows fast isolation if one layer feels wrong.

---

## Recommended Final Shape For Phase 1

**Implement in this order:**

1. `enablePerlinNoise`
2. idle drift helper
3. tracking drift helper
4. weight breathing helper
5. inspector tuning

Do not change:
- public `SetLookTarget()`
- `GlanceAt()`
- main interpolation pattern
- current player head-height bias logic

This keeps the component stable while improving embodiment quality.
