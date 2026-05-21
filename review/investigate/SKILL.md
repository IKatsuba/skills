---
name: review:investigate
description: Investigate Problem - analyzes a problem in the codebase and proposes actionable solutions
argument-hint: ["problem description"]
---

# Investigate Problem

Performs a focused investigation of a specific problem — bug, performance issue, unexpected behavior, or technical challenge — and proposes concrete solutions. Works directly without spec files: understand the problem, dig into the code, and present options.

## When to use

Use this skill when the user needs to:
- Understand why something is broken or behaving unexpectedly
- Get solution options for a specific technical problem
- Investigate a bug, error, or performance issue
- Explore approaches to a focused challenge without full spec overhead

## Instructions

### Step 1: Understand the Problem

If `$ARGUMENTS` contains a problem description, use it as starting context.

Use the `AskUserQuestion` tool to clarify:
1. **What is the problem?** — symptoms, error messages, unexpected behavior
2. **Where does it happen?** — specific files, components, endpoints, user flows
3. **When did it start?** — recent change, always been there, intermittent
4. **What has been tried?** — previous attempts to fix, workarounds in place

Provide meaningful options where possible (e.g., "bug", "performance", "unexpected behavior", "design question"). Skip questions the user has already answered.

### Step 2: Investigate the Codebase

Launch **parallel** `Task` tools with `subagent_type=Explore` to investigate:

1. **Root cause agent** — trace the problem through the code, find the source of the issue. Follow the data flow, identify where behavior diverges from expectations.
2. **Context agent** — find related code, tests, recent changes (git log), and similar patterns elsewhere in the codebase that work correctly.

Look for:
- The exact point where the bug or issue originates
- Related tests that pass or fail
- Recent commits that may have introduced the problem
- Similar patterns in the codebase that handle this correctly

### Step 3: Research External Sources (if needed)

If the problem involves libraries, frameworks, or external APIs:

1. Use `resolve-library-id` and `query-docs` from Context7 MCP to check documentation for known issues, correct usage, or recent API changes
2. Use `WebSearch` to find known bugs, GitHub issues, or community solutions

Skip this step if the problem is purely internal to the codebase.

### Step 4: Propose Solutions

Present findings and solutions to the user in this structure:

```
## Problem Summary

[One paragraph explaining the root cause or nature of the problem]

## Evidence

- [What was found in the code — specific files and lines]
- [Relevant test results or git history]
- [Documentation or external references if applicable]

## Proposed Solutions

### Solution 1: [Name] (Recommended)

**What to do:** [Concrete steps — which files to change, what to add/remove]

**Why it works:** [How this addresses the root cause]

**Effort:** [Low / Medium / High]
**Risk:** [Low / Medium / High]

### Solution 2: [Name]

**What to do:** [Concrete steps]

**Why it works:** [Explanation]

**Effort:** [Low / Medium / High]
**Risk:** [Low / Medium / High]

### Solution 3: [Name] (if applicable)

[Same structure]
```

Guidelines for solutions:
- Always lead with the **recommended** solution
- Provide 2-3 solutions — not more, not fewer (unless the fix is trivial, then 1 is fine)
- Each solution must be **concrete** — name specific files, functions, and changes
- Clearly mark effort and risk
- If only one viable solution exists, say so and explain why alternatives don't work

### Step 5: Discuss Next Steps

Use the `AskUserQuestion` tool to ask the user how to proceed, with options like:
- "Implement Solution 1"
- "Implement Solution 2"
- "Investigate deeper"
- "I'll handle it myself"

If the user chooses to implement, apply the chosen solution directly — make the code changes, run relevant tests, and verify the fix.

## Arguments

- `$ARGUMENTS` - Problem description (optional, free-form text)
  - Can include error messages, file paths, or symptom descriptions
  - If empty, the skill will ask interactively

Examples:
- `investigate login fails after session timeout` - Investigate a specific bug
- `investigate why API response is slow on /users endpoint` - Investigate performance
- `investigate` - Start interactive problem gathering
