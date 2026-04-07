# VITL Medical — Milestone 1 Working Brief

**Status:** active working brief  
**Last updated:** 2026-04-07

## Milestone objective

Milestone 1 should prove an end-to-end learner loop for the infant UTI case:

1. learner starts the simulation
2. mother opens with concern
3. learner responds by text or voice
4. learner input is routed through `VITLSimulationManager`
5. communication is scored with the model-backed scoring service
6. simulation state is updated before the mother responds
7. Activity 1 can complete through authored thresholds
8. Activity 2 begins as a structured patient-history capture phase

## Current milestone definition

The first meaningful VITL milestone is not "full clinical grading."
It is a coherent mini-simulation that proves:

- simulation-aware voice routing works
- model-backed communication scoring works
- scenario progression works
- the mother response reflects updated simulation state
- Activity 2 has a real structured intake path
- conversation history and documented patient history are kept separate

## Confirmed current system shape

### Core runtime roles

- `MetaDynVoiceController`
  - front-end AI delivery layer
  - handles text input, Whisper transcription, LLM requests, TTS, hidden prompt delivery

- `VITLSimulationManager`
  - scenario-state authority
  - owns lifecycle, activities, timers, escalation, scoring hooks, learner history, and hidden simulation overlay

- `VITLCommunicationScoringService`
  - model-backed learner communication scoring through OpenRouter
  - returns numeric scores used by the simulation manager for progression checks

### Input flow

When a simulation is active:

1. learner types or speaks
2. `MetaDynVoiceController` routes input to `VITLSimulationManager`
3. the manager stores the learner turn
4. scoring runs
5. emotional / baby state hooks update
6. simulation overlay is refreshed
7. activity progression is evaluated
8. learner text is sent back into the voice controller
9. the mother responds using updated simulation context

That ordering is an important strength of the current design.

## Current case focus

The active case is a pediatric infant UTI encounter involving communication with the infant's concerned mother.

### Activity 1

Greeting / rapport activity.

Learner should:
- introduce themselves
- acknowledge concern
- explain they will help assess the baby
- communicate calmly and clearly

### Activity 2

History-taking activity.

Current structured field scope:
- symptom onset
- urine concerns
- fever history
- feeding changes
- diaper history
- behavior changes
- freeform notes

## Key product / system decisions already visible in the docs

### 1. Conversation history is not the source of truth for patient history

The learner-entered intake UI should be the canonical structured patient-history record.

Conversation history remains useful for:
- communication review
- scoring context
- audit of what the learner asked or said

But the structured intake form is what should drive documented history state.

### 2. `VITLSimulationManager` should remain the authority for progression

The model can score the learner, but progression should still be decided by authored threshold rules inside the simulation manager.

### 3. Activity 2 should use explicit runtime session state

Recommended split:
- static authored truth in config/assets if needed later
- mutable learner-entered intake record for the current session
- dedicated intake controller for UI writes and completeness tracking

### 4. Model-backed scoring is primary, fallback scoring is resilience

The project should treat OpenRouter-backed scoring as the intended path, while keeping heuristic/default fallback so testing does not hard-fail.

### 5. Structured payloads are a future-facing architecture improvement, not Milestone 1 scope creep

The event layer is currently string-heavy.
The docs point toward a staged migration to structured payloads for analytics, reporting, and assessment, starting with learner input, activity events, score payloads, and history intake.

## Milestone 1 in-scope items

- greeting / rapport flow
- model-backed communication scoring
- threshold-based activity completion
- simulation-aware mother response after scoring
- Activity 2 structured intake UI / record pattern
- analytics-safe milestone events where practical

## Explicitly out of scope for Milestone 1

- automatic extraction of structured history from AI dialogue
- full correctness scoring against case truth
- full reporting/export system
- full string-event replacement everywhere
- complex branching cases beyond the first Activity 1 -> Activity 2 path

## Recommended next implementation sequence

1. lock the Activity 1 -> Activity 2 path as the first canonical demo flow
2. build `VITLPatientIntakeRecord` as runtime session data
3. build `VITLPatientIntakeController` as the UI/data owner for Activity 2
4. implement required-fields + learner-confirmation completion behavior
5. add analytics-safe intake milestone events
6. defer correctness comparison and richer assessment until the first loop feels solid

## Useful test examples

### Strong greeting
`Hi, I'm your nurse. I can see you're worried, and I'm going to help check on your baby and explain each step as we go.`

### Weak greeting
`Calm down. Babies get sick. Just wait over there.`

### Useful Activity 2 questions
- When did you first notice the fever or that something was wrong?
- Has your baby been feeding normally today?
- Have there been fewer wet diapers than usual?
- Has your baby seemed more fussy or uncomfortable?
- Have you noticed anything different about the urine or diapers?

## Main risk to avoid

The main architecture risk is blurring together:
- learner conversation
- learner scoring
- simulation state
- patient-history documentation

The docs are strongest when they keep those as separate layers with clear ownership.
