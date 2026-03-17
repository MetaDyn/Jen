# WebRTC Scaling Options (LiveKit vs Cloudflare)

## Goal
Upgrade current WebRTC voice chat to support large rooms by moving from P2P mesh to an SFU‑based architecture, while keeping existing Unity/WebGL client flow.

---

## Option A: LiveKit (Current Path)
### What Changes
- Use LiveKit SFU for media routing instead of P2P mesh.
- Replace local signaling with LiveKit token + room join.
- Unity/WebGL client publishes mic stream to LiveKit; subscribes to remote tracks.

### Pros
- Mature SFU product, strong docs, active ecosystem.
- Built‑in rooms, tokens, permissions.
- Good observability and recording options.

### Cons
- Extra infra (LiveKit server) to run/manage.
- Cost scales with usage.

### Integration Touchpoints
- `Assets/MetaDyn/Managers/WebRTCManager.cs`
- `Assets/Plugins/WebGL/WebRTCVoice.jslib`
- Token minting endpoint in dashboard/server

---

## Option B: Cloudflare (RealtimeKit + SFU + TURN)
### What Changes
- RealtimeKit handles session signaling and auth.
- Cloudflare SFU handles media routing.
- Cloudflare TURN used for NAT fallback.

### Pros
- Global edge network + low latency.
- Consolidated vendor stack (auth + SFU + TURN).
- Built for large‑scale RTC usage.

### Cons
- Less Unity‑specific reference material than LiveKit.
- Still need integration work for token/session management.

### Integration Touchpoints
- Replace LiveKit token/room logic with Cloudflare session APIs.
- Update WebRTC client code to connect to Cloudflare SFU.
- ICE server list points to Cloudflare TURN.

---

## Basic Migration Steps (Either Option)
1. **Keep Unity voice capture + audio playback.**
2. Replace P2P signaling with SFU join/auth flow.
3. Publish local mic track to SFU, subscribe to remote tracks.
4. Update ICE server config (TURN + STUN).
5. Add a server endpoint to mint session tokens.

---

## Recommendation (Technical)
- **Short‑term:** LiveKit if you want the fastest swap with existing tooling.
- **Long‑term:** Cloudflare if you want edge‑native scaling + consolidated services.

---

## Next Questions
- Target room size (50? 200? 1000+)?
- Expected budget per active user?
- Do you want recording, moderation, or spatial audio mixing at the SFU layer?

