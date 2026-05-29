# Team Mode — parallel implementation with an agent team

Team mode implements several **shippable groups** concurrently using a Claude Code
agent team, instead of one subagent at a time. It is opt-in and only worthwhile when
the plan has multiple groups that can progress in parallel.

> **Requires** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to be enabled (Claude Code
> v2.1.32+). If the variable is not set, this mode is unavailable — fall back to the
> standard sequential/parallel subagent execution in `SKILL.md`.

## When to use it

Offer team mode only when **all** hold:
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set.
- `tasks.md` has **2+ shippable groups** with at least two that are not strictly
  chained (i.e. some parallelism actually exists).
- The user opts in (or invoked `spec:implement <spec> team`).

Otherwise use the standard modes. A single-group or fully-linear plan gains nothing
from a team and just costs ~3× the tokens.

## Roles

- **You are the lead.** The session running this skill creates and owns the team. The
  lead is fixed — it cannot be transferred, and teammates cannot spawn their own teams.
- **Teammates are named engineers**, one per independent group (or a small pool of N
  if there are more groups than you want running at once). Each is a full Claude Code
  session with its own context, inheriting this repo's CLAUDE.md, skills, and MCP.

## Setup

1. **Build the shared task list from the group plan.** Read the **Shippable Groups**
   table in `tasks.md`. Create one task per group with `TaskCreate`, and encode the
   group dependencies with `addBlockedBy` (e.g. Group B `addBlockedBy` Group A). This
   is the coordination backbone — teammates claim from it and dependencies
   auto-unblock as prerequisite groups complete.
2. **Spawn named teammates** with the `Agent` tool, passing `team_name` and a
   descriptive `name` (e.g. `eng-api`, `eng-ui`). Spawn one per group you want running
   now; for a pool, spawn N and let them claim the next unblocked group when free.
3. **Brief every teammate** (in its spawn prompt) with: the spec paths
   (`requirements.md`, `design.md`, the specific group in `tasks.md`), the
   **Subagent Rules** and **Verification Checklist** from `SKILL.md`, the commit
   convention (one commit per subtask/group via `git:commit`), and the collision
   protocol below.

## Collision protocol — no worktrees

All teammates work in the **same working tree**. There are no git worktrees. Avoid
clobbering each other by coordinating, not by isolating:

1. **Announce before editing.** Before a teammate touches a file, it posts the file
   paths it is about to modify — both as a note on its task (`TaskUpdate`) and, for
   anything outside its own group's obvious surface, a broadcast via `SendMessage`.
2. **Check before claiming.** Before starting work, a teammate scans the shared task
   list for files other teammates have announced. If a file it needs is already
   claimed, it coordinates over `SendMessage` and **serializes** — waits, or agrees
   who edits first — rather than editing in parallel.
3. **Groups are vertical slices.** Because each group is a self-contained slice
   (`spec:tasks` slicing rules), genuine overlap should be rare. When it happens,
   messaging resolves it; when in doubt, serialize the conflicting edits.
4. **Commit narrowly and often.** Small, frequent commits scoped to the announced
   files keep the shared tree coherent and make collisions obvious early.

## Execution rules for teammates

- Follow the **Subagent Rules** and **Verification Checklist** from `SKILL.md` exactly.
- **Do not call `AskUserQuestion`.** Teammates cannot prompt the user. On any design
  deviation (per the deviation protocol) or blocker, **escalate to the lead via
  `SendMessage`** and wait — the lead decides or relays to the user.
- Mark tasks `[-]`/`[x]` in `tasks.md` as work progresses, and update the shared task
  list so dependencies unblock.
- Never run `git push`, `gh pr create`, or any remote/PR command.

## Lead responsibilities

- Monitor the shared task list and teammate messages; relay any escalation that needs
  a human decision to the user.
- **Verify before closing a group.** Teammate task status can lag — before treating a
  group as done, confirm its checkboxes are `[x]` and run the group's checkpoint.
- When all groups are done, produce the same **group → commits** map the standard mode
  produces, remind the user no PR was opened, and clean up the team.

## Known limitations (state these to the user up front)

- **~3× token cost** with a few teammates vs. a single session.
- **One team at a time**; the lead must clean up before creating another.
- **No nested teams** — teammates can't spawn teammates.
- **In-process teammates don't survive `/resume` or `/rewind`** — if the session is
  resumed, the team is gone; re-spawn or finish remaining groups with standard mode.
- **Task status can lag** — hence the lead's verify-before-close step.
