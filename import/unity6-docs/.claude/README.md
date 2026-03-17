# Claude Context System for MetaDyn

This folder contains context files to help Claude maintain continuity across conversations.

## Folder Structure

```
.claude/
├── README.md                    # This file - explains the system
├── CHANGELOG.md                 # Record of changes, updates, and additions
├── DECISIONS.md                 # Architectural and design decisions log
├── Quick Reference/
│   └── QUICK_REFERENCE.md       # Key file locations, patterns, and shortcuts
└── session_notes/               # Individual session notes (optional)
    └── YYYY-MM-DD_session.md
```

## Workflow

### At Start of Conversation:
1. Claude reads `.claude/Quick Reference/STARTUP_SUMMARY.md` for minimal startup context
2. Claude reads `.claude/CHANGELOG.md` for recent updates
3. Claude reads deeper docs under `.claude/Quick Reference/` only if the task touches those systems
4. Claude reads `/Assets/Docs/Project_Evaluation.md` only if deep project context is needed

## Instruction Compliance

- **FOLLOW USER DIRECTIONS EXACTLY.**
- **DO ONLY WHAT THE USER ASKED.**
- **DO NOT EXPAND SCOPE WITHOUT PERMISSION.**
- **DO NOT RUN EXTRA CHECKS OR "HELPFUL" INVESTIGATION UNLESS THE USER ASKED FOR IT.**
- **IF AN EXTRA STEP MIGHT HELP, ASK FIRST.**
- **WHEN TOLD TO READ DOCS OR RULES, READ THEM AND FOLLOW THEM.**

### During Conversation:
- Update `CHANGELOG.md` when making significant changes
- Add to `DECISIONS.md` when making architectural choices
- Update `QUICK_REFERENCE.md` if new patterns or important files are added

### At End of Session (Optional):
- Create session note in `session_notes/` if major work was completed

## Document Purposes

### CHANGELOG.md
**What:** Record of what changed, when, and why
**When to update:** After implementing new features, fixing bugs, or refactoring
**Format:** Date, change description, files affected

### DECISIONS.md
**What:** Architectural and design decisions with rationale
**When to update:** When choosing between implementation approaches
**Format:** Decision title, context, options considered, choice made, rationale

### QUICK_REFERENCE.md
**What:** Fast lookup of key information (file paths, design patterns, conventions)
**When to update:** When establishing new patterns or frequently accessing files
**Format:** Categorized shortcuts and references

## Benefits

- **Continuity:** Claude remembers project state across conversations
- **Context:** Quick refresh on project without re-analyzing entire codebase
- **History:** Track why decisions were made and what changed
- **Efficiency:** Faster startup time for conversations
- **Documentation:** Automatic project history and decision log

## Usage Notes

- Keep documents concise and scannable
- Use markdown formatting for readability
- Date all entries for temporal context
- Cross-reference related entries when helpful
