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
- **Cutovers are conditional, not mandatory.** A cutover only appears in the plan when a specific task observably changes production behaviour (env-var flip, traffic switch, schema swap, removal of in-use code). If no such moment exists, the plan has no ⚠️ tasks, no "Cutover points" section, and no soak paragraphs — it's just groups in dependency order. Do not invent risk that isn't there.

Creates a tasks document based on the requirements and design documents. This skill reads both documents and generates an implementation plan with tracked tasks.

## When to use

Use this skill when the user needs to:
- Create an implementation plan from existing requirements and design
- Generate a task breakdown for development work
- Plan the order of implementation with dependencies

## Instructions

### Step 0: Check Prerequisites

Prerequisites are checked by **file existence**, not by an approval status. There is no approval step in this pipeline.

| Prerequisite | Path | Requirement |
|---|---|---|
| design | `.specs/<spec-name>/design.md` | required |

- **Required prerequisite missing** (`design.md` does not exist): Display: "Cannot proceed: `design.md` does not exist. Run `spec:design <spec-name>` first." Use `AskUserQuestion` with options: "Run spec:design now", "Cancel".
- **Prerequisite exists**: Proceed silently to Step 1.

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
2. Review `design.md`'s Decisions table for the variants chosen per problem area, and cross-reference `research.md` for the menu of variants those decisions were picked from
3. Identify dependencies between components
4. Determine the optimal order of implementation
5. Note checkpoints for verification

### Step 2.5: Slice Into Shippable Groups

A **shippable group** is a set of tasks that, once committed and merged together, leaves `main` in a working state. The whole plan is a sequence of groups in dependency order. Most features ship as a chain of additive groups and stop there. Cutovers only enter the picture when a specific moment observably changes production.

#### Slicing rules (always apply)

1. **Each group is independently green.** With only this group's commits applied (and all earlier groups), build, type-check, lint, and tests pass.
2. **Additive first, destructive last.** Group additive changes (new files, new fields, new endpoints, dual-writes) ahead of any group that removes or replaces existing behaviour.
3. **Group by surface area, not by layer.** Cut vertically through the stack (schema + query + API + UI for one slice), not horizontally (all schemas in one group, all UI in another).
4. **Hard cap on size.** If a group would exceed ~10 subtasks or touch unrelated subsystems, split it. A reviewer must be able to read the whole diff in one sitting.
5. **Order by dependencies inside a group.** Prerequisites first; no backtracking.
6. **Keep old paths alive until consumers move.** Within a group, do not delete or rename anything that earlier groups (or unrelated existing code) still depend on.

#### Cutover detection (apply only if relevant)

After slicing, scan the plan for **cutover moments** — a single task that observably changes production behaviour. Typical sources:

- An env-var flip that switches traffic, origin, or behaviour (e.g. `NEXT_PUBLIC_API_URL` changes value).
- A schema swap or destructive DB op on populated state.
- Removal of an in-use code path / public type / endpoint.
- DNS / domain / IAM change that affects who can reach what.
- Flipping a feature flag that exposes the new behaviour to real users.

If — and only if — at least one such moment exists, apply the **cutover-only rules** to those specific tasks (not to the whole plan):

- **C1. Cutovers are isolated and revertable.** Each cutover is a *single* observable change. State its revert procedure on the task itself (e.g. "flip env back", "revert commit + redeploy"). Mark with a `⚠️` glyph.
- **C2. No-op-in-prod before the cutover.** Groups that ship *before* a cutover must leave end-user behaviour unchanged. Allowed forms: infra-only (inert until consumed), env-only (new vars not yet read), inert code (no callers), same-value swaps, parallel-rule additions.
- **C3. Expand → migrate → contract for risky refactors.** Expand (new next to old) → Migrate (switch consumers, old still callable) → Contract (delete old after soak).
- **C4. Soak between high-risk cutovers.** Insert an italic stabilization paragraph between cutover groups stating what to monitor and for how long.

If no cutover moment exists, none of C1–C4 apply: skip ⚠️, skip "no-op before cutover" language, skip soak paragraphs.

#### Blast radius (always state, but stays short when boring)

For each group, declare in one line: *safe* (merge anytime), *gated* (behind a flag/config — name the flag), or *coupled to group X* (must ship together). A pure additive group is just `safe` — no narrative required. A cutover group earns a full revert sentence.

#### Pre-write check

Before writing the document, produce a brief group plan listing each group's intent and blast radius. If any group has a cutover, also note what observably changes and how to revert. Borderline "is this a cutover?" cases default to **no cutover** — if in doubt, the feature doesn't need the ⚠️ machinery.

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
created: <today's date YYYY-MM-DD>
updated: <today's date YYYY-MM-DD>
---
```

Use this structure. **Cutover-related sections are conditional** — include them only if the plan actually contains a cutover moment (per Step 2.5). For a plain additive feature, drop the "Cutover points" subsection, the ⚠️ tasks, the soak paragraphs, the env-vars table, the threat model, and the atomic-changeset invariants section.

```markdown
# Implementation Plan: [Feature Name]

## Overview

[2–4 sentences: what is being built and how the rollout is sequenced.]

The plan is split into N groups in dependency order. Each group is independently mergeable — build, tests, and prod behaviour stay green with only that group (and earlier ones) applied.

[Add this sentence ONLY if the plan has at least one cutover:]
Groups before a cutover are no-ops in production; cutover tasks are flagged with ⚠️ and state their revert procedure.

### Cutover points

[Include this subsection ONLY if the plan has cutovers. Otherwise omit entirely — do not write "no cutovers" placeholder text.]

- **[Cutover name] (Group X)** — [what changes]. Revert = [procedure].
- **[Cutover name] (Group Y)** — [what changes]. Revert = [procedure].

### [Optional: a paragraph naming the central technical decision]

[For non-trivial rollouts, devote a short subsection to the load-bearing decision — the one whose rationale every reviewer needs to internalize before reading individual tasks. Examples: "Why a shared-secret header instead of mTLS", "Why dual-write instead of online migration". Keep it under ~10 lines plus, if it helps, a small request-flow / state matrix.]

## Tasks

### Group A — [Short name] ([category, e.g. "new feature surface", "server-side migration", "cutover", "cleanup"])

[1–2 sentences: what this group delivers and its blast radius. For groups preceding a cutover, also state the invariant that keeps prod behaviour unchanged (e.g. "no traffic carries the new header yet, so the new rules are inert"). For pure additive groups, a single sentence is enough.]

- [ ] 1. [Task title — describe what is being changed, not "PR — …"]
  - [What to do, with bullet points for each concrete change]
  - [File to create/modify: `path/to/file.ts:line` where useful]
  - [Sub-bullet for tests: what to assert]
  - **Why safe**: [REQUIRED only on (a) cutover tasks — state observable change + revert; (b) tasks in pre-cutover groups — state why this task is a no-op in prod. OMIT on plain additive tasks where the safety is self-evident.]
  - _Requirements: X.X_

- [ ] 2. [Next task]
  - …
  - _Requirements: X.X_

- [ ] 3. Checkpoint — Group A verification
  - Run tests written in this group: `[test command]`
  - Run existing tests for affected files to catch regressions
  - Confirm `main` would still build and pass tests with only Group A's commits applied
  - [Group-specific observable check — only meaningful if the group changed something observable. For a pure additive group, the test-run is the check.]

[OPTIONAL — include the soak paragraph below ONLY between groups separated by a cutover or a destructive step. Omit between plain additive groups.]
_— Stabilize for [duration] before Group B. Monitor: [metric 1], [metric 2], [error/log signal]. —_

### Group B — [Short name] ([category])

[1–2 sentences on what this group delivers. If it follows or contains a cutover, state what changes vs. Group A and what stays preserved.]

[Examples below mix plain implementation, cutover, and external tasks — use only the kinds your plan actually needs.]

- [ ] 4. ⚠️ Cutover — [observable change, e.g. "flip NEXT_PUBLIC_API_URL value"]
  - [Exactly what is changed, where, in what order across environments]
  - **Validation per env**: [bullets — what to check before moving on]
  - **Revert**: [exact steps]
  - _Requirements: X.X_

- [ ] 5. External — [third-party console action, e.g. "add new OAuth callback URL (keep old)"]
  - [Steps in the external system]
  - **Why safe**: [include only if this precedes a cutover and the safety is non-obvious]
  - _Requirements: X.X_

- [ ] 6. Checkpoint — Group B verification
  - [Group-specific checks]

### Group C — [Cleanup / contract step] ⟵ omit this section entirely if there is nothing to clean up

[1–2 sentences: why this is now safe — typically "old code path has had no traffic for N days" or "all consumers migrated in Group B".]

- [ ] 7. [Cleanup task]
  - _Requirements: X.X_

- [ ] N. Final checkpoint — everything green
  - Full test suite passes
  - All requirements traceable to a shipped task
  - [Observable end-state checks — logs, metrics, env state — only when relevant]

## Notes

[Every subsection below is OPTIONAL — include it only if it earns its place. A plain additive feature may only have "Scope boundaries" and nothing else.]

### Atomic-changeset invariants

[Include ONLY if the plan has at least one cutover. Otherwise omit.]

- **Every task before [first cutover] is a no-op in prod.** [One sentence per category — infra-only / env-only / inert code / same-value swap.]
- **Every task between [cutover 1] and [cutover 2] preserves the [old contract].** [What stays the same.]
- **The two cutovers are isolated.** [Why each one can be reverted without the other.]

### Env vars / state at a glance

[Include ONLY when the rollout shifts env values. Drop otherwise.]

| Var | Scope | Before | After cutover 1 | After cutover 2 |
|---|---|---|---|---|
| `EXAMPLE_VAR` | … | … | … | … |

### Safety / threat model

[Include ONLY when the rollout has security-relevant moving parts. Address obvious questions a reviewer will ask: "what if X leaks", "what about spoofing", "what's the blast radius if this is misconfigured".]

- [Concern + mitigation]
- [Concern + mitigation]

### Scope boundaries

- **[X] is out of scope.** [Why, and what handles it instead.]
- [Other deliberate non-goals.]

### Codebase verification findings

[From Step 3 — include ONLY if drift was found. Otherwise drop the section.]

- [Path:line — observation]
```

**Hard rules for the document:**
- Every major task and checkpoint lives inside exactly one `### Group X — …` heading. No orphan tasks.
- A task that does not fit any group means the group plan is wrong — go back to Step 2.5.
- Do **not** use the term "PR" anywhere in the tasks document. Tasks are commits / changesets; the user decides how to bundle them into PRs externally. Use "task", "changeset", "group", "cutover" as appropriate.
- Non-code tasks are titled with a leading `External — …` (third-party consoles) or `Infra — …` (Terraform / cloud) when that distinction is useful.

**Cutover-conditional rules — apply ONLY if the plan has at least one cutover moment (per Step 2.5):**
- Cutover tasks are titled with a leading `⚠️ Cutover — …` and MUST include an explicit revert procedure.
- Groups before the first cutover must be no-ops in production; tasks in those groups carry a `**Why safe**:` line.
- Soak paragraphs (`_— Stabilize for … —_`) sit between groups separated by a cutover or destructive step.
- The Overview gets a "Cutover points" subsection listing each cutover with its revert.

**If the plan has no cutover:**
- No `⚠️` tasks. No "Cutover points" subsection. No soak paragraphs. No "Atomic-changeset invariants" section. No env-vars table. No `**Why safe**:` lines on plain implementation tasks.
- Plan is just groups in dependency order with their checkpoints. Do not pad with cutover language to make it look more thorough.

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

Tag tasks in their title when the kind affects how the implementer (or a future reader) treats them. Tags 4 (cutover) and 7 (soak) only appear when the plan actually has a cutover moment — do not introduce them otherwise.

1. **Implementation** (default, no tag) — Create or modify code
2. **Infra — …** — Terraform, cloud resources, IAM bindings
3. **External — …** — Third-party console action (Google Cloud, Vercel, Stripe, etc.) that a human performs outside the repo
4. **⚠️ Cutover — …** — A single observable production change (env-var flip, code-deploy that switches behaviour). Must include a revert procedure. *Only when an actual cutover exists.*
5. **Cleanup** — Remove old code or config that earlier groups left dual-running
6. **Checkpoint** — Verify a milestone (see Checkpoint Guidelines)
7. **Soak** — A non-task italic paragraph between groups stating what to monitor and for how long before proceeding. *Only between groups separated by a cutover or destructive step.*

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

### Step 5: Confirm and Chain

After creating the document, show the user:
1. The location of the created file
2. The **group plan** — list each group (ID, name, blast radius, dependencies) so the user can sanity-check the merge ordering. Flag any cutovers explicitly; if there are none, say so in one line ("no cutovers — plan is purely additive").
3. A summary of the task breakdown
4. Total counts: groups, major tasks, subtasks, and checkpoints
5. Use the `AskUserQuestion` tool to offer the next step. There is no separate approval step — the plan is ready to execute as soon as it exists. Options:
   - **"Start first group"** — invoke `spec:implement <spec-name> gA` now.
   - **"Run all groups"** — invoke `spec:implement <spec-name>` now.
   - **"Regroup"** — revise the group slicing in place.
   - **"Stop here"** — end; the user can resume later with `spec:implement <spec-name>`.

If the user picks a run option, invoke `spec:implement` now — do not wait for any approval command.

## Arguments

- `$ARGUMENTS` - The spec name via `$0` (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
