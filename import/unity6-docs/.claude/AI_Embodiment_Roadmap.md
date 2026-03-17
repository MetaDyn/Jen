# MetaDyn AI Embodiment System: Evaluation & Feature Roadmap

**Date:** 2025-12-30
**Purpose:** Strategic analysis of current AI perception system and roadmap for industry-leading embodied AI

---

## Executive Summary

MetaDyn's current AI embodiment system is **remarkably solid for an independent platform** and already implements several features that competitors like Inworld and Convai charge premium prices for. However, there are significant opportunities to leapfrog the competition by implementing features that don't exist anywhere yet—or exist only in academic research.

**Current Grade:** B+ (Strong foundation, production-ready)
**Potential Grade:** A++ (Industry-leading with proposed features)

---

## Part 1: Current System Analysis

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MetaDynVoiceController                       │
│              (Orchestration Hub - Production Edition)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │AIPerception  │  │   AIEye      │  │  HeadLookController  │  │
│  │Manager       │  │   (Vision)   │  │  (IK Movement)       │  │
│  │(Spatial)     │  │              │  │                      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │              │
│         ▼                 ▼                      ▼              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 LLM Context Injection                    │   │
│  │     (Perception JSON + Vision Base64 + User Message)     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              OpenRouter (Gemini 1.5/2.0 Flash)           │   │
│  │                     Streaming Response                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               ElevenLabs TTS (Streaming)                 │   │
│  │            + Wolf3D Lip Sync + Animator Triggers         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component-by-Component Analysis

#### 1. AIPerceptionManager (The "Visual Cortex")

**Strengths:**
- ✅ Dual scanning strategy (Logic + Physics) - More robust than pure physics-based approaches
- ✅ SDK component awareness (SeatHotspot, ProjectionSurface, Interactable)
- ✅ Relative direction calculation ("In front", "To the left")
- ✅ Short-term memory with distance-based prioritization
- ✅ Clean JSON output format for LLM consumption
- ✅ Event-driven user detection (OnUserDetected)

**Gaps Identified:**
- ❌ No awareness of user emotional state or body language
- ❌ No awareness of user activities (typing, sitting, moving, idle)
- ❌ Static "Pavilion" location - no dynamic zone awareness
- ❌ No temporal awareness (how long user has been nearby, conversation duration)
- ❌ No multi-user tracking (only tracks single activeUser)
- ❌ "Another Player" is anonymous - no networked name integration
- ❌ No awareness of audio environment (music playing, noise levels)

#### 2. AIEye (The "Retina")

**Strengths:**
- ✅ WebGL-optimized (RGB24, JPEG compression)
- ✅ Cooldown system prevents performance spikes
- ✅ Configurable resolution and quality
- ✅ Manual rendering (camera disabled when not capturing)
- ✅ Clean Base64 output for multimodal LLMs

**Gaps Identified:**
- ❌ Single static camera position (no saccadic eye movement simulation)
- ❌ No attention-based focusing (always captures full FOV)
- ❌ No video/temporal understanding (single frame only)
- ❌ No depth information passed to LLM
- ❌ No object detection annotations (LLM must interpret raw image)
- ❌ No gaze direction influence on capture angle

#### 3. HeadLookController (Natural Movement)

**Strengths:**
- ✅ IK-based head/eye tracking (industry standard)
- ✅ Smooth interpolation prevents robotic movement
- ✅ Configurable weights for body/head/eyes
- ✅ GlanceAt() for temporary attention shifts
- ✅ Body rotation to face target (full avatar orientation)
- ✅ Player-specific eye height targeting

**Gaps Identified:**
- ❌ No idle behaviors (subtle movements when not looking at anything)
- ❌ No blink animation integration
- ❌ No eyebrow/facial expression coupling with head movement
- ❌ No attention distribution (can only look at one target)
- ❌ No awareness of personal space (discomfort at close range)
- ❌ No cultural variations in eye contact behavior

#### 4. MetaDynVoiceController (Orchestration Hub)

**Strengths:**
- ✅ Full pipeline: Whisper STT → LLM → ElevenLabs TTS
- ✅ Streaming response with sentence-by-sentence TTS
- ✅ Instant interrupt logic (critical for natural conversation)
- ✅ Vision keyword detection triggers AIEye
- ✅ Perception context auto-injection
- ✅ Conversation history with memory trimming (20 messages)
- ✅ Clean text filtering for TTS (*actions*, (thoughts), <tags>)
- ✅ Input locking integration
- ✅ Event system for animation/UI hooks

**Gaps Identified:**
- ❌ No emotion detection from user voice (Whisper doesn't provide this)
- ❌ No prosody/emotion control for TTS output
- ❌ Single animation trigger (Talk/Idle) - no gesture variation
- ❌ No conversational turn-taking awareness
- ❌ No personality persistence across sessions
- ❌ No relationship/rapport tracking with user
- ❌ No multi-turn intent tracking (goals, tasks in progress)

---

## Part 2: Competitive Landscape Analysis

### Direct Competitors

| Feature | MetaDyn (Current) | Inworld AI | Convai | NVIDIA ACE |
|---------|-------------------|------------|--------|------------|
| **Spatial Awareness** | ✅ SDK Components | ✅ Limited | ✅ Advanced | ✅ Via Convai |
| **Vision/Multimodal** | ✅ Gemini | ❌ Text Only | ❌ Text Only | ❌ Text Only |
| **Long-term Memory** | ⚠️ 20 messages | ✅ Advanced | ✅ Basic | ⚠️ Via Partners |
| **Emotion Engine** | ❌ | ✅ | ✅ Basic | ✅ |
| **Gesture Generation** | ❌ Talk/Idle only | ✅ | ✅ | ✅ |
| **Voice Cloning** | ✅ ElevenLabs | ✅ | ✅ | ✅ |
| **Interrupt Logic** | ✅ | ✅ | ⚠️ | ✅ |
| **NPC-to-NPC** | ❌ | ✅ | ✅ | ✅ |
| **WebGL Native** | ✅ | ❌ Plugin | ✅ Plugin | ❌ Cloud |
| **Open/Self-hosted** | ✅ | ❌ SaaS | ❌ SaaS | ❌ Cloud |

### MetaDyn's Unique Advantages

1. **Vision-Enabled AI** - Neither Inworld nor Convai offer native multimodal vision. MetaDyn can literally SEE the environment.

2. **WebGL-Native** - Built for browser deployment, not bolted-on plugins.

3. **Open Architecture** - Uses standard APIs (OpenRouter, ElevenLabs), not locked into proprietary platforms.

4. **SDK Integration** - AI understands MetaDyn's own SDK components natively (seats, screens, interactables).

5. **Full Source Control** - Can implement features competitors can't offer.

---

## Part 3: Feature Opportunities

### Tier 1: Low-Hanging Fruit (1-3 days each, High Impact)

#### 1.1 User Activity Awareness
**Impact:** ★★★★★ | **Effort:** ★☆☆☆☆

Add user state tracking to perception context:

```csharp
// In AIPerceptionManager
public class UserContext
{
    public string name;
    public string distance;
    public string position;
    public string activity;      // NEW: "Standing", "Sitting", "Walking", "Typing"
    public string facingAI;      // NEW: "Looking at me", "Looking away"
    public float timeNearby;     // NEW: How long they've been in range
}
```

**Why it matters:** AI can say "I see you've been standing there for a while, would you like to sit?" or "I notice you're looking at the screen, would you like me to explain what's on it?"

#### 1.2 Other Player Name Resolution
**Impact:** ★★★★☆ | **Effort:** ★☆☆☆☆

Currently shows "Another Player" - integrate with Player.NetworkedName:

```csharp
// In ScanEnvironment()
var playerComponent = obj.GetComponent<Player>();
string playerName = playerComponent?.NetworkedName?.ToString() ?? "Unknown";
perceivedObjects.Add(new ObjectContext
{
    name = playerName,
    type = "Human",
    status = playerComponent?.IsSitting ? "Sitting" : "Standing",
    distance = $"{dist:F1}m"
});
```

**Why it matters:** AI can say "I see Alex is also here, about 5 meters behind you" - creates social awareness.

#### 1.3 Conversation Duration Tracking
**Impact:** ★★★★☆ | **Effort:** ★☆☆☆☆

Track how long the conversation has been going:

```csharp
private float _conversationStartTime;
private int _turnCount;

// Include in system prompt injection
$"[Conversation has been ongoing for {(Time.time - _conversationStartTime):F0} seconds, {_turnCount} exchanges]"
```

**Why it matters:** AI can naturally wind down long conversations: "We've been chatting for 10 minutes! Feel free to explore, I'll be here if you need me."

#### 1.4 Dynamic Zone Awareness
**Impact:** ★★★★☆ | **Effort:** ★★☆☆☆

Use Trigger components to update location context:

```csharp
// Create ZoneDetector component for AI
public class AIZoneDetector : MonoBehaviour
{
    public AIPerceptionManager perceptionManager;
    public string zoneName = "Main Hall";

    private void OnTriggerEnter(Collider other)
    {
        if (other.GetComponent<AIPerceptionManager>())
        {
            perceptionManager.currentZone = zoneName;
        }
    }
}
```

**Why it matters:** AI knows it's in the "Conference Room" vs "Lobby" and can provide context-appropriate responses.

#### 1.5 Idle Micro-Movements
**Impact:** ★★★★★ | **Effort:** ★★☆☆☆

Add subtle idle behaviors to HeadLookController:

```csharp
private void UpdateIdleBehavior()
{
    if (currentLookTarget == null)
    {
        // Subtle random look variations
        float noiseX = Mathf.PerlinNoise(Time.time * 0.3f, 0) - 0.5f;
        float noiseY = Mathf.PerlinNoise(0, Time.time * 0.2f) - 0.5f;

        Vector3 idleOffset = new Vector3(noiseX * 2f, noiseY * 1f, 0);
        _currentLookPos += idleOffset;
    }
}
```

**Why it matters:** Eliminates "dead-eyed stare" effect. Avatar feels alive even when not engaged.

---

### Tier 2: Medium Effort (1-2 weeks each, Differentiating)

#### 2.1 Emotion-Aware Responses (Emotional Intelligence)
**Impact:** ★★★★★ | **Effort:** ★★★☆☆

Integrate voice emotion detection via Hume AI or similar:

```csharp
[Header("Emotion Detection")]
public bool enableEmotionDetection = true;
public string humeApiKey;

private async Task<EmotionResult> DetectEmotion(byte[] audioData)
{
    // Send to Hume AI for prosody analysis
    // Returns: joy, sadness, anger, fear, surprise, disgust
}

// Inject into context
$"[User emotional state: {emotion.primary} ({emotion.confidence:P0})]"
```

**Why it matters:** AI responds appropriately to frustrated users: "You sound a bit frustrated - is there something specific I can help clarify?" This is what Inworld charges premium for.

#### 2.2 Co-Speech Gesture Generation
**Impact:** ★★★★★ | **Effort:** ★★★★☆

Generate contextual gestures from LLM response:

```csharp
// Add gesture tags to system prompt
systemInstruction += @"
When responding, include gesture cues in square brackets:
[wave] for greetings
[point:{direction}] when indicating objects
[shrug] for uncertainty
[nod] for agreement
[thinking] when pondering
";

// Parse and execute gestures
private void ProcessGestureTag(string tag)
{
    switch (tag)
    {
        case "wave": animator.SetTrigger("Wave"); break;
        case "nod": animator.SetTrigger("Nod"); break;
        case "point:left": animator.SetTrigger("PointLeft"); break;
        // etc.
    }
}
```

**Why it matters:** AI pointing at a screen while saying "That display shows the schedule" creates convincing embodiment.

#### 2.3 Long-Term Memory with Supabase
**Impact:** ★★★★★ | **Effort:** ★★★☆☆

Persist user relationships and conversation summaries:

```csharp
[System.Serializable]
public class UserMemory
{
    public string userId;
    public string userName;
    public int totalInteractions;
    public List<string> importantFacts;      // "Works in marketing", "Prefers formal tone"
    public List<string> conversationTopics;   // Topics discussed
    public float rapportScore;                // 0-1 relationship strength
    public DateTime firstMet;
    public DateTime lastSeen;
}

// On conversation end
private async Task SaveMemory()
{
    // Summarize conversation via LLM
    string summary = await SummarizeConversation();

    // Extract key facts
    List<string> facts = await ExtractKeyFacts();

    // Save to Supabase
    await SupabaseClient.From<UserMemory>().Upsert(memory);
}
```

**Why it matters:** AI remembers "Welcome back, Sarah! Last time we talked about the upcoming conference. Did that go well?" This creates genuine relationship building.

#### 2.4 Gaze-Directed Vision
**Impact:** ★★★★☆ | **Effort:** ★★★☆☆

Capture from where the AI is actually looking:

```csharp
public byte[] CaptureSnapshotBytes()
{
    // Align camera with current look direction
    if (headLookController != null)
    {
        eyeCamera.transform.LookAt(_currentLookPos);
    }

    // ... rest of capture
}
```

**Why it matters:** When user asks "What do you see?", the AI captures what it's actually looking at, not a fixed forward view.

#### 2.5 Attention Distribution System
**Impact:** ★★★★☆ | **Effort:** ★★★☆☆

Track multiple points of interest:

```csharp
public class AttentionSystem : MonoBehaviour
{
    public List<AttentionTarget> targets = new List<AttentionTarget>();

    [System.Serializable]
    public class AttentionTarget
    {
        public Transform target;
        public float salience;        // How interesting (0-1)
        public float lastLookedAt;    // Time since looked at
    }

    public Transform GetNextAttentionTarget()
    {
        // Weighted random selection based on salience and time since last look
        // Creates natural attention shifting behavior
    }
}
```

**Why it matters:** AI naturally shifts attention between multiple users or objects, creating lifelike presence.

---

### Tier 3: Pie in the Sky (Revolutionary, 1-3 months each)

#### 3.1 Real-Time User Emotion from Camera (MorphCast Integration)
**Impact:** ★★★★★ | **Effort:** ★★★★★

Use WebGL-based facial emotion recognition on user's camera:

```javascript
// In browser via MorphCast SDK
MorphCast.start({
    onEmotionChange: (emotions) => {
        // Send to Unity via jslib
        SendEmotionToUnity(JSON.stringify(emotions));
    }
});
```

**Why it matters:** AI sees user smile and responds warmly. Sees confusion and automatically clarifies. This doesn't exist in any metaverse platform yet.

**Privacy consideration:** Opt-in only, with clear disclosure. Processing happens locally in browser.

#### 3.2 Procedural Gesture Animation from Speech
**Impact:** ★★★★★ | **Effort:** ★★★★★

Generate gestures directly from audio/text using ML model:

Based on SIGGRAPH Asia 2024's "Semantic Gesticulator" and AAMAS 2025's LLM gesture selection:

```csharp
// Two-stage approach:
// 1. LLM selects gesture type and timing
// 2. Procedural system blends animations

[System.Serializable]
public class GestureCue
{
    public float timestamp;      // When in speech
    public string gestureType;   // "beat", "iconic", "deictic", "metaphoric"
    public string parameters;    // "point:screen", "size:large"
}

// Blend gestures with speech audio
private void SynchronizeGestures(List<GestureCue> cues, AudioClip speech)
{
    foreach (var cue in cues)
    {
        StartCoroutine(TriggerGestureAt(cue.timestamp, cue));
    }
}
```

**Why it matters:** Every sentence has unique, contextually appropriate body language. Currently only NVIDIA ACE partners have this.

#### 3.3 NPC-to-NPC Autonomous Conversations
**Impact:** ★★★★★ | **Effort:** ★★★★☆

Multiple AI avatars that converse independently:

```csharp
public class NPCConversationManager : MonoBehaviour
{
    public List<MetaDynVoiceController> npcs;

    public void StartNPCConversation(MetaDynVoiceController npc1, MetaDynVoiceController npc2, string topic)
    {
        // NPCs take turns speaking about a topic
        // Player can observe or join the conversation
    }
}
```

**Why it matters:** Players walk into a room and find AI characters already engaged in conversation about the world. Massive immersion boost.

#### 3.4 Embodied Reasoning with 3D Understanding
**Impact:** ★★★★★ | **Effort:** ★★★★★

Based on Google's Gemini 3 Pro spatial understanding:

```csharp
// Capture depth buffer alongside color
public class SpatialCapture
{
    public byte[] colorImage;
    public byte[] depthImage;
    public Matrix4x4 cameraMatrix;
    public List<DetectedObject> objects;  // Pre-annotated via Unity
}

// Enhanced context
{
    "spatial": {
        "room_dimensions": "8m x 6m",
        "objects_3d": [
            {"name": "Chair", "position": [2.1, 0, 3.4], "distance": "2.1m", "reachable": true},
            {"name": "Screen", "position": [0, 2, -4], "distance": "5.7m", "reachable": false}
        ],
        "navigation_suggestion": "Walk forward 3m, turn left"
    }
}
```

**Why it matters:** AI can give precise navigation instructions: "Walk about 3 meters forward, then turn left - you'll see the information desk." This level of spatial reasoning is cutting-edge research.

#### 3.5 Personality Learning & Adaptation
**Impact:** ★★★★★ | **Effort:** ★★★★★

AI adapts its personality based on user preferences:

```csharp
public class PersonalityAdapter
{
    // Track what communication styles work for each user
    public Dictionary<string, float> formalityPreference;    // Formal vs Casual
    public Dictionary<string, float> verbosityPreference;    // Detailed vs Brief
    public Dictionary<string, float> humorPreference;        // Serious vs Playful

    // Fine-tune system prompt per user
    public string GetAdaptedSystemPrompt(string userId)
    {
        var prefs = GetUserPreferences(userId);
        return basePrompt + $@"
            Communication style for this user:
            - Formality: {prefs.formality:P0} (0=casual, 100%=formal)
            - Detail level: {prefs.verbosity:P0} (0=brief, 100%=detailed)
            - Humor: {prefs.humor:P0} (0=serious, 100%=playful)
        ";
    }
}
```

**Why it matters:** AI learns that user A prefers quick, casual responses while user B wants detailed, formal explanations. Creates genuinely personalized experience.

#### 3.6 Proactive Behavior System
**Impact:** ★★★★★ | **Effort:** ★★★★☆

AI initiates interaction based on observed context:

```csharp
public class ProactiveBehavior : MonoBehaviour
{
    public AIPerceptionManager perception;
    public MetaDynVoiceController voice;

    private void Update()
    {
        // Check for proactive triggers
        if (UserLookingLostForTooLong())
        {
            voice.SpeakUnprompted("You look like you might be searching for something. Can I help?");
        }

        if (UserStaringAtObjectForTooLong(out string objectName))
        {
            voice.SpeakUnprompted($"I see you're interested in the {objectName}. Would you like to know more?");
        }

        if (NewUserEnteredRange())
        {
            voice.SpeakUnprompted("Hello! Welcome to the Pavilion. Feel free to ask if you need any help.");
        }
    }
}
```

**Why it matters:** AI doesn't wait to be spoken to - it engages naturally like a real person would. This is the "uncanny valley" breakthrough for social AI.

---

## Part 4: Prioritized Roadmap

### Phase 1: Quick Wins (Week 1)
1. **User Activity Awareness** - 1 day
2. **Other Player Name Resolution** - 0.5 days
3. **Conversation Duration Tracking** - 0.5 days
4. **Dynamic Zone Awareness** - 1 day
5. **Idle Micro-Movements** - 1 day

**Outcome:** AI feels significantly more aware and alive. No new infrastructure needed.

### Phase 2: Emotional Intelligence (Weeks 2-3)
1. **Emotion-Aware Responses** (Hume AI integration) - 1 week
2. **Co-Speech Gesture Generation** - 1 week

**Outcome:** AI responds to emotional state and uses body language. Major differentiation from competitors.

### Phase 3: Persistent Relationships (Weeks 4-5)
1. **Long-Term Memory with Supabase** - 1.5 weeks
2. **Gaze-Directed Vision** - 0.5 days
3. **Attention Distribution System** - 1 week

**Outcome:** AI remembers users across sessions. Creates genuine relationship building.

### Phase 4: Advanced Embodiment (Month 2)
1. **Proactive Behavior System** - 1 week
2. **NPC-to-NPC Conversations** - 2 weeks
3. **Procedural Gesture Animation** - 2 weeks

**Outcome:** AI feels genuinely alive - initiates conversations, interacts with other AIs.

### Phase 5: Revolutionary Features (Month 3+)
1. **Real-Time User Emotion from Camera** - 2 weeks
2. **Embodied Reasoning with 3D Understanding** - 3 weeks
3. **Personality Learning & Adaptation** - 2 weeks

**Outcome:** Industry-leading embodied AI that doesn't exist anywhere else.

---

## Part 5: "First in the Industry" Opportunities

These are features that, to my knowledge, **no metaverse platform currently offers**:

### 1. Vision-Enabled AI in Real-Time Virtual Worlds
**MetaDyn already has this!** Inworld, Convai, and NVIDIA ACE are all text-only. Market this heavily.

### 2. User Camera Emotion → AI Response Loop
MorphCast + Unity WebGL could enable the AI to literally see your real face and respond to your expressions. No competitor does this.

### 3. Proactive Greeting Based on User Behavior
AI that approaches users who look lost, not just responds when spoken to. This is the "Apple Store Greeter" experience in the metaverse.

### 4. Cross-Session Personality Learning
AI that adapts its communication style to each user over time. Beyond simple memory - actual personality calibration.

### 5. Real-Time Gesture Synthesis
Beyond canned animations - procedural body language that matches speech content and emotion.

---

## Appendix: Technical Implementation Notes

### API Cost Estimates (per 1000 interactions)

| Service | Current | Optimized |
|---------|---------|-----------|
| OpenRouter (Gemini Flash) | ~$0.50 | ~$0.30 (with caching) |
| ElevenLabs TTS | ~$3.00 | ~$1.50 (turbo model) |
| Whisper STT | ~$0.30 | ~$0.30 |
| Hume AI (emotion) | ~$1.00 | ~$1.00 |
| **Total per interaction** | ~$0.005 | ~$0.003 |

### Performance Budgets (WebGL)

| Component | Current | Target |
|-----------|---------|--------|
| Perception Scan | 1-2ms | <1ms (with caching) |
| Vision Capture | 10-20ms | <15ms |
| IK Update | 0.1-0.5ms | <0.5ms |
| Audio Processing | N/A | <5ms |

### Recommended Animation Set

For full gesture support, RPM avatar needs these additional animations:
- Wave (greeting)
- Nod (agreement)
- Shake head (disagreement)
- Shrug (uncertainty)
- Point left/right/forward
- Thinking pose
- Excited gesture
- Calming gesture
- Hands together (emphasis)

---

## Conclusion

MetaDyn's AI embodiment system is already more capable than many realize - the vision integration alone puts it ahead of Inworld and Convai. The opportunity is to:

1. **Quickly implement low-hanging fruit** that makes the AI feel dramatically more aware
2. **Add emotional intelligence** that creates genuine connection
3. **Build persistent relationships** that bring users back
4. **Implement proactive behaviors** that feel magical
5. **Pioneer features** that don't exist anywhere yet

The goal isn't just to catch up to competitors - it's to leapfrog them by implementing features from cutting-edge research that SaaS platforms can't easily replicate.

**Bottom line:** MetaDyn can be the platform where AI avatars feel genuinely alive, not just responsive.

---

## Sources

- [Inworld AI - Long-Term Memory](https://inworld.ai/blog/introducing-long-term-memory)
- [Convai - Conversational AI for Virtual Worlds](https://www.convai.com/)
- [NVIDIA ACE Architecture](https://www.nvidia.com/en-us/geforce/news/nvidia-ace-architecture-ai-npc-personalities/)
- [MorphCast Facial Emotion AI](https://www.morphcast.com/)
- [Semantic Gesticulator - SIGGRAPH Asia 2024](https://dl.acm.org/doi/10.1145/3680528.3687648)
- [LLM Gesture Selection - AAMAS 2025 Best Student Paper](https://ict.usc.edu/news/essays/language-models-with-body-language-advancing-gesture-selection-for-virtual-humans/)
- [Google Gemini 3 Pro Vision](https://blog.google/technology/developers/gemini-3-pro-vision/)
- [Microsoft MindJourney - 3D Spatial Reasoning](https://www.microsoft.com/en-us/research/blog/mindjourney-enables-ai-to-explore-simulated-3d-worlds-to-improve-spatial-interpretation/)
- [NeurIPS 2025 Workshop on Space in Vision, Language, and Embodied AI](https://space-in-vision-language-embodied-ai.github.io/)
- [TED-Culture: Culturally Inclusive Gesture Generation](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1546765/full)
