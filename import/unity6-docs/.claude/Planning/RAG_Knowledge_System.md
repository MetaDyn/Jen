# RAG & Knowledge Base Integration Plan

**Status:** Draft
**Date:** 2026-01-07
**Related Systems:** AI Embodiment, Cloudflare Memory, MetaDynVoiceController

## Overview

This document outlines the architecture for adding **Retrieval-Augmented Generation (RAG)** to the MetaDyn AI Agents. This system allows agents to "read" and reference static documentation (PDFs, manuals, lore sheets) to answer user questions accurately without requiring model fine-tuning.

## Architecture

The system follows a hybrid "Edge-Retrieved, Client-Injected" pattern, leveraging the existing Cloudflare infrastructure to keep the Unity client lightweight.

```
┌─────────────────┐       ┌──────────────────────────────┐       ┌─────────────────┐
│  Admin / Dev    │       │   Cloudflare Edge Worker     │       │   Unity Client  │
│  (Ingestion)    │       │   (Retrieval Logic)          │       │   (Generation)  │
└────────┬────────┘       └──────────────┬───────────────┘       └────────┬────────┘
         │                               │                                │
         │ 1. Parse & Chunk              │ 3. Semantic Search             │ 5. Inject Context
         │ 2. Embed & Upload             │    (Dual Query)                │    & Generate
         ▼                               ▼                                │
┌─────────────────┐       ┌──────────────────────────────┐                │
│ Cloudflare      │       │ Indexes:                     │                │
│ Vectorize       │◄──────┤ • metadyn-memory (User)      │◄───────────────┘
│ & D1 Database   │       │ • metadyn-knowledge (Docs)   │      4. JSON Response
└─────────────────┘       └──────────────────────────────┘      { knowledge: [...] }
```

## 1. Ingestion Pipeline (Admin Tool)

Since Unity is ill-suited for heavy PDF parsing, ingestion occurs offline via a dedicated script (Python or Node.js).

### Workflow
1.  **Text Extraction:** Script reads PDF/Markdown files from a source directory.
2.  **Chunking:** Content is split into semantic chunks (e.g., 512 tokens with 50-token overlap).
3.  **Embedding:** Chunks are sent to OpenAI (`text-embedding-3-small`) to generate 1536d vectors.
4.  **Storage:**
    *   **Vectors:** Stored in a NEW Cloudflare Vectorize index (`metadyn-knowledge-base`).
    *   **Content:** Text chunks + Metadata (Source file, Page #) stored in D1 Database.

### Database Schema (D1) Extension
```sql
CREATE TABLE knowledge_chunks (
    id TEXT PRIMARY KEY,            -- UUID
    content TEXT NOT NULL,          -- The actual text chunk
    source_filename TEXT,           -- e.g. "Employee_Handbook.pdf"
    page_number INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 2. Backend Implementation (Cloudflare Worker)

The existing `memory.metadyn.xyz` worker will be updated to perform "Dual Retrieval".

### Logic Flow
1.  Receive `query` from Unity Client.
2.  Generate Embedding for `query`.
3.  **Parallel Execution:**
    *   **Task A:** Query `metadyn-conversation-embeddings` (User Memory).
    *   **Task B:** Query `metadyn-knowledge-base` (Knowledge).
4.  **Filtering:**
    *   Filter Knowledge results for high similarity (> 0.75).
    *   Limit to top 3 relevant chunks.
5.  **Response Construction:**
    *   Merge results into the returned JSON object.

### Response JSON Structure
```json
{
  "user": { ... },
  "relevantMemories": [ ... ],
  "knowledge": [
    {
      "text": "Flux capacitors require 1.21 gigawatts of electricity...",
      "source": "Manual.pdf"
    }
  ]
}
```

## 3. Unity Client Implementation

### `AIMemoryManager.cs`
Update `MemoryContext` to deserialize the new data.

```csharp
[Serializable]
public class MemoryContext
{
    // ... existing fields ...
    public KnowledgeChunk[] knowledge; // New field
}

[Serializable]
public class KnowledgeChunk
{
    public string text;
    public string source;
}
```

### `MetaDynVoiceController.cs`
Update `BuildChatJson` to inject the retrieved knowledge into the System Prompt. This ensures the AI "knows" the information before answering the user.

**Context Injection Format:**
```text
[INTERNAL CONTEXT]
[MEMORY: User likes sci-fi...]
[REFERENCE MATERIAL:
 - (Source: Manual.pdf) Flux capacitors require 1.21 gigawatts...
 - (Source: Safety.pdf) Always wear gloves...]
[SPATIAL: User is near the engine...]
```

**System Instruction Update:**
Add to the Agent's system prompt: *"If [REFERENCE MATERIAL] is provided, prioritize that information over your general training data to answer user questions."*

## 4. Execution Steps

1.  **Cloudflare:**
    *   Create new Vectorize Index: `metadyn-knowledge-base`.
    *   Run D1 migration for `knowledge_chunks` table.
2.  **Tooling:**
    *   Write `ingest_docs.py` script.
3.  **Worker:**
    *   Update `src/index.ts` to query the new index.
4.  **Unity:**
    *   Update `AIMemoryManager` serialization.
    *   Update `MetaDynVoiceController` prompt building logic.
