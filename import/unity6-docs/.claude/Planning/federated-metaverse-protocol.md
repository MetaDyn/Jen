# MetaDyn Federated Metaverse Protocol (MFMP)

**Date:** 2026-01-11
**Status:** Research & Design Phase
**Contributors:** Unity Architect, Metaverse CTO

---

## Executive Summary

This document outlines the technical architecture and strategic framework for enabling **federated cross-world connectivity** in MetaDyn - allowing independently-hosted Unity WebGL worlds to interconnect, display visual representations of adjacent worlds, and enable seamless avatar teleportation between them.

This is inspired by Second Life's HyperGrid protocol but designed for modern WebGL constraints and opportunities.

---

# Part 1: Strategic Analysis (Metaverse CTO)

## 1.1 Protocol Design Philosophy

### Open vs Proprietary Considerations

| Approach | Pros | Cons |
|----------|------|------|
| **Fully Open Protocol** | Community adoption, ecosystem growth, defensible moat through being "the standard" | Competitors can use it, harder to monetize |
| **Proprietary Closed** | Full control, monetization flexibility | Limited adoption, walled garden |
| **Open Core + Premium Features** | Best of both - adoption + monetization | More complex to implement |

**Recommendation:** **Open Core Model**
- Open-source the base federation protocol (MFMP-Core)
- Premium features: Enhanced analytics, priority routing, verified world badges
- This positions MetaDyn as the "HTTP of the metaverse" while maintaining revenue

### Competitive Landscape Analysis

| Platform | Federation Status | Approach |
|----------|-------------------|----------|
| **Second Life HyperGrid** | Partial federation | OpenSim-based, works but fragmented identity, limited adoption |
| **VRChat** | Walled garden | No federation, all worlds hosted on VRChat servers |
| **Spatial** | Walled garden | Enterprise focus, no interop |
| **Decentraland** | Blockchain-based | Land parcels on Ethereum, technically federated but high friction |
| **Horizon Worlds** | Walled garden | Meta-controlled, no outside worlds |

**Key Insight:** No WebGL-native metaverse has successfully implemented federation. This is a **blue ocean opportunity**.

### Lessons from Second Life HyperGrid

**What Worked:**
- Asset UUID system for cross-grid identity
- Teleport protocol between independently-hosted regions
- Avatar appearance persistence across grids

**What Failed:**
- Fragmented identity (different accounts per grid)
- No unified economy (currency didn't transfer)
- Trust issues (griefers could hop between grids)
- Technical complexity kept adoption low

**MetaDyn Should:**
- Unified identity from day one (Supabase auth + portable credentials)
- Federation opt-in per world (trust levels)
- Start with visual continuity, add teleportation later

---

## 1.2 Trust & Identity Layer

### World Trust Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    TRUST LEVELS                             │
├─────────────────────────────────────────────────────────────┤
│ Level 0: Unknown       - No data exchange                   │
│ Level 1: Visible       - Can see horizon/imposter           │
│ Level 2: Previewable   - Can see live player counts         │
│ Level 3: Traversable   - Avatars can teleport               │
│ Level 4: Trusted       - Full inventory/economy exchange    │
│ Level 5: Verified      - MetaDyn-verified partner world     │
└─────────────────────────────────────────────────────────────┘
```

### Identity Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 METADYN IDENTITY TOKEN (MIT)                │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "mid": "uuid-v4",           // MetaDyn ID (permanent)     │
│   "display_name": "string",   // User-chosen name           │
│   "avatar_hash": "sha256",    // Current avatar appearance  │
│   "home_world": "url",        // Origin world               │
│   "permissions": [],          // Portable permissions       │
│   "reputation": 0-1000,       // Cross-world reputation     │
│   "created": "ISO-8601",                                    │
│   "signature": "jwt"          // Signed by Supabase         │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
```

**Key Decisions:**
- Identity anchored to Supabase (not per-world accounts)
- JWT-signed tokens for cross-world auth
- Reputation travels with user (grief in one world, reputation follows)
- Avatar appearance hash allows destination to verify/reconstruct

### Avatar Portability Tiers

| Tier | What Transfers | Use Case |
|------|----------------|----------|
| **Basic** | Name, reputation only | Minimalist worlds |
| **Appearance** | + Avatar mesh/texture hashes | Most worlds |
| **Full** | + Inventory, animations, emotes | Trusted partners |

---

## 1.3 Economic Implications

### Federation Impact on Virtual Economy

**Risks:**
- Currency arbitrage between worlds with different economies
- Asset duplication exploits
- "Race to bottom" on creator royalties
- Value leakage from premium worlds

**Opportunities:**
- Larger addressable market for creators
- Network effects increase platform value
- Cross-world events and experiences
- "Metaverse tourism" drives engagement

### Revenue Models Comparison

| Model | Walled Garden | Federated |
|-------|---------------|-----------|
| World hosting fees | High control | Lower per-world, more worlds |
| Transaction fees | 100% capture | Shared with federation |
| Creator royalties | Platform-enforced | Requires protocol-level DRM |
| Advertising | Controlled placement | Distributed, harder to price |
| Premium features | Per-world | Cross-world premium tiers |

**Recommendation:** Hybrid Model
- Base federation is free (drives adoption)
- Premium tier: Analytics, priority teleport routing, verified badges
- Transaction fees: 2.5% on cross-world asset transfers
- Creator protection: Protocol-level royalty enforcement

### Creator Rights Across Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│              ASSET RIGHTS METADATA (ARM)                    │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "asset_id": "uuid",                                       │
│   "creator_mid": "uuid",        // Creator's MetaDyn ID     │
│   "license": "MIT|CC|Custom",   // License type             │
│   "transferable": true|false,   // Can leave origin world?  │
│   "royalty_pct": 0-100,         // On resale                │
│   "allowed_worlds": ["*"|urls], // Where asset can appear   │
│   "signature": "creator_jwt"                                │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 1.4 Competitive Positioning

### Would Federation Be a Differentiator?

**Strong Yes** - Here's Why:

1. **No WebGL metaverse has it** - First-mover advantage
2. **Aligns with Web3 ethos** - Decentralization without blockchain complexity
3. **Reduces hosting burden** - Community hosts their own worlds
4. **Network effects** - Each federated world adds value to all others
5. **Creator appeal** - "Build once, deploy everywhere"

### Risks of Open Interconnection

| Risk | Mitigation |
|------|------------|
| Quality control (bad worlds reflect on MetaDyn) | Trust levels, verified badges, reporting |
| Security (exploits spread across worlds) | Sandboxed teleport, asset validation |
| Brand dilution | "Powered by MetaDyn" branding requirements |
| Support burden | Community-driven support for federated worlds |

### Strategic Moats

1. **Protocol ownership** - MetaDyn defines the standard
2. **Identity anchor** - Supabase-backed portable identity
3. **Reference implementation** - Best SDK, easiest to use
4. **Verification program** - "MetaDyn Verified World" badge
5. **Analytics platform** - Cross-world insights (premium)

---

## 1.5 Phased Roadmap

### Phase 1: Foundation (Months 1-3)
**Goal:** Protocol specification + reference implementation

- [ ] Define MFMP protocol specification (JSON-based)
- [ ] Implement MetaDyn Identity Token (MIT) in Supabase
- [ ] Create WorldManifest.json format for world metadata
- [ ] Build basic world discovery (registry)
- [ ] SDK component: `FederationEndpoint`

**Success Metric:** Two MetaDyn worlds can register with each other

### Phase 2: Visual Continuity (Months 4-6)
**Goal:** See neighboring worlds on the horizon

- [ ] Implement horizon imposter system (cubemaps/low-poly)
- [ ] WorldManifest includes horizon snapshot URLs
- [ ] Real-time player count sharing between worlds
- [ ] SDK component: `WorldHorizon` (renders distant worlds)
- [ ] Distance-based LOD for adjacent world visualization

**Success Metric:** Standing at world edge, can see neighboring world

### Phase 3: Teleportation (Months 7-9)
**Goal:** Seamless avatar transfer between worlds

- [ ] Avatar state serialization format
- [ ] Background world preloading system
- [ ] Photon room handoff protocol
- [ ] SDK component: `TeleportGate`
- [ ] Destination world validation + trust check

**Success Metric:** Avatar can teleport between two independently-hosted worlds

### Phase 4: Economy & Assets (Months 10-12)
**Goal:** Cross-world commerce

- [ ] Asset Rights Metadata (ARM) implementation
- [ ] Cross-world inventory API
- [ ] Creator royalty enforcement
- [ ] Premium federation tier
- [ ] Marketplace cross-listing

**Success Metric:** Creator sells asset in World A, buyer uses in World B

---

# Part 2: Technical Architecture (Unity Architect)

## 2.1 Cross-World Connectivity Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         WORLD A (Origin)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Player    │  │  Photon     │  │ Federation  │                 │
│  │   Avatar    │──│  Fusion     │──│  Manager    │                 │
│  └─────────────┘  └─────────────┘  └──────┬──────┘                 │
└────────────────────────────────────────────┼────────────────────────┘
                                             │ HTTPS/WebSocket
                                             ▼
                              ┌──────────────────────────┐
                              │   Federation Registry    │
                              │   (Supabase + Edge)      │
                              └──────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────┼────────────────────────┐
│                         WORLD B (Destination)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌──────┴──────┐                 │
│  │   Player    │  │  Photon     │  │ Federation  │                 │
│  │   Spawned   │◀─│  Fusion     │◀─│  Manager    │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
```

### WorldManifest.json Specification

Each federated world publishes a manifest at `https://world.example.com/metadyn/manifest.json`:

```json
{
  "mfmp_version": "1.0",
  "world_id": "uuid-v4",
  "name": "Crystal Caverns",
  "description": "An underground crystal world",
  "owner_mid": "uuid-v4",
  "trust_level": 3,

  "endpoints": {
    "entry": "https://crystalcaverns.io/",
    "api": "https://crystalcaverns.io/api/federation/",
    "photon_app_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "photon_region": "us"
  },

  "coordinates": {
    "grid_x": 100,
    "grid_y": 200,
    "bounds": { "width": 500, "height": 500 }
  },

  "horizon": {
    "cubemap_url": "https://cdn.crystalcaverns.io/horizon.ktx2",
    "lowpoly_url": "https://cdn.crystalcaverns.io/horizon.glb",
    "update_frequency": 3600
  },

  "capacity": {
    "current_players": 12,
    "max_players": 50
  },

  "requirements": {
    "min_reputation": 0,
    "required_permissions": [],
    "blocked_users": []
  },

  "signature": "jwt-signed-by-owner"
}
```

---

## 2.2 Avatar State Serialization

### AvatarTransferPacket Structure

```csharp
namespace MetaDyn.Federation
{
    /// <summary>
    /// Complete avatar state for cross-world teleportation
    /// Serialized to JSON for transmission
    /// </summary>
    [System.Serializable]
    public class AvatarTransferPacket
    {
        // Identity (from MetaDyn Identity Token)
        public string MetaDynId;
        public string DisplayName;
        public string IdentityToken;  // JWT for verification

        // Avatar Appearance
        public string AvatarPrefabId;      // Which avatar prefab
        public string AvatarMeshHash;       // SHA256 of mesh data
        public AvatarCustomization Customization;

        // Position (relative to teleport gate)
        public SerializableVector3 EntryPosition;
        public SerializableQuaternion EntryRotation;

        // State
        public string CurrentEmote;
        public bool IsMuted;
        public float VoiceVolume;

        // Inventory (if trust level allows)
        public InventorySnapshot Inventory;

        // Metadata
        public string OriginWorldId;
        public string OriginWorldUrl;
        public long Timestamp;
        public string PacketSignature;  // Signed by origin world
    }

    [System.Serializable]
    public class AvatarCustomization
    {
        public string SkinColor;
        public string HairStyle;
        public string HairColor;
        public string[] EquippedItems;
        // Extensible for RPM/AvatarSDK parameters
    }

    [System.Serializable]
    public class SerializableVector3
    {
        public float x, y, z;

        public static implicit operator Vector3(SerializableVector3 v)
            => new Vector3(v.x, v.y, v.z);
        public static implicit operator SerializableVector3(Vector3 v)
            => new SerializableVector3 { x = v.x, y = v.y, z = v.z };
    }
}
```

### Serialization Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Player    │───▶│  Serialize  │───▶│   Encrypt   │───▶│  Transmit   │
│   State     │    │  to JSON    │    │   + Sign    │    │  via HTTPS  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                │
                                                                ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Spawn     │◀───│ Deserialize │◀───│   Verify    │◀───│   Receive   │
│   Avatar    │    │  from JSON  │    │   + Decrypt │    │   Packet    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 2.3 Photon Fusion Cross-Room Handoff

### The Challenge

Photon Fusion rooms are isolated - you can't directly transfer a NetworkObject between rooms/servers. We need a **disconnect-reconnect pattern** with state preservation.

### Handoff Sequence

```
Timeline:
─────────────────────────────────────────────────────────────────────────▶

WORLD A (Origin)                           WORLD B (Destination)
┌─────────────────────────┐               ┌─────────────────────────┐
│ 1. Player enters gate   │               │                         │
│ 2. Serialize avatar     │               │                         │
│ 3. Send transfer packet │──────────────▶│ 4. Receive packet       │
│ 4. Preload World B      │               │ 5. Validate identity    │
│    (iframe/background)  │               │ 6. Reserve spawn slot   │
│ 5. Confirm ready        │◀──────────────│ 7. Send ready signal    │
│ 6. Disconnect Photon A  │               │                         │
│ 7. Fade to black        │               │                         │
│ 8. Unload World A       │               │                         │
│ 9. Navigate to World B  │──────────────▶│ 10. Player arrives      │
│                         │               │ 11. Connect Photon B    │
│                         │               │ 12. Spawn with state    │
│                         │               │ 13. Fade from black     │
└─────────────────────────┘               └─────────────────────────┘
```

### Implementation: FederationManager

```csharp
namespace MetaDyn.Federation
{
    /// <summary>
    /// Manages cross-world federation, teleportation, and horizon rendering
    /// Singleton attached to persistent GameObject
    /// </summary>
    public class FederationManager : MonoBehaviour
    {
        public static FederationManager Instance { get; private set; }

        [Header("Configuration")]
        [Tooltip("URL of the federation registry")]
        public string RegistryUrl = "https://registry.metadyn.com/api/v1/";

        [Tooltip("This world's manifest")]
        public WorldManifest LocalManifest;

        [Header("Teleportation")]
        [Tooltip("Seconds to preload destination before transfer")]
        public float PreloadTimeout = 30f;

        [Tooltip("Fade duration for world transition")]
        public float FadeDuration = 1f;

        // Runtime state
        private Dictionary<string, WorldManifest> _knownWorlds = new();
        private string _pendingTransferWorldId;
        private AvatarTransferPacket _incomingTransfer;

        // Events
        public event Action<WorldManifest> OnWorldDiscovered;
        public event Action<string> OnTeleportStarted;
        public event Action<string> OnTeleportCompleted;
        public event Action<string, string> OnTeleportFailed;

        private void Awake()
        {
            if (Instance != null) { Destroy(gameObject); return; }
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }

        /// <summary>
        /// Initiate teleportation to another world
        /// </summary>
        public async Task<bool> TeleportToWorld(string worldId, Vector3 entryPoint)
        {
            if (!_knownWorlds.TryGetValue(worldId, out var destWorld))
            {
                Debug.LogError($"[Federation] Unknown world: {worldId}");
                OnTeleportFailed?.Invoke(worldId, "World not found");
                return false;
            }

            OnTeleportStarted?.Invoke(worldId);

            try
            {
                // 1. Serialize local player state
                var packet = SerializeLocalPlayer();
                packet.EntryPosition = entryPoint;

                // 2. Request transfer from destination
                var accepted = await RequestTransfer(destWorld, packet);
                if (!accepted)
                {
                    OnTeleportFailed?.Invoke(worldId, "Transfer rejected");
                    return false;
                }

                // 3. Preload destination world (WebGL: hidden iframe)
                await PreloadDestinationWorld(destWorld);

                // 4. Disconnect from current Photon room
                await DisconnectFromCurrentWorld();

                // 5. Navigate to destination
                await NavigateToWorld(destWorld, packet);

                OnTeleportCompleted?.Invoke(worldId);
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[Federation] Teleport failed: {ex.Message}");
                OnTeleportFailed?.Invoke(worldId, ex.Message);
                return false;
            }
        }

        private AvatarTransferPacket SerializeLocalPlayer()
        {
            var player = Player.Local;
            if (player == null) throw new InvalidOperationException("No local player");

            return new AvatarTransferPacket
            {
                MetaDynId = AuthManager.Instance.UserId,
                DisplayName = player.DisplayName,
                IdentityToken = AuthManager.Instance.GetIdentityToken(),
                AvatarPrefabId = player.AvatarPrefabId,
                Customization = player.GetCustomization(),
                IsMuted = player.IsMuted,
                OriginWorldId = LocalManifest.WorldId,
                OriginWorldUrl = LocalManifest.Endpoints.Entry,
                Timestamp = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };
        }

        private async Task<bool> RequestTransfer(WorldManifest dest, AvatarTransferPacket packet)
        {
            var json = JsonUtility.ToJson(packet);
            var url = $"{dest.Endpoints.Api}transfer/request";

            using var request = UnityWebRequest.Post(url, json, "application/json");
            request.SetRequestHeader("Authorization", $"Bearer {packet.IdentityToken}");

            await request.SendWebRequest();

            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"[Federation] Transfer request failed: {request.error}");
                return false;
            }

            var response = JsonUtility.FromJson<TransferResponse>(request.downloadHandler.text);
            return response.Accepted;
        }

        #if UNITY_WEBGL && !UNITY_EDITOR
        [DllImport("__Internal")]
        private static extern void NavigateToUrl(string url);

        [DllImport("__Internal")]
        private static extern void PreloadIframe(string url);
        #endif

        private async Task PreloadDestinationWorld(WorldManifest dest)
        {
            #if UNITY_WEBGL && !UNITY_EDITOR
            PreloadIframe(dest.Endpoints.Entry + "?preload=true");
            await Task.Delay((int)(PreloadTimeout * 1000));
            #else
            // Editor: just wait briefly
            await Task.Delay(1000);
            #endif
        }

        private async Task NavigateToWorld(WorldManifest dest, AvatarTransferPacket packet)
        {
            // Store transfer packet in session storage for destination to retrieve
            var packetJson = JsonUtility.ToJson(packet);

            #if UNITY_WEBGL && !UNITY_EDITOR
            // Store in sessionStorage, navigate to destination
            StoreTransferPacket(packetJson);
            NavigateToUrl(dest.Endpoints.Entry + "?transfer=" + dest.WorldId);
            #else
            // Editor: Log the transfer
            Debug.Log($"[Federation] Would navigate to: {dest.Endpoints.Entry}");
            #endif
        }
    }
}
```

---

## 2.4 Visual Continuity: Horizon Imposters

### WebGL Constraints

**What's NOT Possible:**
- Two Unity WebGL instances sharing GPU resources
- Real-time cross-context rendering
- Shared depth buffer between iframes

**What IS Possible:**
- Pre-rendered cubemaps/skyboxes of distant worlds
- Low-poly GLB meshes loaded dynamically
- Periodic snapshot updates (not real-time)
- Addressables loading from external CDNs

### Horizon Rendering Approach

```
┌─────────────────────────────────────────────────────────────┐
│                     CURRENT WORLD                           │
│                                                             │
│    ┌─────────────────────────────────────────────────────┐ │
│    │                    WORLD BOUNDS                     │ │
│    │                                                     │ │
│    │                   [Player]                          │ │
│    │                                                     │ │
│    └─────────────────────────────────────────────────────┘ │
│                            │                                │
│    ════════════════════════╪════════════════════════════   │
│         HORIZON ZONE       │       (50-200m from edge)     │
│                            ▼                                │
│    ┌─────────────────────────────────────────────────────┐ │
│    │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│    │  ░░░ ADJACENT WORLD IMPOSTER (Cubemap/LowPoly) ░░░ │ │
│    │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│    └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### SDK Component: WorldHorizon

```csharp
namespace MetaDyn.Federation
{
    /// <summary>
    /// Renders distant federated worlds as imposters on the horizon.
    /// Attach to an empty GameObject at world boundaries.
    /// </summary>
    public class WorldHorizon : MonoBehaviour
    {
        [Header("Configuration")]
        [Tooltip("World ID of the adjacent world to render")]
        public string AdjacentWorldId;

        [Tooltip("Direction this horizon faces (from world center)")]
        public Vector3 HorizonDirection = Vector3.forward;

        [Tooltip("Distance from world edge where horizon becomes visible")]
        public float VisibilityDistance = 200f;

        [Header("Rendering")]
        [Tooltip("Material for cubemap skybox rendering")]
        public Material CubemapMaterial;

        [Tooltip("Container for low-poly mesh")]
        public Transform MeshContainer;

        [Header("Runtime")]
        [SerializeField, ReadOnly]
        private WorldManifest _adjacentManifest;

        [SerializeField, ReadOnly]
        private int _currentPlayerCount;

        private Cubemap _horizonCubemap;
        private GameObject _lowPolyMesh;
        private bool _isLoaded;

        private async void Start()
        {
            if (string.IsNullOrEmpty(AdjacentWorldId)) return;

            await LoadAdjacentWorldData();
        }

        private async Task LoadAdjacentWorldData()
        {
            // Fetch manifest from registry
            _adjacentManifest = await FederationManager.Instance
                .GetWorldManifest(AdjacentWorldId);

            if (_adjacentManifest == null)
            {
                Debug.LogWarning($"[WorldHorizon] Could not load manifest for {AdjacentWorldId}");
                return;
            }

            // Load horizon assets
            await LoadHorizonAssets();

            // Start periodic player count updates
            StartCoroutine(UpdatePlayerCountRoutine());
        }

        private async Task LoadHorizonAssets()
        {
            var horizon = _adjacentManifest.Horizon;

            // Load cubemap (KTX2 format for WebGL compression)
            if (!string.IsNullOrEmpty(horizon.CubemapUrl))
            {
                _horizonCubemap = await LoadCubemapFromUrl(horizon.CubemapUrl);
                if (_horizonCubemap != null && CubemapMaterial != null)
                {
                    CubemapMaterial.SetTexture("_Cubemap", _horizonCubemap);
                }
            }

            // Load low-poly mesh (GLB format)
            if (!string.IsNullOrEmpty(horizon.LowpolyUrl) && MeshContainer != null)
            {
                _lowPolyMesh = await LoadGLBFromUrl(horizon.LowpolyUrl);
                if (_lowPolyMesh != null)
                {
                    _lowPolyMesh.transform.SetParent(MeshContainer, false);
                }
            }

            _isLoaded = true;
        }

        private void Update()
        {
            if (!_isLoaded) return;

            // Fade based on player distance to horizon
            var player = Player.Local?.transform;
            if (player == null) return;

            var distanceToEdge = CalculateDistanceToWorldEdge(player.position);
            var visibility = Mathf.InverseLerp(VisibilityDistance, 50f, distanceToEdge);

            // Apply visibility to renderers
            SetHorizonVisibility(visibility);
        }

        private IEnumerator UpdatePlayerCountRoutine()
        {
            while (true)
            {
                yield return new WaitForSeconds(30f);

                var count = await FederationManager.Instance
                    .GetWorldPlayerCount(AdjacentWorldId);
                _currentPlayerCount = count;
            }
        }

        #if UNITY_EDITOR
        private void OnDrawGizmos()
        {
            Gizmos.color = Color.cyan;
            Gizmos.DrawRay(transform.position, HorizonDirection.normalized * 50f);

            Gizmos.color = new Color(0, 1, 1, 0.2f);
            Gizmos.DrawWireSphere(transform.position, VisibilityDistance);

            // Draw adjacent world label
            UnityEditor.Handles.Label(
                transform.position + Vector3.up * 5f,
                $"Horizon: {AdjacentWorldId}\nPlayers: {_currentPlayerCount}"
            );
        }
        #endif
    }
}
```

---

## 2.5 Addressables for Cross-Server Asset Loading

### Architecture for External Asset Bundles

```
┌─────────────────────────────────────────────────────────────┐
│                    METADYN WORLD                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ADDRESSABLES SYSTEM                     │   │
│  │                                                      │   │
│  │  Local Catalog ──┬── Local Assets                   │   │
│  │                  │                                   │   │
│  │  Remote Catalog ─┴── https://cdn.otherworld.io/     │   │
│  │                      └── horizon_assets/            │   │
│  │                          ├── cubemap.ktx2           │   │
│  │                          ├── lowpoly.glb            │   │
│  │                          └── preview.jpg            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Dynamic Catalog Loading

```csharp
namespace MetaDyn.Federation
{
    /// <summary>
    /// Loads assets from federated world CDNs via Addressables
    /// </summary>
    public static class FederatedAssetLoader
    {
        private static HashSet<string> _loadedCatalogs = new();

        /// <summary>
        /// Load a remote Addressables catalog from a federated world
        /// </summary>
        public static async Task<bool> LoadWorldCatalog(WorldManifest world)
        {
            var catalogUrl = $"{world.Endpoints.Api}addressables/catalog.json";

            if (_loadedCatalogs.Contains(catalogUrl))
                return true;

            try
            {
                var handle = Addressables.LoadContentCatalogAsync(catalogUrl);
                await handle.Task;

                if (handle.Status == AsyncOperationStatus.Succeeded)
                {
                    _loadedCatalogs.Add(catalogUrl);
                    Debug.Log($"[FederatedAssets] Loaded catalog from {world.Name}");
                    return true;
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[FederatedAssets] Failed to load catalog: {ex.Message}");
            }

            return false;
        }

        /// <summary>
        /// Load an asset from a federated world by key
        /// </summary>
        public static async Task<T> LoadAsset<T>(string worldId, string assetKey)
            where T : UnityEngine.Object
        {
            // Asset keys are namespaced: "worldId/assetKey"
            var fullKey = $"{worldId}/{assetKey}";

            try
            {
                var handle = Addressables.LoadAssetAsync<T>(fullKey);
                await handle.Task;

                if (handle.Status == AsyncOperationStatus.Succeeded)
                {
                    return handle.Result;
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[FederatedAssets] Failed to load {fullKey}: {ex.Message}");
            }

            return null;
        }
    }
}
```

---

## 2.6 SDK Components Overview

### Component Hierarchy

```
MetaDyn.Federation
├── FederationManager         (Singleton - manages all federation)
├── WorldHorizon              (SDK Component - renders distant world)
├── TeleportGate              (SDK Component - teleport trigger)
├── FederationEndpoint        (SDK Component - marks world entry/exit points)
└── WorldBoundary             (SDK Component - defines world edges)
```

### SDK Component: TeleportGate

```csharp
namespace MetaDyn.Federation
{
    /// <summary>
    /// Interactive gate that teleports players to another federated world.
    /// Place at world boundaries where players should transition.
    /// </summary>
    public class TeleportGate : MonoBehaviour
    {
        [Header("Destination")]
        [Tooltip("World ID to teleport to (from registry)")]
        public string DestinationWorldId;

        [Tooltip("Spawn point ID in destination world")]
        public string DestinationSpawnPoint = "default";

        [Header("Interaction")]
        [Tooltip("Radius within which player can activate gate")]
        public float InteractionRadius = 3f;

        [Tooltip("Key to activate teleport")]
        public KeyCode ActivationKey = KeyCode.E;

        [Tooltip("Require confirmation before teleporting")]
        public bool RequireConfirmation = true;

        [Header("Visual")]
        [Tooltip("Particle system to play when gate is active")]
        public ParticleSystem GateParticles;

        [Tooltip("Audio to play when teleporting")]
        public AudioClip TeleportSound;

        [Header("Runtime Info")]
        [SerializeField, ReadOnly]
        private WorldManifest _destinationManifest;

        [SerializeField, ReadOnly]
        private bool _playerInRange;

        [SerializeField, ReadOnly]
        private bool _isLoading;

        // Events
        public event Action OnTeleportStarted;
        public event Action OnTeleportCancelled;

        private async void Start()
        {
            if (string.IsNullOrEmpty(DestinationWorldId))
            {
                Debug.LogWarning($"[TeleportGate] No destination configured on {gameObject.name}");
                return;
            }

            _destinationManifest = await FederationManager.Instance
                .GetWorldManifest(DestinationWorldId);

            if (_destinationManifest != null && GateParticles != null)
            {
                GateParticles.Play();
            }
        }

        private void Update()
        {
            if (_isLoading) return;

            var player = Player.Local?.transform;
            if (player == null) return;

            var distance = Vector3.Distance(transform.position, player.position);
            _playerInRange = distance <= InteractionRadius;

            if (_playerInRange && Input.GetKeyDown(ActivationKey))
            {
                StartTeleport();
            }
        }

        private async void StartTeleport()
        {
            if (_destinationManifest == null)
            {
                Debug.LogError("[TeleportGate] Destination not loaded");
                return;
            }

            if (RequireConfirmation)
            {
                // Show confirmation UI
                var confirmed = await UIManager.Instance.ShowConfirmation(
                    "Teleport",
                    $"Travel to {_destinationManifest.Name}?\n" +
                    $"Current players: {_destinationManifest.Capacity.CurrentPlayers}"
                );

                if (!confirmed)
                {
                    OnTeleportCancelled?.Invoke();
                    return;
                }
            }

            _isLoading = true;
            OnTeleportStarted?.Invoke();

            if (TeleportSound != null)
            {
                AudioSource.PlayClipAtPoint(TeleportSound, transform.position);
            }

            var success = await FederationManager.Instance.TeleportToWorld(
                DestinationWorldId,
                Vector3.zero  // Destination will use DestinationSpawnPoint
            );

            if (!success)
            {
                _isLoading = false;
                UIManager.Instance.ShowError("Teleport failed. Please try again.");
            }
        }

        /// <summary>
        /// Public API: Trigger teleport programmatically
        /// </summary>
        public void Activate()
        {
            if (!_isLoading && _destinationManifest != null)
            {
                StartTeleport();
            }
        }

        #if UNITY_EDITOR
        private void OnDrawGizmos()
        {
            // Draw gate frame
            Gizmos.color = Color.magenta;
            Gizmos.DrawWireCube(transform.position, new Vector3(2f, 3f, 0.5f));

            // Draw interaction radius
            Gizmos.color = new Color(1, 0, 1, 0.3f);
            Gizmos.DrawWireSphere(transform.position, InteractionRadius);

            // Draw destination label
            var label = string.IsNullOrEmpty(DestinationWorldId)
                ? "No Destination"
                : $"To: {DestinationWorldId}";
            UnityEditor.Handles.Label(transform.position + Vector3.up * 3.5f, label);

            // Draw arrow showing direction
            Gizmos.color = Color.yellow;
            var arrowStart = transform.position;
            var arrowEnd = transform.position + transform.forward * 2f;
            Gizmos.DrawLine(arrowStart, arrowEnd);
            Gizmos.DrawSphere(arrowEnd, 0.2f);
        }

        private void OnDrawGizmosSelected()
        {
            // Draw activation key hint
            Gizmos.color = Color.white;
            UnityEditor.Handles.Label(
                transform.position + Vector3.up * 4f,
                $"Press [{ActivationKey}] to teleport"
            );
        }
        #endif
    }
}
```

---

## 2.7 WebGL-Specific Implementation

### JavaScript Interop (Federation.jslib)

```javascript
// Assets/Plugins/WebGL/Federation.jslib

mergeInto(LibraryManager.library, {

    // Store transfer packet in sessionStorage for destination world
    StoreTransferPacket: function(packetJsonPtr) {
        var packetJson = UTF8ToString(packetJsonPtr);
        sessionStorage.setItem('metadyn_transfer_packet', packetJson);
    },

    // Retrieve transfer packet (called by destination world on load)
    GetTransferPacket: function() {
        var packet = sessionStorage.getItem('metadyn_transfer_packet');
        sessionStorage.removeItem('metadyn_transfer_packet');  // One-time use

        if (packet) {
            var bufferSize = lengthBytesUTF8(packet) + 1;
            var buffer = _malloc(bufferSize);
            stringToUTF8(packet, buffer, bufferSize);
            return buffer;
        }
        return null;
    },

    // Navigate to destination world URL
    NavigateToUrl: function(urlPtr) {
        var url = UTF8ToString(urlPtr);
        window.location.href = url;
    },

    // Preload destination in hidden iframe
    PreloadIframe: function(urlPtr) {
        var url = UTF8ToString(urlPtr);

        var iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = url;
        iframe.id = 'metadyn-preload';
        document.body.appendChild(iframe);

        // Remove after timeout
        setTimeout(function() {
            var el = document.getElementById('metadyn-preload');
            if (el) el.remove();
        }, 30000);
    },

    // Post message to parent (for iframe-based preview)
    PostToParent: function(messagePtr) {
        var message = UTF8ToString(messagePtr);
        if (window.parent !== window) {
            window.parent.postMessage(JSON.parse(message), '*');
        }
    },

    // Listen for messages from parent/other frames
    RegisterMessageHandler: function(callbackPtr) {
        window.addEventListener('message', function(event) {
            // Validate origin in production
            var data = JSON.stringify(event.data);
            var bufferSize = lengthBytesUTF8(data) + 1;
            var buffer = _malloc(bufferSize);
            stringToUTF8(data, buffer, bufferSize);
            dynCall_vi(callbackPtr, buffer);
        });
    }
});
```

### C# Bindings

```csharp
namespace MetaDyn.Federation
{
    public static class FederationJSBridge
    {
        #if UNITY_WEBGL && !UNITY_EDITOR
        [DllImport("__Internal")]
        public static extern void StoreTransferPacket(string packetJson);

        [DllImport("__Internal")]
        public static extern string GetTransferPacket();

        [DllImport("__Internal")]
        public static extern void NavigateToUrl(string url);

        [DllImport("__Internal")]
        public static extern void PreloadIframe(string url);

        [DllImport("__Internal")]
        public static extern void PostToParent(string message);

        public delegate void MessageCallback(string message);

        [DllImport("__Internal")]
        public static extern void RegisterMessageHandler(MessageCallback callback);
        #else
        // Editor stubs
        public static void StoreTransferPacket(string packetJson)
            => Debug.Log($"[JSBridge] StoreTransferPacket: {packetJson.Substring(0, 100)}...");

        public static string GetTransferPacket() => null;

        public static void NavigateToUrl(string url)
            => Debug.Log($"[JSBridge] NavigateToUrl: {url}");

        public static void PreloadIframe(string url)
            => Debug.Log($"[JSBridge] PreloadIframe: {url}");

        public static void PostToParent(string message)
            => Debug.Log($"[JSBridge] PostToParent: {message}");
        #endif
    }
}
```

---

# Part 3: Implementation Priorities

## Critical Path (Must Have for MVP)

1. **WorldManifest.json specification** - Foundation for everything
2. **FederationManager singleton** - Central coordination
3. **AvatarTransferPacket serialization** - State preservation
4. **TeleportGate SDK component** - User-facing feature
5. **Federation.jslib for WebGL** - Browser navigation

## Nice to Have (Phase 2)

1. **WorldHorizon imposters** - Visual continuity
2. **Addressables cross-CDN loading** - Asset sharing
3. **Player count real-time sync** - Social proof
4. **Trust level validation** - Security

## Future (Phase 3+)

1. **Cross-world inventory** - Asset portability
2. **Economic integration** - Currency/marketplace
3. **Reputation system** - Cross-world moderation
4. **Verified world badges** - Quality signals

---

# Part 4: Open Questions

1. **Photon App ID sharing** - Do federated worlds share a Photon app, or each has their own? (Recommendation: each their own, cleaner isolation)

2. **Avatar mesh compatibility** - How do we handle worlds with different avatar systems? (Recommendation: Basic humanoid rig as fallback)

3. **Coordinate system** - Global 2D grid (like SL) or 3D spatial addressing? (Recommendation: 2D grid simpler, sufficient)

4. **Governance** - Who decides world trust levels? (Recommendation: Self-declared + MetaDyn verification for premium)

5. **Offline worlds** - What happens when destination is offline? (Recommendation: Pre-flight check, graceful error)

---

# Appendix A: Protocol Message Examples

## Transfer Request

```json
POST /api/federation/transfer/request
Authorization: Bearer <identity_token>

{
  "packet": {
    "metadyn_id": "550e8400-e29b-41d4-a716-446655440000",
    "display_name": "CrystalExplorer",
    "avatar_prefab_id": "rpm_casual_01",
    "origin_world_id": "world-alpha-001",
    "timestamp": 1704931200
  },
  "destination_spawn": "main-entrance"
}
```

## Transfer Response

```json
{
  "accepted": true,
  "spawn_point": { "x": 10.5, "y": 0, "z": 25.3 },
  "photon_room": "crystal-caverns-main",
  "estimated_load_time": 5.2,
  "message": "Welcome to Crystal Caverns!"
}
```

---

# Appendix B: Decision Record

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Protocol format | JSON over HTTPS | WebGL compatible, human readable |
| Identity anchor | Supabase JWT | Already integrated, secure |
| Coordinate system | 2D grid | Simpler, matches SL model |
| Asset format | GLB/KTX2 | WebGL optimized, compressed |
| Trust model | Self-declared + verification | Balances openness with quality |

---

**Document Version:** 1.0
**Last Updated:** 2026-01-11
**Next Review:** After Phase 1 implementation
