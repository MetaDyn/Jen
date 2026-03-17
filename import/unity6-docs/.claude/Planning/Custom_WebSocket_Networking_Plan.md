# Custom WebSocket Networking Plan

Replace Photon Fusion with custom WebSocket-based multiplayer sync.

**Created:** 2026-01-20

---

## Current Photon Dependencies

### Core Files Using Photon Fusion

| File | Photon Dependencies |
|------|---------------------|
| `Player.cs` | `NetworkBehaviour`, `[Networked]` props, `Rpc`, `FixedUpdateNetwork`, `Render`, `Spawned` |
| `GameManager.cs` | `NetworkBehaviour`, `NetworkObject`, `IPlayerJoined/Left`, `Runner.Spawn()` |
| `UserListManager.cs` | `NetworkBehaviour`, `NetworkDictionary`, `Rpc`, `IPlayerLeft`, `Runner.Disconnect()` |
| `UserData.cs` | `INetworkStruct`, `PlayerRef`, `NetworkString`, `NetworkBool` |
| `WebRTCManager.cs` | `NetworkBehaviour`, `INetworkRunnerCallbacks`, `[Networked]`, `Runner.SendReliableDataToPlayer()` |
| `ChatManager.cs` | Photon Chat SDK (separate) - `ChatClient`, `IChatClientListener` |

### Networked Properties to Sync

```
Player.cs:
  - _isJumping (NetworkBool)
  - NetworkedName (NetworkString<_32>)
  - Position/Rotation (via SimpleKCC)

UserListManager.cs:
  - Users (NetworkDictionary<PlayerRef, UserData>)

UserData struct:
  - PlayerRef, PlayerName, IsMuted, PermissionLevel

WebRTCManager.cs:
  - IsSpeaking (NetworkBool)
```

---

## Custom WebSocket Architecture

### Server Options (Pick One)

**Option A: Node.js + ws (Simplest)**
```
Node.js server
├── ws (WebSocket library)
├── Room management
├── State broadcast
└── Authority validation
```

**Option B: .NET + SignalR**
```
ASP.NET Core
├── SignalR (WebSocket abstraction)
├── Type-safe message contracts
└── Same language as Unity client
```

**Option C: Colyseus (Game-focused)**
```
Colyseus server
├── Built-in room/state management
├── Delta compression
├── Schema-based sync
└── Has Unity SDK
```

**Recommendation:** Option A (Node.js + ws) for simplest setup, or Option C (Colyseus) if you want built-in game features.

---

## Message Protocol

### Message Types

```json
// Client → Server
{ "type": "join", "name": "PlayerName", "userId": "supabase-id", "avatarIndex": 0 }
{ "type": "state", "position": [x,y,z], "rotation": [x,y,z,w], "isJumping": false }
{ "type": "rpc", "method": "kick", "target": "player-id" }
{ "type": "chat", "message": "Hello" }
{ "type": "webrtc_signal", "target": "peer-id", "signal": "..." }

// Server → Client
{ "type": "welcome", "playerId": "uuid", "isHost": true }
{ "type": "player_joined", "playerId": "uuid", "name": "...", "position": [...] }
{ "type": "player_left", "playerId": "uuid" }
{ "type": "state_update", "players": { "id": { position, rotation, ... } } }
{ "type": "user_list", "users": [...] }
{ "type": "chat", "sender": "...", "message": "..." }
{ "type": "webrtc_signal", "from": "peer-id", "signal": "..." }
```

---

## Unity Client Implementation

### 1. NetworkManager (Replace NetworkRunner)

```csharp
// /Assets/MetaDyn/Networking/CustomNetworkManager.cs
public class CustomNetworkManager : MonoBehaviour
{
    public static CustomNetworkManager Instance { get; private set; }

    public string PlayerId { get; private set; }
    public bool IsHost { get; private set; }
    public bool IsConnected => _ws?.ReadyState == WebSocketState.Open;

    // Events
    public event Action OnConnected;
    public event Action OnDisconnected;
    public event Action<string, PlayerState> OnPlayerJoined;
    public event Action<string> OnPlayerLeft;
    public event Action<Dictionary<string, PlayerState>> OnStateUpdate;

    private WebSocket _ws;
    private Dictionary<string, PlayerState> _players = new();

    public void Connect(string serverUrl, string roomName, string playerName, string userId);
    public void Disconnect();
    public void SendState(PlayerState state);
    public void SendRpc(string method, string targetId, object data);
    public void SendWebRTCSignal(string targetId, string signal);
}
```

### 2. NetworkBehaviour Replacement

```csharp
// /Assets/MetaDyn/Networking/CustomNetworkBehaviour.cs
public abstract class CustomNetworkBehaviour : MonoBehaviour
{
    public string NetworkId { get; set; }
    public bool IsLocalPlayer => NetworkId == CustomNetworkManager.Instance?.PlayerId;
    public bool IsHost => CustomNetworkManager.Instance?.IsHost ?? false;

    // Called when spawned on network
    public virtual void OnNetworkSpawn() { }

    // Called every network tick (e.g., 20Hz)
    public virtual void OnNetworkUpdate() { }

    // Called when despawned
    public virtual void OnNetworkDespawn() { }
}
```

### 3. PlayerState Struct

```csharp
// /Assets/MetaDyn/Networking/PlayerState.cs
[Serializable]
public struct PlayerState
{
    public string playerId;
    public string playerName;
    public Vector3 position;
    public Quaternion rotation;
    public bool isJumping;
    public bool isSpeaking;
    public bool isMuted;
    public byte permissionLevel;
}
```

---

## File Migration Guide

### Phase 1: Core Infrastructure

1. **Create WebSocket client wrapper**
   - `/Assets/MetaDyn/Networking/WebSocketClient.cs`
   - Use NativeWebSocket for WebGL: https://github.com/endel/NativeWebSocket

2. **Create CustomNetworkManager**
   - `/Assets/MetaDyn/Networking/CustomNetworkManager.cs`
   - Handle connect/disconnect, message routing

3. **Create PlayerState and message DTOs**
   - `/Assets/MetaDyn/Networking/NetworkMessages.cs`

### Phase 2: Player Migration

**Player.cs Changes:**

```csharp
// BEFORE (Photon)
public sealed class Player : NetworkBehaviour
{
    [Networked] private NetworkBool _isJumping { get; set; }
    [Networked] public NetworkString<_32> NetworkedName { get; set; }

    public override void Spawned() { ... }
    public override void FixedUpdateNetwork() { ... }
    public override void Render() { ... }

    [Rpc(RpcSources.StateAuthority, RpcTargets.All)]
    private void RPC_RegisterWithUserList(...) { ... }
}

// AFTER (Custom WebSocket)
public sealed class Player : CustomNetworkBehaviour
{
    private bool _isJumping;
    public string PlayerName { get; private set; }

    public override void OnNetworkSpawn()
    {
        if (IsLocalPlayer)
        {
            PlayerName = PlayerPrefs.GetString("PlayerName", "Guest");
            // Register with server
            CustomNetworkManager.Instance.SendRpc("register", null, new { name = PlayerName });
        }
    }

    void Update()
    {
        if (!IsLocalPlayer) return;
        ProcessInput();

        // Send state at fixed rate
        if (Time.time > _nextStateSend)
        {
            SendPlayerState();
            _nextStateSend = Time.time + 0.05f; // 20Hz
        }
    }

    private void SendPlayerState()
    {
        CustomNetworkManager.Instance.SendState(new PlayerState
        {
            position = transform.position,
            rotation = transform.rotation,
            isJumping = _isJumping
        });
    }

    // Called by NetworkManager when receiving remote state
    public void ApplyRemoteState(PlayerState state)
    {
        transform.position = Vector3.Lerp(transform.position, state.position, 0.3f);
        transform.rotation = Quaternion.Slerp(transform.rotation, state.rotation, 0.3f);
        _isJumping = state.isJumping;
    }
}
```

### Phase 3: GameManager Migration

**GameManager.cs Changes:**

```csharp
// BEFORE
public sealed class GameManager : NetworkBehaviour, IPlayerJoined, IPlayerLeft
{
    public override void Spawned()
    {
        NetworkObject spawnedPlayer = Runner.Spawn(avatarPrefab, spawnPos, spawnRot, Runner.LocalPlayer);
    }
}

// AFTER
public sealed class GameManager : MonoBehaviour
{
    void Start()
    {
        CustomNetworkManager.Instance.OnConnected += OnConnected;
        CustomNetworkManager.Instance.OnPlayerJoined += OnPlayerJoined;
        CustomNetworkManager.Instance.OnPlayerLeft += OnPlayerLeft;
    }

    private void OnConnected()
    {
        // Spawn local player
        var spawnPoint = GetRandomSpawnPoint();
        var player = Instantiate(GetAvatarPrefab(), spawnPoint.position, spawnPoint.rotation);
        player.GetComponent<Player>().NetworkId = CustomNetworkManager.Instance.PlayerId;
        player.GetComponent<Player>().OnNetworkSpawn();
    }

    private void OnPlayerJoined(string playerId, PlayerState state)
    {
        // Spawn remote player
        var player = Instantiate(GetAvatarPrefab(), state.position, state.rotation);
        player.GetComponent<Player>().NetworkId = playerId;
        _remotePlayers[playerId] = player;
    }
}
```

### Phase 4: UserListManager Migration

```csharp
// BEFORE
[Networked, Capacity(100)]
private NetworkDictionary<PlayerRef, UserData> Users => default;

[Rpc(RpcSources.All, RpcTargets.StateAuthority)]
private void RPC_KickPlayer(PlayerRef playerRef) { ... }

// AFTER
private Dictionary<string, UserData> _users = new();

public void KickPlayer(string targetId)
{
    if (!IsHost) return;
    CustomNetworkManager.Instance.SendRpc("kick", targetId, null);
}

// Server handles kick and broadcasts player_left
```

### Phase 5: WebRTCManager Migration

WebRTCManager is simpler because signaling just needs a relay:

```csharp
// BEFORE
Runner.SendReliableDataToPlayer(targetPlayer, ReliableKey.FromInts(0, 1), data);

// AFTER
CustomNetworkManager.Instance.SendWebRTCSignal(targetPlayerId, jsonSignal);
```

### Phase 6: ChatManager Migration

Replace Photon Chat with WebSocket chat channel:

```csharp
// BEFORE
_chatClient.PublishMessage(_currentChannelName, message);

// AFTER
CustomNetworkManager.Instance.SendChat(message);
// Server broadcasts to all in room
```

---

## Server Implementation (Node.js Example)

```javascript
// server.js
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');

const wss = new WebSocket.Server({ port: 8080 });
const rooms = new Map(); // roomName -> { players: Map<playerId, { ws, state }>, host: playerId }

wss.on('connection', (ws) => {
    let playerId = null;
    let roomName = null;

    ws.on('message', (data) => {
        const msg = JSON.parse(data);

        switch (msg.type) {
            case 'join':
                playerId = uuidv4();
                roomName = msg.roomName;

                if (!rooms.has(roomName)) {
                    rooms.set(roomName, { players: new Map(), host: playerId });
                }

                const room = rooms.get(roomName);
                room.players.set(playerId, { ws, state: { name: msg.name, userId: msg.userId } });

                // Send welcome
                ws.send(JSON.stringify({
                    type: 'welcome',
                    playerId,
                    isHost: room.host === playerId
                }));

                // Broadcast join
                broadcast(room, { type: 'player_joined', playerId, name: msg.name });
                break;

            case 'state':
                if (rooms.has(roomName)) {
                    const room = rooms.get(roomName);
                    room.players.get(playerId).state = { ...room.players.get(playerId).state, ...msg };

                    // Broadcast state to others
                    broadcastExcept(room, playerId, { type: 'state_update', playerId, ...msg });
                }
                break;

            case 'webrtc_signal':
                // Relay signal to target
                const targetWs = rooms.get(roomName)?.players.get(msg.target)?.ws;
                if (targetWs) {
                    targetWs.send(JSON.stringify({ type: 'webrtc_signal', from: playerId, signal: msg.signal }));
                }
                break;

            case 'chat':
                broadcast(rooms.get(roomName), { type: 'chat', sender: playerId, message: msg.message });
                break;
        }
    });

    ws.on('close', () => {
        if (roomName && rooms.has(roomName)) {
            const room = rooms.get(roomName);
            room.players.delete(playerId);
            broadcast(room, { type: 'player_left', playerId });

            // Host migration if needed
            if (room.host === playerId && room.players.size > 0) {
                room.host = room.players.keys().next().value;
                broadcast(room, { type: 'host_changed', newHost: room.host });
            }
        }
    });
});
```

---

## Migration Checklist

- [ ] Set up WebSocket server (Node.js/Colyseus)
- [ ] Add NativeWebSocket to Unity project
- [ ] Create `CustomNetworkManager.cs`
- [ ] Create `CustomNetworkBehaviour.cs`
- [ ] Create message DTOs (`NetworkMessages.cs`)
- [ ] Migrate `Player.cs` (remove NetworkBehaviour, add state sync)
- [ ] Migrate `GameManager.cs` (remove NetworkBehaviour, use events)
- [ ] Migrate `UserListManager.cs` (Dictionary instead of NetworkDictionary)
- [ ] Migrate `UserData.cs` (plain struct, no INetworkStruct)
- [ ] Migrate `WebRTCManager.cs` (use WebSocket for signaling)
- [ ] Migrate `ChatManager.cs` (use WebSocket instead of Photon Chat)
- [ ] Test 2-player sync
- [ ] Test host migration
- [ ] Test WebRTC voice with new signaling
- [ ] Load test with 10+ players

---

## Considerations

### Pros of Custom WebSocket
- No Photon licensing costs
- Full control over server logic
- Can host on any infrastructure
- Simpler debugging (no Photon magic)

### Cons of Custom WebSocket
- No built-in interpolation/prediction
- Must implement authority model manually
- No Photon's global relay infrastructure
- More code to maintain

### When to Stay with Photon
- Need proven scalability out of the box
- Want enterprise support
- Don't want to maintain server infrastructure
- Need Photon's edge servers for global latency

---

## Next Steps

1. Decide on server stack (Node.js vs Colyseus vs .NET)
2. Set up basic server with room join/leave
3. Create Unity WebSocket client
4. Migrate Player.cs as proof of concept
5. Expand to full migration

---

**Related Plans:**
- `UGS_Networking_Plan.md` (Unity Gaming Services alternative - TBD)
