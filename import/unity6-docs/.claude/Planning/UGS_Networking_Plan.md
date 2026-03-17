# Unity Gaming Services (UGS) Networking Plan

Replace Photon Fusion with Unity Gaming Services (Netcode for GameObjects + Relay + Lobby).

**Created:** 2026-01-20
**Related:** [Custom_WebSocket_Networking_Plan.md](Custom_WebSocket_Networking_Plan.md)

---

## UGS Stack Overview

| Service | Purpose | Replaces |
|---------|---------|----------|
| **Netcode for GameObjects (NGO)** | State sync, RPCs, spawning | Photon Fusion core |
| **Unity Relay** | NAT traversal, relay servers | Photon Cloud relay |
| **Unity Lobby** | Room discovery, matchmaking | Photon matchmaking |
| **Vivox** | Voice & text chat | Photon Voice + Chat |
| **Unity Authentication** | Player identity | (Optional, have Supabase) |

---

## Why UGS Over Photon

| Aspect | Photon Fusion | UGS |
|--------|---------------|-----|
| Unity integration | Third-party SDK | First-party, tighter integration |
| Pricing model | Per CCU flat | Per CCU + bandwidth (can be cheaper) |
| Free tier | 20 CCU | 50 CCU + 5000 PCU Vivox |
| Voice chat | Photon Voice (add-on) | Vivox (5000 PCU free) |
| Learning curve | Medium | Medium |
| WebGL support | Full | Full (Relay + NGO) |
| Documentation | Good | Good |
| Lock-in | High | Medium (NGO is open source) |

---

## Architecture Comparison

### Current (Photon Fusion)

```
Unity Client
    │
    ▼
Photon Fusion SDK
    │
    ▼
Photon Cloud (Relay + Matchmaking)
    │
    ▼
Other Clients
```

### Target (UGS)

```
Unity Client
    │
    ├─► Netcode for GameObjects (State Sync)
    │         │
    │         ▼
    │   Unity Relay (NAT Traversal)
    │         │
    │         ▼
    │   Other Clients
    │
    ├─► Unity Lobby (Room Discovery)
    │
    └─► Vivox (Voice + Text Chat)
```

---

## Package Requirements

```json
// Packages/manifest.json additions
{
  "dependencies": {
    "com.unity.netcode.gameobjects": "1.8.1",
    "com.unity.services.relay": "1.0.5",
    "com.unity.services.lobby": "1.2.0",
    "com.unity.services.authentication": "3.3.0",
    "com.unity.services.vivox": "16.2.0"
  }
}
```

---

## Current Photon Dependencies to Replace

| File | Photon Usage | UGS Replacement |
|------|--------------|-----------------|
| `Player.cs` | `NetworkBehaviour`, `[Networked]`, `Rpc` | `NetworkBehaviour`, `NetworkVariable`, `Rpc` |
| `GameManager.cs` | `NetworkBehaviour`, `Runner.Spawn()` | `NetworkBehaviour`, `NetworkManager.Spawn()` |
| `UserListManager.cs` | `NetworkDictionary`, `Rpc` | `NetworkList`, `Rpc` |
| `UserData.cs` | `INetworkStruct`, `NetworkString` | `INetworkSerializable`, `FixedString32Bytes` |
| `WebRTCManager.cs` | `Runner.SendReliableDataToPlayer()` | Custom messaging or keep WebRTC |
| `ChatManager.cs` | Photon Chat SDK | Vivox text chat |

---

## Implementation Guide

### Phase 1: Project Setup

#### 1.1 Install UGS Packages

```
Window → Package Manager → Add package by name:
- com.unity.netcode.gameobjects
- com.unity.services.relay
- com.unity.services.lobby
- com.unity.services.authentication
- com.unity.services.vivox
```

#### 1.2 Initialize UGS

```csharp
// /Assets/MetaDyn/Networking/UGSInitializer.cs
using Unity.Services.Core;
using Unity.Services.Authentication;
using UnityEngine;

public class UGSInitializer : MonoBehaviour
{
    public static UGSInitializer Instance { get; private set; }
    public bool IsInitialized { get; private set; }
    public string PlayerId => AuthenticationService.Instance.PlayerId;

    async void Awake()
    {
        if (Instance == null) Instance = this;
        else { Destroy(gameObject); return; }

        DontDestroyOnLoad(gameObject);

        try
        {
            await UnityServices.InitializeAsync();

            // Anonymous auth (or link to Supabase later)
            if (!AuthenticationService.Instance.IsSignedIn)
            {
                await AuthenticationService.Instance.SignInAnonymouslyAsync();
            }

            IsInitialized = true;
            Debug.Log($"[UGS] Initialized. PlayerId: {PlayerId}");
        }
        catch (System.Exception e)
        {
            Debug.LogError($"[UGS] Initialization failed: {e.Message}");
        }
    }
}
```

### Phase 2: Relay + Lobby Setup

#### 2.1 Create/Join Lobby with Relay

```csharp
// /Assets/MetaDyn/Networking/UGSNetworkManager.cs
using Unity.Services.Relay;
using Unity.Services.Relay.Models;
using Unity.Services.Lobbies;
using Unity.Services.Lobbies.Models;
using Unity.Netcode;
using Unity.Netcode.Transports.UTP;
using UnityEngine;
using System.Threading.Tasks;

public class UGSNetworkManager : MonoBehaviour
{
    public static UGSNetworkManager Instance { get; private set; }

    [Header("Settings")]
    [SerializeField] private int maxPlayers = 50;

    private Lobby _currentLobby;
    private string _relayJoinCode;

    // Events
    public event System.Action OnConnectedAsHost;
    public event System.Action OnConnectedAsClient;
    public event System.Action OnDisconnected;

    void Awake()
    {
        if (Instance == null) Instance = this;
        else Destroy(gameObject);
    }

    /// <summary>
    /// Create a new lobby and start hosting
    /// </summary>
    public async Task<bool> CreateLobby(string lobbyName, string playerName)
    {
        try
        {
            // 1. Create Relay allocation
            Allocation allocation = await RelayService.Instance.CreateAllocationAsync(maxPlayers - 1);
            _relayJoinCode = await RelayService.Instance.GetJoinCodeAsync(allocation.AllocationId);

            // 2. Configure transport
            var transport = NetworkManager.Singleton.GetComponent<UnityTransport>();
            transport.SetHostRelayData(
                allocation.RelayServer.IpV4,
                (ushort)allocation.RelayServer.Port,
                allocation.AllocationIdBytes,
                allocation.Key,
                allocation.ConnectionData
            );

            // 3. Create Lobby with Relay code
            CreateLobbyOptions options = new CreateLobbyOptions
            {
                IsPrivate = false,
                Data = new System.Collections.Generic.Dictionary<string, DataObject>
                {
                    { "RelayCode", new DataObject(DataObject.VisibilityOptions.Public, _relayJoinCode) },
                    { "HostName", new DataObject(DataObject.VisibilityOptions.Public, playerName) }
                }
            };

            _currentLobby = await LobbyService.Instance.CreateLobbyAsync(lobbyName, maxPlayers, options);

            // 4. Start hosting
            NetworkManager.Singleton.StartHost();

            // 5. Start lobby heartbeat
            StartCoroutine(HeartbeatLobby());

            Debug.Log($"[UGS] Created lobby: {lobbyName}, Relay code: {_relayJoinCode}");
            OnConnectedAsHost?.Invoke();
            return true;
        }
        catch (System.Exception e)
        {
            Debug.LogError($"[UGS] Failed to create lobby: {e.Message}");
            return false;
        }
    }

    /// <summary>
    /// Join an existing lobby
    /// </summary>
    public async Task<bool> JoinLobby(string lobbyId, string playerName)
    {
        try
        {
            // 1. Join the lobby
            _currentLobby = await LobbyService.Instance.JoinLobbyByIdAsync(lobbyId);

            // 2. Get Relay code from lobby data
            string relayCode = _currentLobby.Data["RelayCode"].Value;

            // 3. Join Relay
            JoinAllocation joinAllocation = await RelayService.Instance.JoinAllocationAsync(relayCode);

            // 4. Configure transport
            var transport = NetworkManager.Singleton.GetComponent<UnityTransport>();
            transport.SetClientRelayData(
                joinAllocation.RelayServer.IpV4,
                (ushort)joinAllocation.RelayServer.Port,
                joinAllocation.AllocationIdBytes,
                joinAllocation.Key,
                joinAllocation.ConnectionData,
                joinAllocation.HostConnectionData
            );

            // 5. Start client
            NetworkManager.Singleton.StartClient();

            Debug.Log($"[UGS] Joined lobby: {_currentLobby.Name}");
            OnConnectedAsClient?.Invoke();
            return true;
        }
        catch (System.Exception e)
        {
            Debug.LogError($"[UGS] Failed to join lobby: {e.Message}");
            return false;
        }
    }

    /// <summary>
    /// Quick join any available lobby, or create new one
    /// </summary>
    public async Task<bool> QuickJoinOrCreate(string lobbyName, string playerName)
    {
        try
        {
            // Try to quick join
            _currentLobby = await LobbyService.Instance.QuickJoinLobbyAsync();
            return await JoinLobby(_currentLobby.Id, playerName);
        }
        catch (LobbyServiceException e) when (e.Reason == LobbyExceptionReason.NoOpenLobbies)
        {
            // No lobbies available, create one
            return await CreateLobby(lobbyName, playerName);
        }
    }

    /// <summary>
    /// Leave current lobby
    /// </summary>
    public async void LeaveLobby()
    {
        try
        {
            if (_currentLobby != null)
            {
                await LobbyService.Instance.RemovePlayerAsync(_currentLobby.Id, AuthenticationService.Instance.PlayerId);
                _currentLobby = null;
            }

            NetworkManager.Singleton.Shutdown();
            OnDisconnected?.Invoke();
        }
        catch (System.Exception e)
        {
            Debug.LogError($"[UGS] Failed to leave lobby: {e.Message}");
        }
    }

    /// <summary>
    /// Get list of available lobbies
    /// </summary>
    public async Task<System.Collections.Generic.List<Lobby>> GetLobbies()
    {
        try
        {
            QueryResponse response = await LobbyService.Instance.QueryLobbiesAsync();
            return response.Results;
        }
        catch (System.Exception e)
        {
            Debug.LogError($"[UGS] Failed to query lobbies: {e.Message}");
            return new System.Collections.Generic.List<Lobby>();
        }
    }

    private System.Collections.IEnumerator HeartbeatLobby()
    {
        while (_currentLobby != null)
        {
            LobbyService.Instance.SendHeartbeatPingAsync(_currentLobby.Id);
            yield return new WaitForSeconds(15);
        }
    }
}
```

### Phase 3: Migrate NetworkBehaviours

#### 3.1 Player.cs Migration

```csharp
// BEFORE (Photon Fusion)
using Fusion;

public sealed class Player : NetworkBehaviour
{
    [Networked] private NetworkBool _isJumping { get; set; }
    [Networked] public NetworkString<_32> NetworkedName { get; set; }

    public override void Spawned()
    {
        if (Object.HasStateAuthority)
        {
            NetworkedName = PlayerPrefs.GetString("PlayerName", "Guest");
            RPC_RegisterWithUserList(NetworkedName.ToString(), userId);
        }
    }

    public override void FixedUpdateNetwork()
    {
        ProcessInput(PlayerInput.CurrentInput);
    }

    public override void Render()
    {
        // Update visuals
    }

    [Rpc(RpcSources.StateAuthority, RpcTargets.All)]
    private void RPC_RegisterWithUserList(string playerName, string userId) { }
}

// AFTER (UGS Netcode for GameObjects)
using Unity.Netcode;
using Unity.Collections;

public sealed class Player : NetworkBehaviour
{
    // NetworkVariables replace [Networked] properties
    private NetworkVariable<bool> _isJumping = new NetworkVariable<bool>();
    private NetworkVariable<FixedString32Bytes> _networkedName = new NetworkVariable<FixedString32Bytes>();

    public string PlayerName => _networkedName.Value.ToString();

    public override void OnNetworkSpawn()
    {
        if (IsOwner)
        {
            // Set name on server
            string name = PlayerPrefs.GetString("PlayerName", "Guest");
            SetNameServerRpc(name);

            // Register with user list
            string userId = GetUserId();
            RegisterWithUserListServerRpc(name, userId);

            // Setup camera
            SetupCamera();
        }

        // Subscribe to name changes for NameTag updates
        _networkedName.OnValueChanged += OnNameChanged;
    }

    public override void OnNetworkDespawn()
    {
        _networkedName.OnValueChanged -= OnNameChanged;
    }

    void Update()
    {
        if (!IsOwner) return;

        ProcessInput();

        // State is automatically synced via NetworkVariables
    }

    void FixedUpdate()
    {
        if (!IsOwner) return;

        // Physics/movement updates
        ProcessMovement();
    }

    private void ProcessInput()
    {
        // Input handling (similar to current)
        bool shouldJump = Input.GetButtonDown("Jump") && _kcc.IsGrounded;
        if (shouldJump)
        {
            SetJumpingServerRpc(true);
        }
    }

    [ServerRpc]
    private void SetNameServerRpc(string name)
    {
        _networkedName.Value = name;
    }

    [ServerRpc]
    private void SetJumpingServerRpc(bool jumping)
    {
        _isJumping.Value = jumping;
    }

    [ServerRpc]
    private void RegisterWithUserListServerRpc(string playerName, string userId)
    {
        // Server handles registration
        if (UserListManager.Instance != null)
        {
            UserListManager.Instance.RegisterPlayer(OwnerClientId, playerName, userId);
        }
    }

    private void OnNameChanged(FixedString32Bytes oldValue, FixedString32Bytes newValue)
    {
        if (_spawnedNameTag != null)
        {
            _spawnedNameTag.SetName(newValue.ToString());
        }
    }

    private string GetUserId()
    {
        if (SupabaseAuthManager.Instance?.IsAuthenticated == true)
            return SupabaseAuthManager.Instance.CurrentSession.user.id;
        return "";
    }
}
```

#### 3.2 GameManager.cs Migration

```csharp
// BEFORE (Photon)
public sealed class GameManager : NetworkBehaviour, IPlayerJoined, IPlayerLeft
{
    public override void Spawned()
    {
        NetworkObject spawnedPlayer = Runner.Spawn(avatarPrefab, spawnPos, spawnRot, Runner.LocalPlayer);
    }

    public void PlayerJoined(PlayerRef player) { }
    public void PlayerLeft(PlayerRef player) { }
}

// AFTER (UGS)
using Unity.Netcode;

public sealed class GameManager : NetworkBehaviour
{
    public static GameManager Instance { get; private set; }

    [Header("Settings")]
    public GameObject PlayerPrefab;
    public List<AvatarEntry> readyPlayerMeAvatars;

    void Awake()
    {
        if (Instance == null) Instance = this;
        else Destroy(gameObject);
    }

    public override void OnNetworkSpawn()
    {
        if (IsServer)
        {
            // Server subscribes to connection events
            NetworkManager.Singleton.OnClientConnectedCallback += OnClientConnected;
            NetworkManager.Singleton.OnClientDisconnectCallback += OnClientDisconnected;
        }

        if (IsClient && IsOwner)
        {
            // Request spawn from server
            RequestSpawnServerRpc(GetAvatarIndex());
        }
    }

    public override void OnNetworkDespawn()
    {
        if (IsServer)
        {
            NetworkManager.Singleton.OnClientConnectedCallback -= OnClientConnected;
            NetworkManager.Singleton.OnClientDisconnectCallback -= OnClientDisconnected;
        }
    }

    [ServerRpc(RequireOwnership = false)]
    private void RequestSpawnServerRpc(int avatarIndex, ServerRpcParams rpcParams = default)
    {
        ulong clientId = rpcParams.Receive.SenderClientId;

        // Get spawn point
        var spawnPoint = GetRandomSpawnPoint();
        Vector3 spawnPos = spawnPoint?.transform.position ?? Vector3.zero;
        Quaternion spawnRot = spawnPoint?.transform.rotation ?? Quaternion.identity;

        // Get avatar prefab
        GameObject prefab = GetAvatarPrefab(avatarIndex);

        // Spawn player
        GameObject playerObj = Instantiate(prefab, spawnPos, spawnRot);
        NetworkObject networkObject = playerObj.GetComponent<NetworkObject>();
        networkObject.SpawnAsPlayerObject(clientId);

        Debug.Log($"[GameManager] Spawned player for client {clientId}");
    }

    private void OnClientConnected(ulong clientId)
    {
        Debug.Log($"[GameManager] Client connected: {clientId}");
        OnPlayerJoined?.Invoke(clientId);
    }

    private void OnClientDisconnected(ulong clientId)
    {
        Debug.Log($"[GameManager] Client disconnected: {clientId}");
        OnPlayerLeft?.Invoke(clientId);
    }

    private int GetAvatarIndex()
    {
        return PlayerPrefs.GetInt("AvatarChoice", 0);
    }
}
```

#### 3.3 UserListManager.cs Migration

```csharp
// BEFORE (Photon)
[Networked, Capacity(100)]
private NetworkDictionary<PlayerRef, UserData> Users => default;

// AFTER (UGS)
using Unity.Netcode;
using System.Collections.Generic;

public class UserListManager : NetworkBehaviour
{
    public static UserListManager Instance { get; private set; }

    // NetworkList for synced user data (server authoritative)
    private NetworkList<UserData> _users;

    // Local lookup by clientId
    private Dictionary<ulong, int> _clientToIndex = new Dictionary<ulong, int>();

    // Events
    public event System.Action<ulong, UserData> OnUserJoined;
    public event System.Action<ulong> OnUserLeft;

    void Awake()
    {
        if (Instance == null) Instance = this;
        else { Destroy(gameObject); return; }

        _users = new NetworkList<UserData>();
    }

    public override void OnNetworkSpawn()
    {
        _users.OnListChanged += OnUsersListChanged;
    }

    public override void OnNetworkDespawn()
    {
        _users.OnListChanged -= OnUsersListChanged;
    }

    public void RegisterPlayer(ulong clientId, string playerName, string userId)
    {
        if (!IsServer) return;

        // Check ownership for admin
        string ownerId = MetaDynRuntimeConfig.Instance?.ownerId ?? "";
        byte permissionLevel = 0;

        if (!string.IsNullOrEmpty(ownerId) && userId == ownerId)
        {
            permissionLevel = 2; // Owner = Admin
        }
        else if (_users.Count == 0)
        {
            permissionLevel = 2; // First player = Admin
        }

        var userData = new UserData
        {
            ClientId = clientId,
            PlayerName = playerName,
            IsMuted = true,
            PermissionLevel = permissionLevel
        };

        _users.Add(userData);
        _clientToIndex[clientId] = _users.Count - 1;

        Debug.Log($"[UserList] Registered: {playerName} (Client: {clientId}, Permission: {permissionLevel})");
    }

    public void UnregisterPlayer(ulong clientId)
    {
        if (!IsServer) return;

        if (_clientToIndex.TryGetValue(clientId, out int index))
        {
            _users.RemoveAt(index);
            _clientToIndex.Remove(clientId);

            // Rebuild index lookup
            RebuildClientIndex();
        }
    }

    public bool TryGetUser(ulong clientId, out UserData userData)
    {
        if (_clientToIndex.TryGetValue(clientId, out int index))
        {
            userData = _users[index];
            return true;
        }
        userData = default;
        return false;
    }

    [ServerRpc(RequireOwnership = false)]
    public void KickPlayerServerRpc(ulong targetClientId, ServerRpcParams rpcParams = default)
    {
        ulong requesterId = rpcParams.Receive.SenderClientId;

        if (!TryGetUser(requesterId, out UserData requester) || requester.PermissionLevel < 2)
        {
            Debug.LogWarning($"[UserList] Kick denied: {requesterId} lacks permission");
            return;
        }

        NetworkManager.Singleton.DisconnectClient(targetClientId);
    }

    private void OnUsersListChanged(NetworkListEvent<UserData> changeEvent)
    {
        switch (changeEvent.Type)
        {
            case NetworkListEvent<UserData>.EventType.Add:
                OnUserJoined?.Invoke(changeEvent.Value.ClientId, changeEvent.Value);
                break;
            case NetworkListEvent<UserData>.EventType.Remove:
                OnUserLeft?.Invoke(changeEvent.Value.ClientId);
                break;
        }
    }

    private void RebuildClientIndex()
    {
        _clientToIndex.Clear();
        for (int i = 0; i < _users.Count; i++)
        {
            _clientToIndex[_users[i].ClientId] = i;
        }
    }
}
```

#### 3.4 UserData.cs Migration

```csharp
// BEFORE (Photon)
using Fusion;

public struct UserData : INetworkStruct
{
    public PlayerRef PlayerRef;
    public NetworkString<_32> PlayerName;
    public NetworkBool IsMuted;
    public byte PermissionLevel;
}

// AFTER (UGS)
using Unity.Netcode;
using Unity.Collections;

public struct UserData : INetworkSerializable, System.IEquatable<UserData>
{
    public ulong ClientId;
    public FixedString32Bytes PlayerName;
    public bool IsMuted;
    public byte PermissionLevel;

    public bool IsAdmin => PermissionLevel >= 2;
    public bool IsModerator => PermissionLevel >= 1;

    public void NetworkSerialize<T>(BufferSerializer<T> serializer) where T : IReaderWriter
    {
        serializer.SerializeValue(ref ClientId);
        serializer.SerializeValue(ref PlayerName);
        serializer.SerializeValue(ref IsMuted);
        serializer.SerializeValue(ref PermissionLevel);
    }

    public bool Equals(UserData other)
    {
        return ClientId == other.ClientId;
    }
}
```

### Phase 4: Vivox Voice Chat

```csharp
// /Assets/MetaDyn/Networking/VivoxManager.cs
using Unity.Services.Vivox;
using UnityEngine;
using System.Threading.Tasks;

public class VivoxManager : MonoBehaviour
{
    public static VivoxManager Instance { get; private set; }

    private VivoxService _vivox;
    private string _currentChannel;

    public event System.Action<string> OnPlayerStartedSpeaking;
    public event System.Action<string> OnPlayerStoppedSpeaking;

    void Awake()
    {
        if (Instance == null) Instance = this;
        else Destroy(gameObject);
    }

    public async Task Initialize()
    {
        await VivoxService.Instance.InitializeAsync();
        Debug.Log("[Vivox] Initialized");
    }

    public async Task JoinChannel(string channelName, bool positional = true)
    {
        try
        {
            // Login if needed
            if (!VivoxService.Instance.IsLoggedIn)
            {
                await VivoxService.Instance.LoginAsync();
            }

            // Join channel
            if (positional)
            {
                await VivoxService.Instance.JoinPositionalChannelAsync(channelName, ChatCapability.AudioOnly);
            }
            else
            {
                await VivoxService.Instance.JoinGroupChannelAsync(channelName, ChatCapability.TextAndAudio);
            }

            _currentChannel = channelName;
            Debug.Log($"[Vivox] Joined channel: {channelName}");

            // Subscribe to events
            VivoxService.Instance.ParticipantAddedToChannel += OnParticipantAdded;
            VivoxService.Instance.ParticipantRemovedFromChannel += OnParticipantRemoved;
        }
        catch (System.Exception e)
        {
            Debug.LogError($"[Vivox] Failed to join channel: {e.Message}");
        }
    }

    public async Task LeaveChannel()
    {
        if (!string.IsNullOrEmpty(_currentChannel))
        {
            await VivoxService.Instance.LeaveChannelAsync(_currentChannel);
            _currentChannel = null;
        }
    }

    public void SetMuted(bool muted)
    {
        VivoxService.Instance.SetInputDeviceMuted(muted);
    }

    public void UpdatePosition(Vector3 position, Vector3 forward, Vector3 up)
    {
        // For positional audio
        VivoxService.Instance.Set3DPosition(position, forward, up);
    }

    private void OnParticipantAdded(VivoxParticipant participant)
    {
        participant.ParticipantSpeechDetected += OnSpeechDetected;
    }

    private void OnParticipantRemoved(VivoxParticipant participant)
    {
        participant.ParticipantSpeechDetected -= OnSpeechDetected;
    }

    private void OnSpeechDetected(VivoxParticipant participant)
    {
        if (participant.IsSpeaking)
            OnPlayerStartedSpeaking?.Invoke(participant.PlayerId);
        else
            OnPlayerStoppedSpeaking?.Invoke(participant.PlayerId);
    }
}
```

---

## WebRTC Signaling

For WebRTC signaling, you have two options:

### Option A: Keep Custom WebRTC with NGO Messaging

```csharp
// Use NetworkManager custom messages for signaling
public class WebRTCSignaling : NetworkBehaviour
{
    [ServerRpc(RequireOwnership = false)]
    public void SendSignalServerRpc(ulong targetClientId, string signal, ServerRpcParams rpcParams = default)
    {
        // Server relays to target
        RelaySignalClientRpc(rpcParams.Receive.SenderClientId, signal, new ClientRpcParams
        {
            Send = new ClientRpcSendParams { TargetClientIds = new[] { targetClientId } }
        });
    }

    [ClientRpc]
    private void RelaySignalClientRpc(ulong senderId, string signal, ClientRpcParams rpcParams = default)
    {
        // Handle incoming signal
        WebRTCManager.Instance?.HandleSignal(senderId.ToString(), signal);
    }
}
```

### Option B: Use Vivox for Voice (Replace WebRTC)

Vivox handles voice natively, so you could:
1. Remove custom WebRTC voice entirely
2. Use Vivox positional audio
3. Keep WebRTC only for other P2P features if needed

---

## Migration Checklist

### Setup
- [ ] Install UGS packages via Package Manager
- [ ] Create Unity Dashboard project
- [ ] Enable Relay, Lobby, Authentication, Vivox services
- [ ] Add `UGSInitializer` to bootstrap scene

### Core Migration
- [ ] Create `UGSNetworkManager.cs` (Relay + Lobby)
- [ ] Replace `NetworkRunner` references with `NetworkManager.Singleton`
- [ ] Migrate `Player.cs` to NGO `NetworkBehaviour`
- [ ] Migrate `GameManager.cs` to NGO
- [ ] Migrate `UserListManager.cs` to NGO
- [ ] Migrate `UserData.cs` to `INetworkSerializable`

### Voice & Chat
- [ ] Implement `VivoxManager.cs`
- [ ] Replace or adapt `WebRTCManager.cs`
- [ ] Replace `ChatManager.cs` with Vivox text chat

### Testing
- [ ] Test Relay connection (host/join)
- [ ] Test player spawning
- [ ] Test state synchronization
- [ ] Test RPCs (kick, mute, etc.)
- [ ] Test Vivox voice chat
- [ ] Test positional audio
- [ ] WebGL build test
- [ ] Load test with 10+ players

---

## Key Differences Summary

| Concept | Photon Fusion | UGS NGO |
|---------|---------------|---------|
| Manager | `NetworkRunner` | `NetworkManager.Singleton` |
| Base class | `NetworkBehaviour` | `NetworkBehaviour` |
| Synced vars | `[Networked]` | `NetworkVariable<T>` |
| Collections | `NetworkDictionary` | `NetworkList<T>` |
| String | `NetworkString<_32>` | `FixedString32Bytes` |
| Bool | `NetworkBool` | `bool` in NetworkVariable |
| Player ID | `PlayerRef` | `ulong` (ClientId) |
| Authority check | `Object.HasStateAuthority` | `IsServer` / `IsOwner` |
| Spawn | `Runner.Spawn()` | `NetworkObject.Spawn()` |
| RPC to server | `[Rpc(Sources.All, Targets.StateAuthority)]` | `[ServerRpc]` |
| RPC to clients | `[Rpc(Sources.StateAuthority, Targets.All)]` | `[ClientRpc]` |
| Network tick | `FixedUpdateNetwork()` | `FixedUpdate()` + IsOwner check |
| Render | `Render()` | `Update()` |
| Spawned | `Spawned()` | `OnNetworkSpawn()` |
| Despawned | `Despawned()` | `OnNetworkDespawn()` |

---

## Estimated Effort

| Phase | Tasks | Effort |
|-------|-------|--------|
| Setup | Packages, dashboard, initializer | 2-4 hours |
| Relay + Lobby | Connection manager | 4-6 hours |
| Player migration | NetworkVariables, RPCs | 4-6 hours |
| GameManager migration | Spawning, events | 2-4 hours |
| UserListManager migration | NetworkList, moderation | 4-6 hours |
| Vivox integration | Voice chat | 4-8 hours |
| Testing & debugging | All systems | 8-16 hours |
| **Total** | | **28-50 hours** |

---

## Related Documentation

- [Custom_WebSocket_Networking_Plan.md](Custom_WebSocket_Networking_Plan.md)
- [Cloudflare_Realtime_Infrastructure.md](Cloudflare_Realtime_Infrastructure.md)
- [Networking_Cost_Comparison.md](Networking_Cost_Comparison.md)
- [Unity NGO Documentation](https://docs-multiplayer.unity3d.com/)
- [Unity Relay Documentation](https://docs.unity.com/relay/)
- [Vivox Documentation](https://docs.unity.com/vivox/)
