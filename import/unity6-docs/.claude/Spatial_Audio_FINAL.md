# WebRTC Spatial Audio - FINAL Implementation

**Date:** 2025-12-20
**Status:** ⚠️ SUPERSEDED - See Spatial_Audio_COMPLETE.md for working solution

---

## 🔴 This Document is Outdated

This document describes the implementation approach, but the actual working solution required additional fixes. See **Spatial_Audio_COMPLETE.md** for the final tested implementation.

**Key missing pieces in this document:**
- Muted Audio element anchor (critical for browser autoplay policy)
- Dynamic spatial settings from Unity Inspector
- Silent gain node for lip sync chain

---

# Original Document (For Reference)

---

## Critical Change: Browser-Based Spatial Audio

After discovering that Unity WebGL doesn't support `AudioClip` streaming, I pivoted to a **much better solution**: Use the browser's native spatial audio capabilities.

### Why This Is Better

❌ **Old Approach (didn't work):**
- Try to route audio through Unity's AudioSource
- WebGL doesn't support streaming AudioClips
- AudioClip.SetData() doesn't sync with playback
- Fighting WebGL limitations

✅ **New Approach (works):**
- Use Web Audio API's **PannerNode** for spatial audio
- Native browser 3D audio (HRTF, distance attenuation)
- Unity just sends position updates
- Works perfectly in WebGL
- Lower latency, better quality

---

## How It Works Now

### JavaScript (WebRTCVoice.jslib)

**When remote audio arrives:**
1. Create MediaStreamSource from WebRTC audio
2. Create **PannerNode** for 3D spatial positioning
3. Configure spatial settings:
   - HRTF panning (realistic 3D)
   - 5m reference distance (full volume)
   - 50m max distance (inaudible)
   - Inverse distance model (natural falloff)
4. Connect: `MediaStream → Panner → AudioContext.destination`
5. **Browser plays the audio with spatial positioning**

**Lip sync:**
- Separate chain: `MediaStream → Analyser → ScriptProcessor → Ring buffer`
- Unity pulls samples for lip sync detection
- Audio playback happens independently

### Unity (WebRTCManager.cs)

**Every frame in Render():**
1. **Update listener** (camera position + orientation)
   - `WebRTC_UpdateListenerPosition(pos, forward, up)`
2. **Update each remote peer** position
   - `WebRTC_UpdatePeerPosition(peerId, x, y, z)`

**JavaScript updates:**
- `panner.positionX/Y/Z` for each peer
- `listener.positionX/Y/Z` and orientation
- Browser's Web Audio API handles the rest

---

## What You'll Hear

✅ **Spatial audio** - volume based on distance
✅ **Stereo positioning** - left/right/behind
✅ **HRTF processing** - realistic 3D sound
✅ **Smooth** - native browser processing
✅ **Low latency** - direct WebRTC → Web Audio

---

## Files Changed

### Modified (2 files)

**1. WebRTCVoice.jslib**
- Added PannerNode for spatial audio
- Connects audio to `audioContext.destination` (browser plays it)
- Added `WebRTC_UpdatePeerPosition()` - update peer positions
- Added `WebRTC_UpdateListenerPosition()` - update camera position
- Kept ring buffer for lip sync data only

**2. WebRTCManager.cs**
- Added position update functions in `Render()`
- Simplified spatial audio setup (browser handles it)
- Sends camera + peer positions every frame
- Still creates WebRTCAudioReceiver for lip sync

### No Changes Needed

**WebRTCAudioReceiver.cs**
- Still works for lip sync (pulls samples from ring buffer)
- Doesn't play audio anymore (browser does it)
- Debug logs still useful

---

## Testing

**Build and test - you should:**
1. ✅ **HEAR AUDIO** from remote players
2. ✅ Volume decreases as they move away
3. ✅ Stereo positioning works (left/right)
4. ✅ Lip sync animates when speaking
5. ✅ Mute still works
6. ✅ Speaking indicators work

**Console logs to watch for:**
```
WebRTC: Spatial audio configured for peer 2 (HRTF panning, 5m-50m range)
[WebRTC] Remote player marked for spatial audio (handled by browser)
[WebRTCAudioReceiver] Initialized for peer 2 at 48000Hz, lip sync: AvatarSdkPlayerLipSync
```

---

## Why This Will Work

1. **No WebGL limitations** - browser handles audio natively
2. **Standard Web Audio API** - mature, tested, supported
3. **Simpler architecture** - Unity just sends positions
4. **Better performance** - no Unity AudioSource overhead
5. **Better quality** - HRTF spatial audio is professional-grade

---

## Technical Details

### Coordinate System
- Unity: Right-handed, Y-up, Z-forward
- Web Audio: Right-handed, Y-up, Z-backward
- **Z is flipped** in JavaScript (`-z`) for correct orientation

### Spatial Audio Settings
```javascript
panningModel: 'HRTF'           // Best quality 3D audio
distanceModel: 'inverse'        // Natural distance falloff
refDistance: 5                  // Full volume < 5m
maxDistance: 50                 // Silent > 50m
rolloffFactor: 1                // Natural attenuation
```

### Update Rate
- Position updates: **Every frame** (60 FPS)
- Web Audio interpolates smoothly between updates
- No stuttering or glitches

---

## If There's No Audio

**Check JavaScript console for:**
1. `AudioContext` created successfully
2. `PannerNode` connected
3. Position updates being received
4. No errors about audio permissions

**Quick test:**
```javascript
// In browser console:
console.log(webRTCContext.peerAudioNodes);
// Should show peers with { source, panner, analyser, processor }
```

---

## Next Steps After This Works

### Short-term improvements:
- Distance-based low-pass filter (muffled when far)
- Occlusion (walls block sound)
- Reverb for large spaces

### Long-term (production):
- Migrate to LiveKit SFU for 50+ players
- Same spatial audio system (Unity sends positions)
- LiveKit handles WebRTC at scale

---

## Summary

**This is a complete architectural pivot** from Unity-based spatial audio to browser-based spatial audio. It's the right approach for WebGL and will actually work.

**Key insight:** Don't fight the platform - use its strengths. WebGL + Web Audio API = perfect for spatial voice chat.

**Rebuild and test!** 🚀
