# Discord Community Manager Rollout Plan

Last updated: 2026-03-20

## Purpose

This document defines how MetaDyn should integrate OpenClaw with Discord so a Community Manager agent can help operate the community safely and effectively.

The goal is not to turn the bot into an autonomous moderator on day one.

The goal is to make it a disciplined community operations assistant that can:

- welcome and route people cleanly
- answer repeat questions from approved source material
- create polls and engagement prompts
- summarize community feedback and recurring questions
- help staff keep Discord active, useful, and on-brand

## Recommended Operating Posture

Start narrow.

The Community Manager agent should begin as a **staff co-pilot with limited public actions**, then expand into broader participation only after it proves reliable.

Recommended initial posture:

- active in one staff/test channel
- active in one onboarding/help surface
- active in one public general/community channel
- no autonomous moderation decisions
- no autonomous role changes
- no autonomous policy statements
- no autonomous handling of sensitive incidents

This matches the current cautious Discord configuration and is the safest way to build trust.

## What Discord Should Be Used For First

High-value, low-risk first capabilities:

- reading channel history for context
- replying when mentioned or explicitly invoked
- creating polls
- reacting to messages
- searching prior discussions
- posting reminders or scheduled prompts
- drafting or posting welcome messages
- creating support/follow-up threads
- producing weekly summaries of community activity and feedback

These capabilities are enough to make the Community Manager genuinely useful without overexposing the system early.

## Phased Rollout

### Phase 0 — Controlled Sandbox

Objective: validate behavior in a staff-only or test channel before broader use.

Enable:

- read
- send
- react
- search
- poll
- thread creation

Operating rules:

- keep `requireMention: true`
- keep allowlist restricted to staff
- test prompts, summaries, polls, onboarding drafts, and FAQ replies
- collect examples of good and bad responses
- define source-of-truth docs before letting it answer more freely

Success criteria:

- replies are accurate and on-brand
- no hallucinated claims about roadmap, pricing, or policy
- summaries are useful
- poll and thread workflows work reliably

### Phase 1 — Staff Co-Pilot

Objective: make the agent useful to staff without yet acting like a full public-facing operator.

Expand usage to:

- drafting announcements
- summarizing feedback from public channels
- preparing welcome messages for staff review
- generating suggested responses to common community questions
- producing weekly reports: sentiment, repeated asks, bugs, feature requests, and activation signals

Operating rules:

- public posting still mostly mention-triggered or staff-initiated
- no direct moderation decisions
- no unsolicited DMs
- no role/channel changes

Success criteria:

- staff save time every week
- community summaries are consistent enough to use operationally
- staff trust the agent’s tone and judgment in low-risk contexts

### Phase 2 — Limited Public Operations

Objective: allow the agent to participate in a few defined public workflows.

Recommended new behaviors:

- greet first-time posters in specific channels
- answer narrow FAQ questions from approved docs
- create polls for engagement or lightweight research
- route people toward beta, feedback, showcase, or help channels
- spin up threads for support or deep-dive questions
- post weekly recap summaries in a designated updates/community thread

Operating rules:

- remove `requireMention` only in approved channels
- keep public participation scoped by channel policy
- restrict autonomous replies to approved workflow categories
- use escalation rules when confidence is low or the topic is sensitive

Success criteria:

- agent participation feels helpful, not spammy
- public replies stay accurate and concise
- community members start using the bot as a utility, not a novelty

### Phase 3 — Trusted Automation

Objective: expand automation after sustained proof.

Possible additions:

- proactive onboarding nudges in approved channels
- event reminders and RSVP prompts
- routine recap posts
- automated “you said / we’re doing” summaries sourced from staff-approved notes
- lightweight triage/routing for recurring questions and support themes

Still keep human-owned:

- disciplinary actions
- conflict mediation
- public statements during incidents
- partnerships, legal, pricing, or contractual claims
- major policy changes or enforcement interpretations

## Safe Autonomous Behaviors vs Human-Approved Behaviors

### Safe to automate early

These are the best first autonomous behaviors:

- welcome reply to first-time posters in approved channels
- simple routing: where to ask for help, where to give feedback, where to find updates
- poll creation from staff-supplied questions or standard templates
- FAQ replies grounded in approved docs
- weekly activity summaries
- event reminder posts based on approved event details
- thread creation for support or follow-up
- simple emoji reactions for acknowledgment

### Human-approved before posting

These should usually be drafted first, then approved by a human:

- announcements
- partnership references
- product roadmap statements
- beta invitations with expectations or promises
- any message that could be interpreted as policy or commitment
- community recaps that include interpretation, attribution, or strategy
- outreach that feels personal or high-stakes

### Human-only

Do not automate these without explicit approval and a later governance decision:

- bans, kicks, timeouts, warnings, or moderation judgments
- role grants/removals tied to trust, access, or status
- staff or founder voice impersonation
- conflict resolution between members
- responses involving harassment, safety, legal, payment, or account disputes
- creation/deletion of channels or major permission changes

## Recommended Discord Capabilities To Enable First

Prioritize these in order:

1. channel read access in approved channels
2. send messages in approved channels
3. reactions
4. polls
5. search/history access
6. thread creation/reply
7. member and role lookup for context only

Delay until later unless clearly needed:

- broad passive monitoring across all channels
- moderation powers
- role management
- channel management
- presence customization
- voice/Stage/event automation beyond simple reminders

### Suggested channel rollout

Start with:

- one internal ops/test channel
- one public `general`-style channel
- one `help` or `questions` channel
- one `beta-feedback` or equivalent feedback channel

That is enough surface area to test real workflows without turning the bot loose everywhere.

## Core Risks

### 1. Over-participation

Risk:
The bot talks too much, inserts itself into normal member conversation, or makes the community feel synthetic.

Guardrails:

- channel allowlist
- reply only in defined workflow cases
- rate limits on autonomous posting
- prefer one good response over repeated interjections

### 2. Hallucinated or overconfident answers

Risk:
The agent states product details, roadmap, policy, or support answers that are not grounded.

Guardrails:

- approved source documents only
- instruct the agent to say when it is unsure
- force escalation for unsupported claims
- review answer quality during sandbox and co-pilot phases

### 3. Accidental authority inflation

Risk:
Members assume the bot can make official commitments.

Guardrails:

- clear voice rules
- avoid speaking as “the company” on sensitive topics
- use drafts for anything strategic, commercial, or policy-related
- escalate when the answer could create expectations

### 4. Moderation mistakes

Risk:
The bot misreads tone, sarcasm, conflict, or community norms.

Guardrails:

- no autonomous moderation early
- route suspected problems to staff
- define explicit incident escalation language

### 5. Onboarding noise or spam

Risk:
Welcome flows become repetitive, robotic, or annoying.

Guardrails:

- one lightweight greeting per new participant max
- prefer first-post welcome over immediate server-join spam at first
- keep messages short and directional

## Example Operating Workflows

### 1. Polls

Use case:
Quick sentiment checks, feature prioritization, event timing, and lightweight engagement.

Workflow:

- staff provides a question or selects a template
- agent creates a Discord poll in the approved channel
- after close, agent summarizes results and key takeaways
- if the poll affects planning, summary goes to staff/internal ops channel too

Good first examples:

- which feature should we demo next
- best day/time for a live session
- what topic should next week’s update focus on

### 2. Onboarding

Use case:
Help new members understand where to go and what to do.

Workflow:

- member posts in `general` or `help`
- agent replies with a short welcome and one clear next step
- if relevant, agent links them to beta, showcase, support, or updates channels
- if the question is deeper, the agent offers or creates a thread

Preferred early style:

- welcome on first post, not necessarily on server join
- keep it short
- avoid corporate boilerplate

### 3. First-Time Posters

Use case:
Make the server feel alive and attentive without being overbearing.

Workflow:

- detect first meaningful message in approved public channels
- send one short, friendly reply
- optionally ask a single high-signal question such as what they’re building or what brought them in
- do not follow up again unless they engage

### 4. Weekly Summaries

Use case:
Turn Discord chatter into useful operating intelligence.

Workflow:

- agent reviews approved channels for the week
- produces two outputs:
  - public-facing summary: community highlights, notable questions, useful wins
  - internal ops summary: repeated friction, feature requests, bugs, sentiment, active members, follow-up needs
- staff reviews before public posting during early phases

This is one of the highest-value Community Manager workflows.

### 5. FAQ Handling

Use case:
Answer repeated questions without making staff repeat themselves.

Workflow:

- member asks common question
- agent answers only from approved source material
- if answer confidence is low or the question is strategic/sensitive, it escalates to staff instead of improvising
- repeated unanswered questions are logged into the weekly summary so docs can improve

Candidate FAQ areas:

- what MetaDyn is
- where beta feedback goes
- how to get access or stay updated
- where demos, updates, or announcements live

### 6. Events

Use case:
Support community calls, demos, showcases, and feedback sessions.

Workflow:

- staff supplies approved event details
- agent drafts or posts reminders
- agent can create a poll for scheduling preference if needed
- agent posts a recap request or feedback prompt afterward
- internal summary captures attendance signals and top follow-ups

### 7. Escalation

Use case:
Prevent the bot from bluffing or handling sensitive moments badly.

Escalate immediately when a message involves:

- conflict or harassment
- moderation or bans
- account/access/payment trouble
- founder, partner, legal, or contractual claims
- roadmap promises
- media/public relations sensitivity
- anything the agent cannot ground confidently

Escalation behavior:

- acknowledge briefly
- avoid guessing
- tell the member a human will follow up if appropriate
- notify staff/internal channel with the context and recommended response draft

## Community Manager Agent Design Guidance

The Community Manager agent should be optimized for:

- calm, welcoming tone
- concise answers
- source-grounded replies
- operational consistency
- knowing when not to speak

It should not be optimized for maximum engagement at all costs.

Desired personality:

- warm but not clingy
- proactive but not noisy
- helpful without pretending to have authority it does not have
- good at routing, summarizing, and lightweight facilitation

## Recommended Decision Policy

A simple rule set for the agent:

- if the action is low-risk, repeatable, and source-grounded, it can usually act
- if the action creates expectations, interprets policy, or affects people materially, draft first
- if the action involves trust, safety, discipline, conflict, or commitments, escalate to a human

## 30-Day Rollout Recommendation

### Week 1

- finalize channel scope
- define approved FAQ/source docs
- test in internal ops channel
- test poll, search, summary, and thread workflows

### Week 2

- enable limited public interaction in one help/onboarding surface
- enable first-time-poster welcome in one channel
- start weekly internal summary

### Week 3

- add one general/community channel
- let the agent handle narrow FAQ and routing autonomously
- staff-review public recap draft

### Week 4

- review outcomes
- identify failure modes and noisy behaviors
- decide whether to expand beyond mention-gated behavior in selected channels
- decide whether to broaden docs, workflows, and permissions

## Success Metrics

Track these weekly:

- number of questions answered without staff intervention
- number of escalations
- response quality issues
- member engagement with polls and prompts
- staff time saved
- repeated unanswered questions
- number of useful insights captured in summaries
- sentiment around bot participation

## Final Recommendation

MetaDyn should introduce the Community Manager on Discord as a **trusted community operations assistant**, not a fully autonomous moderator.

The strongest early use cases are:

- onboarding
- polls
- FAQ handling
- routing and thread creation
- weekly summaries
- event reminders

If those become reliable, then broader community participation can expand safely from there.
