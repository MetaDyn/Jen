# MetaDyn Daily Agenda Framework

## Purpose
This framework is for Josh's **combined daily MetaDyn agenda**.

The morning agenda should not be limited to Discord. It should roll up the most important items across MetaDyn for the day and week, with **Discord/community work included as one important section** alongside product, platform, outreach, operations, and strategic follow-through.

## Guiding principle
Each morning agenda should answer:
- What matters most today?
- What needs movement this week?
- What founder-visible actions should happen today?
- What community-facing actions should happen today?
- What can be deferred if time gets tight?

## Daily agenda structure
Use this structure for the automated morning agenda:

1. **Top priorities today**
   - 3-5 highest-value MetaDyn actions for the day

2. **Platform / product build**
   - Current build item, feature review, blocker, test, or implementation priority

3. **Community / Discord**
   - The key Discord/community action for the day
   - One engagement mechanic or post if relevant
   - One follow-up/community ops task if relevant

4. **Beta / user outreach**
   - Survey follow-up, beta onboarding, tester check-ins, founder outreach, or partner follow-up

5. **Business / strategy / coordination**
   - Coordination with co-founders, planning, messaging, positioning, documentation, or next-step decisions

6. **If there’s extra time**
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
- Include only what is actionable and relevant
- Keep it concise and easy to scan
- If there are no fresh inputs for a category, still keep the category lightweight rather than inventing work
- Carry forward meaningful new updates, decisions, published communications, and strategic signals from recent conversation unless Josh indicates they are one-off or no longer relevant
- Discord/community should usually appear, but should not dominate unless it is the highest-priority area that day
- After writing or updating any agenda file under `docs/operations/daily-agendas/`, run `python3 /home/jza/.openclaw/workspace/scripts/sync_control_ui_daily_agendas.py` so the control-ui directory/dashboard canvas reflects the real archive instead of drifting behind it

## Current standing Discord/community rhythm
Use the weekly Discord plan as a supporting source, not the whole agenda.
Reference file:
- `/home/jza/.openclaw/workspace/docs/community/weekly-discord-plan.md`

## Suggested daily output format

**MetaDyn Daily Agenda**
- **Top priorities today:**
  - ...
- **Platform / product build:**
  - ...
- **Community / Discord:**
  - ...
- **Beta / user outreach:**
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
