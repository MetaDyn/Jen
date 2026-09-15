# Jen Context Intake — Plan and Punch List

**Date:** 2026-09-15
**Status:** Draft for Josh's review; manual workflow, not background automation.

## Goal

Let Josh hand off rough context quickly without organizing it first. Turn that material into durable, findable project knowledge and a small set of clear next actions that Josh and the team can use independently of chat.

Build on `../runbooks/ingest-platform-context.md` and the existing docs structure. Do not create a second knowledge base or duplicate task tracker.

## Simple Intake Protocol

Josh can say **“Context dump”** and send notes, links, documents, or a rough explanation. No template required. For multiple messages, say **“done”** when ready for synthesis; until then, acknowledge briefly and avoid premature conclusions.

Jen then:

1. **Read and triage.** Identify the project/topic, source, date, and any sensitive material. Clearly flag inaccessible links or unprocessed attachments rather than implying they were read.
2. **Separate meaning.** Distinguish confirmed facts, decisions, ideas/proposals, action items, and open questions. User-described implementation is not independent verification.
3. **Reconcile.** Check existing relevant docs. Preserve useful history and flag conflicts; do not silently replace established decisions with ambiguous notes.
4. **File in the existing home.** Update the relevant project or canonical doc, retain source references, and add only durable distilled context to memory. Use daily notes for session history. Ask before inventing a new structure; avoid unnecessary duplicate files.
5. **Extract next steps.** Record actionable work in the existing appropriate punch list, with an owner when known. Mark unknown owners and deadlines as unset rather than guessing. Capturing a task does not authorize executing it.
6. **Close the loop briefly.** Report what was captured, where it lives, the most useful next action, and only questions that materially block progress. Explicitly identify anything still unprocessed.

Suggested confirmation:

> Captured: [short summary]. Saved in: [links/paths]. Next: [one action]. Needs your input: [only blocking questions].

## Scope and Safety

- Accept rough input without requiring Josh to classify or rewrite it.
- Do not store credentials, secrets, or sensitive client data in the repository. Sanitize material before committing; ask about an approved destination when needed.
- Persist knowledge in files, not promises of perfect chat recall. Disclose unavailable retrieval when relevant and use direct document inspection where possible.
- Do not interpret a dump as approval for deployments, architecture changes, external communications, new services, or destructive work.
- Commit workspace edits. Report local commit versus remote push accurately; never imply remote availability without verifying it.
- Do not claim continuous monitoring or automatic ingestion. This draft is a user-triggered workflow.
- Keep detailed truth in canonical docs and memory concise. Make the result understandable to other team members, not only Jen.

## Punch List

### Establish the workflow
- [x] Draft a lightweight intake protocol in the existing planning directory.
- [x] Reuse the existing ingestion runbook and documentation conventions.
- [ ] Josh reviews the proposed “Context dump” / “done” convention.
- [ ] Run one small real dump through the full workflow.
- [ ] Verify that Josh can find the result and understand the next action without rereading the chat.
- [ ] Refine the protocol based on that test.

### Reduce the current mental load
- [ ] Ask Josh which project or cluster of loose notes feels hardest to keep track of; start there rather than auditing everything.
- [ ] Reconcile that material against its existing docs and punch lists.
- [ ] Surface unresolved decisions, missing owners, and genuinely blocked work.
- [ ] Agree on a short next-action list; do not turn every idea into a commitment.
- [ ] Identify where another team member or specialist should verify technical details or share ownership.

### Optional later improvements — require agreement
- [ ] Decide whether a recurring review is useful and who participates. No reminder or background job is authorized by this document.
- [ ] When connected subagents are available, define scoped context packets and verified result write-back using the connected-development plan. Do not assume that integration exists today.

## Related Documents

- [Platform context ingestion runbook](../runbooks/ingest-platform-context.md)
- [Documentation standards](../standards/documentation.md)
- [Jen-connected development](jen-connected-development.md)
- [Project workspaces](../projects/README.md)
