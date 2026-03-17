# Claude Context Workflow for MetaDyn

## Overview

This document explains the workflow for maintaining context across Claude conversations.

---

## Suggested Workflow

## Non-Negotiable Rule

- **FOLLOW USER DIRECTIONS EXACTLY.**
- **DO ONLY WHAT THE USER ASKED.**
- **DO NOT EXPAND SCOPE WITHOUT PERMISSION.**
- **DO NOT RUN EXTRA CHECKS, VALIDATION, OR ADJACENT INVESTIGATION UNLESS THE USER ASKED FOR IT.**
- **IF AN EXTRA STEP MIGHT HELP, ASK FIRST.**
- **WHEN TOLD TO READ DOCS OR RULES, READ THEM AND FOLLOW THEM BEFORE DOING ANYTHING ELSE.**

### 🟢 At the Start of Each Conversation

**Claude should read (in order):**

1. **`.claude/Quick Reference/STARTUP_SUMMARY.md`** (fast read)
   - Minimal startup context
   - Rules, platform snapshot, and doc routing

2. **`.claude/CHANGELOG.md`** (1-2 min read)
   - What changed since last time
   - Recent additions and modifications
   - Context for current state

3. **Relevant docs under `.claude/Quick Reference/`** (load on demand)
   - Read only the docs required by the task area
   - Do not preload the entire folder by default

4. **`Assets/Docs/Project_Evaluation.md`** (Optional, if deep context needed)
   - Comprehensive project analysis
   - Only read if working on major features or refactoring
   - Can skip for small changes or bug fixes

**Scope rule during startup:** **Do not perform any additional checks, verification, or related investigation unless the user explicitly asks for it. Reading startup docs is not permission to inspect adjacent issues.**

**Total startup time:** minimal for normal tasks, deeper only when needed

---

### 🟡 During Active Work

**Update as you go:**

**CHANGELOG.md** - Update when:
- Adding new features
- Fixing bugs
- Refactoring code
- Making significant changes

**Format:**
```markdown
## 2025-11-30 - Feature Name

**Added:** New files or features
**Changed:** Modified code
**Fixed:** Bug fixes
**Files:** /path/to/files.cs
**Reason:** Why this change was made
```

**DECISIONS.md** - Update when:
- Choosing between implementation approaches
- Making architectural decisions
- Establishing new patterns or conventions

**Format:**
```markdown
## Decision Title

**Date:** 2025-11-30
**Status:** Accepted
**Context:** Why decision was needed
**Options Considered:** A, B, C with pros/cons
**Decision:** What was chosen
**Rationale:** Why
**Consequences:** Impact
```

**QUICK_REFERENCE.md** - Update when:
- Adding new key files or systems
- Establishing new code patterns
- Creating shortcuts or conventions
- Information would save time in future conversations

---

### 🔴 At End of Major Work Sessions (Optional)

**Create session note** in `.claude/session_notes/`:

```markdown
# Session: 2025-11-30 - Feature Name

## Summary
What was accomplished this session.

## Changes Made
- Feature A implemented
- Bug B fixed
- System C refactored

## Files Modified
- /path/to/file1.cs
- /path/to/file2.cs

## Next Steps
- [ ] Task A remaining
- [ ] Task B to do next
- [ ] Issue C to investigate

## Notes
Any important context for next time.
```

**When to create session notes:**
- Major features implemented (e.g., voice chat streaming)
- Significant refactoring (e.g., inventory system)
- Complex bug fixes that need documentation
- Work that spans multiple conversations

**When to skip session notes:**
- Small bug fixes
- Minor tweaks
- Quick changes
- Work fully captured in CHANGELOG

---

## File Purposes

### QUICK_REFERENCE.md
**Goal:** Fast context refresh
**Contents:**
- Key file locations
- Common code patterns
- Design patterns used
- Performance targets
- Useful shortcuts
- Project stats

**Update frequency:** As needed when adding new patterns or important files

---

### CHANGELOG.md
**Goal:** Track what changed, when, and why
**Contents:**
- Date-ordered list of changes
- Files affected
- Reason for change
- Impact on project

**Update frequency:** After each significant change

---

### DECISIONS.md
**Goal:** Document why architectural choices were made
**Contents:**
- Decision title and date
- Context and options considered
- Final decision and rationale
- Consequences and trade-offs

**Update frequency:** When making important architectural decisions

---

### Project_Evaluation.md (in /Assets/Docs/)
**Goal:** Comprehensive project analysis and reference
**Contents:**
- Full system architecture
- Code quality assessment
- Feature analysis
- Maturity evaluation
- Recommended roadmap

**Update frequency:** Major milestones (quarterly or when significant features complete)

---

## Benefits of This Workflow

### For Claude:
✅ **Fast Context Loading** - 3-5 minutes to full project understanding
✅ **No Repeated Analysis** - Don't re-analyze same files each conversation
✅ **Historical Context** - Understand why decisions were made
✅ **Pattern Recognition** - Learn project conventions quickly

### For You:
✅ **Continuity** - Pick up where you left off seamlessly
✅ **Documentation** - Automatic project history
✅ **Onboarding** - Easy to share context with others
✅ **Decision Log** - Remember why choices were made

---

## Example Conversation Startup

```
User: "Hey Claude, I want to add voice chat streaming"

Claude:
1. Reads STARTUP_SUMMARY.md
   - Sees voice features live in infrastructure/audio docs
   - Knows which deeper docs to load for the task

2. Reads CHANGELOG.md
   - Sees recent user list improvements
   - Notes no voice streaming yet

3. Reads only the needed deeper docs (for example QUICK_REFERENCE.md or INFRASTRUCTURE.md)

4. Begins conversation with task-relevant context:
   "I see you have voice recording infrastructure ready with
   WAV encoding. Let me help add voice streaming using
   Photon Voice/Vivox/Agora. Your MicrophoneRecorder.cs
   already captures audio..."
```

**Total time:** small startup footprint vs. loading every doc every session.

---

## Tips for Maintaining Context Files

### Keep It Concise
- Use bullet points
- Scannable formatting
- Link related entries
- Date everything

### Update Regularly
- Update during work, not after
- Small, frequent updates better than large batch updates
- Don't let it get stale

### Cross-Reference
- Link CHANGELOG entries to DECISIONS
- Reference file paths consistently
- Use markdown links between documents

### Be Specific
- "Fixed user list sync bug" → "Fixed race condition in UserListManager.DetectUserChanges()"
- "Added voice feature" → "Implemented Photon Voice streaming with spatial audio"

---

## Maintenance Schedule

### After Every Session
- [ ] Update CHANGELOG.md with changes made
- [ ] Update DECISIONS.md if architectural choices made
- [ ] Update QUICK_REFERENCE.md if new patterns established

### Monthly
- [ ] Review and clean up outdated entries
- [ ] Consolidate related entries
- [ ] Update project stats in QUICK_REFERENCE

### Major Milestones
- [ ] Update Project_Evaluation.md
- [ ] Create summary session note
- [ ] Review and refine documented patterns

---

## Document Locations

```
MetaDyn/
├── Assets/
│   └── Docs/
│       └── Project_Evaluation.md      # Comprehensive evaluation
│
└── .claude/
    ├── README.md                      # System explanation
    ├── WORKFLOW.md                    # This file
    ├── Quick Reference/
    │   ├── STARTUP_SUMMARY.md         # Minimal startup file (read first!)
    │   └── QUICK_REFERENCE.md         # Broad reference, load when needed
    ├── CHANGELOG.md                   # Change history (read second!)
    ├── DECISIONS.md                   # Architectural decisions
    └── session_notes/                 # Optional session logs
        └── YYYY-MM-DD_feature.md
```

---

## Quick Start Checklist

**For Claude at conversation start:**
- [ ] Read STARTUP_SUMMARY.md
- [ ] Read CHANGELOG.md (2 min)
- [ ] Read only the needed Quick Reference domain docs
- [ ] Read Project_Evaluation.md (optional, for major work)
- [ ] Ready to work with full context!

**During work:**
- [ ] Update CHANGELOG as changes are made
- [ ] Document decisions in DECISIONS.md
- [ ] Add new patterns to QUICK_REFERENCE if relevant

**End of session:**
- [ ] Verify CHANGELOG is up to date
- [ ] Create session note if major work completed
- [ ] Note any TODO items for next time

---

**This workflow ensures Claude has the best possible context for every conversation while minimizing startup time and maximizing productivity.**
