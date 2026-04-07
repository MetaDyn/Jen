# VITL Activity 2 History Intake Data Flow

Design note for how the second VITL activity should operate when the learner asks the mother questions, receives answers through the AI conversation, and enters patient information into a dedicated UI.

**Scope:** Activity 2 only 
**Target Activity Pattern:** history-taking after greeting/rapport 
**Status:** planning/documentation only

## Related Docs

- [VITL_Example_Scenarios.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Example_Scenarios.md)
- [VITL_Activity_Design_Guide.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Activity_Design_Guide.md)
- [VITLSimulationManager_Function_Reference.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITLSimulationManager_Function_Reference.md)
- [VITL_Simulation_Voice_Routing_and_Testing_Guide.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Simulation_Voice_Routing_and_Testing_Guide.md)

## Source-Limited Intake Scope

Per the current VITL docs, the history-taking activity is asking for the following information only:

- symptom onset
- urine concerns
- fever history
- feeding changes
- diapers or wet diapers
- behavior

The example authored mother findings currently documented are:

- baby felt warm
- fussier than usual
- not feeding normally
- fewer wet diapers
- seems uncomfortable
- had a fever earlier

These items come from the existing authored examples and should define the initial structured intake scope for Activity 2. This document does not add any new clinical fields beyond those already described in the VITL docs.

## Activity 2 Goal

After the greeting activity completes, the simulation enters the history-taking activity. During this activity:

1. The learner asks the mother questions through the existing AI conversation flow.
2. The mother answers through `MetaDynVoiceController`.
3. The learner enters the gathered history into a dedicated patient-information UI.
4. The intake UI stores the learner-entered values as structured session data.
5. The simulation can use that structured intake state for completion checks, review, export, and analytics.

The important separation is:

- AI conversation remains the dialogue layer
- intake UI becomes the structured data-entry layer
- simulation manager remains the activity/state layer

## Recommended Storage Shape

The collected patient information for Activity 2 should be stored as runtime session data, not as a `ScriptableObject`.

Recommended split:

- `ScriptableObject`
 - use only for authored case definition or expected answers
 - this is static case content

- runtime serializable data class
 - use for the learner's collected patient information during the current simulation run
 - this is mutable session state

- manager or controller component
 - owns the runtime instance
 - updates it from the UI
 - exposes it to simulation logic and analytics

## Proposed Runtime Data Model

Activity 2 should maintain a single runtime intake record for the current simulation session.

Suggested field set based on the current docs:

- `symptomOnset`
- `urineConcerns`
- `feverHistory`
- `feedingChanges`
- `diaperHistory`
- `behaviorChanges`
- `freeformNotes`

Suggested metadata alongside those fields:

- `lastUpdatedUtc`
- `updatedByLearner`
- `sourceActivityIndex`
- `isComplete`
- `completionPercent`

This should be stored as a plain serializable runtime object owned by a MonoBehaviour or other session-state container.

## Recommended Ownership

Preferred ownership pattern:

- `VITLSimulationManager`
 - remains the source of truth for current activity state
 - knows when Activity 2 begins and ends

- new intake-specific controller
 - example role name: `VITLPatientIntakeController`
 - owns the structured runtime intake record
 - accepts UI field updates
 - can report completion state back to the simulation manager

This keeps the simulation manager from becoming overloaded with direct UI form responsibilities while still allowing it to coordinate the activity.

## Data Entry Flow

Recommended Activity 2 user flow:

1. Activity 2 starts.
2. `VITLSimulationManager` updates status text and begins the history-taking phase.
3. The learner asks questions through the existing AI chat or voice flow.
4. The mother responds in-character through `MetaDynVoiceController`.
5. The learner manually enters the discovered information into the patient-information UI.
6. Each UI field write updates the runtime intake record.
7. The intake controller can emit change events or update the simulation manager on completeness.
8. Once the minimum required intake fields are filled, the activity can be marked ready for completion.

This approach intentionally keeps structured storage based on learner-entered UI values, not inferred LLM output.

## Why Manual UI Entry Should Be The Source Of Truth

For Activity 2, the most defensible structured source of truth is the learner-entered UI, not automatic extraction from the AI conversation.

Reasons:

- it matches the training goal of collecting and documenting patient history
- it avoids uncertain parsing of freeform mother dialogue
- it makes learner performance auditable
- it supports review of what the learner believed they heard
- it creates cleaner analytics

The AI conversation can remain supporting evidence, but the intake form should be the canonical structured record.

## Relationship To Existing Learner Turn Storage

Current `VITLSimulationManager` behavior already stores learner turns in `LearnerTurnRecord` and exposes them via `GetLearnerTurnHistory()`.

That existing storage should remain, but it should be treated as conversation history, not structured patient intake.

Recommended distinction:

- `LearnerTurnRecord`
 - stores what the learner said
 - useful for communication review and scoring

- intake record
 - stores what the learner documented about the patient
 - useful for clinical information capture and completion logic

Both are useful and should coexist.

## Completion Logic Options

There are several valid ways Activity 2 could determine completion.

### Option A: Required Fields Complete

Mark the activity complete when the required intake fields are non-empty.

Example rule:

- symptom onset entered
- fever history entered
- feeding changes entered
- diaper history entered

Pros:

- simple
- deterministic
- easy to QA

Cons:

- checks completion, not correctness

### Option B: Required Fields Plus Learner Confirmation

Require the fields plus a learner action such as `Submit Intake` or `Confirm History`.

Pros:

- better training ritual
- clearer UX boundary

Cons:

- adds one more interaction step

### Option C: Field Completeness Plus Comparison To Authored Case Truth

Compare the learner-entered intake record against the authored scenario facts stored in a case-definition asset.

Pros:

- supports assessment
- supports scoring analytics

Cons:

- more implementation work
- requires authoritative case-answer definitions

Recommended initial path:

- start with Option B
- add Option C later when formal assessment scoring is ready

## Analytics Integration Options

The project already has a working analytics path through `MetaDyn.UmamiAnalytics.TrackEvent(...)`, and the current scene already uses simple simulation-manager UnityEvents for:

- simulation started
- simulation ended
- activity started
- activity completed

That same pattern should be used for Activity 2 intake analytics.

### Option 1: Reuse Current UnityEvent Wiring

Add new UnityEvents on the intake controller or simulation manager for:

- intake field updated
- intake section completed
- intake submitted
- intake corrected

These can be wired in the scene to `UmamiAnalytics.TrackEvent(string)`.

Pros:

- matches the current project pattern
- low code complexity

Cons:

- string-only events do not carry rich structured payloads

Good for:

- milestone-only tracking

### Option 2: Add Typed Analytics Calls In Code

Call `UmamiAnalytics.TrackEvent(string, Dictionary<string, object>)` directly from the intake controller when key actions happen.

Example event payload shapes:

- `vitl_history_field_updated`
 - `activity_name`
 - `field_name`
 - `has_value`
 - `character_count`

- `vitl_history_section_completed`
 - `activity_name`
 - `completed_fields`
 - `required_fields`
 - `completion_percent`

- `vitl_history_submitted`
 - `activity_name`
 - `completion_percent`
 - `time_in_activity_s`

- `vitl_history_corrected`
 - `field_name`
 - `edit_count`

Pros:

- supports richer analysis
- better for dashboards later

Cons:

- requires explicit code integration

Good for:

- production analytics and learning insight

### Option 3: Hybrid Pattern

Use:

- UnityEvents for broad milestone events
- direct code analytics for structured field-level data

This is the recommended pattern.

## Analytics Privacy Boundary

If analytics are sent for Activity 2, avoid sending full freeform clinical text by default.

Recommended analytics payload style:

- send field names
- send completion state
- send whether data exists
- send time-to-complete
- send count of edits
- send whether submission occurred

Avoid sending:

- raw freeform note text
- full mother response text
- full learner-entered narrative text

If later analytics need deeper content review, that should be an explicit product decision rather than the default behavior.

## Recommended System Breakdown

Recommended implementation shape for Activity 2:

- `VITLSimulationManager`
 - starts and governs Activity 2
 - receives completion readiness from intake controller
 - keeps current conversation-scoring behavior

- `VITLPatientIntakeController`
 - owns the runtime intake record
 - exposes setters for each intake field
 - tracks completeness
 - raises analytics and status events

- `VITLPatientIntakeRecord`
 - serializable runtime data container
 - no MonoBehaviour responsibilities

- optional `VITLCaseDefinition` ScriptableObject
 - stores authored expected patient-history truth for the case
 - useful later for assessment comparison

## Recommended First Implementation Boundary

For the first pass of Activity 2, the system should do only this:

- allow learner-entered structured history fields
- store them in a runtime intake record
- expose completion percentage
- allow a final submit or confirm action
- emit analytics-safe milestone events

It should not yet:

- auto-extract structured data from mother dialogue
- rely on LLM parsing for clinical field storage
- send raw intake text to analytics by default

## Summary

Activity 2 should be implemented as a structured history-intake phase layered on top of the existing AI conversation.

Recommended architecture:

- learner asks the mother questions through the current AI system
- learner documents findings in a dedicated UI
- the UI writes to a runtime intake record
- the intake record becomes the authoritative structured patient-information store for the session
- analytics should reuse the current Umami event pattern, with a hybrid model for richer field-level telemetry when needed

The key rule is simple:

- conversation history is not the same thing as structured patient history
- Activity 2 needs both
