# WebRTC Spatial Audio Implementation Plan

## Overview
Implement 3D spatial audio for WebRTC voice chat by routing audio streams through Unity's AudioSource system instead of browser's Audio elements. This enables distance-based volume, directionality, and integration with Wolf3DLipSync for avatar mouth animations.

---

## Current State Analysis

### What Works
✅ P2P WebRTC connections between players (mesh topology)
✅ Microphone capture and transmission
✅ Mute/unmute system with permissions
✅ Speaking detection (audio level analysis)
✅ Crystal clear audio quality

### Current Limitation
❌ **Audio plays directly in browser via `new Audio()` element (WebRTCVoice.jslib:105)**
- No spatial audio (same volume regardless of distance)
- No directionality (stereo positioning)
- No integration with Unity's audio system
- Cannot connect to Wolf3DLipSync for mouth animations

### Architecture
```
┌─────────────┐  WebRTC P2P   ┌─────────────┐
│  Player A   │ ←──────────→  │  Player B   │
│ (Local)     │               │ (Remote)    │
└─────────────┘               └─────────────┘
      │                              │
      ├─ Mic Input                   ├─ Receives Audio Stream
      ├─ Audio Analysis              └─ new Audio().play()
      └─ Speaking Detection               ❌ Bypasses Unity!
```

**Target Architecture:**
```
┌─────────────────────────────────────────────────┐
│  Player Prefab (Remote)                         │
│  ┌────────────────────────────────────────────┐ │
│  │ WebRTCAudioReceiver Component              │ │
│  │  - Receives MediaStream from JavaScript    │ │
│  │  - Streams to AudioSource                  │ │
│  └────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────┐ │
│  │ AudioSource (3D Spatial)                   │ │
│  │  - Spatial blend: 1.0 (full 3D)           │ │
│  │  - Rolloff: Logarithmic                    │ │
│  │  - Min distance: 5m                        │ │
│  │  - Max distance: 50m                       │ │
│  └────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────┐ │
│  │ Wolf3DLipSync (on RPM avatar child)        │ │
│  │  - Receives audio data for mouth animation │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Phase 1: JavaScript Audio Stream Routing (WebRTCVoice.jslib)

**File:** `/Assets/Plugins/WebGL/WebRTCVoice.jslib`

**Current Code (Lines 104-115):**
```javascript
pc.ontrack = (event) => {
    const audio = new Audio();
    audio.srcObject = event.streams[0];
    audio.volume = 1.0;
    audio.play().then(() => {
        console.log("WebRTC: Playing remote audio from " + peerIdStr);
    }).catch(err => {
        console.error("WebRTC: Failed to play audio from " + peerIdStr, err);
    });
};
```

**New Approach:**
Instead of playing audio directly, we need to:
1. Store the MediaStream in a dictionary (peerIdStr → MediaStream)
2. Notify Unity that audio is available
3. Let Unity request audio data via OnAudioFilterRead

**Modified Code:**
```javascript
$webRTCContext: {
    // ... existing properties ...
    peerAudioStreams: {},  // NEW: Store MediaStreams for Unity access

    // ... existing functions ...
},

createPeer: function(peerIdStr, isInitiator) {
    // ... existing code ...

    // Handle incoming audio - MODIFIED
    pc.ontrack = (event) => {
        console.log("WebRTC: Received audio track from " + peerIdStr);

        // Store the MediaStream for Unity to access
        webRTCContext.peerAudioStreams[peerIdStr] = event.streams[0];

        // Notify Unity that audio stream is ready
        const gameObjectName = 'WebRTCManager_' + webRTCContext.localPlayerId;
        SendMessage(gameObjectName, 'OnRemoteAudioStreamReady', peerIdStr);
    };

    // ... rest of existing code ...
},

// NEW: Function to get audio data for Unity AudioSource
WebRTC_GetAudioData__deps: ['$webRTCContext'],
WebRTC_GetAudioData: function(peerIdPtr, bufferPtr, bufferSize) {
    var peerId = UTF8ToString(peerIdPtr);
    var stream = webRTCContext.peerAudioStreams[peerId];

    if (!stream) {
        console.warn("WebRTC: No audio stream for peer " + peerId);
        return 0;
    }

    // TODO: Extract PCM audio data from MediaStream
    // This requires Web Audio API routing (see Phase 1B)
    return 0; // Number of samples written
}
```

**Challenge:** MediaStream cannot directly provide PCM data. We need Web Audio API.

---

### Phase 1B: Web Audio API Integration (CRITICAL)

**Problem:** Unity's AudioSource.OnAudioFilterRead expects PCM float samples, but MediaStream is a high-level API.

**Solution:** Use Web Audio API to route and process audio:

```javascript
$webRTCContext: {
    // ... existing ...
    audioContext: null,        // Already exists for speaking detection
    peerAudioNodes: {},        // NEW: ScriptProcessorNode per peer
    peerAudioBuffers: {},      // NEW: Ring buffers for Unity consumption
},

createPeer: function(peerIdStr, isInitiator) {
    // ... existing code ...

    pc.ontrack = (event) => {
        console.log("WebRTC: Received audio track from " + peerIdStr);

        // Create Web Audio processing chain
        if (!webRTCContext.audioContext) {
            webRTCContext.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        const audioCtx = webRTCContext.audioContext;
        const mediaStreamSource = audioCtx.createMediaStreamSource(event.streams[0]);

        // Create ScriptProcessor (4096 buffer size for smooth playback)
        const scriptNode = audioCtx.createScriptProcessor(4096, 1, 1);

        // Ring buffer for Unity to consume (store 1 second of audio)
        const sampleRate = audioCtx.sampleRate;
        const ringBufferSize = sampleRate * 1; // 1 second buffer
        webRTCContext.peerAudioBuffers[peerIdStr] = {
            buffer: new Float32Array(ringBufferSize),
            writeIndex: 0,
            readIndex: 0,
            sampleRate: sampleRate
        };

        // Process audio samples
        scriptNode.onaudioprocess = (audioEvent) => {
            const inputBuffer = audioEvent.inputBuffer;
            const inputData = inputBuffer.getChannelData(0);
            const ringBuffer = webRTCContext.peerAudioBuffers[peerIdStr];

            // Write to ring buffer
            for (let i = 0; i < inputData.length; i++) {
                ringBuffer.buffer[ringBuffer.writeIndex] = inputData[i];
                ringBuffer.writeIndex = (ringBuffer.writeIndex + 1) % ringBufferSize;
            }
        };

        // Connect: MediaStream → ScriptProcessor
        // NOTE: We don't connect to destination (no browser playback)
        mediaStreamSource.connect(scriptNode);

        // Store for cleanup
        webRTCContext.peerAudioNodes[peerIdStr] = scriptNode;

        // Notify Unity
        const gameObjectName = 'WebRTCManager_' + webRTCContext.localPlayerId;
        SendMessage(gameObjectName, 'OnRemoteAudioStreamReady', peerIdStr);
    };
},

// NEW: Unity calls this from OnAudioFilterRead
WebRTC_GetAudioSamples__deps: ['$webRTCContext'],
WebRTC_GetAudioSamples: function(peerIdPtr, bufferPtr, sampleCount) {
    var peerId = UTF8ToString(peerIdPtr);
    var ringBuffer = webRTCContext.peerAudioBuffers[peerId];

    if (!ringBuffer) {
        return 0; // No audio available
    }

    // Calculate available samples
    let available = ringBuffer.writeIndex - ringBuffer.readIndex;
    if (available < 0) available += ringBuffer.buffer.length;

    // Read requested samples (or less if not available)
    const samplesToRead = Math.min(sampleCount, available);

    for (let i = 0; i < samplesToRead; i++) {
        const sample = ringBuffer.buffer[ringBuffer.readIndex];
        HEAPF32[(bufferPtr >> 2) + i] = sample; // Write to Unity buffer
        ringBuffer.readIndex = (ringBuffer.readIndex + 1) % ringBuffer.buffer.length;
    }

    return samplesToRead;
},

// NEW: Get audio sample rate
WebRTC_GetAudioSampleRate__deps: ['$webRTCContext'],
WebRTC_GetAudioSampleRate: function(peerIdPtr) {
    var peerId = UTF8ToString(peerIdPtr);
    var ringBuffer = webRTCContext.peerAudioBuffers[peerId];
    return ringBuffer ? ringBuffer.sampleRate : 0;
},

// MODIFIED: Cleanup on disconnect
WebRTC_DisconnectPeer__deps: ['$webRTCContext'],
WebRTC_DisconnectPeer: function(peerIdPtr) {
    var peerId = UTF8ToString(peerIdPtr);
    var pc = webRTCContext.peerConnections[peerId];

    if (pc) {
        pc.close();
        delete webRTCContext.peerConnections[peerId];
    }

    // Clean up audio nodes
    if (webRTCContext.peerAudioNodes[peerId]) {
        webRTCContext.peerAudioNodes[peerId].disconnect();
        delete webRTCContext.peerAudioNodes[peerId];
    }

    // Clean up audio buffers
    delete webRTCContext.peerAudioBuffers[peerId];

    console.log("WebRTC: Disconnected from peer " + peerId);
}
```

---

### Phase 2: Unity WebRTCAudioReceiver Component

**File:** `/Assets/MetaDyn/Managers/WebRTCAudioReceiver.cs` (NEW)

**Purpose:** Receives audio from JavaScript and streams to AudioSource

```csharp
using UnityEngine;
using System.Runtime.InteropServices;

namespace MetaDyn
{
    /// <summary>
    /// Receives WebRTC audio stream from JavaScript and plays through Unity AudioSource.
    /// Enables spatial 3D audio for remote player voices.
    /// </summary>
    [RequireComponent(typeof(AudioSource))]
    public class WebRTCAudioReceiver : MonoBehaviour
    {
        #if UNITY_WEBGL && !UNITY_EDITOR
        [DllImport("__Internal")]
        private static extern int WebRTC_GetAudioSamples(string peerId, float[] buffer, int sampleCount);

        [DllImport("__Internal")]
        private static extern int WebRTC_GetAudioSampleRate(string peerId);
        #endif

        [Header("Configuration")]
        [Tooltip("Player ID to receive audio from")]
        public string remotePeerId;

        [Header("Lip Sync Integration")]
        [Tooltip("Optional Wolf3DLipSync component for mouth animation")]
        public Wolf3DLipSync lipSyncController;

        private AudioSource _audioSource;
        private bool _isInitialized = false;
        private int _sampleRate = 48000;
        private float[] _audioBuffer;
        private const int BUFFER_SIZE = 4096;

        // Audio level tracking for lip sync
        private float _currentAudioLevel = 0f;
        private const float SPEAKING_THRESHOLD = 0.01f;

        private void Awake()
        {
            _audioSource = GetComponent<AudioSource>();
            _audioBuffer = new float[BUFFER_SIZE];

            // Configure AudioSource for streaming
            _audioSource.loop = true;
            _audioSource.playOnAwake = false;
        }

        /// <summary>
        /// Initialize with remote player ID
        /// </summary>
        public void Initialize(string peerId, Wolf3DLipSync lipSync = null)
        {
            remotePeerId = peerId;
            lipSyncController = lipSync;

            #if UNITY_WEBGL && !UNITY_EDITOR
            // Get sample rate from JavaScript
            _sampleRate = WebRTC_GetAudioSampleRate(remotePeerId);
            if (_sampleRate == 0) _sampleRate = 48000; // Fallback

            // Create AudioClip for streaming
            _audioSource.clip = AudioClip.Create(
                $"WebRTC_{remotePeerId}",
                _sampleRate, // 1 second buffer
                1,           // Mono
                _sampleRate,
                true,        // Stream
                OnAudioRead
            );

            _audioSource.Play();
            _isInitialized = true;

            Debug.Log($"[WebRTCAudioReceiver] Initialized for peer {remotePeerId} at {_sampleRate}Hz");
            #endif
        }

        private void OnAudioRead(float[] data)
        {
            #if UNITY_WEBGL && !UNITY_EDITOR
            if (string.IsNullOrEmpty(remotePeerId)) return;

            // Request audio samples from JavaScript
            int samplesReceived = WebRTC_GetAudioSamples(remotePeerId, data, data.Length);

            // Fill remaining with silence if not enough data
            for (int i = samplesReceived; i < data.Length; i++)
            {
                data[i] = 0f;
            }

            // Calculate audio level for lip sync
            UpdateAudioLevel(data, samplesReceived);
            #endif
        }

        private void UpdateAudioLevel(float[] data, int sampleCount)
        {
            if (sampleCount == 0) return;

            // Calculate RMS (root mean square) for audio level
            float sum = 0f;
            for (int i = 0; i < sampleCount; i++)
            {
                sum += data[i] * data[i];
            }
            _currentAudioLevel = Mathf.Sqrt(sum / sampleCount);

            // Update lip sync
            if (lipSyncController != null)
            {
                lipSyncController.isTalking = _currentAudioLevel > SPEAKING_THRESHOLD;
            }
        }

        private void OnDestroy()
        {
            if (_audioSource != null && _audioSource.isPlaying)
            {
                _audioSource.Stop();
            }
        }
    }
}
```

---

### Phase 3: WebRTCManager Integration

**File:** `/Assets/MetaDyn/Managers/WebRTCManager.cs`

**Changes:**

1. Add DllImport declarations for new JavaScript functions
2. Add callback for `OnRemoteAudioStreamReady`
3. Create WebRTCAudioReceiver components for remote peers
4. Find and connect to Wolf3DLipSync on remote players

```csharp
public class WebRTCManager : NetworkBehaviour, INetworkRunnerCallbacks
{
    // ... existing DllImports ...

    #if UNITY_WEBGL && !UNITY_EDITOR
    [DllImport("__Internal")]
    private static extern int WebRTC_GetAudioSamples(string peerId, float[] buffer, int sampleCount);

    [DllImport("__Internal")]
    private static extern int WebRTC_GetAudioSampleRate(string peerId);
    #endif

    // ... existing fields ...

    // NEW: Track audio receivers for remote peers
    private Dictionary<string, WebRTCAudioReceiver> _audioReceivers = new Dictionary<string, WebRTCAudioReceiver>();

    // NEW: AudioSource for spatial audio (assigned in inspector)
    [Header("Spatial Audio")]
    [SerializeField] private AudioSource spatialAudioSource;

    public override void Spawned()
    {
        // ... existing code ...

        // Setup spatial audio source for REMOTE players only
        if (!Object.HasInputAuthority)
        {
            SetupSpatialAudioSource();
        }
    }

    private void SetupSpatialAudioSource()
    {
        if (spatialAudioSource == null)
        {
            spatialAudioSource = gameObject.AddComponent<AudioSource>();
        }

        // Configure for 3D spatial audio
        spatialAudioSource.spatialBlend = 1.0f;        // Full 3D
        spatialAudioSource.rolloffMode = AudioRolloffMode.Logarithmic;
        spatialAudioSource.minDistance = 5f;           // Full volume within 5m
        spatialAudioSource.maxDistance = 50f;          // Inaudible beyond 50m
        spatialAudioSource.spread = 60f;               // Stereo spread
        spatialAudioSource.dopplerLevel = 0f;          // Disable doppler (players move slowly)

        Debug.Log("[WebRTC] Spatial audio source configured");
    }

    // NEW: Called from JavaScript when remote audio stream is ready
    public void OnRemoteAudioStreamReady(string peerId)
    {
        Debug.Log($"[WebRTC] Remote audio stream ready for peer {peerId}");

        // Only process if this is a remote player (not our own voice)
        if (Object.HasInputAuthority)
        {
            Debug.LogWarning("[WebRTC] Received audio stream callback on local player - this shouldn't happen");
            return;
        }

        // Find or create WebRTCAudioReceiver
        if (!_audioReceivers.ContainsKey(peerId))
        {
            var receiver = gameObject.AddComponent<WebRTCAudioReceiver>();

            // Find Wolf3DLipSync on RPM avatar
            Wolf3DLipSync lipSync = GetComponentInChildren<Wolf3DLipSync>();

            // Initialize receiver
            receiver.Initialize(peerId, lipSync);

            _audioReceivers[peerId] = receiver;

            Debug.Log($"[WebRTC] Created audio receiver for peer {peerId}, lip sync: {(lipSync != null ? "connected" : "not found")}");
        }
    }

    public override void Despawned(NetworkRunner runner, bool hasState)
    {
        // ... existing code ...

        // Cleanup audio receivers
        foreach (var receiver in _audioReceivers.Values)
        {
            if (receiver != null)
            {
                Destroy(receiver);
            }
        }
        _audioReceivers.Clear();
    }
}
```

---

### Phase 4: Player Prefab Configuration

**File:** Player prefab in Unity Editor

**Required Components:**
1. **WebRTCManager** (already exists)
2. **AudioSource** (NEW) - for spatial audio
3. **Wolf3DLipSync** (already on RPM avatar child)

**AudioSource Settings (Inspector):**
```
Output: AudioMixer (optional - for volume control)
Mute: false
Bypass Effects: false
Play On Awake: false
Loop: true (set by WebRTCAudioReceiver)

3D Sound Settings:
- Spatial Blend: 1.0 (full 3D)
- Doppler Level: 0
- Spread: 60
- Volume Rolloff: Logarithmic
- Min Distance: 5
- Max Distance: 50
```

**Prefab Hierarchy:**
```
Player
├─ WebRTCManager (existing)
├─ AudioSource (NEW - spatial audio for WebRTC)
├─ NameTag (existing)
└─ RPM_Avatar
   └─ Wolf3DLipSync (existing - for lip sync)
```

---

## Phase 5: Testing & Validation

### Local Testing (Unity Editor)
❌ **Cannot test in editor** - WebGL and microphone required
✅ Script compilation and component setup

### WebGL Build Testing
1. Build WebGL with 2+ browser windows
2. Test checklist:

**Spatial Audio:**
- [ ] Volume decreases with distance
- [ ] Stereo positioning works (left/right)
- [ ] Inaudible beyond max distance (50m)
- [ ] Full volume within min distance (5m)

**Lip Sync:**
- [ ] Remote player's mouth moves when they speak
- [ ] Mouth stops when they're silent
- [ ] Lip sync synchronized with audio

**Integration:**
- [ ] Mute system still works
- [ ] Speaking indicator on NameTag syncs with audio
- [ ] No audio feedback loops (player hears own voice)
- [ ] Audio cleanup when player disconnects

**Performance:**
- [ ] No audio stuttering
- [ ] Latency < 200ms
- [ ] FPS stable (60+)
- [ ] No memory leaks

---

## Potential Issues & Solutions

### Issue 1: ScriptProcessorNode is Deprecated
**Problem:** Web Audio API's ScriptProcessorNode is deprecated in favor of AudioWorklet

**Solution (Future):** Migrate to AudioWorklet for better performance
```javascript
// Future improvement - AudioWorklet processor
class WebRTCAudioProcessor extends AudioWorkletProcessor {
    process(inputs, outputs, parameters) {
        // More efficient, runs in separate thread
    }
}
```
**Current:** ScriptProcessorNode works fine for 8 players, optimize later if needed

---

### Issue 2: Sample Rate Mismatch
**Problem:** Browser audio (48kHz) vs Unity (variable)

**Solution:** Unity's AudioClip.Create handles resampling automatically
- JavaScript provides native sample rate
- Unity resamples if needed

---

### Issue 3: Audio Latency
**Problem:** Ring buffer + Unity audio pipeline adds latency

**Solution:**
- Use 4096 sample buffer (85ms at 48kHz)
- Acceptable for voice chat
- Monitor with performance testing

---

### Issue 4: Local Player Hearing Own Voice
**Problem:** Audio feedback if local player's audio is routed

**Solution:** Only remote players create AudioSource (line 66 in WebRTCManager)
```csharp
if (!Object.HasInputAuthority)
{
    SetupSpatialAudioSource(); // Only for remote players
}
```

---

### Issue 5: Lip Sync Not Working
**Possible causes:**
1. Wolf3DLipSync not found on avatar
2. Audio level threshold too high/low
3. Component disabled or missing

**Debug:**
```csharp
Debug.Log($"Lip sync found: {lipSync != null}");
Debug.Log($"Audio level: {_currentAudioLevel}, threshold: {SPEAKING_THRESHOLD}");
```

---

## Files Modified/Created

### Modified Files
1. `/Assets/Plugins/WebGL/WebRTCVoice.jslib`
   - Add peerAudioNodes, peerAudioBuffers
   - Modify pc.ontrack to route through Web Audio API
   - Add WebRTC_GetAudioSamples, WebRTC_GetAudioSampleRate
   - Update WebRTC_DisconnectPeer cleanup

2. `/Assets/MetaDyn/Managers/WebRTCManager.cs`
   - Add DllImport for audio functions
   - Add OnRemoteAudioStreamReady callback
   - Add SetupSpatialAudioSource method
   - Create WebRTCAudioReceiver components
   - Connect to Wolf3DLipSync

3. `Player.prefab`
   - Add AudioSource component
   - Configure spatial audio settings

### New Files
1. `/Assets/MetaDyn/Managers/WebRTCAudioReceiver.cs`
   - Component for streaming WebRTC audio
   - OnAudioRead callback for Unity AudioClip
   - Audio level analysis
   - Lip sync integration

---

## Implementation Timeline

**Phase 1 (JavaScript):** 2-3 hours
- Modify WebRTCVoice.jslib
- Test audio stream routing
- Verify ring buffer

**Phase 2 (WebRTCAudioReceiver):** 1-2 hours
- Create component
- Implement OnAudioRead
- Test audio playback

**Phase 3 (WebRTCManager):** 1 hour
- Add callback handling
- Create receivers
- Connect lip sync

**Phase 4 (Prefab Setup):** 30 minutes
- Add AudioSource to prefab
- Configure spatial settings
- Wire up references

**Phase 5 (Testing):** 2-3 hours
- WebGL build testing
- Bug fixes
- Performance tuning

**Total: 7-9.5 hours**

---

## Success Criteria

✅ Remote player voices have 3D spatial audio
✅ Volume changes based on distance (5m-50m range)
✅ Stereo positioning works correctly
✅ Wolf3DLipSync animates mouths when speaking
✅ No audio feedback (player doesn't hear themselves)
✅ Mute system still functions
✅ Speaking indicators sync with audio
✅ No performance degradation
✅ Clean audio on disconnect

---

## Future Enhancements (Post-MVP)

1. **Voice Effects**
   - Reverb for large spaces
   - Distance-based low-pass filter (muffled far away)
   - Spatial audio occlusion (walls block sound)

2. **Performance Optimization**
   - Migrate to AudioWorklet (more efficient)
   - Adaptive buffer sizing
   - Audio culling for very distant players

3. **Advanced Lip Sync**
   - Phoneme-based animation (analyze frequencies)
   - Better synchronization
   - Emotion detection

4. **LiveKit Migration (50+ players)**
   - SFU for scalability
   - Same spatial audio system in Unity
   - Better bandwidth management

---

## Notes

- This plan maintains the existing WebRTC P2P architecture
- No breaking changes to mute system or networking
- AudioSource already exists on Player prefab for AI voice (if applicable)
- Wolf3DLipSync integration is optional but recommended
- WebGL-only feature (native builds would need different approach)
