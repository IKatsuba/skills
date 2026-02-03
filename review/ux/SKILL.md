---
name: review:ux
description: UX Review - analyzes feature implementation for user experience quality, flow efficiency, and UI consistency
---

# UX Review

Performs a detailed user experience review of a feature being developed. Analyzes user flows, UI consistency, and edge case handling by examining spec documents and the actual codebase implementation. Focuses on what the user sees and does, not on code internals.

## When to use

Use this skill when the user needs to:
- Validate that a feature is convenient and intuitive before release
- Check user flows for unnecessary steps or navigation hops
- Verify UI consistency with the rest of the application
- Ensure edge cases (empty states, errors, loading) are handled gracefully
- Review a feature from the end-user perspective after implementation

## Instructions

### Step 1: Determine Review Target

Parse `<args>` to determine what to review:

1. **Spec name** — if provided, read documents from `.specs/<spec-name>/` (requirements, design, tasks)
2. **File paths** — if provided, review specific files or directories
3. **Branch diff** — if `branch` is specified, review all changes on the current branch vs main

If no arguments provided:
1. Check if there are specs in `.specs/` and list them
2. Check if there are uncommitted changes or branch changes
3. Ask the user what to review

### Step 2: Gather Context

Read all available materials depending on the target:

#### From spec documents (if available):
- `requirements.md` — extract user stories, acceptance criteria, and described user flows
- `design.md` — extract UI components, data flow diagrams, and interaction patterns

#### From codebase:
Use **parallel sub-agents** (`subagent_type: "Explore"`) to investigate:

1. **UI components agent** — find all UI components related to the feature (forms, dialogs, pages, lists, buttons)
2. **Routing agent** — find route definitions and navigation logic for the feature
3. **Error handling agent** — find error boundaries, error messages, toast notifications, fallback UI related to the feature
4. **Existing patterns agent** — examine 2-3 similar existing features in the app to understand established UX patterns (component layouts, form patterns, feedback patterns)

Launch all four agents in a **single message** (parallel tool calls).

### Step 3: Analyze User Flows

For each user flow described in the requirements (or inferred from the code):

#### 3a. Flow Efficiency

| Check | What to look for |
|-------|-----------------|
| **Navigation hops** | Can the user complete the task without leaving the current page? Are related entities creatable inline (modals, dropdowns with quick-add)? |
| **Click count** | Is the number of interactions minimal for the task? Are there redundant confirmation steps? |
| **Data entry** | Are forms pre-filled with sensible defaults? Are optional fields clearly marked? Is field ordering logical? |
| **Feedback** | Does the user get immediate feedback after every action (save, delete, create)? Are success/error states clearly communicated? |
| **Reversibility** | Can the user undo or correct mistakes easily? Is there confirmation before destructive actions? |

#### 3b. Edge Cases and Error States

| Check | What to look for |
|-------|-----------------|
| **Empty states** | What does the user see when a list is empty, data hasn't loaded, or no results match a filter? Is there a clear call-to-action? |
| **Loading states** | Are loading indicators shown during async operations? Are skeleton screens or spinners used appropriately? |
| **Error messages** | Are errors user-friendly (not technical stack traces)? Do they explain what happened and what the user can do? |
| **Validation** | Is form validation shown inline as the user types, or only on submit? Are validation messages clear and specific? |
| **Boundary conditions** | What happens with very long text, many items, special characters, or zero values? |
| **Concurrent actions** | What happens if the user double-clicks a submit button or navigates away mid-operation? |

#### 3c. UI Consistency

| Check | What to look for |
|-------|-----------------|
| **Component reuse** | Does the feature use existing UI components from the project, or does it introduce new ones for similar purposes? |
| **Layout patterns** | Are page layouts, spacing, and section ordering consistent with the rest of the app? |
| **Interaction patterns** | Do similar actions (create, edit, delete) follow the same patterns as in other parts of the app? |
| **Terminology** | Are labels, button texts, and messages consistent with the vocabulary used elsewhere? |
| **Visual hierarchy** | Are primary actions visually prominent? Are secondary actions de-emphasized? |
| **Responsive behavior** | If the app supports it, does the feature work on different screen sizes? |

### Step 4: Cross-Reference with Spec

If spec documents are available, verify:

1. **All user stories covered** — every user story in requirements has a corresponding UI flow
2. **Acceptance criteria met** — each acceptance criterion is achievable through the implemented UI
3. **Design followed** — UI components match what the design document describes
4. **No orphan UI** — no screens or flows exist that aren't backed by requirements

### Step 5: Generate UX Review Report

Present a structured report:

```markdown
# UX Review: [Feature Name]

**Scope:** [What was reviewed — spec docs, files, branch diff]
**Overall UX Assessment:** [Good / Needs Improvement / Major Issues]

---

## User Flows Analyzed

1. [Flow name] — [Brief description]
2. [Flow name] — [Brief description]

---

## 🔴 Critical UX Issues

> Problems that will confuse or block users

### [Issue Title]
**Flow:** [Which user flow is affected]
**Location:** `path/to/component.tsx` (or spec document section)

[Description: what the user experiences and why it's a problem]

**Recommendation:** [How to improve the experience]

---

## 🟠 UX Warnings

> Issues that degrade the experience

- **[Flow/Location]** — [Brief description of the friction point]
- **[Flow/Location]** — [Brief description of the friction point]

---

## 🟡 UX Suggestions

> Enhancements that would polish the experience

- [Suggestion 1]
- [Suggestion 2]

---

## ✅ What Works Well

- [Positive UX observation 1]
- [Positive UX observation 2]

---

## Edge Case Coverage

| Scenario | Status | Notes |
|----------|--------|-------|
| Empty state | ✅ / ⚠️ / ❌ | [How it's handled] |
| Loading state | ✅ / ⚠️ / ❌ | [How it's handled] |
| Error state | ✅ / ⚠️ / ❌ | [How it's handled] |
| Long content | ✅ / ⚠️ / ❌ | [How it's handled] |
| No permissions | ✅ / ⚠️ / ❌ | [How it's handled] |

---

## UI Consistency Check

| Aspect | Consistent | Notes |
|--------|-----------|-------|
| Component reuse | ✅ / ⚠️ / ❌ | [Details] |
| Layout patterns | ✅ / ⚠️ / ❌ | [Details] |
| Interaction patterns | ✅ / ⚠️ / ❌ | [Details] |
| Terminology | ✅ / ⚠️ / ❌ | [Details] |

---

## Summary

- **Critical:** [N] issues
- **Warnings:** [N] issues
- **Suggestions:** [N] items
- **Edge cases covered:** [N/M]
```

### Step 6: Offer Next Steps

After presenting the report, offer actions:

1. **Fix issues** — help update the spec documents or code to resolve UX findings
2. **Re-review** — run the review again after changes
3. **Deep dive** — analyze a specific flow or issue in more detail
4. **Proceed** — continue with implementation despite findings

## Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| 🔴 Critical | User is blocked, confused, or loses data; flow requires unnecessary navigation hops for basic tasks | Must fix |
| 🟠 Warning | User can complete the task but with friction; inconsistent patterns; missing feedback | Should fix |
| 🟡 Suggestion | Polish improvements; better defaults; minor wording changes | Nice to have |

## Arguments

- `<args>` - Spec name, file paths, or review scope
  - `<spec-name>` — review UX based on spec documents and related code
  - `<file-path>` — review UX of specific files or directories
  - `branch` — review UX of all changes on current branch vs main

Examples:
- `review:ux user-auth` — review UX for the user-auth feature spec
- `review:ux src/pages/settings/` — review UX of the settings pages
- `review:ux branch` — review UX of all UI changes on the current branch
