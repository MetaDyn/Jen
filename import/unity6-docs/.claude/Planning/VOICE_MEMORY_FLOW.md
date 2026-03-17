# Voice Memory Flow

Code-traced documentation of how `MetaDynVoiceController` uses memory, context, voice input, and vision.

This document reflects the current implementation in:

- `Assets/MetaDyn/AI/MetaDynVoiceController.cs`
- `Assets/MetaDyn/AI/AIMemoryManager.cs`
- `Assets/MetaDyn/AI/AIEye.cs`

## Short Answer

The current code does **not** send "context + user input + image" as one embedding and save that as memory from Unity.

What actually happens:

1. User voice is transcribed to text with Whisper.
2. On the first turn, the text query is used to **recall** existing memories from the backend.
3. If vision is triggered, a JPG snapshot is attached to the **live LLM request only**.
4. After the conversation, Unity builds a short **text summary** from recent user/assistant turns.
5. Unity asks the LLM to extract `topics` and `sentiment`.
6. Unity sends that text summary plus metadata to the memory backend.
7. The backend is expected to generate/store the embedding for semantic recall.

So:

- Memory recall is embedding-backed.
- Memory storage is embedding-backed on the backend.
- The Unity client does **not** create embeddings locally.
- The current Unity code does **not** save the captured image as memory.

## End-to-End Runtime Flow

## 1. User Identity Is Established

When a user is detected, `MetaDynVoiceController.OnUserDetected(...)` builds a user ID and records the encounter:

- `displayName` comes from `Player.NetworkedName` if available
- `userId` is currently derived from the display name, for example `player_josh_garrett`

Code path:

- `MetaDynVoiceController.OnUserDetected(...)`
- `AIMemoryManager.RecordUserSeen(...)`
- `AIMemoryManager.PostUserSeen(...)`

What is sent to memory backend:

```json
POST /user/seen
{
  "user_id": "player_josh_garrett",
  "display_name": "Josh Garrett"
}
```

Purpose:

- mark the user as seen
- determine whether the user is new or returning
- prime memory context for the next interaction

## 2. Voice Input Becomes Text

If the user speaks through `MicrophoneRecorder`, the controller sends WAV data to Whisper:

Code path:

- `MetaDynVoiceController.ProcessVoiceInput(...)`
- `MetaDynVoiceController.TranscribeAudio(...)`

What happens:

- WAV bytes are posted to `https://api.openai.com/v1/audio/transcriptions`
- Whisper returns `response.text`
- that transcript becomes `userText`
- `ProcessUserMessage(userText)` is then called

This transcript is the actual text input used for memory recall and chat.

## 3. First Turn Memory Recall Uses Text Query

On the first turn of a conversation, the controller recalls relevant memories:

Code path:

- `MetaDynVoiceController.ProcessUserMessage(...)`
- `AIMemoryManager.RecallMemories(...)`
- `AIMemoryManager.PostRecallMemory(...)`

What Unity sends:

```json
POST /memory/recall
{
  "query": "<userText>",
  "user_id": "<currentUserId>",
  "limit": 5
}
```

Important detail:

- the recall query is the **transcribed or typed user text**
- Unity is not embedding the text itself
- the backend is expected to embed/query semantically

Returned data is cached into:

- `_lastRecall`
- `_currentMemoryContext`
- `_currentGreetingHint`

Then `GetMemoryContext()` and `GetUserGreetingHint()` format it for prompt injection.

## 4. Dynamic Context Is Injected Into The Live LLM Request

Before sending the chat request, `BuildChatJson(...)` injects:

- memory context from previous recall
- greeting hint
- fresh spatial/perception context from `GetCompactPerceptionContext()`

Code path:

- `MetaDynVoiceController.BuildChatJson(...)`

The injected dynamic context contains:

- memory hint such as new/returning user
- recalled memory snippets
- current spatial context like nearby users, seats, screens, and objects

Important detail:

- this context is **not stored in conversation history**
- it is only injected into the current request as a system message
- it is **not** what gets saved as memory later

## 5. Vision Flow Adds Image To The Live Chat Request Only

If the user message matches a vision keyword, the controller captures a snapshot:

Code path:

- `MetaDynVoiceController.IsVisionIntent(...)`
- `AIEye.CaptureSnapshotBytes(...)`
- `MetaDynVoiceController.ProcessUserMessage(...)`
- `MetaDynVoiceController.BuildChatJson(...)`

What happens:

1. User text is checked against `visionKeywords`
2. `AIEye` renders the scene camera to a JPG
3. JPG bytes are converted to Base64
4. The Base64 image is attached only to the last user message in OpenRouter content

The request shape becomes roughly:

```json
{
  "role": "user",
  "content": [
    { "type": "text", "text": "<userText>" },
    { "type": "image_url", "image_url": { "url": "data:image/jpeg;base64,..." } }
  ]
}
```

Important clarification:

- the image is **not** sent to `AIMemoryManager`
- the image is **not** stored as memory by Unity
- the image is **not** embedded by Unity
- the image is only used to improve the current multimodal LLM response

## 6. Conversation History Stored In Unity Is Text Only

The in-memory conversation history is maintained in `_conversationHistory`.

What gets stored there:

- system prompt
- user messages as text
- assistant messages as text

What does **not** get stored there:

- Base64 image payloads
- recalled memory blocks
- spatial context blocks

The image only exists during the live request construction for the final user message.

## 7. Memory Save Happens Later From A Text Summary

When the conversation closes, or auto-save triggers, the controller stores memory from a summary:

Code path:

- `MetaDynVoiceController.StoreConversationMemory()`
- `MetaDynVoiceController.StoreConversationWithAnalysis()`
- `AIMemoryManager.StoreConversation(...)`
- `AIMemoryManager.PostStoreConversation(...)`

Trigger paths:

- `OnCloseButtonClicked()`
- `OnPlayerLeft(...)`
- `AutoSaveMemoryRoutine()`

The controller builds a summary from the last few user/assistant messages:

- walks backward through `_conversationHistory`
- keeps up to 6 messages
- truncates each message to 100 chars
- creates plain text lines like:

```text
user: Where is the screen?
assistant: The main screen is ahead on your right.
user: Can you look at it?
assistant: I can see it now. It appears to be off.
```

Important detail:

- this is **text only**
- no raw spatial context is sent
- no raw image bytes are sent
- no full chat history is sent

## 8. Topics And Sentiment Are Extracted Before Saving

Before sending to memory backend, Unity asks OpenRouter to analyze the short conversation text:

Code path:

- `MetaDynVoiceController.StoreConversationWithAnalysis()`

Expected response format:

```json
{
  "topics": ["topic1", "topic2"],
  "sentiment": "positive"
}
```

The controller then flattens:

- `topics` into a comma-separated string
- `sentiment` into a single label

## 9. What Unity Actually Sends To Memory Storage

After analysis, Unity sends:

```json
POST /conversation/store
{
  "user_id": "<currentUserId>",
  "summary": "<conversationText>",
  "topics": "topic1, topic2",
  "sentiment": "positive",
  "location": "<scene name>"
}
```

From code, the stored payload includes:

- `user_id`
- `summary`
- `topics`
- `sentiment`
- `location`

It does **not** include:

- image bytes
- image embedding
- full prompt context
- recalled memory block
- spatial context string

## 10. Where Embeddings Actually Enter The Flow

According to the project docs and backend contract:

- `/memory/recall` is semantic recall
- `/memory/store` stores memory with embedding
- `/conversation/store` stores a conversation summary that the backend then embeds for later recall

This means the embedding work is expected on the backend, not in Unity.

Documented backend expectation:

- Vectorize performs semantic search
- summaries or memory content are embedded and stored there

## What Is And Is Not Saved As Memory

## Saved

- user encounter metadata via `/user/seen`
- conversation summary text
- topics
- sentiment
- location
- backend-managed semantic embedding of the summary/content

## Not Saved By Current Unity Code

- live Base64 snapshot image
- image embedding
- full dynamic prompt context
- full conversation transcript beyond the short summary sent to backend

## Practical Interpretation

If the user asks a vision question like:

`"Can you look at that sign?"`

the current flow is:

1. Whisper transcribes the audio to text
2. first-turn memory recall may run using that text
3. a snapshot is captured and sent to the LLM request
4. the assistant responds using memory + spatial context + image
5. later, Unity stores only a short text summary of the exchange, plus topics/sentiment/location
6. the backend embeds that summary for future semantic recall

So the memory system is currently **conversation-summary memory**, not **multimodal memory with stored image embeddings**.

## If You Need True Image Memory Later

That would require a different implementation than what exists now.

Current code would need additions such as:

- store captured snapshots in R2 or similar
- store image references with conversation records
- generate image or multimodal embeddings on the backend
- include those records in recall results

None of that is present in the current Unity implementation.
