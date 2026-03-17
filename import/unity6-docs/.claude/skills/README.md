# MetaDyn Expert Agent Skills

This directory contains specialized AI agent skills for MetaDyn platform development. Each skill represents a domain expert that can be invoked automatically by Claude Code when relevant topics are discussed.

## Available Skills

### 1. Metaverse CTO (`metaverse-cto`)
**Expertise:** Platform strategy, virtual economies, scalability, monetization, competitive positioning

**When to use:**
- Designing business models or revenue strategies
- Planning platform growth from 10 → 10K → 100K users
- Virtual economy and token economics
- Competitive analysis vs VRChat, Spatial, Decentraland
- High-level architecture decisions

**Example prompts:**
- "Should MetaDyn support land ownership? What's the economic model?"
- "Design a sustainable economy that prevents inflation"
- "What's our scaling roadmap to 10,000 concurrent users?"
- "How should we monetize without alienating users?"

---

### 2. Unity Technical Architect (`unity-architect`)
**Expertise:** Unity 6, Photon Fusion networking, WebGL optimization, SDK component design

**When to use:**
- Implementing new features or components
- Debugging technical issues
- Performance optimization
- Network synchronization problems
- Following MetaDyn SDK patterns

**Example prompts:**
- "Create an Interactable component for generic object interaction"
- "Optimize blend shape performance for lip sync"
- "How should I sync emote animations across players?"
- "Implement networked object pooling for this use case"

---

### 3. UX Architect (`ux-architect`)
**Expertise:** Player-facing systems, onboarding, social features, avatar customization, engagement

**When to use:**
- Designing user interfaces or flows
- Improving onboarding experience
- Social feature design (friends, parties, chat)
- Avatar customization UX
- Engagement and retention optimization

**Example prompts:**
- "Design the first-time user onboarding experience"
- "How should friend requests and social discovery work?"
- "Create a world browser with discovery and filtering"
- "Improve the avatar selection flow for new players"

---

### 4. DevOps Specialist (`devops-specialist`)
**Expertise:** Build optimization, CI/CD, server deployment, monitoring, database scaling, cost analysis

**When to use:**
- Setting up deployment pipelines
- Infrastructure and scaling questions
- Cost modeling and optimization
- Monitoring and analytics setup
- Database performance and scaling

**Example prompts:**
- "Set up automated WebGL builds with GitHub Actions"
- "What should we monitor in production?"
- "Cost analysis for hosting 1000 concurrent users"
- "When should we migrate from Supabase to self-hosted PostgreSQL?"

---

### 5. Marketing Strategist (`marketing-strategist`)
**Expertise:** User acquisition, brand positioning, growth marketing, partnerships, content strategy, go-to-market planning

**When to use:**
- Planning marketing campaigns or user acquisition
- Brand positioning and messaging
- Growth strategy and viral mechanics
- Partnership and influencer outreach
- Launch planning and PR
- Conversion funnel optimization

**Example prompts:**
- "What should MetaDyn's go-to-market strategy be?"
- "Design a user acquisition campaign for beta launch"
- "How should we position MetaDyn vs VRChat and Spatial?"
- "Create a content marketing strategy for creators"

---

### 6. Community Manager (`community-manager`)
**Expertise:** Community building, moderation policies, Discord management, event planning, creator programs, conflict resolution

**When to use:**
- Building community infrastructure
- Creating moderation policies and Code of Conduct
- Planning community events and programs
- Managing Discord or social channels
- Handling community conflicts
- Designing creator programs

**Example prompts:**
- "Create a Code of Conduct for MetaDyn"
- "How should we structure our Discord server?"
- "Design a creator showcase program"
- "What events should we run for the community?"

---

## How Skills Work

Skills are **automatically activated** by Claude Code when you ask relevant questions. You don't need to explicitly call them - just ask your question naturally.

### Automatic Activation
```
You: "Should MetaDyn have land ownership?"
→ Automatically activates metaverse-cto skill
→ Provides strategic economic analysis

You: "Implement a door interaction system"
→ Automatically activates unity-architect skill
→ Provides implementation-ready code
```

### Invoking Specific Skills
If you want to ensure a specific skill is used:
```
You: "Ask the Metaverse CTO: What's our monetization strategy?"
You: "Unity Architect: Create an Interactable component"
You: "UX Architect: Design the friend system"
You: "DevOps: Set up monitoring and analytics"
You: "Marketing Strategist: Plan our beta launch"
You: "Community Manager: Create a Discord structure"
```

### Collaborative Workflows

Skills are designed to work together:

1. **CTO** defines the strategy → **Marketing** plans go-to-market → **UX** designs the experience → **Unity** implements it → **DevOps** deploys it → **Community** engages users

**Example workflow:**
```
1. You: "Should we add voice channels for private groups?"
   → CTO analyzes business value, technical requirements

2. You: "How do we market this feature?"
   → Marketing Strategist creates launch campaign

3. You: "Design the UX for voice channels"
   → UX Architect creates player flows and UI mockups

4. You: "Implement voice channel room system"
   → Unity Architect builds the feature following specs

5. You: "What monitoring do we need for voice channels?"
   → DevOps sets up metrics and alerts

6. You: "How do we onboard users to this feature?"
   → Community Manager creates tutorials and events
```

---

## Skill Contexts

All skills have access to:
- `.claude/Quick Reference/QUICK_REFERENCE.md` - Complete platform status
- `.claude/DECISIONS.md` - Past architectural decisions
- `.claude/CHANGELOG.md` - Recent changes
- `Assets/MetaDyn/Managers/WebRTC-Voice-System.md` - Voice architecture

They understand:
- Current platform maturity (80-85% complete)
- Technical stack (Unity 6, Fusion, WebGL, Supabase)
- Constraints (WebRTC mesh = 6 players, needs LiveKit for scale)
- Existing patterns (SDK components, networking, deployment)

---

## Best Practices

### Ask Strategic Questions First
Before writing code, consult the CTO:
```
❌ "Implement land ownership system" (jumps to code)
✅ "Should MetaDyn support land ownership?" (strategy first)
   → CTO provides analysis
   → Then ask Unity Architect to implement Phase 1
```

### Specify Your Audience
Be clear who you're asking:
```
✅ "CTO: What's our competitive moat vs Spatial?"
✅ "UX: How should onboarding work for mobile users?"
✅ "DevOps: Cost breakdown for 1000 users?"
```

### Combine Multiple Skills
For complex features:
```
You: "I want to add a creator marketplace"

1. Ask CTO: Business model and economics
2. Ask Marketing: User acquisition and positioning
3. Ask Community: Creator programs and engagement
4. Ask UX: Player flows and discovery
5. Ask Unity: Implementation plan
6. Ask DevOps: Infrastructure and costs
```

---

## Updating Skills

Skills are stored in `.claude/skills/` and versioned with your project. When you update platform code or make architectural changes, the skills automatically reference the latest:

- Code patterns from existing files
- Documentation from `.claude/` directory
- Recent changes from `CHANGELOG.md`
- Current status from `QUICK_REFERENCE.md`

---

## Contributing New Skills

To add a new specialized skill:

1. Create directory: `.claude/skills/skill-name/`
2. Create `SKILL.md` with frontmatter:
```yaml
---
name: skill-name
description: What this skill does and when Claude should use it
---

# Skill Name

[Expertise, instructions, examples]
```

3. Commit to git (skills are shared with your team)

---

## FAQ

**Q: Do I need to manually invoke skills?**
A: No, Claude automatically uses them when relevant. But you can be explicit if you want.

**Q: Can I use multiple skills at once?**
A: Yes! Ask a question that spans domains and multiple skills may activate.

**Q: How do I know which skill is active?**
A: Claude will often indicate which perspective it's using (e.g., "From a CTO perspective..." or "As a Unity architect...")

**Q: Can I create my own skills?**
A: Yes! Follow the structure in existing skills and commit to `.claude/skills/`

**Q: Do skills remember past conversations?**
A: Skills read your project's documentation (QUICK_REFERENCE.md, CHANGELOG.md, etc.) to stay current, but they don't have conversation memory across sessions.

---

## Getting Started

Try asking these questions to test each skill:

```bash
# Test Metaverse CTO
"What should our monetization strategy be for MetaDyn?"

# Test Unity Architect
"Create a Trigger component for zone-based events"

# Test UX Architect
"Design the player profile page with stats and achievements"

# Test DevOps Specialist
"Set up error tracking and monitoring for production"

# Test Marketing Strategist
"Design a go-to-market plan for MetaDyn's beta launch"

# Test Community Manager
"Create a Code of Conduct and Discord structure for MetaDyn"
```

---

**Last Updated:** 2025-12-20
**Skills Version:** 2.0 (6 skills)
**Team:** MetaDyn Development
