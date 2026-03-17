# Infrastructure & Production Systems

Complete documentation for MetaDyn's production infrastructure, hosting, deployment, and network architecture.

**Last Updated:** 2026-01-02

---

## Production Infrastructure & Hosting

### Overview
Complete production infrastructure for MetaDyn platform, featuring enterprise-grade CDN delivery, PWA website, and optimized Unity WebGL hosting.

---

## MetaDyn.xyz Website (PWA)

**Location:** `/mnt/c/Metaverse/MetaDyn/Dev/website-v2`
**Live URL:** https://metadyn.xyz
**Status:** Production (Deployed)

### Tech Stack
- Next.js 13.5.6 (App Router, Static Export)
- React 18.2.0 + TypeScript 5.2.2
- Tailwind CSS 3.3.5 (Glassmorphism UI)
- Three.js 0.157.0 (@react-three/fiber, @react-three/drei)
- Framer Motion 10.16.4 (Scroll animations)
- Cloudflare Workers (Contact form backend)
- Resend API (Email delivery with DKIM/SPF)

### Progressive Web App (PWA) Features
- Installable as native-like desktop/mobile app
- Standalone display mode (no browser UI)
- Custom app icons (16x16, 32x32, 180x180, 192x192, 512x512)
- Web App Manifest configured
- Theme color integration (#0ea5e9 cyan)
- Offline-capable architecture (future: service worker)

### PWA Installation Experience
```
1. User visits metadyn.xyz
2. Browser shows "Install App" prompt in address bar
3. User clicks "Install"
4. MetaDyn appears as desktop/mobile app
5. Launch icon added to Start Menu/Applications/Home Screen
6. Opens in standalone window (no browser chrome)
7. Perfect for /platform route → Unity WebGL launcher
```

### SEO & Metadata
- Comprehensive Open Graph tags (Facebook, LinkedIn)
- Twitter Card integration (@MetaverseDyn)
- 25+ targeted keywords (metaverse, Unity 6, WebRTC, AI agents)
- Canonical URLs and sitemap
- Robots.txt configuration
- Google/Bing crawl optimization

### Contact System
- Cloudflare Worker at `https://email.metadyn.xyz/send`
- Resend API integration with custom domain
- Dual emails: notification + branded auto-reply
- Full DKIM/SPF authentication (zero spam flags)
- Form fields: Name, Email, Phone, Budget (dropdown), Message

### Page Structure
- Home (Hero with 3D background)
- About (Company vision & approach)
- **Platform** (MetaDynPavilion showcase with hero image)
- Services (Metaverse development services)
- Portfolio (Project showcases)
- Contact (Form with Cloudflare backend)

### Future Integration
```
/platform route (planned):
- Full-viewport Unity WebGL embed
- PWA standalone mode = native metaverse launcher
- No browser UI overhead
- Faster performance vs browser tab
- Service worker caching for Unity build files
- Deep linking to specific worlds/experiences
```

### Documentation
- See `/mnt/c/Metaverse/MetaDyn/Dev/website-v2/memory-bank/` for detailed context
- `claude.md` - Quick reference for website development
- `emailArchitecture.md` - Email system documentation
- `techContext.md` - Technologies and infrastructure

---

## Cloudflare CDN Infrastructure

### DNS & Routing
- Full DNS moved to Cloudflare (1.1.1.1 infrastructure)
- Anycast global network (300+ edge locations)
- Fastest DNS resolution globally (10-20ms vs 50-200ms)
- Automatic HTTPS/SSL certificates

### Unity WebGL Subdomain (Proxied)
- **Subdomain:** `[unity-subdomain].metadyn.xyz`
- **Status:** Proxied (Orange Cloud)
- **Backend:** nginx server
- **Compression:** Brotli (pre-compressed Unity builds)

### Performance Stack

```
User Request
    ↓
Cloudflare Edge (nearest of 300+ locations - 2ms latency)
    ↓
Cache HIT (Unity .wasm, .js, .data, .framework.js files)
    ↓
Brotli-compressed assets served from edge
    ↓
User browser (instant load)

First Load in Region:
User → Cloudflare Edge → nginx (Brotli-compressed) → Cache at edge

Subsequent Loads:
User → Cloudflare Edge (milliseconds)
```

### What Cloudflare Provides (Automatic)
- **Global CDN caching** - Unity build files cached at 300+ edge locations
- **HTTP/3 + QUIC support** - Faster than HTTP/2 for high-latency connections
- **Brotli/Gzip compression** - Respects pre-compressed nginx assets
- **WebSocket proxying** - Photon Fusion + WebRTC signaling pass-through
- **DDoS protection** - Automatic threat mitigation
- **Smart routing** - Optimized paths to OpenAI/OpenRouter APIs
- **SSL/TLS edge termination** - Faster handshakes
- **Automatic optimization** - Image/JS/CSS minification

### WebSocket Support (Critical for Unity)
- WebSocket upgrade headers auto-detected
- Bidirectional frame proxying (Cloudflare Edge ↔ nginx)
- Works with Photon Fusion signaling (wss://)
- Works with WebRTC signaling (STUN/TURN bypass)
- No connection limits on WebSocket duration
- Available on ALL Cloudflare plans (including Free)

### SSL/TLS Configuration
- Mode: Full or Full (Strict)
- Edge certificates: Auto-provisioned by Cloudflare
- Origin certificates: Valid SSL on nginx
- End-to-end encryption: User ↔ Cloudflare ↔ nginx

### Performance Gains Observed
- **Unity load times: 50-70% faster** (edge caching + HTTP/3)
- **OpenAI/OpenRouter API calls: Noticeably faster** (smart routing)
- **DNS lookups: 10-20ms** (vs 50-200ms before Cloudflare)
- **WebSocket connections: Instant** (zero overhead from proxy)
- **nginx bandwidth: 90%+ reduction** (Cloudflare serves most requests)

### Cache Status Verification
```bash
# Check if asset is cached
curl -I https://[unity-subdomain].metadyn.xyz/Build/unity.wasm

# Look for these headers:
cf-cache-status: HIT        # Served from edge
cf-ray: [id]-[location]     # Edge location identifier
content-encoding: br        # Brotli compression preserved
server: cloudflare          # Cloudflare in front
```

### What Gets Cached
- Unity build files: `.wasm`, `.data`, `.framework.js`, `.loader.js`
- Static assets: Images, fonts, JSON configs
- Cache duration: Controlled by nginx Cache-Control headers

### What Doesn't Get Cached
- Dynamic API responses (OpenAI, OpenRouter, Supabase)
- WebSocket connections (proxied, not cached)
- POST requests (contact form, API calls)

### Infrastructure Comparison

**Before Cloudflare:**
```
User → ISP routing → nginx server → Unity loads
        (variable latency, direct to origin)
- DNS: 50-200ms
- First byte: 200-500ms (depends on distance)
- WebSocket: Direct connection
- API calls: Standard internet routing
```

**After Cloudflare:**
```
User → Cloudflare Edge (2ms) → nginx (if cache miss)
                             → Edge cache (if cache hit)
- DNS: 10-20ms (1.1.1.1 infrastructure)
- First byte: 10-50ms (edge proximity)
- WebSocket: Proxied with zero overhead
- API calls: Optimized Cloudflare backbone routing
```

### Cost Benefits
- Free tier supports all current features
- Bandwidth savings on origin server (90%+ reduction)
- No additional cost for WebSocket support
- DDoS protection included (no separate service needed)

### Cloudflare Page Rules (Recommended)
```
Pattern: *[unity-subdomain].metadyn.xyz/Build/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
  - Browser Cache TTL: 4 hours
  - Brotli: On (respects pre-compression)
```

---

## Deployment System

### One-Click Deployment Flow
1. Configure server profile (SSH details)
2. Set world config (room name, max players, spaceId)
3. Build WebGL in Unity
4. Click "Deploy to Server" in MetaDynProjectConfig window
5. System runs SSH/SCP to upload build
6. MetaDynRuntimeConfig embedded in build for auto-join

### Shared Hosting Model (Planned / Confirmed Direction)

MetaDyn will support a **shared hosting** model similar in spirit to shared hosting platforms like Spatial.io:

- multiple spaces can live on the same server/VPS
- each space still remains its **own build / deployment unit**
- spaces are isolated by directory, routing, and metadata
- the host server routes each domain/subdomain to the correct space

This does **not** mean one shared runtime for all spaces.

It means:
- one physical/virtual host can serve many spaces
- each space has its own deployed files or app instance
- deployment/provisioning creates or updates the routing needed for that space

### Self-Hosted Model (Also Supported)

MetaDyn will also support **self-hosting**:

- a customer, partner, or studio can deploy a space to infrastructure they control
- deployment still uses the same basic model:
  - build output
  - target server/profile
  - runtime config
  - routing/proxy layer

### Canonical Space Rule

Each space is its **own build**.

This remains true in both:
- shared-hosting deployments
- self-hosted deployments

### Unity WebGL Shared Hosting Pattern

Expected shared-hosting flow for Unity spaces:

1. Use an existing Unity/WebGL space template or built space
2. Create a per-space deployment directory
3. Copy the built WebGL files into that space directory
4. Create or update reverse-proxy/static routing config
5. Attach the desired domain/subdomain
6. Ensure SSL/proxy path is active
7. Publish space metadata and access info

Typical directory pattern:

```text
{remotePath}/{roomName}-{spaceId}/
```

### Hyperfy Shared Hosting Pattern

Expected shared-hosting flow for Hyperfy spaces:

1. Use an existing Hyperfy space/world template
2. Create or copy a per-space Hyperfy app/world instance
3. Create or update reverse-proxy config for that instance
4. Attach the correct domain/subdomain
5. Ensure SSL/proxy path is active
6. Publish/update metadata for that space

### Dynamic Proxy / Routing Model

Shared hosting depends on dynamic routing/proxy setup.

Current intended pattern:
- provision space files/app into isolated directory/instance
- create or update nginx config (or equivalent origin routing)
- point hostname/subdomain at the right target
- use Cloudflare in front for DNS, proxying, SSL, and edge performance

This means a new space deployment may require:
- directory creation
- file copy/sync
- routing config update
- origin reload/restart if required
- DNS/proxy record verification

### SSL Model

Expected SSL model:
- Cloudflare handles external DNS + proxy + edge SSL
- origin server/nginx still has valid SSL configuration or Cloudflare origin cert
- each hosted space should resolve cleanly through its assigned hostname/subdomain
- Reference nginx template: see `../config/unity-proxy-config.md` for the name-based SSL proxy configuration pattern currently used for Unity/Hyperfy-style subdomain routing
- Current MetaDyn standard for `*.metadyn.xyz` deployments: use the Let's Encrypt certificate lineage at `/etc/letsencrypt/live/metadyn.xyz/`

In practice, SSL may involve two layers:
- Cloudflare-managed edge certificate
- origin-side cert/origin trust configuration

### Why This Model Makes Sense

Benefits:
- efficient infrastructure use
- multiple spaces on one VPS/server
- easy managed hosting story
- clearer per-space isolation than trying to force many spaces into one build
- works for both Unity WebGL and Hyperfy style deployments

Tradeoffs:
- more routing/proxy automation required
- more deployment metadata to manage
- origin server organization matters more
- rollback/version tracking becomes important as hosted space count grows

### Dynamic Space Deployment (NEW 2025-01-02)
- **Isolated Directories**: Builds are deployed to `{profile.remotePath}/{roomName}-{spaceId}/`.
- **URL Stability**: The deployment URL is automatically updated to match the unique space subfolder.
- **Organization**: Keeps production server organized by space GUIDs, matching industry standards (Spatial.io style).

### Unity-Dashboard Sync (NEW 2025-01-02)
- **Metadata Sync**: Bidirectional synchronization of the "Display Name" field between Unity Editor and Supabase `spaces` table.
- **Manual Control**: "Sync" button in Unity enables pushing local changes to the dashboard.
- **Auto-Pull**: Editor automatically fetches the latest dashboard name on load to ensure data consistency.

### Developer Authentication (NEW 2025-01-02)
- **Token-Based Auth**: Unity Editor uses an "API Token" (JWT) copied from the dashboard to authenticate Supabase requests.
- **Security**: Allows developers to bypass RLS (Row Level Security) safely without exposing service keys.
- **Storage**: Tokens are saved locally in `EditorPrefs` for session persistence.

### SSH Command Pattern
```bash
# rsync (preferred)
rsync -avz -e "ssh -p {port} -o BatchMode=yes -i {keyPath}" {localPath}/ {user}@{server}:{remotePath}/

# scp (fallback)
scp -P {port} -o BatchMode=yes -i {keyPath} -r {localPath}/* {user}@{server}:{remotePath}/
```

### Remote Directory Preflight
- Before `rsync` or `scp`, deployment now runs an SSH preflight that creates the remote directory with `mkdir -p`, applies `chmod 755`, and verifies the path exists.
- If that preflight cannot be confirmed, deployment stops immediately instead of attempting transfer anyway.
- Unity shows a blocking editor dialog with the server, remote path, and SSH error details so the failure is actionable.

### Key Files
```
/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs  # SSH/SCP
/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs      # Editor UI
/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynServerProfile.cs      # ScriptableObject
/Assets/MetaDyn/Core/Runtime/MetaDynRuntimeConfig.cs                # World config
```

### Deployment Metadata Requirements (Planned)

To support shared hosting and self-hosting cleanly, each deployed space should eventually track metadata such as:

- `spaceId`
- `roomName`
- `worldDisplayName`
- deployment type (`shared` or `self_hosted`)
- target host/server profile
- target path/directory
- public URL
- owner/admin identity
- deployment timestamp
- deployed build version
- rollback/reference version

Some of this should remain Unity-authored, while some should eventually be dashboard-configurable or dashboard-visible.

### Recommended Next Steps

1. Define the deployment metadata schema for spaces
2. Define how nginx/proxy configs are generated or updated per space
3. Decide whether deployment config changes are file-templated or dashboard/API-generated
4. Define shared-hosting provisioning flow separately for:
   - Unity WebGL spaces
   - Hyperfy spaces
5. Add deployment history / rollback metadata
6. Define how dashboard surfaces shared-hosted vs self-hosted spaces

### Hardening Priorities

As shared hosting expands, harden:

1. **Routing automation**
   - avoid manual proxy config drift
   - standardize server block/templates

2. **Deployment isolation**
   - ensure each space directory/app instance is isolated
   - avoid accidental overwrite of unrelated spaces

3. **Version tracking**
   - track deployed version/build per space
   - support rollback path

4. **Access control**
   - define who can deploy which space and to which target
   - separate dev/staging/prod deployment permissions later

5. **Origin security**
   - review current SSH assumptions
   - tighten trust/host verification where practical
   - standardize credential/key handling

6. **Observability**
   - know which spaces are deployed where
   - know last deploy time/status
   - know routing target and public URL

7. **Template discipline**
   - keep Unity and Hyperfy template sources explicit
   - avoid ad hoc production copies becoming source-of-truth

---

## Network Architecture

### Authority Model
- **Player Objects:** Each player has StateAuthority over their own Player NetworkObject
- **UserListManager:** Only host has StateAuthority
- **Registration:** Players use RPC to register with host's UserListManager
- **Moderation:** Only host can kick/ban (authority-checked)
- **Admin Permissions (New 2026-01-05):**
  - **Primary Check:** Database-driven. Player's Supabase `userId` is compared against the Space Owner's ID (stored in `MetaDynRuntimeConfig` via build/deployment). Matches = Admin (Permission Level 2).
  - **Fallback:** If no owner configured, the first player to join becomes Admin automatically.

### Synchronization Strategy
- **NetworkDictionary:** Used for user list (automatic sync)
- **NetworkString/NetworkBool:** For player names and mute state
- **Change Detection:** Frame-by-frame diff in Render() for user list updates
- **RPCs:** For admin actions (kick, ban) and registration

### Session Management
- **Max Players:** 50 per session (WebRTC P2P mesh topology, bandwidth-dependent)
- **Session Properties:** GameMode identifier for filtering
- **Auto-Join:** MetaDynRuntimeConfig provides room name for automatic joining
- **Spawn Points:** Random selection from EntrancePoint markers
- **Voice Scale:** WebRTC mesh topology supports up to 50 concurrent players before requiring LiveKit SFU migration

---

## Voice Recording System

### Push-to-Talk Pattern
```csharp
// Hold button to record
if (Input.GetMouseButtonDown(0)) StartRecording();
if (Input.GetMouseButtonUp(0)) StopRecording();
```

### WebGL Browser Settings
```javascript
echoCancellation: false    // Disabled for performance
noiseSuppression: false    // Disabled for performance
autoGainControl: false     // Disabled for performance
bufferSize: 8192           // 185ms protection against frame drops
```

### WAV Encoding
```csharp
byte[] wavData = AudioUtils.AudioClipToWav(audioClip);
OnRecordingCompleted?.Invoke(wavData);
```

### Key Files
```
/Assets/MetaDyn/Audio/MicrophoneRecorder.cs         # Push-to-talk recording (AI voice)
/Assets/MetaDyn/Audio/AudioUtils.cs                 # WAV encoding
/Assets/MetaDyn/Audio/MicrophonePlugin.jslib        # WebGL browser mic (AI voice)
/Assets/MetaDyn/Managers/WebRTCManager.cs           # WebRTC voice chat (player-to-player)
/Assets/Plugins/WebGL/WebRTCVoice.jslib             # Browser WebRTC implementation
/Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs  # Player lip sync (WebRTC + AudioSource)
```

---

## Voice Communication Systems

### AI Voice (Push-to-Talk) - PRODUCTION READY
- Microphone recording (MicrophoneRecorder.cs)
- OpenAI Whisper speech-to-text
- OpenRouter integration (Gemini 1.5/2.0 Flash models)
- ElevenLabs TTS with streaming audio
- Lip sync integration with RPM avatars (Wolf3D)
- Animation triggers (talking/idle)
- AIPerceptionManager environmental context injection
- AIEye vision system for multimodal conversations
- HeadLookController natural head tracking
- Instant interrupt logic for responsive conversations
- Conversation history management (20 message limit)

### Player-to-Player Voice Chat (WebRTC) - PRODUCTION READY
- Browser's native WebRTC API (P2P audio)
- Per-player WebRTCManager on Player prefab
- Fusion ReliableData for signaling (SDP/ICE with sender wrapping)
- Unique GameObject naming per player (`WebRTCManager_{PlayerId}`)
- Pending signal queue for async microphone initialization
- **Mesh Topology:** P2P bandwidth-dependent, scales to 50 concurrent players
- **Spatial Audio:** Verified working (2025-12-20)
- **Lip Sync:** Verified working (2025-12-20)
- **Audio Quality:** Crystal clear, no distortion
- **Lip Sync Integration:** AvatarSdkPlayerLipSync with WebRTC audio level detection
- **Status:** Production ready as of 2025-12-22
- **Future Scale (50+ players):** LiveKit SFU migration (deferred until needed)
- **See:** `/Assets/MetaDyn/Managers/WebRTC-Voice-System.md`

---

## Performance Targets

- **FPS:** 60+ on mid-range hardware
- **Ping:** < 50ms for good experience
- **Memory:** Monitor GC allocations (use pooling)
- **Network:** Up to 50 players per session (WebRTC P2P mesh, bandwidth-dependent)
- **Voice Bandwidth:** ~50-100 kbps upload per player connection (mesh topology)

---

## Testing Checklist

### Local Testing
- [ ] Player spawns at EntrancePoint
- [ ] NameTag appears above player
- [ ] Name syncs across clients
- [ ] User list updates when players join/leave
- [ ] First player becomes admin
- [ ] Permissions work (block/kick/ban)
- [ ] Voice recording captures audio
- [ ] Stats display shows FPS/ping

### WebGL Testing
- [ ] Builds successfully
- [ ] Microphone permission prompt appears
- [ ] Voice recording works in browser
- [ ] WebRTC voice chat connects (P2P mesh)
- [ ] Spatial audio works with distance falloff
- [ ] Lip sync synchronized with voice
- [ ] Performance acceptable (30+ FPS with 8+ players)
- [ ] Deployment to server successful
- [ ] Auto-join works from runtime config
- [ ] Test with 8-20 concurrent players (bandwidth/performance)

### Cloudflare Testing
- [x] Unity WebGL loads from Cloudflare edge
- [x] WebSocket connections work (Photon Fusion)
- [x] WebRTC signaling works (voice chat)
- [x] Spatial audio functions correctly
- [x] Brotli compression preserved
- [x] Cache hit ratio >90% after warmup
- [x] DNS resolves in <20ms
- [x] No CORS issues with cached assets
- [x] SSL/TLS certificates valid
- [x] OpenAI/OpenRouter APIs faster

---

## Related Documentation

- **Main Quick Reference:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **AI System:** [AI_EMBODIMENT.md](AI_EMBODIMENT.md)
- **Authentication:** [AUTH_SYSTEM.md](AUTH_SYSTEM.md)
- **WebRTC Voice System:** `/Assets/MetaDyn/Managers/WebRTC-Voice-System.md`

---

**Last Updated:** 2026-01-02
