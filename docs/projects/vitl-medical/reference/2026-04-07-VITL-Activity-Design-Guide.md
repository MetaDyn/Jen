# VITL Activity Design Guide

Designer-facing guide for building and tuning `VITLSimulationManager` activities in the Unity Inspector.

**Audience:** simulation designers, instructional designers, QA testers 
**Primary File:** [VITLSimulationManager.cs](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/Assets/VITL_Assets/Scripts/VITLSimulationManager.cs)

## Related Docs

- [VITLSimulationManager_Function_Reference.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITLSimulationManager_Function_Reference.md)
- [VITL_Simulation_Voice_Routing_and_Testing_Guide.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Simulation_Voice_Routing_and_Testing_Guide.md)
- [VITL_Example_Scenarios.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Example_Scenarios.md)

## Purpose

This guide explains how to create activities for the VITL simulation without needing to understand the code implementation in detail.

It covers:

- what an activity is
- how activities progress
- what each inspector field means
- how to make a simple starter activity
- how to design good prompts
- how to use scoring thresholds
- how to use inactivity escalation
- recommended patterns for common activity types

## What an Activity Is

An activity is one phase of the simulation.

Examples:

- greeting and rapport building
- history taking
- physical exam explanation
- procedure explanation
- discharge and follow-up education

The `VITLSimulationManager` runs activities in order from top to bottom in the `activities` list.

For each activity, the manager can:

- start the phase
- optionally send an opening hidden prompt to the mother AI
- wait for learner input
- score the learner's communication
- escalate if the learner is delayed or ineffective
- complete, fail, or move on

## How Activity Progression Works

At a high level:

1. simulation starts
2. first activity becomes active
3. the mother receives any configured opening prompt
4. learner responds by text or voice
5. learner response is scored
6. if thresholds are met and the activity allows it, the activity completes
7. the manager advances to the next activity
8. after the last activity, the simulation ends

An activity can also:

- auto-complete after a timer
- fail after a timer
- escalate concern if the learner does not respond
- fail at the third escalation if configured

## Inspector Fields

Each activity is an `ActivityDefinition` in the `activities` list.

### Identity

#### `activityName`

Human-readable activity name.

Use clear labels such as:

- `Greeting and Rapport`
- `History Intake`
- `Explain Urine Collection`

#### `activityGoal`

Short description of what the learner is supposed to accomplish in this phase.

This should describe the instructional outcome, not the mother's line.

Good examples:

- `Learner introduces self and reassures the mother.`
- `Learner gathers symptom history and addresses the mother’s concern.`
- `Learner explains the catheterized urine sample in calm, understandable language.`

#### `designerNotes`

Optional internal notes for your team.

Use this for:

- author intent
- special scoring considerations
- assumptions about learner behavior
- reminders for future revisions

The AI does not use this field directly.

### Activity Type

#### `activityType`

This labels the phase category and is sent to external systems such as emotion and baby-state controllers.

Available values:

- `Onboarding`
- `History`
- `PhysicalExam`
- `Diagnostics`
- `ProcedureExplanation`
- `ProcedureExecution`
- `ResultsAndDischarge`

Choose the closest instructional phase, even if the label is approximate.

## Flow Settings

### `maxDurationSeconds`

Maximum time allowed for the activity.

What it does:

- if time runs out and `autoCompleteOnTimer` is true, the activity completes automatically
- if time runs out and `autoCompleteOnTimer` is false, the activity fails

Recommended ranges:

- smoke test: `5-15`
- greeting phase: `60-120`
- history/explanation phases: `120-300`

### `autoCompleteOnTimer`

If enabled, the activity completes when the timer expires.

Use this for:

- passive demo phases
- smoke tests
- non-evaluated pacing moments

Avoid this for:

- learner communication checkpoints
- empathy-based evaluation phases

### `failEndsSimulation`

If enabled, failing this activity fails the full simulation.

Use this for:

- critical safety communication moments
- required core objectives

Leave off for:

- practice-friendly early phases
- non-critical communication misses

### `requiresLearnerResponse`

If enabled, the system expects a learner response during this activity.

What it affects:

- inactivity timer runs
- inactivity escalation can trigger
- progression logic expects learner participation

Set this to `false` for:

- auto-play moments
- setup beats
- scripted transitions

### `completeAfterValidLearnerResponse`

If enabled, the activity completes automatically once the learner's scored response meets the configured thresholds.

This is the most common setting for communication activities.

Use this for:

- greeting
- empathy checks
- explanation tasks
- education/discharge tasks

## Scoring Thresholds

These fields define the minimum score required for the learner to "pass" the activity.

### `minimumPassingScore`

Minimum overall score required.

### `minimumEmpathyScore`

Minimum empathy score required.

### `minimumClarityScore`

Minimum clarity score required.

### How thresholds work

The manager treats the learner response as passing only if all of these are true:

- `overallScore >= minimumPassingScore`
- `empathyScore >= minimumEmpathyScore`
- `clarityScore >= minimumClarityScore`

If that passes and `completeAfterValidLearnerResponse` is enabled, the activity completes.

### Practical threshold guidance

For early testing:

- `minimumPassingScore = 3`
- `minimumEmpathyScore = 3`
- `minimumClarityScore = 2`

For stricter empathy-driven activities:

- `minimumPassingScore = 4`
- `minimumEmpathyScore = 4`
- `minimumClarityScore = 3`

For explanation-heavy tasks:

- `minimumPassingScore = 4`
- `minimumEmpathyScore = 3`
- `minimumClarityScore = 4`

## Mom Prompt Fields

### `initialMomPrompt`

Hidden prompt sent when the activity starts.

Use it to set the mother's immediate behavior and opening line.

Best use:

- define the emotional tone
- state the immediate concern
- tell the AI what to say first

Good examples:

- `The mother looks worried and says, "Hi... I'm really worried about my baby."`
- `The mother asks what is happening and why the baby has a fever.`
- `The mother hesitates and asks whether the procedure will hurt.`

### `completionMomPrompt`

Hidden prompt sent when the activity completes.

Use it to show the mother's reaction to a successful learner response.

Good examples:

- `The mother relaxes slightly and says, "Okay... thank you."`
- `The mother becomes more cooperative and agrees to continue.`
- `The mother nods and says she understands the explanation better now.`

## Inactivity Escalation

Inactivity escalation is how the mother becomes more concerned if the learner does not respond in time.

### `enableInactivityEscalation`

Turns escalation on or off for the activity.

### `firstEscalationSeconds`

Time in seconds before the first escalation fires.

### `secondEscalationSeconds`

Time in seconds before the second escalation fires.

### `thirdEscalationSeconds`

Time in seconds before the third escalation fires.

### `thirdEscalationFailsActivity`

If enabled, reaching the third escalation fails the activity.

### Escalation prompts

Fields:

- `firstEscalationPrompt`
- `secondEscalationPrompt`
- `thirdEscalationPrompt`

These are hidden prompts sent to the mother AI when escalation occurs.

Good escalation pattern:

- first: concern
- second: frustration or distress
- third: protective or interfering behavior

Example progression:

- first: `The mother becomes more concerned and asks what is happening.`
- second: `The mother becomes upset and says the learner is not listening.`
- third: `The mother moves protectively toward the baby and threatens to leave. *walk_to:baby*`

## How to Write Good Prompts

Prompts should be:

- short
- specific
- behavior-focused
- in-character

Avoid:

- long paragraphs
- clinical rubric language
- internal state labels like `score = 2`
- instructions that conflict with the activity goal

### Good prompt pattern

Use this structure:

- emotional state
- what the mother wants or fears
- what she says or does

Example:

`The mother is worried and needs reassurance. She says, "Can you please tell me what's going on with my baby?"`

### Use movement sparingly

Movement tags can be used in prompts if appropriate:

- `*walk_to:baby*`
- `*stop_walking*`

Use them only when movement meaningfully supports the scene.

## Recommended Starter Activity

Use this activity to verify the system is working end-to-end:

- `activityName`: `Greeting Test`
- `activityType`: `Onboarding`
- `activityGoal`: `Learner introduces self and reassures mother`
- `maxDurationSeconds`: `120`
- `autoCompleteOnTimer`: `false`
- `failEndsSimulation`: `false`
- `requiresLearnerResponse`: `true`
- `completeAfterValidLearnerResponse`: `true`
- `minimumPassingScore`: `3`
- `minimumEmpathyScore`: `3`
- `minimumClarityScore`: `2`
- `initialMomPrompt`: `The mother looks worried and says, "Hi... I'm really worried about my baby."`
- `completionMomPrompt`: `The mother looks a little calmer and says, "Okay... thank you."`
- `enableInactivityEscalation`: `false`

Why this is a good first activity:

- fast to configure
- easy to test by text or voice
- clearly shows start and completion
- does not require complex branching

This starter test is the same one used in [VITL_Simulation_Voice_Routing_and_Testing_Guide.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Simulation_Voice_Routing_and_Testing_Guide.md). For richer authored sequences, see [VITL_Example_Scenarios.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Example_Scenarios.md).

## Recommended Smoke Test Activity

Use this when you only want to test lifecycle behavior:

- `activityName`: `Auto Complete Test`
- `activityType`: `Onboarding`
- `activityGoal`: `Verify start and completion flow`
- `maxDurationSeconds`: `5`
- `autoCompleteOnTimer`: `true`
- `failEndsSimulation`: `false`
- `requiresLearnerResponse`: `false`
- `completeAfterValidLearnerResponse`: `false`
- `enableInactivityEscalation`: `false`

This verifies:

- simulation start
- activity start
- timer update
- completion
- simulation end

without learner input.

## Suggested Design Patterns by Phase

### Greeting / Rapport

Recommended:

- `activityType = Onboarding`
- medium empathy threshold
- modest clarity threshold
- completion after valid learner response
- no escalation or very gentle escalation

Goal:

- build trust
- establish role
- calm the mother

### History Taking

Recommended:

- `activityType = History`
- moderate empathy threshold
- moderate clarity threshold
- learner response required
- escalation enabled if silence should create pressure

Goal:

- elicit symptoms and timeline
- maintain trust

### Procedure Explanation

Recommended:

- `activityType = ProcedureExplanation`
- higher clarity threshold
- medium empathy threshold
- completion after valid learner response

Goal:

- explain what will happen
- reduce fear
- gain cooperation

### Procedure Execution

Recommended:

- `activityType = ProcedureExecution`
- stronger escalation options
- consider `failEndsSimulation` for critical breakdowns

Goal:

- handle distress
- maintain control and safety

### Discharge / Results

Recommended:

- `activityType = ResultsAndDischarge`
- moderate empathy and clarity thresholds
- completion after valid learner response

Goal:

- confirm understanding
- ensure reassurance and clarity

## Designer Checklist

Before testing an activity:

- activity has a clear `activityName`
- activity has a meaningful `activityGoal`
- `activityType` is appropriate
- timing values are intentional
- completion behavior is intentional
- thresholds are realistic
- `initialMomPrompt` is present if the mother should open the phase
- escalation is either configured carefully or disabled
- the activity order in the list is correct

## QA Checklist

When testing a new activity, verify:

- simulation starts correctly
- correct activity becomes active
- initial mother prompt is delivered
- learner text input works
- learner voice input works
- the mother responds in character
- completion happens when expected
- escalation happens when expected
- the next activity starts correctly
- final activity ends the simulation correctly

## Common Mistakes

### Thresholds too strict

Symptom:

- learner gives a reasonable response but the activity never completes

Fix:

- lower `minimumPassingScore`
- lower empathy or clarity thresholds

### No learner response expected when one is needed

Symptom:

- activity never escalates and may feel passive

Fix:

- enable `requiresLearnerResponse`

### Completion never happens

Symptom:

- learner responds, but phase stays active

Check:

- `completeAfterValidLearnerResponse`
- scoring thresholds
- scoring service behavior

### Escalation too aggressive

Symptom:

- mother becomes distressed too fast

Fix:

- raise escalation timers
- soften escalation prompts
- disable third-fails-activity for early phases

## Authoring Philosophy

Good activities are:

- focused on one communication objective
- short enough to test easily
- emotionally coherent
- strict only where training value requires it

It is better to build several simple activities with clear goals than one overloaded activity trying to cover too much at once.

## Related Docs

- [VITL_Simulation_Voice_Routing_and_Testing_Guide.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Simulation_Voice_Routing_and_Testing_Guide.md)
- [VITLSimulationManager_Function_Reference.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITLSimulationManager_Function_Reference.md)
- [VITL_Example_Scenarios.md](/mnt/c/Metaverse/MetaDyn/Projects/VITL-Medical/VITL-Medical/.claude/Planning/VITL/VITL_Example_Scenarios.md)
