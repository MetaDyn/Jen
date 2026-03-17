# Cloudflare AI Memory Integration Plan

**Date:** 2025-12-30
**Status:** Planning
**Purpose:** Production-ready AI long-term memory using Cloudflare edge infrastructure

---

## Executive Summary

This document outlines the integration of Cloudflare's edge services (Vectorize, D1, Workers KV, R2) with MetaDyn's existing AI embodiment system to provide persistent, semantic memory for AI avatars.

**Approach:** Hybrid architecture maintaining Supabase for authentication while adding Cloudflare for AI-specific memory and retrieval.

---

## Part 1: Current Architecture

### Existing Systems

```
┌─────────────────────────────────────────────────────────────────┐
│                     CURRENT ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐         ┌─────────────────────────────┐    │
│  │   Supabase      │         │      Cloudflare CDN         │    │
│  │                 │         │                             │    │
│  │  • Auth (JWT)   │         │  • DNS (metadyn.xyz)        │    │
│  │  • Profiles     │         │  • Edge caching             │    │
│  │  • Spaces       │         │  • WebGL build delivery     │    │
│  │                 │         │  • WebSocket proxy          │    │
│  └────────┬────────┘         └──────────────┬──────────────┘    │
│           │                                  │                   │
│           └──────────────┬───────────────────┘                   │
│                          │                                       │
│                          ▼                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  Unity WebGL Client                        │  │
│  │                                                            │  │
│  │  MetaDynVoiceController:                                   │  │
│  │  • 20-message conversation history (in-memory)             │  │
│  │  • No persistence across sessions                          │  │
│  │  • No semantic memory retrieval                            │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Current Limitations

| Limitation | Impact |
|------------|--------|
| Memory lost on page refresh | AI forgets everything each session |
| No cross-session relationships | Can't build rapport over time |
| Linear history only | Can't recall relevant past topics |
| No user preferences learned | Same behavior for all users |
| 20-message cap | Long conversations lose early context |

---

## Part 2: Proposed Architecture

### Hybrid Cloudflare + Supabase

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       PROPOSED ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────┐                    ┌─────────────────────────────┐ │
│  │   Supabase      │                    │   Cloudflare AI Memory      │ │
│  │   (Unchanged)   │                    │   (NEW)                     │ │
│  │                 │                    │                             │ │
│  │  • Auth (JWT)   │                    │  ┌─────────────────────┐    │ │
│  │  • User ID      │◄───────────────────┤  │  Worker API         │    │ │
│  │  • Profiles     │   (Auth Token)     │  │  memory.metadyn.xyz │    │ │
│  │  • Spaces       │                    │  └──────────┬──────────┘    │ │
│  │                 │                    │             │               │ │
│  └─────────────────┘                    │  ┌──────────┴──────────┐    │ │
│                                         │  │                     │    │ │
│                                         │  ▼                     ▼    │ │
│                                         │ ┌────────┐ ┌────────┐      │ │
│                                         │ │Vectorize│ │   D1   │      │ │
│                                         │ │(Semantic│ │(Struct)│      │ │
│                                         │ │ Memory) │ │ Data)  │      │ │
│                                         │ └────────┘ └────────┘      │ │
│                                         │                             │ │
│                                         │ ┌────────┐ ┌────────┐      │ │
│                                         │ │   KV   │ │   R2   │      │ │
│                                         │ │(Cache) │ │(Media) │      │ │
│                                         │ └────────┘ └────────┘      │ │
│                                         │                             │ │
│                                         └─────────────────────────────┘ │
│                                                       │                  │
│                                                       │                  │
│  ┌────────────────────────────────────────────────────┴─────────────┐   │
│  │                     Unity WebGL Client                            │   │
│  │                                                                   │   │
│  │  MetaDynVoiceController (Enhanced):                               │   │
│  │  • Fetches relevant memories before each message                  │   │
│  │  • Stores conversation summaries after each session               │   │
│  │  • Maintains user relationship data                               │   │
│  │  • Learns user preferences over time                              │   │
│  │                                                                   │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Cloudflare Service Configuration

### 3.1 D1 Database Schema

**Database Name:** `metadyn-ai-memory`

```sql
-- User relationship tracking
CREATE TABLE user_profiles (
    user_id TEXT PRIMARY KEY,           -- From Supabase auth
    display_name TEXT,
    first_interaction_at DATETIME,
    last_interaction_at DATETIME,
    total_interactions INTEGER DEFAULT 0,
    total_conversation_time_seconds INTEGER DEFAULT 0,
    rapport_score REAL DEFAULT 0.5,     -- 0.0 to 1.0
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Key facts learned about users
CREATE TABLE user_facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    fact_type TEXT NOT NULL,            -- 'preference', 'personal', 'professional', 'interest'
    fact_content TEXT NOT NULL,         -- "Works in marketing", "Prefers casual tone"
    confidence REAL DEFAULT 0.8,        -- How certain we are (0.0 to 1.0)
    source_conversation_id TEXT,        -- Which conversation this came from
    extracted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_referenced_at DATETIME,
    reference_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

-- Conversation metadata
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,                -- UUID
    user_id TEXT NOT NULL,
    ai_agent_id TEXT DEFAULT 'pavilion-assistant',
    started_at DATETIME,
    ended_at DATETIME,
    duration_seconds INTEGER,
    turn_count INTEGER,
    summary TEXT,                       -- LLM-generated summary
    topics TEXT,                        -- JSON array of topics discussed
    sentiment_avg REAL,                 -- Average sentiment (optional)
    transcript_r2_key TEXT,             -- Reference to full transcript in R2
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

-- User communication preferences (learned over time)
CREATE TABLE user_preferences (
    user_id TEXT PRIMARY KEY,
    formality_score REAL DEFAULT 0.5,   -- 0=casual, 1=formal
    verbosity_score REAL DEFAULT 0.5,   -- 0=brief, 1=detailed
    humor_score REAL DEFAULT 0.5,       -- 0=serious, 1=playful
    topics_of_interest TEXT,            -- JSON array
    topics_to_avoid TEXT,               -- JSON array
    preferred_greeting TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

-- Indexes for common queries
CREATE INDEX idx_user_facts_user ON user_facts(user_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_time ON conversations(started_at DESC);
```

### 3.2 Vectorize Configuration

**Index Name:** `metadyn-conversation-embeddings`

```typescript
// Vectorize index configuration
{
  name: "metadyn-conversation-embeddings",
  dimensions: 1536,  // OpenAI text-embedding-3-small
  metric: "cosine"
}

// Vector metadata structure
interface ConversationVector {
  id: string;                    // conversation_id
  values: number[];              // 1536-dim embedding
  metadata: {
    user_id: string;
    timestamp: number;
    summary: string;             // For display without re-fetching
    topics: string[];
    sentiment: number;
  }
}
```

### 3.3 Workers KV Namespace

**Namespace:** `METADYN_AI_CACHE`

```typescript
// KV key patterns
{
  // Quick user profile lookup (TTL: 5 minutes)
  "user:{user_id}:profile": UserProfileCache,

  // Recent memories for active session (TTL: 30 minutes)
  "user:{user_id}:active_memories": RelevantMemory[],

  // Preference cache (TTL: 1 hour)
  "user:{user_id}:preferences": UserPreferences,

  // Rate limiting (TTL: 1 minute)
  "ratelimit:{user_id}": number
}
```

### 3.4 R2 Bucket Structure

**Bucket Name:** `metadyn-ai-storage`

```
metadyn-ai-storage/
├── transcripts/
│   └── {user_id}/
│       └── {conversation_id}.json     # Full conversation transcript
├── snapshots/
│   └── {user_id}/
│       └── {timestamp}.jpg            # AI vision captures
└── audio/
    └── {user_id}/
        └── {conversation_id}/
            └── {turn_id}.wav          # Voice recordings (optional)
```

---

## Part 4: Worker API Design

### Endpoint: `memory.metadyn.xyz`

```typescript
// worker/src/index.ts

import { Hono } from 'hono';
import { cors } from 'hono/cors';

type Bindings = {
  DB: D1Database;
  VECTORIZE: VectorizeIndex;
  KV: KVNamespace;
  R2: R2Bucket;
  OPENAI_API_KEY: string;
  SUPABASE_JWT_SECRET: string;
};

const app = new Hono<{ Bindings: Bindings }>();

// CORS for Unity WebGL
app.use('*', cors({
  origin: ['https://metadyn.xyz', 'https://pavilion.metadyn.xyz', 'http://localhost'],
  allowMethods: ['GET', 'POST', 'PUT'],
  allowHeaders: ['Content-Type', 'Authorization'],
}));

// Auth middleware - validates Supabase JWT
app.use('*', async (c, next) => {
  const authHeader = c.req.header('Authorization');
  if (!authHeader?.startsWith('Bearer ')) {
    return c.json({ error: 'Unauthorized' }, 401);
  }

  const token = authHeader.slice(7);
  const user = await verifySupabaseJWT(token, c.env.SUPABASE_JWT_SECRET);

  if (!user) {
    return c.json({ error: 'Invalid token' }, 401);
  }

  c.set('user', user);
  await next();
});

// ============================================
// MEMORY RETRIEVAL (Called before each AI message)
// ============================================

app.post('/api/memory/recall', async (c) => {
  const user = c.get('user');
  const { query, limit = 5 } = await c.req.json();

  // 1. Check KV cache first
  const cacheKey = `user:${user.id}:active_memories`;
  const cached = await c.env.KV.get(cacheKey, 'json');

  // 2. Get user profile from D1
  const profile = await c.env.DB.prepare(`
    SELECT * FROM user_profiles WHERE user_id = ?
  `).bind(user.id).first();

  // 3. Get user facts
  const facts = await c.env.DB.prepare(`
    SELECT fact_type, fact_content, confidence
    FROM user_facts
    WHERE user_id = ?
    ORDER BY reference_count DESC, confidence DESC
    LIMIT 10
  `).bind(user.id).all();

  // 4. Semantic search for relevant past conversations
  const embedding = await generateEmbedding(query, c.env.OPENAI_API_KEY);

  const vectorResults = await c.env.VECTORIZE.query(embedding, {
    topK: limit,
    filter: { user_id: user.id },
    returnMetadata: true
  });

  // 5. Get user preferences
  const preferences = await c.env.DB.prepare(`
    SELECT * FROM user_preferences WHERE user_id = ?
  `).bind(user.id).first();

  // 6. Build memory context
  const memoryContext = {
    user: {
      name: profile?.display_name || 'User',
      firstMet: profile?.first_interaction_at,
      totalInteractions: profile?.total_interactions || 0,
      rapportScore: profile?.rapport_score || 0.5
    },
    facts: facts.results?.map(f => ({
      type: f.fact_type,
      content: f.fact_content
    })) || [],
    relevantMemories: vectorResults.matches?.map(m => ({
      summary: m.metadata?.summary,
      topics: m.metadata?.topics,
      when: new Date(m.metadata?.timestamp).toLocaleDateString()
    })) || [],
    preferences: preferences ? {
      formality: preferences.formality_score,
      verbosity: preferences.verbosity_score,
      humor: preferences.humor_score
    } : null
  };

  // 7. Cache for session
  await c.env.KV.put(cacheKey, JSON.stringify(memoryContext), { expirationTtl: 1800 });

  return c.json(memoryContext);
});

// ============================================
// MEMORY STORAGE (Called after conversation ends)
// ============================================

app.post('/api/memory/store', async (c) => {
  const user = c.get('user');
  const {
    conversationId,
    transcript,
    duration,
    turnCount
  } = await c.req.json();

  // 1. Generate summary and extract facts via LLM
  const analysis = await analyzeConversation(transcript, c.env.OPENAI_API_KEY);

  // 2. Store full transcript in R2
  const transcriptKey = `transcripts/${user.id}/${conversationId}.json`;
  await c.env.R2.put(transcriptKey, JSON.stringify({
    id: conversationId,
    user_id: user.id,
    transcript,
    analyzed_at: new Date().toISOString()
  }));

  // 3. Update/create user profile
  await c.env.DB.prepare(`
    INSERT INTO user_profiles (user_id, display_name, first_interaction_at, last_interaction_at, total_interactions, total_conversation_time_seconds)
    VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1, ?)
    ON CONFLICT(user_id) DO UPDATE SET
      last_interaction_at = CURRENT_TIMESTAMP,
      total_interactions = total_interactions + 1,
      total_conversation_time_seconds = total_conversation_time_seconds + ?,
      updated_at = CURRENT_TIMESTAMP
  `).bind(user.id, user.name || 'User', duration, duration).run();

  // 4. Store conversation metadata
  await c.env.DB.prepare(`
    INSERT INTO conversations (id, user_id, started_at, ended_at, duration_seconds, turn_count, summary, topics, transcript_r2_key)
    VALUES (?, ?, datetime('now', '-' || ? || ' seconds'), CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
  `).bind(
    conversationId,
    user.id,
    duration,
    duration,
    turnCount,
    analysis.summary,
    JSON.stringify(analysis.topics),
    transcriptKey
  ).run();

  // 5. Store extracted facts
  for (const fact of analysis.facts) {
    await c.env.DB.prepare(`
      INSERT INTO user_facts (user_id, fact_type, fact_content, confidence, source_conversation_id)
      VALUES (?, ?, ?, ?, ?)
    `).bind(user.id, fact.type, fact.content, fact.confidence, conversationId).run();
  }

  // 6. Generate and store embedding for semantic search
  const embedding = await generateEmbedding(analysis.summary, c.env.OPENAI_API_KEY);

  await c.env.VECTORIZE.insert([{
    id: conversationId,
    values: embedding,
    metadata: {
      user_id: user.id,
      timestamp: Date.now(),
      summary: analysis.summary,
      topics: analysis.topics,
      sentiment: analysis.sentiment
    }
  }]);

  // 7. Update preferences if patterns detected
  if (analysis.preferenceSignals) {
    await updateUserPreferences(c.env.DB, user.id, analysis.preferenceSignals);
  }

  return c.json({ success: true, conversationId });
});

// ============================================
// HELPER: Store vision snapshot
// ============================================

app.post('/api/memory/snapshot', async (c) => {
  const user = c.get('user');
  const formData = await c.req.formData();
  const image = formData.get('image') as File;
  const context = formData.get('context') as string;

  const timestamp = Date.now();
  const key = `snapshots/${user.id}/${timestamp}.jpg`;

  await c.env.R2.put(key, await image.arrayBuffer(), {
    customMetadata: { context, user_id: user.id }
  });

  return c.json({ success: true, key });
});

export default app;

// ============================================
// HELPER FUNCTIONS
// ============================================

async function generateEmbedding(text: string, apiKey: string): Promise<number[]> {
  const response = await fetch('https://api.openai.com/v1/embeddings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'text-embedding-3-small',
      input: text
    })
  });

  const data = await response.json();
  return data.data[0].embedding;
}

async function analyzeConversation(transcript: any[], apiKey: string) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4o-mini',
      messages: [
        {
          role: 'system',
          content: `Analyze this conversation and extract:
1. A 1-2 sentence summary
2. Main topics discussed (array of strings)
3. Key facts learned about the user (array of {type, content, confidence})
4. Overall sentiment (-1 to 1)
5. Any preference signals (formality, verbosity, humor preferences)

Return as JSON.`
        },
        {
          role: 'user',
          content: JSON.stringify(transcript)
        }
      ],
      response_format: { type: 'json_object' }
    })
  });

  const data = await response.json();
  return JSON.parse(data.choices[0].message.content);
}

async function verifySupabaseJWT(token: string, secret: string) {
  // JWT verification logic
  // Returns user object or null
}

async function updateUserPreferences(db: D1Database, userId: string, signals: any) {
  // Incrementally update preference scores based on signals
}
```

---

## Part 5: Unity Integration

### 5.1 New Component: AIMemoryManager

**File:** `/Assets/MetaDyn/AI/AIMemoryManager.cs`

```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;

namespace MetaDyn.AI
{
    /// <summary>
    /// Manages persistent AI memory via Cloudflare edge infrastructure.
    /// Integrates with existing Supabase auth for user identification.
    /// </summary>
    public class AIMemoryManager : MonoBehaviour
    {
        [Header("Configuration")]
        [Tooltip("Cloudflare Worker endpoint for AI memory")]
        public string memoryApiUrl = "https://memory.metadyn.xyz/api";

        [Tooltip("Maximum memories to retrieve per query")]
        public int maxMemoriesToRetrieve = 5;

        [Header("References")]
        public SupabaseAuthManager authManager;

        // Cached memory context for current session
        private MemoryContext _currentMemoryContext;
        private string _currentConversationId;
        private float _conversationStartTime;
        private List<ConversationTurn> _currentTranscript = new List<ConversationTurn>();

        public static AIMemoryManager Instance { get; private set; }

        private void Awake()
        {
            if (Instance == null)
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
            }
            else
            {
                Destroy(gameObject);
            }
        }

        /// <summary>
        /// Retrieve relevant memories for the current query.
        /// Called by MetaDynVoiceController before each LLM request.
        /// </summary>
        public IEnumerator RecallMemories(string query, Action<MemoryContext> onComplete)
        {
            if (authManager == null || !authManager.IsLoggedIn)
            {
                Debug.LogWarning("[AIMemory] User not authenticated, skipping memory recall");
                onComplete?.Invoke(null);
                yield break;
            }

            var requestBody = new RecallRequest { query = query, limit = maxMemoriesToRetrieve };
            string json = JsonUtility.ToJson(requestBody);

            using (UnityWebRequest www = new UnityWebRequest($"{memoryApiUrl}/memory/recall", "POST"))
            {
                byte[] bodyRaw = Encoding.UTF8.GetBytes(json);
                www.uploadHandler = new UploadHandlerRaw(bodyRaw);
                www.downloadHandler = new DownloadHandlerBuffer();
                www.SetRequestHeader("Content-Type", "application/json");
                www.SetRequestHeader("Authorization", $"Bearer {authManager.AccessToken}");

                yield return www.SendWebRequest();

                if (www.result == UnityWebRequest.Result.Success)
                {
                    _currentMemoryContext = JsonUtility.FromJson<MemoryContext>(www.downloadHandler.text);
                    onComplete?.Invoke(_currentMemoryContext);
                }
                else
                {
                    Debug.LogError($"[AIMemory] Recall failed: {www.error}");
                    onComplete?.Invoke(null);
                }
            }
        }

        /// <summary>
        /// Generate memory context string for LLM injection.
        /// </summary>
        public string GetMemoryContextForLLM()
        {
            if (_currentMemoryContext == null) return "";

            StringBuilder sb = new StringBuilder();
            sb.AppendLine("[LONG-TERM MEMORY - Use naturally, don't quote directly]");

            // User relationship
            if (_currentMemoryContext.user != null)
            {
                sb.AppendLine($"User: {_currentMemoryContext.user.name}");
                sb.AppendLine($"Relationship: Met {_currentMemoryContext.user.totalInteractions} times");
                if (!string.IsNullOrEmpty(_currentMemoryContext.user.firstMet))
                {
                    sb.AppendLine($"First met: {_currentMemoryContext.user.firstMet}");
                }
            }

            // Known facts
            if (_currentMemoryContext.facts != null && _currentMemoryContext.facts.Length > 0)
            {
                sb.AppendLine("Known facts about user:");
                foreach (var fact in _currentMemoryContext.facts)
                {
                    sb.AppendLine($"  - {fact.content}");
                }
            }

            // Relevant past conversations
            if (_currentMemoryContext.relevantMemories != null && _currentMemoryContext.relevantMemories.Length > 0)
            {
                sb.AppendLine("Relevant past conversations:");
                foreach (var memory in _currentMemoryContext.relevantMemories)
                {
                    sb.AppendLine($"  - {memory.when}: {memory.summary}");
                }
            }

            // Communication preferences
            if (_currentMemoryContext.preferences != null)
            {
                var p = _currentMemoryContext.preferences;
                string style = "";
                if (p.formality > 0.7f) style += "formal, ";
                else if (p.formality < 0.3f) style += "casual, ";
                if (p.verbosity > 0.7f) style += "detailed, ";
                else if (p.verbosity < 0.3f) style += "brief, ";
                if (p.humor > 0.7f) style += "playful";
                else if (p.humor < 0.3f) style += "serious";

                if (!string.IsNullOrEmpty(style))
                {
                    sb.AppendLine($"User prefers: {style.TrimEnd(',', ' ')}");
                }
            }

            return sb.ToString();
        }

        /// <summary>
        /// Start tracking a new conversation.
        /// </summary>
        public void StartConversation()
        {
            _currentConversationId = Guid.NewGuid().ToString();
            _conversationStartTime = Time.time;
            _currentTranscript.Clear();
            Debug.Log($"[AIMemory] Started conversation: {_currentConversationId}");
        }

        /// <summary>
        /// Record a conversation turn.
        /// </summary>
        public void RecordTurn(string role, string content)
        {
            _currentTranscript.Add(new ConversationTurn
            {
                role = role,
                content = content,
                timestamp = Time.time - _conversationStartTime
            });
        }

        /// <summary>
        /// End conversation and store memories.
        /// Called when chat panel closes or user disconnects.
        /// </summary>
        public IEnumerator EndConversation()
        {
            if (string.IsNullOrEmpty(_currentConversationId) || _currentTranscript.Count < 2)
            {
                Debug.Log("[AIMemory] No meaningful conversation to store");
                yield break;
            }

            if (authManager == null || !authManager.IsLoggedIn)
            {
                Debug.LogWarning("[AIMemory] User not authenticated, skipping memory storage");
                yield break;
            }

            float duration = Time.time - _conversationStartTime;

            var storeRequest = new StoreRequest
            {
                conversationId = _currentConversationId,
                transcript = _currentTranscript.ToArray(),
                duration = (int)duration,
                turnCount = _currentTranscript.Count
            };

            string json = JsonUtility.ToJson(storeRequest);

            using (UnityWebRequest www = new UnityWebRequest($"{memoryApiUrl}/memory/store", "POST"))
            {
                byte[] bodyRaw = Encoding.UTF8.GetBytes(json);
                www.uploadHandler = new UploadHandlerRaw(bodyRaw);
                www.downloadHandler = new DownloadHandlerBuffer();
                www.SetRequestHeader("Content-Type", "application/json");
                www.SetRequestHeader("Authorization", $"Bearer {authManager.AccessToken}");

                yield return www.SendWebRequest();

                if (www.result == UnityWebRequest.Result.Success)
                {
                    Debug.Log($"[AIMemory] Conversation stored: {_currentConversationId}");
                }
                else
                {
                    Debug.LogError($"[AIMemory] Store failed: {www.error}");
                }
            }

            // Reset for next conversation
            _currentConversationId = null;
            _currentTranscript.Clear();
        }

        // ============================================
        // DATA STRUCTURES
        // ============================================

        [Serializable]
        private class RecallRequest
        {
            public string query;
            public int limit;
        }

        [Serializable]
        private class StoreRequest
        {
            public string conversationId;
            public ConversationTurn[] transcript;
            public int duration;
            public int turnCount;
        }

        [Serializable]
        public class ConversationTurn
        {
            public string role;
            public string content;
            public float timestamp;
        }

        [Serializable]
        public class MemoryContext
        {
            public UserInfo user;
            public Fact[] facts;
            public Memory[] relevantMemories;
            public Preferences preferences;
        }

        [Serializable]
        public class UserInfo
        {
            public string name;
            public string firstMet;
            public int totalInteractions;
            public float rapportScore;
        }

        [Serializable]
        public class Fact
        {
            public string type;
            public string content;
        }

        [Serializable]
        public class Memory
        {
            public string summary;
            public string[] topics;
            public string when;
        }

        [Serializable]
        public class Preferences
        {
            public float formality;
            public float verbosity;
            public float humor;
        }
    }
}
```

### 5.2 MetaDynVoiceController Integration

**Changes to existing file:**

```csharp
// Add to MetaDynVoiceController.cs

[Header("Long-Term Memory")]
public AIMemoryManager memoryManager;
public bool enableLongTermMemory = true;

// Modify Start()
void Start()
{
    // ... existing code ...

    // Start conversation tracking
    if (enableLongTermMemory && memoryManager != null)
    {
        memoryManager.StartConversation();
    }
}

// Modify ProcessUserMessage() - add memory recall
IEnumerator ProcessUserMessage(string userText, bool hidden = false)
{
    // ... existing interrupt logic ...

    // NEW: Recall relevant memories before first user message
    if (enableLongTermMemory && memoryManager != null && _conversationHistory.Count <= 2)
    {
        yield return StartCoroutine(memoryManager.RecallMemories(userText, null));
    }

    // NEW: Record user turn
    if (enableLongTermMemory && memoryManager != null && !hidden)
    {
        memoryManager.RecordTurn("user", userText);
    }

    // 1. Perception Context (existing)
    if (perceptionManager != null)
    {
        string context = perceptionManager.GetPerceptionContext();
        _conversationHistory.Add(new ChatMessage {
            role = "system",
            content = $"[SPATIAL CONTEXT: {context}]"
        });
    }

    // NEW: Long-term memory context
    if (enableLongTermMemory && memoryManager != null)
    {
        string memoryContext = memoryManager.GetMemoryContextForLLM();
        if (!string.IsNullOrEmpty(memoryContext))
        {
            _conversationHistory.Add(new ChatMessage {
                role = "system",
                content = memoryContext
            });
        }
    }

    // ... rest of existing code ...
}

// Modify OnCloseButtonClicked()
void OnCloseButtonClicked()
{
    // ... existing code ...

    // NEW: Store conversation memories
    if (enableLongTermMemory && memoryManager != null)
    {
        StartCoroutine(memoryManager.EndConversation());
    }
}

// NEW: Record assistant responses
private void OnTextChunkReceived(string textChunk)
{
    // ... existing code ...

    // Record complete responses (check for sentence end)
    // This is handled in the existing sentence splitting logic
}

// Add after response complete in StreamOpenRouterResponse
// After: _conversationHistory.Add(new ChatMessage { role = "assistant", content = _fullResponseAccumulator.ToString() });
if (enableLongTermMemory && memoryManager != null)
{
    memoryManager.RecordTurn("assistant", _fullResponseAccumulator.ToString());
}
```

---

## Part 6: Deployment Checklist

### Cloudflare Setup

```bash
# 1. Create D1 database
wrangler d1 create metadyn-ai-memory

# 2. Apply schema
wrangler d1 execute metadyn-ai-memory --file=./schema.sql

# 3. Create Vectorize index
wrangler vectorize create metadyn-conversation-embeddings --dimensions=1536 --metric=cosine

# 4. Create KV namespace
wrangler kv:namespace create METADYN_AI_CACHE

# 5. Create R2 bucket
wrangler r2 bucket create metadyn-ai-storage

# 6. Add secrets
wrangler secret put OPENAI_API_KEY
wrangler secret put SUPABASE_JWT_SECRET

# 7. Deploy worker
wrangler deploy
```

### wrangler.toml

```toml
name = "metadyn-ai-memory"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "metadyn-ai-memory"
database_id = "<your-database-id>"

[[vectorize]]
binding = "VECTORIZE"
index_name = "metadyn-conversation-embeddings"

[[kv_namespaces]]
binding = "KV"
id = "<your-kv-namespace-id>"

[[r2_buckets]]
binding = "R2"
bucket_name = "metadyn-ai-storage"

[vars]
ENVIRONMENT = "production"
```

### DNS Configuration

Add CNAME record in Cloudflare:
```
memory.metadyn.xyz -> <worker-subdomain>.workers.dev
```

---

## Part 7: Cost Estimates

### Cloudflare (Monthly, 10K active users)

| Service | Usage Estimate | Cost |
|---------|----------------|------|
| Workers | 1M requests | Free tier |
| D1 | 5GB storage, 25M reads | ~$5 |
| Vectorize | 100K vectors, 500K queries | ~$10 |
| KV | 10M reads, 1M writes | Free tier |
| R2 | 10GB storage | ~$0.15 |
| **Total** | | **~$15/month** |

### OpenAI (for embeddings + analysis)

| Operation | Volume | Cost |
|-----------|--------|------|
| Embeddings | 50K/month | ~$1 |
| Conversation analysis | 10K/month | ~$5 |
| **Total** | | **~$6/month** |

**Combined Total: ~$21/month** for 10K active users

---

## Part 8: Migration Path

### Phase 1: Deploy Infrastructure (1 day)
1. Create Cloudflare resources (D1, Vectorize, KV, R2)
2. Deploy Worker API
3. Test endpoints with curl/Postman

### Phase 2: Unity Integration (2 days)
1. Add AIMemoryManager component
2. Integrate with MetaDynVoiceController
3. Test locally with Supabase auth

### Phase 3: Gradual Rollout (1 week)
1. Enable for internal testing
2. Monitor costs and performance
3. Enable for all users

### Rollback Plan
- AIMemoryManager has `enableLongTermMemory` toggle
- Can disable without code changes
- Existing 20-message in-memory history still works as fallback

---

## Appendix: Example Conversation Flow

```
[User approaches AI for first time]

1. Unity calls: POST /api/memory/recall
   → Returns empty context (new user)

2. AI greets: "Hello! Welcome to the Pavilion. I'm your assistant."

3. Conversation happens...
   User: "I'm looking for the conference room"
   AI: "The conference room is to your left, about 10 meters away."
   User: "Thanks! I work in marketing and we have a presentation."
   AI: "Good luck with your presentation!"

4. User closes chat
   → Unity calls: POST /api/memory/store
   → Worker analyzes conversation:
     - Summary: "User asked for directions to conference room for marketing presentation"
     - Facts: [{type: "professional", content: "Works in marketing"}]
     - Embedding stored in Vectorize

[Same user returns next day]

1. Unity calls: POST /api/memory/recall
   → Returns:
   {
     user: { name: "Alex", totalInteractions: 1, firstMet: "2025-12-29" },
     facts: [{ type: "professional", content: "Works in marketing" }],
     relevantMemories: [{ summary: "Asked for directions to conference room", when: "Yesterday" }],
     preferences: null
   }

2. AI greets: "Welcome back, Alex! How did your marketing presentation go?"

[User is impressed - AI remembered them!]
```

---

**Document Status:** Ready for implementation
**Next Step:** Deploy Cloudflare infrastructure
**Dependencies:** Supabase auth must be operational
