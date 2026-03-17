# Cloudflare Realtime Infrastructure

Cloudflare-native implementation for MetaDyn multiplayer networking using Durable Objects and Workers.

**Created:** 2026-01-20
**Related:** [Custom_WebSocket_Networking_Plan.md](Custom_WebSocket_Networking_Plan.md)

---

## Why Cloudflare

MetaDyn already uses Cloudflare for:
- **CDN** - Unity WebGL builds cached at edge
- **DNS** - 1.1.1.1 infrastructure (10-20ms lookups)
- **Vectorize** - AI memory embeddings
- **Workers** - Email backend (email.metadyn.xyz)

Adding realtime infrastructure keeps everything on the same network with minimal latency between services.

---

## Architecture Overview

```
Unity WebGL Client
       │
       ▼
┌─────────────────────────────────────────────────────┐
│                 Cloudflare Edge                      │
│  ┌───────────────┐    ┌──────────────────────────┐  │
│  │    Worker     │───▶│    Durable Object        │  │
│  │  (Router)     │    │    (Game Room)           │  │
│  │               │    │                          │  │
│  │ - Auth check  │    │ - WebSocket connections  │  │
│  │ - Room lookup │    │ - Player state           │  │
│  │ - Rate limit  │    │ - Broadcast messages     │  │
│  └───────────────┘    │ - Authority validation   │  │
│         │             └──────────────────────────┘  │
│         │                        │                  │
│         ▼                        ▼                  │
│  ┌───────────────┐    ┌──────────────────────────┐  │
│  │      D1       │    │      Vectorize           │  │
│  │  (Persistent) │    │    (AI Memory)           │  │
│  │               │    │                          │  │
│  │ - Ban lists   │    │ - Already integrated     │  │
│  │ - Room config │    │ - Same edge location     │  │
│  └───────────────┘    └──────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Durable Objects: Perfect for Game Rooms

Each Durable Object instance:
- Has a unique ID (room name)
- Maintains WebSocket connections
- Stores in-memory state (players, positions)
- Runs at the edge closest to first connection
- Supports hibernation (WebSockets stay open, DO sleeps)

**Key benefit:** WebSocket Hibernation API means you only pay when messages are sent, not for idle connections.

---

## Implementation

### Project Structure

```
/cloudflare-realtime/
├── src/
│   ├── index.ts           # Worker entry point
│   ├── GameRoom.ts        # Durable Object class
│   ├── types.ts           # Message types
│   └── auth.ts            # Supabase JWT validation
├── wrangler.toml
├── package.json
└── tsconfig.json
```

### wrangler.toml

```toml
name = "metadyn-realtime"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Durable Objects binding
[durable_objects]
bindings = [
  { name = "GAME_ROOM", class_name = "GameRoom" }
]

# Migrations for Durable Objects
[[migrations]]
tag = "v1"
new_classes = ["GameRoom"]

# D1 Database (optional - for persistence)
[[d1_databases]]
binding = "DB"
database_name = "metadyn-realtime"
database_id = "your-database-id"

# Environment variables
[vars]
SUPABASE_JWT_SECRET = "your-jwt-secret"

# Custom domain
[routes]
pattern = "realtime.metadyn.xyz/*"
```

### Worker Entry Point (src/index.ts)

```typescript
import { GameRoom } from './GameRoom';

export { GameRoom };

export interface Env {
  GAME_ROOM: DurableObjectNamespace;
  DB: D1Database;
  SUPABASE_JWT_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // WebSocket upgrade request
    if (request.headers.get('Upgrade') === 'websocket') {
      return handleWebSocket(request, env);
    }

    // REST endpoints
    if (url.pathname === '/rooms') {
      return handleRoomList(env);
    }

    return new Response('MetaDyn Realtime Server', { status: 200 });
  }
};

async function handleWebSocket(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const roomName = url.searchParams.get('room');
  const token = url.searchParams.get('token');

  if (!roomName) {
    return new Response('Missing room parameter', { status: 400 });
  }

  // Optional: Validate Supabase JWT
  // const user = await validateToken(token, env.SUPABASE_JWT_SECRET);

  // Get or create Durable Object for this room
  const roomId = env.GAME_ROOM.idFromName(roomName);
  const room = env.GAME_ROOM.get(roomId);

  // Forward the WebSocket request to the Durable Object
  return room.fetch(request);
}

async function handleRoomList(env: Env): Promise<Response> {
  // Could query D1 for active rooms
  return new Response(JSON.stringify({ rooms: [] }), {
    headers: { 'Content-Type': 'application/json' }
  });
}
```

### Durable Object: GameRoom (src/GameRoom.ts)

```typescript
import { DurableObject } from 'cloudflare:workers';

interface Player {
  id: string;
  name: string;
  userId: string;
  position: [number, number, number];
  rotation: [number, number, number, number];
  isJumping: boolean;
  isSpeaking: boolean;
  isMuted: boolean;
  permissionLevel: number;
}

interface Session {
  webSocket: WebSocket;
  playerId: string;
  player: Player;
}

export class GameRoom extends DurableObject {
  private sessions: Map<WebSocket, Session> = new Map();
  private host: string | null = null;

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);

    // Restore any hibernated WebSocket sessions
    this.ctx.getWebSockets().forEach((ws) => {
      const meta = ws.deserializeAttachment() as Session;
      if (meta) {
        this.sessions.set(ws, meta);
      }
    });
  }

  async fetch(request: Request): Promise<Response> {
    if (request.headers.get('Upgrade') !== 'websocket') {
      return new Response('Expected WebSocket', { status: 400 });
    }

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    // Accept the WebSocket with hibernation enabled
    this.ctx.acceptWebSocket(server);

    return new Response(null, { status: 101, webSocket: client });
  }

  // Called when a WebSocket message is received (hibernation-aware)
  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer) {
    const data = JSON.parse(message as string);

    switch (data.type) {
      case 'join':
        this.handleJoin(ws, data);
        break;

      case 'state':
        this.handleState(ws, data);
        break;

      case 'rpc':
        this.handleRpc(ws, data);
        break;

      case 'chat':
        this.handleChat(ws, data);
        break;

      case 'webrtc_signal':
        this.handleWebRTCSignal(ws, data);
        break;
    }
  }

  // Called when a WebSocket is closed
  async webSocketClose(ws: WebSocket, code: number, reason: string) {
    const session = this.sessions.get(ws);
    if (session) {
      this.sessions.delete(ws);

      // Broadcast player left
      this.broadcast({
        type: 'player_left',
        playerId: session.playerId
      }, ws);

      // Host migration
      if (this.host === session.playerId && this.sessions.size > 0) {
        const newHost = this.sessions.values().next().value;
        this.host = newHost.playerId;
        this.broadcast({
          type: 'host_changed',
          newHost: this.host
        });
      }
    }
  }

  // Called when a WebSocket encounters an error
  async webSocketError(ws: WebSocket, error: unknown) {
    console.error('WebSocket error:', error);
    this.webSocketClose(ws, 1011, 'WebSocket error');
  }

  private handleJoin(ws: WebSocket, data: any) {
    const playerId = crypto.randomUUID();
    const isFirstPlayer = this.sessions.size === 0;

    if (isFirstPlayer) {
      this.host = playerId;
    }

    const player: Player = {
      id: playerId,
      name: data.name || 'Guest',
      userId: data.userId || '',
      position: data.position || [0, 0, 0],
      rotation: data.rotation || [0, 0, 0, 1],
      isJumping: false,
      isSpeaking: false,
      isMuted: true,
      permissionLevel: isFirstPlayer ? 2 : 0 // First player = admin
    };

    const session: Session = { webSocket: ws, playerId, player };
    this.sessions.set(ws, session);

    // Persist session for hibernation
    ws.serializeAttachment(session);

    // Send welcome to new player
    ws.send(JSON.stringify({
      type: 'welcome',
      playerId,
      isHost: this.host === playerId,
      players: this.getPlayersSnapshot()
    }));

    // Broadcast join to others
    this.broadcast({
      type: 'player_joined',
      playerId,
      player
    }, ws);
  }

  private handleState(ws: WebSocket, data: any) {
    const session = this.sessions.get(ws);
    if (!session) return;

    // Update player state
    if (data.position) session.player.position = data.position;
    if (data.rotation) session.player.rotation = data.rotation;
    if (data.isJumping !== undefined) session.player.isJumping = data.isJumping;
    if (data.isSpeaking !== undefined) session.player.isSpeaking = data.isSpeaking;

    // Persist for hibernation
    ws.serializeAttachment(session);

    // Broadcast to others (not back to sender)
    this.broadcast({
      type: 'state_update',
      playerId: session.playerId,
      position: session.player.position,
      rotation: session.player.rotation,
      isJumping: session.player.isJumping,
      isSpeaking: session.player.isSpeaking
    }, ws);
  }

  private handleRpc(ws: WebSocket, data: any) {
    const session = this.sessions.get(ws);
    if (!session) return;

    switch (data.method) {
      case 'kick':
        if (session.player.permissionLevel >= 2) {
          this.kickPlayer(data.target);
        }
        break;

      case 'mute':
        this.handleMuteRequest(session, data.target, data.muted);
        break;

      case 'set_permission':
        if (session.player.permissionLevel >= 2) {
          this.setPermission(data.target, data.level);
        }
        break;
    }
  }

  private handleChat(ws: WebSocket, data: any) {
    const session = this.sessions.get(ws);
    if (!session) return;

    this.broadcast({
      type: 'chat',
      senderId: session.playerId,
      senderName: session.player.name,
      message: data.message,
      timestamp: Date.now()
    });
  }

  private handleWebRTCSignal(ws: WebSocket, data: any) {
    const session = this.sessions.get(ws);
    if (!session) return;

    // Find target WebSocket
    for (const [targetWs, targetSession] of this.sessions) {
      if (targetSession.playerId === data.target) {
        targetWs.send(JSON.stringify({
          type: 'webrtc_signal',
          from: session.playerId,
          signal: data.signal
        }));
        break;
      }
    }
  }

  private kickPlayer(targetId: string) {
    for (const [ws, session] of this.sessions) {
      if (session.playerId === targetId) {
        ws.close(4000, 'Kicked by admin');
        break;
      }
    }
  }

  private handleMuteRequest(requester: Session, targetId: string, muted: boolean) {
    // Self-mute always allowed, admin can mute anyone
    const isSelf = requester.playerId === targetId;
    const isAdmin = requester.player.permissionLevel >= 2;

    if (!isSelf && !isAdmin) return;

    for (const [ws, session] of this.sessions) {
      if (session.playerId === targetId) {
        session.player.isMuted = muted;
        ws.serializeAttachment(session);

        this.broadcast({
          type: 'player_muted',
          playerId: targetId,
          isMuted: muted
        });
        break;
      }
    }
  }

  private setPermission(targetId: string, level: number) {
    for (const [ws, session] of this.sessions) {
      if (session.playerId === targetId) {
        session.player.permissionLevel = level;
        ws.serializeAttachment(session);

        this.broadcast({
          type: 'permission_changed',
          playerId: targetId,
          permissionLevel: level
        });
        break;
      }
    }
  }

  private broadcast(message: any, exclude?: WebSocket) {
    const json = JSON.stringify(message);
    for (const [ws] of this.sessions) {
      if (ws !== exclude) {
        ws.send(json);
      }
    }
  }

  private getPlayersSnapshot(): Record<string, Player> {
    const players: Record<string, Player> = {};
    for (const [, session] of this.sessions) {
      players[session.playerId] = session.player;
    }
    return players;
  }
}
```

### Message Types (src/types.ts)

```typescript
// Client → Server
export type ClientMessage =
  | { type: 'join'; name: string; userId?: string; avatarIndex?: number }
  | { type: 'state'; position?: [number, number, number]; rotation?: [number, number, number, number]; isJumping?: boolean; isSpeaking?: boolean }
  | { type: 'rpc'; method: string; target?: string; [key: string]: any }
  | { type: 'chat'; message: string }
  | { type: 'webrtc_signal'; target: string; signal: string };

// Server → Client
export type ServerMessage =
  | { type: 'welcome'; playerId: string; isHost: boolean; players: Record<string, Player> }
  | { type: 'player_joined'; playerId: string; player: Player }
  | { type: 'player_left'; playerId: string }
  | { type: 'state_update'; playerId: string; position: [number, number, number]; rotation: [number, number, number, number]; isJumping: boolean; isSpeaking: boolean }
  | { type: 'host_changed'; newHost: string }
  | { type: 'chat'; senderId: string; senderName: string; message: string; timestamp: number }
  | { type: 'webrtc_signal'; from: string; signal: string }
  | { type: 'player_muted'; playerId: string; isMuted: boolean }
  | { type: 'permission_changed'; playerId: string; permissionLevel: number };
```

---

## Unity Client Changes

Update `CustomNetworkManager.cs` from the [Custom WebSocket Plan](Custom_WebSocket_Networking_Plan.md) to connect to Cloudflare:

```csharp
public class CustomNetworkManager : MonoBehaviour
{
    [Header("Cloudflare Settings")]
    [SerializeField] private string serverUrl = "wss://realtime.metadyn.xyz";

    public void Connect(string roomName, string playerName, string userId = "")
    {
        string url = $"{serverUrl}?room={roomName}";

        // Optional: Add Supabase token for auth
        if (SupabaseAuthManager.Instance?.IsAuthenticated == true)
        {
            string token = SupabaseAuthManager.Instance.CurrentSession.access_token;
            url += $"&token={token}";
        }

        _ws = new WebSocket(url);
        _ws.OnOpen += OnOpen;
        _ws.OnMessage += OnMessage;
        _ws.OnClose += OnClose;
        _ws.OnError += OnError;
        _ws.Connect();
    }

    private void OnOpen()
    {
        // Send join message
        Send(new { type = "join", name = _playerName, userId = _userId });
    }
}
```

---

## Deployment

```bash
# Install wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create D1 database (optional)
wrangler d1 create metadyn-realtime

# Deploy
wrangler deploy

# View logs
wrangler tail
```

### Custom Domain Setup

1. Add DNS record: `realtime.metadyn.xyz` → Workers route
2. In wrangler.toml, add route pattern
3. SSL automatically provisioned by Cloudflare

---

## Cost Estimate

### Durable Objects Pricing (as of 2024)

| Resource | Free Tier | Paid |
|----------|-----------|------|
| Requests | 100k/month | $0.15/million |
| Duration | 400k GB-s/month | $12.50/million GB-s |
| Storage | 1 GB | $0.20/GB |

### Example: 50 Concurrent Players

```
Assumptions:
- 50 players in 1 room
- 20 state updates/second per player
- 8 hours of play per day
- 30 days

Calculations:
- Messages/day: 50 players × 20 msg/s × 8 hours × 3600 = 28.8M messages
- Messages/month: 28.8M × 30 = 864M messages

Cost:
- Requests: 864M × $0.15/M = $129.60/month
- Duration: Minimal (hibernation keeps DO sleeping between messages)
- Storage: Minimal (in-memory state only)

Total: ~$130/month for 50 concurrent players, 8hrs/day
```

**With hibernation:** DO sleeps between messages, so duration cost is near zero. Only charged per message.

**Comparison to Photon:**
- Photon Fusion: $0.06/CCU/day = $90/month for 50 CCU
- Cloudflare: ~$130/month but includes all infrastructure (no separate chat/voice signaling costs)

---

## Integration with Existing Cloudflare Services

### Vectorize (AI Memory)

The Durable Object can query Vectorize for AI context:

```typescript
// In GameRoom.ts, if env includes Vectorize binding
async getAIContext(playerId: string): Promise<string[]> {
  const results = await this.env.VECTORIZE.query(
    embedding,
    { topK: 5, namespace: playerId }
  );
  return results.matches.map(m => m.metadata.content);
}
```

### D1 (Persistent Data)

Store ban lists, room configs, analytics:

```typescript
// Check ban list on join
async isPlayerBanned(userId: string): Promise<boolean> {
  const result = await this.env.DB
    .prepare('SELECT 1 FROM bans WHERE user_id = ?')
    .bind(userId)
    .first();
  return !!result;
}

// Log analytics
async logSession(roomName: string, playerCount: number, duration: number) {
  await this.env.DB
    .prepare('INSERT INTO sessions (room, players, duration, timestamp) VALUES (?, ?, ?, ?)')
    .bind(roomName, playerCount, duration, Date.now())
    .run();
}
```

---

## Advantages Over Standalone Server

| Aspect | Standalone (Node.js) | Cloudflare DO |
|--------|---------------------|---------------|
| Deployment | Manage server, SSL, scaling | `wrangler deploy` |
| Global latency | Single region or complex setup | Edge by default |
| Scaling | Manual or K8s | Automatic |
| WebSocket idle cost | Always running | Hibernation (near-zero) |
| Integration | Separate services | Same network as CDN, DNS, Vectorize |
| Maintenance | Updates, security patches | Managed by Cloudflare |

---

## Migration Checklist

- [ ] Create Cloudflare account (if not already)
- [ ] Install wrangler CLI
- [ ] Initialize project with `wrangler init`
- [ ] Implement GameRoom Durable Object
- [ ] Implement Worker router
- [ ] Create D1 database for persistence (optional)
- [ ] Deploy to Cloudflare
- [ ] Set up custom domain (realtime.metadyn.xyz)
- [ ] Update Unity `CustomNetworkManager` to use Cloudflare URL
- [ ] Test WebSocket connection from WebGL build
- [ ] Test with 2 players
- [ ] Test WebRTC signaling
- [ ] Load test with 10+ players
- [ ] Monitor costs in Cloudflare dashboard

---

## Next Steps

1. Set up `/cloudflare-realtime/` project in MetaDyn monorepo
2. Implement basic GameRoom with join/leave/state
3. Test from Unity Editor with WebSocket
4. Add WebRTC signaling relay
5. Deploy and test from WebGL build
6. Add D1 integration for ban lists
7. Performance tuning and cost monitoring

---

**Related Documentation:**
- [Custom_WebSocket_Networking_Plan.md](Custom_WebSocket_Networking_Plan.md) - Unity client implementation details
- [INFRASTRUCTURE.md](../Quick%20Reference/INFRASTRUCTURE.md) - Current Cloudflare CDN setup
