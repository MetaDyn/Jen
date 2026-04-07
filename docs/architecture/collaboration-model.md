# Collaboration Model

## Core Human Contacts

Jen is expected to interact primarily with a small set of core human collaborators.

Current key contacts:
- **Josh Garrett**
- **Marzio Camaso**
- **MetaMike**

At present, there is **no formal user system** for identity resolution, which means collaboration and attribution rules will need to be handled carefully until a clearer user/account model exists.

Until that user system is in place, Jen should assume it is speaking with **Josh Garrett**.

## Partner Context

MetaDyn also works in relationship with important industry partners.

Current notable partner context:
- **Polycount** is an industry partner
- **Michael Potts** is the CEO of Polycount
- **Josh Garrett** is Director of Spatial Engineering at Polycount

## Implications For Jen

Because multiple people will interact with Jen, but formal user identity is not yet established, Jen should be designed to:
- avoid over-assuming who is speaking when identity is ambiguous
- preserve important decisions in canonical docs rather than relying on chat memory alone
- support collaboration across multiple company members
- track partner context separately from internal company roles
- be cautious about authority, attribution, and external-facing statements

## Agent Collaboration Model

Jen is intended to orchestrate a core set of subordinate specialist agents.

Current planned set:
- **Metaverse CTO**
- **Marketing Strategist**
- **DevOps Specialist**
- **Unity Architect**
- **UX Architect**
- **Community Manager**

Current state:
- **Metaverse CTO** is already set up
- the remaining agents are planned and their skill packages are expected to be assembled

These agents are expected to operate in a blended model:
- internal coordination under Jen
- collaboration with human counterparts externally
- cross-agent delegation where tasks require combined expertise
- backend coordination with additional agents running on other servers

For the more detailed control-plane model and proposed API contract for remote machine-hosted subagents, see:
- `../ai-systems/agent-orchestration-and-remote-subagents.md`

## Future Expansion

This model should later expand to include:
- formal user/account identity handling
- role definitions and permissions
- internal vs partner vs community distinctions
- delegation and approval rules
- how subordinate agents map to human owners or domains
- backend federation rules for other-server agent collaboration
