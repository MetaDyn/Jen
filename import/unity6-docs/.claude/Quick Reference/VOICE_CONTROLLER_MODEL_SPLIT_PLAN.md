# Voice Controller Model Split Plan

Planning notes for separating text chat, vision, and analysis model selection in `MetaDynVoiceController`.

**Status:** Planned | **Last Updated:** 2026-02-24

---

## Current Behavior (Confirmed)

`MetaDynVoiceController` currently uses a single OpenRouter model field (`openRouterModel`) for:

- Main chat LLM responses (text + optional vision payload)
- Vision-capable requests when an image is attached
- Conversation analysis for memory topics/sentiment extraction

### Implementation References

- Single model inspector field: `Assets/MetaDyn/AI/MetaDynVoiceController.cs:28`
- Main OpenRouter request uses `openRouterModel`: `Assets/MetaDyn/AI/MetaDynVoiceController.cs:635`
- Vision request is same chat payload with `image_url` content block: `Assets/MetaDyn/AI/MetaDynVoiceController.cs:1182`
- Memory analysis request also uses `openRouterModel`: `Assets/MetaDyn/AI/MetaDynVoiceController.cs:412`

---

## Why Split Models (Future Work)

Using one model for all tasks is simple, but it limits optimization:

- Chat may prefer a balanced/reliable model.
- Vision may require a model with strong multimodal support.
- Memory analysis can use a cheaper/faster structured-output model.

This also makes experimentation harder because changing one field affects all three paths.

---

## Proposed Design

Add separate inspector-configurable model fields with fallback behavior:

- `chatModel` (default current `openRouterModel` value)
- `visionModel` (fallback to `chatModel` if empty)
- `analysisModel` (fallback to `chatModel` if empty)

Optional migration compatibility:

- Keep `openRouterModel` temporarily as legacy field (hidden/deprecated), or migrate values in `OnValidate`/upgrade logic.

---

## Proposed Runtime Routing

- Text-only user message:
  - Use `chatModel`
- Vision-triggered user message (`base64Image != null`):
  - Use `visionModel` (fallback `chatModel`)
- Memory conversation analysis (`StoreConversationWithAnalysis()`):
  - Use `analysisModel` (fallback `chatModel`)

---

## Implementation Tasks (Later)

1. Add inspector fields for `chatModel`, `visionModel`, `analysisModel`.
2. Preserve backward compatibility for existing scenes/prefabs using `openRouterModel`.
3. Update `StreamOpenRouterResponse(...)` to select model based on whether image payload is present.
4. Update `StoreConversationWithAnalysis()` to use `analysisModel`.
5. Add debug logs that print which model path was selected (chat/vision/analysis).
6. Update `AI_EMBODIMENT.md` and any inspector/setup docs.
7. Test in Editor and WebGL.

---

## Open Questions

- Should analysis stay on OpenRouter/Gemini, or move to a cheaper JSON-friendly model?
- Do we want a separate fallback chain for vision if the selected model rejects image input?
- Should per-space runtime config override these model selections outside the inspector?

---

## Acceptance Criteria

- Text chat can use a different model than vision requests.
- Memory analysis can use a different model than chat/vision.
- Existing scenes do not break on upgrade.
- Behavior is documented in quick reference docs.
