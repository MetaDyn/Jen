# MML (Metaverse Markup Language) Integration Plan

**Created:** 2026-02-06 | **Status:** Research / Planning | **Priority:** High

---

## What is MML?

MML is an open-source markup language for describing 3D multi-user interactive objects and experiences, built on top of HTML and JavaScript. It's maintained by [mml-io](https://github.com/mml-io/mml) and backed by Somnia Network.

The key innovation is **Networked DOM** — MML documents run server-side (Node.js + JSDOM), and their DOM state is synchronized to all connected clients via WebSocket. Clients send events (clicks, collisions, position updates) back to the server. The server is the single source of truth.

```
┌─────────────────────────────────────────────────────────────────┐
│                    MML Architecture                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   MML Document Server (Node.js)                                  │
│   ├── Runs HTML+JS via JSDOM                                     │
│   ├── Maintains authoritative DOM state                          │
│   ├── Broadcasts DOM mutations via WebSocket                     │
│   └── Receives user events (click, collision, position)          │
│              ↕ WebSocket (networked-dom protocol)                │
│   ┌─────────┼─────────┐                                         │
│   ↓         ↓         ↓                                         │
│ Three.js  PlayCanvas  Unity (NEW)                                │
│ Client    Client      Client                                     │
│                                                                  │
│ All clients see the same state. Any client's interaction         │
│ updates ALL clients in real-time.                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why This Matters for MetaDyn

### Cross-Platform Object Sync
MML objects placed in a Unity scene would be visible and interactive from a Three.js/React web client connecting to the same server — and vice versa. This enables:

- **Web viewers** that show the same interactive objects as the Unity WebGL build
- **Lightweight web clients** (React/Three.js) for spectators or mobile users
- **Dashboard integration** — live 3D previews of spaces on dashboard.metadyn.xyz
- **Interoperability** with other MML-compatible platforms (Somnia, Otherside)

### Server-Authoritative Interactive Objects
Instead of syncing object state through Photon Fusion RPCs/NetworkObjects, MML objects run their logic on a Node.js server. This means:

- Object behavior defined in familiar HTML + JavaScript
- No Unity rebuilds needed to change object behavior
- Hot-reloadable interactive content
- Creator-friendly scripting (web devs can build metaverse objects)

### Composability
Multiple MML document servers can feed into a single world. Each object/experience can be hosted independently and composed together:

```
World Server
├── ws://objects.metadyn.xyz/fountain    → Interactive fountain
├── ws://objects.metadyn.xyz/jukebox     → Shared music player
├── ws://objects.metadyn.xyz/scoreboard  → Live scoreboard
└── ws://objects.metadyn.xyz/npc-quest   → Quest NPC dialog tree
```

---

## MML Elements (Available Tags)

### 3D Primitives
| Element | Description |
|---------|-------------|
| `<m-cube>` | Box/cube geometry |
| `<m-sphere>` | Sphere geometry |
| `<m-cylinder>` | Cylinder geometry |
| `<m-plane>` | Flat plane |
| `<m-group>` | Transform container (like Unity empty GameObject) |

### Content
| Element | Description |
|---------|-------------|
| `<m-model>` | 3D model (GLTF/GLB) |
| `<m-character>` | Animated character/avatar |
| `<m-image>` | 2D image in 3D space |
| `<m-video>` | Video playback surface |
| `<m-audio>` | Spatial audio source |
| `<m-label>` | Text label in 3D space |

### Interactive
| Element | Description |
|---------|-------------|
| `<m-interaction>` | Interaction zone |
| `<m-prompt>` | User prompt/dialog |
| `<m-link>` | Navigation link |
| `<m-chat-probe>` | Chat message capture |
| `<m-frame>` | Embed another MML document (composability) |

### Animation
| Element | Description |
|---------|-------------|
| `<m-attr-anim>` | Attribute animation (keyframe) |
| `<m-attr-lerp>` | Attribute interpolation |

### Common Attributes (all elements)
- `x`, `y`, `z` — Position
- `rx`, `ry`, `rz` — Rotation
- `sx`, `sy`, `sz` — Scale
- `color` — Material color
- `visible` — Visibility toggle

### Events
- `click` — User click/tap
- `collisionstart` / `collisionmove` / `collisionend` — Physics collisions
- `positionenter` / `positionmove` / `positionleave` — User position tracking
- `chatmessage` — Chat probe messages
- `prompt` — Prompt responses

---

## WebSocket Protocol (Networked DOM)

### Protocol Versions
- **v0.1** — Initial protocol
- **v0.2** — Current (improved)

### Message Flow

**Server → Client (DOM Updates):**
```
1. Initial snapshot: Full DOM tree serialized as JSON
2. Mutations: Incremental updates (add/remove/modify nodes and attributes)
3. Each node has a numeric ID for efficient referencing
```

**Client → Server (User Events):**
```
1. DOM events: click, collision, position updates
2. Events include the target node ID + event data
3. Server-side JS handlers process events, mutate DOM
4. Mutations broadcast to all clients
```

### Connection Lifecycle
```
Client connects via WebSocket (ws:// or wss://)
    → Server sends full DOM snapshot
    → Client renders 3D scene from DOM
    → User interacts → Client sends event to server
    → Server JS processes event → DOM mutates
    → Server broadcasts mutation to ALL connected clients
    → All clients update their 3D scene
```

---

## Implementation Strategy for MetaDyn

### Phase 1: Unity MML Client (C# WebSocket Consumer)

Build a Unity-side MML client that connects to Networked DOM servers and renders MML elements as Unity GameObjects.

**Key Components:**

```
/Assets/MetaDyn/MML/
├── MMLClient.cs                 # WebSocket connection to MML document server
├── MMLDocumentRenderer.cs       # Converts DOM tree → Unity GameObjects
├── MMLElementFactory.cs         # Maps m-* tags to Unity primitives/prefabs
├── MMLAttributeParser.cs        # Parses MML attributes → Unity transforms/materials
├── MMLEventDispatcher.cs        # Sends user events back to server
├── MMLFrameLoader.cs            # Handles <m-frame> composition
└── Elements/
    ├── MCubeElement.cs          # m-cube → Unity cube primitive
    ├── MSphereElement.cs        # m-sphere → Unity sphere primitive
    ├── MModelElement.cs         # m-model → GLTFUtility loader
    ├── MVideoElement.cs         # m-video → Unity VideoPlayer
    ├── MAudioElement.cs         # m-audio → Unity AudioSource (spatial)
    ├── MImageElement.cs         # m-image → Unity quad + texture
    ├── MLabelElement.cs         # m-label → TextMeshPro
    └── MCharacterElement.cs     # m-character → RPM avatar loader
```

**WebSocket Library:** [NativeWebSocket](https://github.com/endel/NativeWebSocket) — no external DLLs, WebGL compatible.

**Protocol Implementation:**
1. Parse incoming JSON DOM snapshots
2. Build a local DOM tree (Dictionary<int, MMLNode>)
3. Apply incremental mutations (add/remove/modify)
4. Map each MMLNode to a Unity GameObject via MMLElementFactory
5. Forward user interactions (clicks, collisions) as events back to server

### Phase 2: Photon Fusion + MML Coexistence

MML objects exist alongside Photon Fusion networked objects. They are NOT mutually exclusive:

```
MetaDyn World
├── Photon Fusion Layer (existing)
│   ├── Players (NetworkObject, StateAuthority)
│   ├── UserListManager (NetworkDictionary)
│   └── WebRTC Voice (P2P)
│
├── MML Layer (new)
│   ├── MMLClient connects to ws://objects.metadyn.xyz/space-id
│   ├── Interactive objects rendered as local GameObjects
│   ├── Clicks/collisions forwarded to MML server
│   └── All players see same MML state (via MML server, not Photon)
│
└── Hybrid: MML objects can reference Photon player data
    └── e.g., m-chat-probe captures local chat → MML server processes
```

### Phase 3: Three.js/React Web Client

Using the existing `@mml-io/mml-web-threejs` package, build a lightweight web viewer:

```
/Dev/metadyn-web-viewer/
├── src/
│   ├── App.tsx                  # React app
│   ├── MMLScene.tsx             # Three.js scene + MML client
│   └── PlayerAvatar.tsx         # Simple avatar representation
├── package.json                 # @mml-io/mml-web-threejs dependency
└── ...
```

This connects to the SAME MML document server as Unity clients, seeing the same objects and state. Could be embedded in dashboard.metadyn.xyz for live space previews.

### Phase 4: MML Document Hosting

Host MML documents on existing Cloudflare infrastructure:

```
objects.metadyn.xyz (Cloudflare Worker or Node.js)
├── /fountain     → Interactive water fountain
├── /jukebox      → Shared music player with playlist
├── /scoreboard   → Real-time event scoreboard
├── /npc/{name}   → AI NPC dialog (could integrate with Aurora!)
└── /space/{id}   → Dynamic objects per space
```

---

## Integration with Existing MetaDyn Systems

### Aurora AI + MML
Aurora could control MML objects through her action tag system:
```
*mml_interact:jukebox:play*     → Send click event to jukebox MML object
*mml_spawn:decoration:tree*     → Request server to add element
```

### SDK Components as MML Objects
Some MetaDyn SDK components could have MML equivalents for cross-platform:
| SDK Component | MML Equivalent |
|---------------|----------------|
| ProjectionSurface | `<m-video>` with shared URL |
| SeatHotspot | `<m-model>` + `<m-interaction>` with sit logic |
| Interactable | `<m-group>` + click handler |

### Dashboard Live Preview
Embed the Three.js MML client in dashboard.metadyn.xyz to show live object state of a space without loading Unity WebGL.

---

## Technical Considerations

### WebGL WebSocket Limits
- Unity WebGL already uses WebSockets for Photon Fusion
- Additional MML WebSocket connections should be lightweight (DOM diffs are small)
- NativeWebSocket supports WebGL builds

### Performance
- MML objects are local GameObjects (no NetworkObject overhead)
- DOM mutations are incremental (not full snapshots every frame)
- Element count should be reasonable per document (<100 elements typical)

### Coordinate System
- MML uses right-handed Y-up (same as Three.js)
- Unity uses left-handed Y-up
- MMLAttributeParser needs to flip Z-axis on positions and rotations

### GLTF Model Loading
- `<m-model>` requires GLTF/GLB loading in Unity
- Options: GLTFUtility, UnityGLTF, or existing RPM loader infrastructure
- Already have RPM SDK which uses GLTF internally

---

## Risks & Unknowns

| Risk | Mitigation |
|------|------------|
| No official Unity client exists | We build our own — protocol is documented and open |
| Protocol may evolve (v0.2 → v0.3) | Abstract protocol layer, version negotiate on connect |
| Coordinate system differences | Centralized conversion in MMLAttributeParser |
| Performance with many MML objects | Limit per-space, use object pooling |
| Two networking layers (Photon + MML WS) | Clear separation of concerns, MML for objects only |

---

## Estimated Effort

| Phase | Scope | Estimate |
|-------|-------|----------|
| Phase 1: Unity MML Client | Core WebSocket + element rendering | Medium |
| Phase 2: Photon Coexistence | Integration layer + event bridging | Small |
| Phase 3: Web Viewer | Three.js client using existing MML packages | Small |
| Phase 4: Document Hosting | Cloudflare Worker MML server | Small-Medium |

---

## Next Steps

1. Clone `mml-io/mml` repo and study the `networked-dom-protocol` source for exact message formats
2. Run the [mml-starter-project](https://github.com/mml-io/mml-starter-project) locally to observe WebSocket traffic
3. Prototype `MMLClient.cs` with NativeWebSocket connecting to a test MML document
4. Render basic primitives (m-cube, m-sphere) as Unity GameObjects
5. Forward click events back to server and verify multi-client sync

---

## References

- [MML GitHub (mml-io/mml)](https://github.com/mml-io/mml)
- [MML Website (mml.io)](https://mml.io/)
- [3D Web Experience](https://github.com/mml-io/3d-web-experience)
- [MML Starter Project](https://github.com/mml-io/mml-starter-project)
- [MML Editor (mmleditor.com)](https://mmleditor.com)
- [Somnia MML Introduction](https://blog.somnia.network/an-introduction-to-mml-somnia-s-core-language-for-defining-interoperable-objects)
- [NativeWebSocket for Unity](https://github.com/endel/NativeWebSocket)

---

**Last Updated:** 2026-02-06
