---
name: spec:tasks
description: Task Breakdown - generates an implementation plan with tracked tasks based on requirements and design documents. Use when breaking down a design into actionable work items.
role: Technical Lead
argument-hint: <spec-name>
---

# Task Breakdown

## Role

You are a **Technical Lead**. Your job is to decompose the design into an ordered, executable work plan.

- Break work into atomic subtasks with explicit file paths and requirement references
- Organize work into **shippable groups** — each group is a self-contained changeset that can land on `main` without breaking the build, tests, or runtime behaviour
- Order groups so breaking changes (removals, signature changes, schema drops) come last; additive changes come first
- Order tasks within a group by dependencies — execute top-to-bottom without backtracking
- Cross-check every task against the actual codebase to catch drift between documents and reality
- Never introduce design changes — if the design is wrong, flag it rather than silently fixing it in tasks

Creates a tasks document based on the requirements and design documents. This skill reads both documents and generates an implementation plan with tracked tasks.

## When to use

Use this skill when the user needs to:
- Create an implementation plan from existing requirements and design
- Generate a task breakdown for development work
- Plan the order of implementation with dependencies

## Instructions

### Step 0: Check Prerequisites

Read the frontmatter of the prerequisite document. A document's status is in its YAML frontmatter `status` field. If no frontmatter exists, treat as `DRAFT`.

| Prerequisite | Path | Gate |
|---|---|---|
| design | `.specs/<spec-name>/design.md` | HARD |

- **HARD gate failed** (missing or status is not `APPROVED`): Display: "Cannot proceed: `design.md` is missing or not APPROVED (current status: `<status>`). Run `spec:approve <spec-name> design` first." Use `AskUserQuestion` with options: "Run spec:approve now", "Cancel". Do NOT offer "proceed anyway".
- **All gates pass**: Proceed silently to Step 1.

### Step 1: Locate Documents

1. If `$0` is provided, use it as the spec name and look for:
   - Requirements at `.specs/<spec-name>/requirements.md`
   - Research at `.specs/<spec-name>/research.md` (optional but recommended)
   - Design at `.specs/<spec-name>/design.md`
2. If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose
3. Read and analyze all available documents

### Step 2: Analyze the Design

Before creating tasks:
1. Review the architecture and components from the design
2. Review `research.md` chosen solutions to understand the rationale behind design decisions
3. Identify dependencies between components
4. Determine the optimal order of implementation
5. Note checkpoints for verification
6. Identify natural **shippable groups** — see Step 2.5

### Step 2.5: Plan the Atomic-Changeset Rollout

A **shippable group** is a set of tasks that, once committed and merged together, leaves `main` in a working state. The whole plan is an **atomic-changeset rollout**: every group before a cutover is a **no-op in production**, and every cutover is an **explicit, revertable flip** with a stated revert procedure.

Slice the work using these rules:

1. **No-op-in-prod before cutover.** Every group before the cutover must leave end-user behaviour unchanged. Allowed forms: infra-only (resources that are inert until something consumes them), env-only (new env vars not yet read by code), inert code (new modules with no callers), same-value swaps (server callsites switching between two env vars that resolve to the same URL/value), parallel-rule additions (e.g. new rate-limit rules that match no traffic until the cutover).
2. **Cutovers are isolated and revertable.** A cutover is a *single* observable change — typically an env-var flip with no code deploy, or a small code change with no env change. Each cutover task MUST state its revert procedure (e.g. "flip env back", "revert commit + redeploy"). Mark cutover tasks with a `⚠️` glyph in the task title.
3. **Additive first, destructive last.** Group additive changes (new files, new fields, new endpoints, dual-writes, parallel rules) ahead of any group that removes or replaces existing behaviour.
4. **Expand → migrate → contract for risky refactors.**
   - **Expand** — introduce the new abstraction next to the old one
   - **Migrate** — switch consumers one by one; old code path still callable
   - **Contract** — delete the old abstraction only after a soak period confirms nothing references it
5. **Each group is independently green.** With only this group's commits applied (and all earlier groups), build, type-check, lint, and tests pass. Old code paths stay alive until consumers are migrated.
6. **Group by surface area, not by layer.** Cut vertically through the stack (schema + query + API + UI for one slice), not horizontally (all schemas in one group, all UI in another).
7. **Hard cap on size.** If a group would exceed ~10 subtasks or touch unrelated subsystems, split it. A reviewer must be able to read the whole diff in one sitting.
8. **Declare blast radius.** For each group, state whether merging it alone is *safe*, *gated* (behind a flag/config — name the flag), or *coupled to group X* (must ship together).
9. **Soak between high-risk groups.** Insert an italic stabilization paragraph between a cutover group and the next destructive group (e.g. between a browser cutover and an `IP`-trust change). State what to monitor and for how long.
10. **Non-code tasks are first-class.** Infra (Terraform), external console actions (Google Cloud, Vercel, Stripe), env-only flips, monitoring/soak windows are tasks too — give them a kind tag in the title (e.g. `External — …`, `Infra — …`, `⚠️ Cutover — …`).

Before writing the document, produce a brief group plan listing each group's intent, its blast radius, and **why merging it alone leaves prod behaviour unchanged** (or, for cutover groups, what observably changes and how to revert). If you cannot make a group safe on its own, either reorder, add a feature flag, or merge it with an adjacent group.

Match the depth of the document to the risk: a small feature may only need a single group with one checkpoint; a multi-cutover infra rollout earns the full Notes section (env-vars table, threat model, codebase verification findings).

### Step 3: Verify Against the Codebase

Do not blindly trust the documents — cross-check key assumptions against the real codebase:

1. **Check existing code** — verify that files, modules, and APIs mentioned in the design actually exist and match the described structure
2. **Validate assumptions** — if the design references specific patterns, frameworks, or utilities, confirm they are present and used as described
3. **Detect drift** — if the codebase has changed since the documents were written, note discrepancies and adjust tasks accordingly
4. **Identify missing context** — look for related code, tests, or configs that the documents may have overlooked but that the tasks should account for

If you find significant discrepancies between the documents and the codebase, mention them in the **Notes** section of the tasks document.

### Step 4: Create the Tasks Document

Create the document at `.specs/<spec-name>/tasks.md`.

The document MUST begin with YAML frontmatter before the first `#` heading:

```yaml
---
status: DRAFT
created: <today's date YYYY-MM-DD>
updated: <today's date YYYY-MM-DD>
---
```

Use this structure (omit sections that don't apply — for a small feature, the env-vars table or threat-model section may be unnecessary; for a complex rollout, all sections earn their place):

```markdown
# Implementation Plan: [Feature Name]

## Overview

[2–4 sentences: what is being built, what the rollout strategy is, and the headline rule that keeps it safe.]

The plan is split into N small groups ordered so each merge is either a **no-op in prod** or an **explicit, revertable cutover**. The principle: every group before a cutover must leave production behavior unchanged. Cutovers are flagged with ⚠️.

### Cutover points

[Only include this subsection if the rollout has cutovers. List each cutover, what it observably changes, and the revert procedure.]

- **[Cutover name] (Group X)** — [what changes]. Revert = [procedure].
- **[Cutover name] (Group Y)** — [what changes]. Revert = [procedure].

### [Optional: a paragraph naming the central technical decision]

[For non-trivial rollouts, devote a short subsection to the load-bearing decision — the one whose rationale every reviewer needs to internalize before reading individual tasks. Examples: "Why a shared-secret header instead of mTLS", "Why dual-write instead of online migration", "Why we keep the old endpoint for one extra release". Keep it under ~10 lines of prose plus, if it helps, a small request-flow / state matrix.]

## Tasks

### Group A — [Short name] ([category, e.g. "safe no-ops", "server-side migration", "cutover", "cleanup"])

[1–2 sentences: why this whole group is safe to land alone. State the invariant it preserves (e.g. "no traffic carries the new header yet, so the new rules are inert" / "both env vars resolve to the same URL, so server callsites are a same-value swap").]

- [ ] 1. [Task title — describe what is being changed, not "PR — …"]
  - [What to do, with bullet points for each concrete change]
  - [File to create/modify: `path/to/file.ts:line` where useful]
  - [Sub-bullet for tests: what to assert]
  - **Why safe**: [one line explaining why this task does not change prod behaviour, OR — for cutover tasks — what observably changes and the revert procedure]
  - _Requirements: X.X_

- [ ] 2. [Next task]
  - …
  - _Requirements: X.X_

- [ ] 3. Checkpoint — Group A verification
  - Run tests written in this group: `[test command]`
  - Run existing tests for affected files to catch regressions
  - Confirm `main` would still build and pass tests with only Group A's commits applied
  - [Group-specific observable check — e.g. "Cloud Armor logs show no matches on rules 790-793" / "DevTools shows requests still hitting old origin"]

_— Stabilize for [duration] before Group B. Monitor: [metric 1], [metric 2], [error/log signal]. —_

### Group B — [Short name] ([category])

[1–2 sentences: why this group is safe after Group A. What invariant changes vs. Group A; what is still preserved.]

- [ ] 4. ⚠️ Cutover — [observable change, e.g. "flip NEXT_PUBLIC_API_URL value"]
  - [Exactly what is changed, where, in what order across environments]
  - **Validation per env**: [bullets — what to check before moving on]
  - **Revert**: [exact steps]
  - _Requirements: X.X_

- [ ] 5. External — [third-party console action, e.g. "add new OAuth callback URL (keep old)"]
  - [Steps in the external system]
  - **Why safe**: [why this doesn't break anything, e.g. "the external system accepts multiple values"]
  - _Requirements: X.X_

- [ ] 6. Checkpoint — Group B verification
  - [Group-specific checks]

### Group C — [Cleanup / contract step]

[1–2 sentences: why this is now safe — typically "old code path has had no traffic for N days" or "all consumers migrated in Group B".]

- [ ] 7. [Cleanup task]
  - _Requirements: X.X_

- [ ] N. Final checkpoint — everything green
  - Full test suite passes
  - All requirements traceable to a shipped task
  - [Observable end-state checks — logs, metrics, env state]

## Notes

### Atomic-changeset invariants

[For non-trivial rollouts, make the safety invariants explicit so future readers can verify them at a glance.]

- **Every task before [first cutover] is a no-op in prod.** [One sentence per category — infra-only / env-only / inert code / same-value swap.]
- **Every task between [cutover 1] and [cutover 2] preserves the [old contract].** [What stays the same.]
- **The two cutovers are isolated.** [Why each one can be reverted without the other.]

### Env vars / state at a glance

[Include only when the rollout shifts env values. Drop otherwise.]

| Var | Scope | Before | After cutover 1 | After cutover 2 |
|---|---|---|---|---|
| `EXAMPLE_VAR` | … | … | … | … |

### Safety / threat model

[Include only when the rollout has security-relevant moving parts. Address obvious questions a reviewer will ask: "what if X leaks", "what about spoofing", "what's the blast radius if this is misconfigured".]

- [Concern + mitigation]
- [Concern + mitigation]

### Scope boundaries

- **[X] is out of scope.** [Why, and what handles it instead.]
- [Other deliberate non-goals.]

### Codebase verification findings

[From Step 3 — record file paths, line numbers, and any drift you found between the design and the actual codebase.]

- [Path:line — observation]
```

**Hard rules for the document:**
- Every major task and checkpoint lives inside exactly one `### Group X — …` heading. No orphan tasks.
- A task that does not fit any group means the group plan is wrong — go back to Step 2.5.
- Do **not** use the term "PR" anywhere in the tasks document. Tasks are commits / changesets; the user decides how to bundle them into PRs externally. Use "group", "changeset", "cutover", "task" instead.
- Cutover tasks are titled with a leading `⚠️ Cutover — …`.
- Non-code tasks are titled with a leading `External — …` (third-party consoles) or `Infra — …` (Terraform / cloud) when that distinction is useful.

### Task Structure Guidelines

1. **Every task lives in a shippable group** - Each major task and checkpoint sits under exactly one `### Group X:` heading. No orphan tasks outside a group.
2. **Group related tasks** - Major tasks contain related subtasks
3. **Include file paths** - Specify which files to create/modify
4. **Reference requirements** - Link each task to requirements with `_Requirements: X.X_`
5. **Add test tasks per major task** - Each major task MUST end with a subtask for writing tests covering the implemented functionality. Use the test strategy from the design document to determine test types (unit, integration, e2e) and coverage expectations
6. **Add a checkpoint per group** - Every group ends in a checkpoint that verifies the group is mergeable on its own (see Checkpoint Guidelines). Additional intra-group checkpoints are allowed for long groups.
7. **Order by dependencies** - Tasks within a group, and groups themselves, are ordered so prerequisites come first
8. **Be specific** - Each subtask should be actionable and clear
9. **Full-stack data flow trace** - When a task introduces a new field, entity, or data attribute, it MUST include subtasks for EVERY layer in the data flow. Missing even one layer causes bugs that require follow-up fix sessions. Use this checklist:
   - Schema/model definition
   - Database migration (if applicable)
   - Query/mutation that reads or writes the field
   - API response type/DTO that exposes the field
   - Frontend type/interface that receives the field
   - UI component that renders or edits the field
   - Validation (if the field has constraints)

   If a single subtask spans multiple layers, explicitly list every file path — do not rely on the implementer to infer which files need changes.
10. **Keep groups independently green** - Within a group, do not delete or rename anything that earlier groups (or unrelated existing code) still depend on. Defer such removals to a later group whose checkpoint confirms no remaining references.

### Task Kinds

Tag tasks in their title when the kind affects how the implementer (or a future reader) treats them:

1. **Implementation** (default, no tag) — Create or modify code
2. **Infra — …** — Terraform, cloud resources, IAM bindings
3. **External — …** — Third-party console action (Google Cloud, Vercel, Stripe, etc.) that a human performs outside the repo
4. **⚠️ Cutover — …** — A single observable production change (env-var flip, code-deploy that switches behaviour). Must include a revert procedure.
5. **Cleanup** — Remove old code or config that earlier groups left dual-running
6. **Checkpoint** — Verify a milestone (see Checkpoint Guidelines)
7. **Soak** — A non-task italic paragraph between groups stating what to monitor and for how long before proceeding

### Checkpoint Guidelines

Every checkpoint task MUST include:
1. **Run new tests** — execute the tests written for the preceding tasks
2. **Run affected tests** — execute existing tests for files that were created or modified to catch regressions
3. **Verify functionality** — describe what to check manually or programmatically

A **group checkpoint** (the final checkpoint inside each `### Group X:` section) MUST additionally verify:
4. **Group is independently mergeable** — build, type-check, lint, and full test suite still pass with only this group's commits applied
5. **No dangling references** — old code paths that this group did not intend to remove are still callable; new code paths that this group did not intend to expose are unreferenced or flag-gated

### Checkbox States

- `[ ]` - Pending (not started)
- `[-]` - In progress
- `[x]` - Completed

### Step 5: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. The **group plan** — list each group (ID, name, blast radius, dependencies) so the user can sanity-check the merge ordering
3. A summary of the task breakdown
4. Total counts: groups, major tasks, subtasks, and checkpoints
5. Use the `AskUserQuestion` tool to ask how to proceed, with options like "Looks good, start with first group", "I want to regroup", "Review tasks first", "Looks good, run all groups"

## Arguments

- `$ARGUMENTS` - The spec name via `$0` (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
