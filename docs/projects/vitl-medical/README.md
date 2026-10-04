# VITL Medical

## Project snapshot

**Project:** VITL Medical  
**Type:** medical simulation / client platform experience  
**Status:** Active  
**Current focus:** Milestone 1 learner loop and pilot PIN analytics/reporting

## Why it matters

VITL is shaping into a meaningful MetaDyn simulation product surface, not just a one-off chat demo. The work now spans:

- simulation-state management
- AI-driven character interaction
- model-backed communication scoring
- structured patient-history capture
- analytics/reporting architecture for future assessment use

## Pilot analytics and reporting update (2026-10-04)

- Unity C# now carries the accepted PIN through session context and adds `pin_code` to the access-granted event and later Umami events. The existing `simulation_started` event is expected to carry that field when it fires after access. Unity does not perform PIN lookup. Source: `VITL-Medical/Assets/MetaDyn/Core/Runtime/Components/Access/MetaDynAccessPanel.cs`, `MetaDynSessionContext.cs`, and `Assets/MetaDyn/Analytics/UmamiAnalytics.cs`.
- The separate, private [VITL-Reporting React repository](https://github.com/MetaDyn/VITL-Reporting) is at commit [`164224a`](https://github.com/MetaDyn/VITL-Reporting/commit/164224a). Its PIN-only page calls the existing Umami site directly, lists matching custom `session_id` values, and opens chronological event reports. It has no separate API host or Netlify Function.
- The dedicated read-only `vitl` Umami account was added to the MetaDyn team holding the website. The reporting app's `VITE_` credential settings are embedded in its static browser build; the project owner accepted that exposure for this account. Do not copy credentials into these docs.
- The project owner reported a successful Netlify build and a visible PIN form over HTTPS. A live PIN lookup and event report are **not yet verified**. The updated Unity code has not been built or deployed as part of this update; a new PIN-gated Unity session is needed to produce lookup data.
- The companion [VITL-Web repository](https://github.com/MetaDyn/VITL-Web) updated the welcome and movement video embeds in commit [`b1eb781`](https://github.com/MetaDyn/VITL-Web/commit/b1eb781).

**Next:** After the project owner deploys the Unity update and records a new session, look up its PIN in VITL-Reporting and confirm the expected events appear in time order. The Unity project remains authoritative for implementation state. Local handoff: `VITL-Medical/.claude/SESSION_HANDOFF.md`.

## Current understanding

VITL is a Unity-based medical simulation where a learner interacts with the mother of an infant patient in a pediatric UTI scenario.

The system is no longer just "talk to an AI mom." It has three distinct layers:

- **AI delivery layer** via `MetaDynVoiceController`
- **simulation-state layer** via `VITLSimulationManager`
- **assessment / intake layer** via communication scoring plus the planned structured patient-history flow

The near-term goal is to validate a coherent first milestone where:

1. the mother opens with concern
2. the learner responds by text or voice
3. the learner response is scored using a model-backed rubric
4. the simulation updates state before the mother responds
5. Activity 1 completes through thresholds when appropriate
6. Activity 2 begins and captures structured patient history through learner-entered UI

## Active threads

- Milestone 1 end-to-end learner flow
- simulation-aware voice routing and testing
- model-backed communication scoring through OpenRouter
- Activity 2 structured patient-history intake architecture
- event / analytics transition from string-heavy events to more structured payloads
- authoring patterns for activities and example scenarios

## Confirmed current state from uploaded docs

- simulation-aware routing between `MetaDynVoiceController` and `VITLSimulationManager` has already been implemented and manually validated
- the project compiled after scorer assignment
- the scoring service, voice controller, and OpenRouter/LLM key were assigned for manual testing
- fallback scoring exists so scoring failures do not hard-stop the simulation
- the first milestone is intentionally focused on greeting, communication scoring, and Activity 2 history intake
- Activity 2 should use learner-entered structured form data as the authoritative patient-history record
- the docs explicitly separate conversation history from documented patient history

## Core architecture

### `MetaDynVoiceController`
Owns:
- text input
- voice transcription
- LLM request / response flow
- TTS output
- hidden prompt delivery

### `VITLSimulationManager`
Owns:
- simulation lifecycle
- activity progression
- timers
- inactivity escalation
- learner turn storage
- score integration
- mother / baby state hooks
- hidden simulation overlay applied before response generation

### `VITLCommunicationScoringService`
Owns:
- OpenRouter-backed scoring requests
- rubric-driven score output
- high/low reference examples
- JSON parsing and clamping
- heuristic/default fallback behavior

### Planned Activity 2 intake layer
Likely shape:
- `VITLPatientIntakeRecord`
- `VITLPatientIntakeController`
- later optional case-definition asset for authored truth comparison

## Key decisions now visible in the docs

- **The simulation manager remains the authority.** Model scoring informs progression, but authored thresholds in `VITLSimulationManager` decide completion.
- **Conversation history and patient-history intake are different things.** The learner-entered intake UI should be the structured source of truth.
- **Activity 2 should start simple.** Required fields + learner confirmation first; correctness comparison later.
- **Fallback scoring is a resilience tool, not the desired long-term assessment layer.**
- **Structured payload migration should happen gradually.** Add structured runtime payloads alongside existing string events rather than forcing a risky rewrite.

## In-scope milestone boundary

Milestone 1 should prove:
- greeting / rapport flow
- model-backed scoring
- threshold-based activity progression
- simulation-aware mother response
- Activity 2 patient-history capture as a distinct structured flow

Milestone 1 should not try to prove:
- full automated clinical grading
- auto-extracted patient history from LLM dialogue
- full review/export/reporting stack
- broad event-system rewrite

## Recommended next actions

- Deploy the updated Unity C# analytics code through the project's normal Unity workflow, then record a new PIN-gated session.
- In VITL-Reporting, use that PIN to confirm the session list and chronological events, including `simulation_started` when recorded. Treat this as pending until observed.
- Continue the Milestone 1 learner-loop and structured-intake work according to the Unity project's current plans.

## Files in this project workspace

- `milestone-1-working-brief.md` — distilled working brief for the current milestone
- `reference/README.md` — imported/source-reference docs currently stored here
- `reference/2026-04-07-VITL-Activity-Design-Guide.md`
- `reference/2026-04-07-VITL-Activity2-History-Intake-Data-Flow.md`
