# MetaDyn Daily Agenda Framework

## Purpose
This framework is for Josh's **combined daily MetaDyn agenda**.

The morning agenda should not be limited to Discord. It should roll up the most important items across MetaDyn for the day and week, with **Discord/community work included as one important section** alongside product, platform, outreach, operations, and strategic follow-through.

## Guiding principle
Each morning agenda should answer:
- What matters most today?
- What changed since yesterday or over the last few days?
- What needs movement this week?
- What founder-visible actions should happen today?
- What current build, deployment, architecture, or coordination threads are actually live right now?
- What can be deferred if time gets tight?

The agenda should feel like a real operator brief, not a recycled suggestion list.

## Daily agenda structure
Use this structure for the automated morning agenda:

1. **Top priorities today**
   - 3-5 highest-value MetaDyn actions for the day

2. **Recent carry-forward context**
   - 2-5 bullets capturing meaningful recent updates from conversation, memory files, sent posts/emails, shipped work, strategy shifts, implementation decisions, or newly stated priorities
   - This section should make the agenda visibly reflect what Josh has said recently
   - Do not include stale trivia; include only updates that should shape near-term execution
   - Prefer things like active build decisions, deployment architecture changes, newly chosen implementation directions, blocked items, or fresh external moves over old generic reminders

3. **Platform / product build**
   - Current build item, feature review, blocker, test, or implementation priority

4. **Deployment / infrastructure / orchestration**
   - Current deployment work, infra decision, orchestration/API thread, environment change, or verification task
   - Use this section whenever active deployment or systems architecture work is more relevant than generic outreach reminders

5. **Community / Discord**
   - The key Discord/community action for the day if relevant
   - One engagement mechanic or post if relevant
   - One follow-up/community ops task if relevant
   - Keep this lightweight when community is not the active priority

6. **Business / strategy / coordination**
   - Coordination with co-founders, planning, messaging, positioning, documentation, partner movement, or next-step decisions
   - If outreach or beta work is active, include it here as a concrete current thread rather than as stale recurring filler

7. **If there’s extra time**
   - Useful but non-critical actions

## Weekly framing
The automated agenda should also maintain awareness of the broader week:
- What outcomes matter most this week?
- What has already happened?
- What must happen before the week ends?
- Which community, build, and outreach threads need continuity?

## How to assemble the daily agenda
When generating the daily agenda:
- Prefer the most current context from this workspace and recent conversation
- Review the latest relevant `memory/YYYY-MM-DD.md` notes and recent documented updates before drafting
- Include only what is actionable and relevant
- Keep it concise and easy to scan
- If there are no fresh inputs for a category, still keep the category lightweight rather than inventing work
- Carry forward meaningful new updates, decisions, published communications, and strategic signals from recent conversation unless Josh indicates they are one-off or no longer relevant
- Explicitly surface the most relevant carry-forward items in the **Recent carry-forward context** section rather than leaving them buried only in memory or docs
- Discord/community should usually appear, but should not dominate unless it is the highest-priority area that day
- Bias toward what is active now: current implementation choices, deployment work, architecture changes, blockers, verification tasks, visible product movement, and coordination that affects this week
- Do not pad the agenda with legacy suggestions just because they used to matter
- If a thread was completed, shipped, posted, thanked, or already handled, treat it as closed unless there is a specific fresh follow-up or unresolved consequence
- If something appears repeatedly across days, require a current reason for it to remain: active, blocked, newly changed, strategically unresolved, or explicitly requested by Josh
- When a previously important thread is now done, it may appear briefly as recent progress or context, but it should not keep reappearing as a current action item
- Prefer concrete nouns over vague placeholders: name the actual build thread, system, decision, deployment surface, doc, or blocker whenever known
- If newer active work exists, it should displace older generic reminders even if the older reminders were once valid
- After writing or updating any agenda file under `docs/operations/daily-agendas/`, run `python3 /home/jza/.openclaw/workspace/scripts/sync_control_ui_daily_agendas.py` so the control-ui directory/dashboard canvas reflects the real archive instead of drifting behind it

## Current standing Discord/community rhythm
Use the weekly Discord plan as a supporting source, not the whole agenda.
Reference file:
- `/home/jza/.openclaw/workspace/docs/community/weekly-discord-plan.md`

## Agenda quality filter
Before finalizing a daily agenda, check each proposed item:
- Is this still active?
- Did this change recently?
- Is there a concrete reason it matters today or this week?
- Is this a real current thread, not just a historically important one?
- Would Josh roll his eyes because this was already done days or weeks ago?

If the last answer is yes, cut it.

## Suggested daily output format

**MetaDyn Daily Agenda**
- **Top priorities today:**
  - ...
- **Recent carry-forward context:**
  - ...
- **Platform / product build:**
  - ...
- **Deployment / infrastructure / orchestration:**
  - ...
- **Community / Discord:**
  - ...
- **Business / strategy / coordination:**
  - ...
- **If there’s extra time:**
  - ...

## Suggested weekly kickoff output format

**MetaDyn Weekly Agenda Kickoff**
- **This week’s primary outcomes:**
  - ...
- **Most important threads to keep moving:**
  - ...
- **Community / Discord focus this week:**
  - ...
- **Build / product focus this week:**
  - ...
- **Outreach / beta focus this week:**
  - ...
- **Biggest risk if ignored:**
  - ...

## Notes for future expansion
This framework can later pull from:
- build plans
- bug or task trackers
- beta tester lists
- docs needing review
- founder priorities mentioned in recent chat
- calendar-driven priorities

Until then, generate the agenda from available workspace context and recent instructions, with Discord included as one important component rather than the entire agenda.

## Structural constraint
When writing daily agendas, preserve the existing archive structure under `docs/operations/daily-agendas/<Month-YYYY>/YYYY-MM-DD-metadyn-daily-agenda.md` unless Josh explicitly approves changing it.

Do not invent or switch to alternate convenience outputs like `*-latest.md`, replacement archive paths, or parallel file schemes without explicit approval.
