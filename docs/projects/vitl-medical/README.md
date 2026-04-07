# VITL Medical

## Project snapshot

**Project:** VITL Medical  
**Type:** medical simulation / client platform experience  
**Status:** Active  
**Current focus:** Milestone 1 end-to-end learner loop for the infant UTI scenario

## Why it matters

VITL is shaping into a meaningful MetaDyn simulation product surface, not just a one-off chat demo. The work now spans:

- simulation-state management
- AI-driven character interaction
- model-backed communication scoring
- structured patient-history capture
- analytics/reporting architecture for future assessment use

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

- turn Milestone 1 into a concrete build checklist
- define the first implementation pass for `VITLPatientIntakeController` and `VITLPatientIntakeRecord`
- document the exact Activity 1 -> Activity 2 demo path as the primary proof sequence
- capture any real repo / scene / prefab specifics once we begin code-grounded implementation review

## Files in this project workspace

- `milestone-1-working-brief.md` — distilled working brief for the current milestone
- `reference/README.md` — imported/source-reference docs currently stored here
- `reference/2026-04-07-VITL-Activity-Design-Guide.md`
- `reference/2026-04-07-VITL-Activity2-History-Intake-Data-Flow.md`
