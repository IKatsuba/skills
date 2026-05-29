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

1. If `$0` contains a spec name, use it directly
2. If `$0` is not provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose
3. If `.specs/` does not exist or is empty, inform the user: "No specs found. Run `spec:requirements` to create one."

### Step 2: Read All Documents

Scan `.specs/<spec-name>/` and note which of these documents **exist**:
- `requirements.md`
- `research.md`
- `design.md`
- `tasks.md`
- `test-plan.md`

Progress is tracked by file existence and checkbox counts — there is no approval status. For each document that exists, extract its `updated` date from frontmatter (if present).

For `tasks.md`, also count checkboxes: `[x]` done, `[-]` in progress, `[ ]` pending.

For `test-plan.md`, also count: `[x]` passed, `[!]` failed, `[s]` skipped, `[ ]` pending.

### Step 3: Display Dashboard

Present to the user:

```
# Spec: <spec-name>

| Document         | Exists | Updated    |
|------------------|--------|------------|
| requirements.md  | ✅     | 2026-03-20 |
| research.md      | ✅     | 2026-03-22 |
| design.md        | ✅     | 2026-03-24 |
| tasks.md         | —      | —          |
| test-plan.md     | —      | —          |

Pipeline:
✅ Requirements → ✅ Research → 🔄 Design → ⏳ Tasks → ⏳ Implement
                                                     → ⏳ Test Plan → ⏳ Test
```

Use these icons:
- ✅ — document exists and the next phase has started (a downstream document exists)
- 🔄 — document exists and is the most recent phase (work likely in progress here)
- ⏳ — document not created yet

If `tasks.md` has progress, show: `Tasks: 8/12 done (2 in progress)`

If `test-plan.md` has progress, show: `Tests: 5/10 passed, 1 failed, 0 skipped`

### Step 4: Identify Blockers

Each skill requires its prerequisite **document to exist** (no approval needed):

| Next skill | Prerequisite (must exist) |
|---|---|
| `spec:research` | requirements.md |
| `spec:design` | requirements.md (research.md recommended) |
| `spec:tasks` | design.md |
| `spec:test-plan` | design.md |
| `spec:implement` | tasks.md (test-plan.md recommended) |
| `spec:test` | test-plan.md + all tasks `[x]` |

Report blockers:
- **Missing prerequisite**: "`<document>` does not exist — run `<generating skill>` before `<skill>` can run"

### Step 5: Suggest Next Action

Based on current state:
1. Most recent document exists, next document missing → suggest the next generating skill
2. Want a quality check on the latest document → suggest `spec:review`
3. Implementation in progress → suggest `spec:implement <name> next`
4. Implementation complete, tests not started → suggest `spec:test-plan` or `spec:test`
5. Tests in progress → suggest `spec:test <name> next`

Use the `AskUserQuestion` tool with 2-3 relevant options.

## Arguments

- `$ARGUMENTS` - The spec name
  - `$0` — spec name (e.g., "user-auth", "payment-flow")

Examples:
- `spec:status user-auth` — show pipeline dashboard for user-auth
- `spec:status` — list specs, ask which to show
