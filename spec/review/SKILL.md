---
name: spec:review
description: Review Specification - validates documents for completeness, quality, and consistency against the codebase. Use when checking spec quality at any pipeline stage.
role: Staff Engineer
argument-hint: <spec-name> [requirements|research|design|tasks|all]
---

# Review Specification

## Role

You are a **Staff Engineer** reviewing for quality. Your job is to find problems others missed, not to validate that everything looks fine.

- Check documents against the codebase, not just against each other
- Apply severity levels honestly — do not downgrade critical issues to avoid confrontation
- Verify cross-document consistency: requirements → research → design → tasks
- Never approve by default — explicitly verify each criterion

Reviews one or more specification documents (requirements, research, design, tasks) for completeness, quality, internal consistency, and alignment with the actual codebase. Can be invoked at **any stage** of the pipeline — after requirements, after research, after design, or after tasks. It reviews whatever documents exist at that point and checks their quality and mutual consistency. Partial reviews (e.g., only requirements exist) are normal and expected.

## When to use

Use this skill when the user needs to:
- Validate a specification at any stage of the pipeline
- Check consistency between whatever documents exist (requirements, research, design, tasks)
- Verify that spec documents accurately reflect the codebase
- Get structured feedback on document quality

## Instructions

### Step 1: Determine Review Scope

Parse `<args>` to determine:

1. **Spec name** — which specification to review
2. **Document scope** — which documents to review:
   - `requirements` — review only requirements.md
   - `research` — review only research.md
   - `design` — review only design.md
   - `tasks` — review only tasks.md
   - `all` (default if omitted) — review all available documents

If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose.

Locate documents in `.specs/<spec-name>/`:
- `requirements.md`
- `research.md`
- `design.md`
- `tasks.md`

If a requested document does not exist, report it and review only the available ones.

### Step 2: Read Documents

Read all documents in scope. If reviewing `all`, also note which documents are missing — their absence is itself a finding.

After reading all documents in scope, update the frontmatter of each document being reviewed: set `status: IN_REVIEW` (only if current status is `DRAFT` — do not downgrade from `APPROVED` or `SUPERSEDED`) and set `updated: <today's date YYYY-MM-DD>`.

### Step 3: Review Each Document

For each document in scope, check the criteria below. Use **parallel sub-agents** (`subagent_type: "Explore"`) to investigate the codebase where needed.

#### 3a. Requirements Review

| Criteria | What to check |
|----------|---------------|
| **Completeness** | Are there enough requirements to describe the feature? Are user stories present? |
| **Testability** | Does every acceptance criterion use SHALL / WHEN-THEN / SHALL NOT format? Can each one be objectively verified? |
| **Atomicity** | Is each requirement a single, independent statement? No compound requirements? |
| **Clarity** | No ambiguous language ("should", "might", "ideally")? No undefined terms without a glossary entry? |
| **Codebase alignment** | Do referenced components, services, or APIs actually exist? Are names consistent with the codebase? |
| **User experience** | Do the described user flows feel natural? Are there cases where the user is forced to navigate between unrelated pages to complete a single logical action? For related entities (e.g., category + subcategory), can the user create or select dependent entities inline without leaving the current context? Flag any flow that requires unnecessary navigation hops. |

#### 3b. Design Review

| Criteria | What to check |
|----------|---------------|
| **Requirements coverage** | Does the design address every requirement? Are any requirements missing from the design? |
| **Architecture** | Are component diagrams present? Do they accurately reflect the project structure? |
| **Interfaces** | Are all new interfaces and types defined? Are they compatible with existing code? |
| **Data flow** | Is the data flow described and diagrammed? Are edge cases covered? |
| **Error handling** | Are error types documented? Do they match the project's error handling patterns? |
| **Testing strategy** | Is a testing approach defined? Are test examples relevant? |
| **Codebase alignment** | Do file paths, module names, and patterns match reality? Are existing APIs used correctly? |
| **User experience** | Does the designed data flow support inline/contextual creation of related entities? Are there unnecessary round-trips or page navigations that could be eliminated? Do UI components allow quick creation of dependent objects (e.g., creating a parent entity from a child entity form via inline dialog or dropdown action)? |

#### 3c. Research Review

| Criteria | What to check |
|----------|---------------|
| **Requirements coverage** | Does the research address all major problem areas from the requirements? Are any significant requirements overlooked? |
| **Variant quality** | Are there at least 2 distinct variants per problem area? Are they meaningfully different (not minor variations)? |
| **CHOSEN/Rejected marking** | Is every variant clearly marked as CHOSEN or Rejected? Is there exactly one CHOSEN variant per problem area? |
| **Evidence basis** | Are variant assessments backed by documentation, codebase examples, or benchmarks? Are pros/cons concrete rather than vague? |
| **Codebase alignment** | Do the proposed solutions respect existing architectural patterns? Are integration points accurately identified? |
| **Clarity** | Are chosen solutions described clearly enough for the design phase to implement them without ambiguity? |

#### 3d. Tasks Review

| Criteria | What to check |
|----------|---------------|
| **Requirements traceability** | Does every task reference requirements with `_Requirements: X.X_`? Are all requirements covered by at least one task? |
| **Design alignment** | Do tasks follow the architecture from the design? Are file paths consistent with the design? |
| **Completeness** | Are there enough tasks to implement the full feature? Are testing and verification tasks included? |
| **Ordering** | Are dependencies respected? Do prerequisite tasks come before dependent ones? |
| **Actionability** | Is each subtask specific enough to implement? Does it include file paths and key implementation points? |
| **Checkpoints** | Are verification checkpoints present after major milestones? |
| **Codebase alignment** | Do mentioned files exist (for modifications) or do parent directories exist (for new files)? |

### Step 4: Cross-Document Consistency (when reviewing multiple documents)

If two or more documents are available, check cross-document consistency. Only check consistency for document pairs that both exist — partial reviews are normal:

1. **Requirements → Research** — every major problem area from requirements is investigated in research; no significant requirements are overlooked
2. **Requirements → Design** — every requirement has a corresponding design component
3. **Research → Design** — CHOSEN variants from research are reflected in the design; any deviation has explicit rationale
4. **Design → Tasks** — every design component has implementation tasks
5. **Requirements → Tasks** — every requirement is traceable through to tasks
6. **Research → Tasks** — tasks implement the chosen solutions from research, not the rejected ones
7. **Terminology** — names, terms, and file paths are consistent across all documents
8. **No orphans** — no tasks reference non-existent requirements; no design components lack a requirements basis
9. **UX flow coherence** — user flows described in requirements are preserved through design and tasks without introducing unnecessary navigation steps or degrading the user experience. If design or tasks split a single user action into multiple disconnected steps (e.g., requiring the user to visit a separate page to create a related entity before returning), flag it as a critical issue.

### Step 5: Generate Review Report

Present a structured report:

```markdown
# Specification Review: [spec-name]

**Documents reviewed:** [list]
**Overall assessment:** [Good / Needs Improvement / Major Issues]

---

## 🔴 Critical Issues

> Problems that must be fixed before proceeding

### [Issue Title]
**Document:** `requirements.md` | `design.md` | `tasks.md`
**Section:** [section reference]

[Description of the issue and why it matters]

**Recommendation:** [How to fix it]

---

## 🟠 Warnings

> Issues that should be addressed

- **[document:section]** — [Brief description]
- **[document:section]** — [Brief description]

---

## 🟡 Suggestions

> Optional improvements

- [Suggestion 1]
- [Suggestion 2]

---

## ✅ What Looks Good

- [Positive observation 1]
- [Positive observation 2]

---

## Coverage Matrix

| Requirement | Research | Design | Tasks | Status |
|-------------|----------|--------|-------|--------|
| 1.1 [name]  | Yes/No   | Yes/No | Yes/No | ✅ / ⚠️ / ❌ |
| 1.2 [name]  | Yes/No   | Yes/No | Yes/No | ✅ / ⚠️ / ❌ |

---

## Summary

- **Critical:** [N] issues
- **Warnings:** [N] issues
- **Suggestions:** [N] items
```

Omit the Coverage Matrix section when reviewing a single document that is not tasks.

### Step 6: Offer Next Steps

After presenting the report, use the `AskUserQuestion` tool to offer next steps, with options like:

1. "Fix issues" — help update the documents to resolve findings
2. "Re-review" — run the review again after changes
3. "Proceed anyway" — continue to the next stage despite findings
4. "Explain a finding" — provide more detail on any finding

## Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| 🔴 Critical | Missing requirements, design gaps, broken traceability, codebase contradictions | Must fix before proceeding |
| 🟠 Warning | Ambiguous wording, weak test coverage, minor inconsistencies | Should fix |
| 🟡 Suggestion | Style improvements, additional edge cases, clearer wording | Nice to have |

## Arguments

- `<args>` - Spec name and optionally which document(s) to review
  - `<spec-name>` — review all documents (default)
  - `<spec-name> requirements` — review only requirements
  - `<spec-name> design` — review only design
  - `<spec-name> tasks` — review only tasks
  - `<spec-name> all` — review all (explicit)

Examples:
- `spec:review user-auth` — review all available documents for user-auth
- `spec:review user-auth requirements` — review only requirements
- `spec:review user-auth research` — review only the research document
- `spec:review user-auth design` — review only the design document
- `spec:review payment-flow tasks` — review only the tasks document
