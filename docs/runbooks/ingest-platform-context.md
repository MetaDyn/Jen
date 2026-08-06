# Ingest Platform Context

Use this when Josh adds or points Jen to new MetaDyn platform docs and wants them to become part of Jen's ongoing understanding.

## Goal

Keep platform understanding current without making every session startup heavy.

The pattern is:

1. Keep detailed truth in canonical docs.
2. Distill durable platform status into `MEMORY.md`.
3. Update the docs index when a new canonical doc should be discoverable.

## Canonical Platform Docs

Treat these as high-priority platform-status references when discussing the MetaDyn platform:

- `docs/planning/MetaDyn_UGS_SDK_Production_PunchList.md`
- `docs/planning/Runtime_Avatar_Upload_And_Rigging_Plan.md`

Add to this list only when Josh clearly wants a document to shape future platform discussions.

## Trigger Phrases

Run this workflow when Josh says things like:

- "ingest this"
- "process properly"
- "make this part of your permanent understanding"
- "this should become context moving forward"
- "make sure you understand the platform status from this"

## Workflow

1. Locate the referenced docs in the repo and pull them into the local working tree if needed.
2. Read the docs.
3. Decide whether they are canonical platform docs or just supporting references.
4. If canonical, add them to `docs/README.md` if they are not already indexed.
5. Update `MEMORY.md` with a concise distilled status note focused on:
   - what is now true
   - what is complete
   - what is still open
   - any important scope boundaries or non-obvious caveats
6. Optionally add a short note to `memory/YYYY-MM-DD.md` if the ingest itself matters as session history.
7. Commit the repo changes.

## Distillation Rules

When updating `MEMORY.md`:

- Prefer durable status over implementation chatter.
- Preserve the difference between "historical milestone reached" and "production-ready now".
- Do not collapse open punch-list items into completed status.
- Capture important caveats if a system works in one tested path but still lacks regression coverage.
- Keep it short enough to be startup-friendly.

## Startup Rule

Do not turn every canonical doc into a mandatory startup read.

Instead:

- keep startup lightweight
- use `MEMORY.md` for distilled always-on understanding
- read the canonical docs directly when platform work needs the full detail

## Minimum Definition Of "Process Properly"

Unless Josh asks for more, "process properly" means:

1. ingest the docs locally
2. index them if needed
3. distill them into `MEMORY.md`
4. commit the changes
