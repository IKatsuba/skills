---
name: spec:approve
description: Approve Document - promotes a spec document to APPROVED status, unblocking downstream pipeline skills. Use when ready to advance the pipeline.
argument-hint: <spec-name> [requirements|research|design|tasks|test-plan|all]
disable-model-invocation: true
---

# Approve Document

Promotes a specification document from DRAFT or IN_REVIEW to APPROVED status. Performs lightweight structural validation before approval. Shows what downstream skills are unblocked and suggests the next step.

## When to use

Use this skill when the user needs to:
- Approve a spec document after review or authoring
- Unblock downstream pipeline skills that require APPROVED prerequisites
- Check what becomes available after approval

## Instructions

### Step 1: Determine Target

Parse `$ARGUMENTS` to determine:
1. **Spec name** (`$0`) — which specification
2. **Document name** (`$1`, optional) — `requirements`, `research`, `design`, `tasks`, `test-plan`

If `$0` is not provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose.

If no document name provided, scan `.specs/<spec-name>/` for all documents, read their frontmatter, and show a status summary:

```
Documents for <spec-name>:
  requirements.md  — DRAFT (created 2026-03-20)
  research.md      — APPROVED (updated 2026-03-22)
  design.md        — DRAFT (created 2026-03-24)
```

Then use the `AskUserQuestion` tool to ask which document to approve. Only show documents with status DRAFT or IN_REVIEW as options.

### Step 2: Validate Structure

Read the target document. Perform lightweight structural validation (not content quality — that is `spec:review`'s job):

| Document | Minimum criteria |
|----------|-----------------|
| requirements.md | Has at least one requirement with acceptance criteria using SHALL or WHEN-THEN |
| research.md | Has at least one problem area with 2+ variants; exactly one CHOSEN per area |
| design.md | Has a Mermaid diagram block and a Components/Interfaces section |
| tasks.md | Has at least one task with a checkbox `[ ]` and a `_Requirements:` reference |
| test-plan.md | Has at least one test case with Steps and Expected sections |

If validation fails, report the specific issues and use the `AskUserQuestion` tool with options: "Approve anyway", "Fix issues first", "Cancel".

### Step 3: Update Status

1. Update the document's YAML frontmatter:
   - Set `status: APPROVED`
   - Set `updated: <today's date YYYY-MM-DD>`
2. Save the file

### Step 4: Show Impact

Determine what is now unblocked:

| Document approved | Unblocks (hard gate) |
|---|---|
| requirements | `spec:research` |
| research | _(soft gate only — no hard unblock)_ |
| design | `spec:tasks`, `spec:test-plan` |
| tasks | `spec:implement` |
| test-plan | `spec:test` (also requires implementation complete) |

Display:

```
✅ Approved: <spec-name>/<document>.md

Unblocked:
  → spec:<skill> <spec-name> — now ready to run

Pipeline:
  requirements.md  — APPROVED
  research.md      — DRAFT
  design.md        — (not created)
  tasks.md         — (not created)
  test-plan.md     — (not created)

Suggested next: spec:<next-skill> <spec-name>
```

Use the `AskUserQuestion` tool to offer 2-3 relevant next actions.

### Step 5: Commit

Stage the modified document and invoke the `git:commit` skill.

## Arguments

- `$ARGUMENTS` - Spec name and optionally document name
  - `$0` — spec name (e.g., "user-auth"); if omitted, show list and ask
  - `$1` — document name: `requirements`, `research`, `design`, `tasks`, `test-plan`, or `all`; if omitted, show documents and ask

Examples:
- `spec:approve user-auth` — show documents, ask which to approve
- `spec:approve user-auth requirements` — approve requirements.md
- `spec:approve user-auth all` — approve all pending documents
