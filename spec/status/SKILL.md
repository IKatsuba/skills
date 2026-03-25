---
name: spec:status
description: Spec Status - displays pipeline progress dashboard for a single specification showing document statuses, blockers, and next action.
argument-hint: <spec-name>
context: fork
agent: Explore
---

# Spec Status

Displays a pipeline dashboard for a single specification. Reads all documents, checks their statuses, and shows the current phase, blockers, and next action.

## When to use

Use this skill when the user needs to:
- See where a spec is in the pipeline
- Understand what is blocking progress
- Get a recommendation for the next step

## Instructions

### Step 1: Find the Spec

1. If `<args>` contains a spec name, use it directly
2. If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose
3. If `.specs/` does not exist or is empty, inform the user: "No specs found. Run `spec:requirements` to create one."

### Step 2: Read All Documents

Scan `.specs/<spec-name>/` and read the frontmatter of every document that exists:
- `requirements.md`
- `research.md`
- `design.md`
- `tasks.md`
- `test-plan.md`

For each document, extract:
- **status** from frontmatter (`DRAFT`, `IN_REVIEW`, `APPROVED`, `SUPERSEDED`). If no frontmatter, treat as `DRAFT`.
- **created** and **updated** dates

For `tasks.md`, also count checkboxes: `[x]` done, `[-]` in progress, `[ ]` pending.

For `test-plan.md`, also count: `[x]` passed, `[!]` failed, `[s]` skipped, `[ ]` pending.

### Step 3: Display Dashboard

Present to the user:

```
# Spec: <spec-name>

| Document         | Status   | Updated    |
|------------------|----------|------------|
| requirements.md  | APPROVED | 2026-03-20 |
| research.md      | APPROVED | 2026-03-22 |
| design.md        | DRAFT    | 2026-03-24 |
| tasks.md         | —        | —          |
| test-plan.md     | —        | —          |

Pipeline:
✅ Requirements → ✅ Research → 🔄 Design → ⏳ Tasks → ⏳ Implement
                                                     → ⏳ Test Plan → ⏳ Test
```

Use these icons:
- ✅ — document APPROVED
- 🔄 — document exists (DRAFT or IN_REVIEW)
- ⏳ — document not created yet
- ⚠️ — document SUPERSEDED (needs attention)

If `tasks.md` has progress, show: `Tasks: 8/12 done (2 in progress)`

If `test-plan.md` has progress, show: `Tests: 5/10 passed, 1 failed, 0 skipped`

### Step 4: Identify Blockers

Check the gate table for the next logical skill:

| Next skill | Hard gate required |
|---|---|
| `spec:research` | requirements APPROVED |
| `spec:design` | requirements APPROVED |
| `spec:tasks` | design APPROVED |
| `spec:test-plan` | design APPROVED |
| `spec:implement` | tasks APPROVED |
| `spec:test` | test-plan APPROVED + all tasks `[x]` |

Report blockers:
- **Hard blocker**: "`<document>` is `<status>` — must be APPROVED before `<skill>` can run"
- **SUPERSEDED warning**: "`<document>` is SUPERSEDED — re-run the generating skill and re-approve"

### Step 5: Suggest Next Action

Based on current state:
1. Most recent document is DRAFT → suggest `spec:approve` or `spec:review`
2. Most recent document is APPROVED, next document missing → suggest the next generating skill
3. Implementation in progress → suggest `spec:implement <name> next`
4. Implementation complete, tests not started → suggest `spec:test-plan` or `spec:test`
5. Tests in progress → suggest `spec:test <name> next`
6. Any document SUPERSEDED → suggest re-running the generating skill

Use the `AskUserQuestion` tool with 2-3 relevant options.

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

Examples:
- `spec:status user-auth` — show pipeline dashboard for user-auth
- `spec:status` — list specs, ask which to show
