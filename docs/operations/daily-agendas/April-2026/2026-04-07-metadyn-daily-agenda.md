# MetaDyn Daily Agenda

**Date:** 2026-04-07
**Timezone:** America/Chicago

- **Top priorities today:**
  - Lock the daily agenda back onto real current work: active implementation decisions, deployment/orchestration architecture, and actual build threads instead of recycled beta/community reminders.
  - Turn the avatar direction into a practical build sequence for Pavilion: validated `VRM`/`GLB` uploads bound onto the canonical MetaDyn player runtime.
  - Tighten the deployment/orchestration model so the dashboard, Jen, and deployment hooks all point at the same execution layer with clear boundaries.
  - Decide which concrete implementation thread should move first this week: uploader prototype, runtime binder, remote execution wrapper, deploy API contract, or dashboard integration path.

- **Recent carry-forward context:**
  - Josh explicitly called out that the daily agenda has become stale and repetitive, especially around already-completed beta/community suggestions, and wants it fixed to be live, dynamic, organic, and actually useful.
  - MetaDyn's avatar direction is now clearly centered on validated `VRM` + `GLB` uploads normalized against a MetaDyn-owned avatar spec and attached to the canonical player runtime rather than replacing it.
  - The new orchestration/deployment docs established that the remote execution API is broader than Jen-only delegation: it should also support dashboard-native non-orchestrated actions and standard deployment hooks.
  - Current high-signal work is shifting toward implementation architecture, deployment flow, runtime ownership, and concrete build sequencing rather than generic community follow-up.

- **Platform / product build:**
  - Define the smallest real Pavilion avatar milestone: upload one `VRM` and one `GLB`, validate them against agreed limits, and bind the result to the existing local player runtime.
  - Write or refine the concrete implementation order for the avatar path so work does not sprawl: uploader surface, validation layer, import path, runtime binder, persistence later.
  - Keep the product proof focused on the real runtime that will receive the merge, not an isolated fake environment that hides actual integration problems.

- **Deployment / infrastructure / orchestration:**
  - Refine the execution-layer model as shared infrastructure, not just “subagent API”: one bounded authenticated contract used by Jen orchestration, dashboard-native tasks, and standard deployment hooks.
  - Clarify the first practical deployment/execution pilot: what host or role should expose the first real task contract, what the approved task shape is, and what approval boundaries must remain explicit.
  - Convert the architecture docs into an implementation-minded next-step list for the dashboard/deploy flow: task submission, status reporting, result handling, and how deployment metadata flows back into the app.

- **Community / Discord:**
  - Keep this lightweight unless there is a real fresh outward-facing move today.
  - If there is something public to share, anchor it to a real implementation thread or architecture milestone rather than another generic momentum post.

- **Business / strategy / coordination:**
  - Align on which technical thread best represents visible MetaDyn momentum right now: avatar uploads/runtime ownership, dashboard deployment flow, or remote execution/orchestration infrastructure.
  - Keep positioning tied to real implementation choices: ownership of runtime, cross-surface continuity, browser-first deployment, and infrastructure that supports actual operations instead of platform captivity.
  - If founder coordination happens today, use it to reduce ambiguity: what is being built first, why that sequence wins, and what counts as proof by the end of the week.

- **If there’s extra time:**
  - Turn the avatar strategy and orchestration/deployment notes into a short implementation checklist with phases, dependencies, and proof points.
  - Identify the next doc or system that still feels too abstract and make it implementation-specific.
