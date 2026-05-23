# Review Skills

Code and UX review skills for quality assurance before committing or releasing.

## Available Skills

| Skill | Description |
|-------|-------------|
| [`review:diff`](diff/) | Diff review with structured feedback before committing |
| [`review:ux`](ux/) | Detailed UX review — user flows, edge cases, and UI consistency |
| [`review:investigate`](investigate/) | Analyze a problem in the codebase and propose actionable solutions |

## Diff Review

Analyze code changes for bugs, security issues, and code quality.

### Usage

```bash
/review:diff                # Auto-detect changes to review
/review:diff staged         # Review staged changes only
/review:diff branch         # Review all branch changes vs main
/review:diff src/auth/      # Review specific directory
```

## UX Review

Review features from the end-user perspective: flow efficiency, edge case handling, and UI consistency.

### Usage

```bash
/review:ux user-auth            # UX review based on spec documents
/review:ux src/pages/settings/  # UX review of specific files
/review:ux branch               # UX review of all UI changes on branch
```

### What it checks

- **User flows** — navigation hops, click count, inline entity creation, feedback after actions
- **Edge cases** — empty states, loading states, error messages, validation, boundary conditions
- **UI consistency** — component reuse, layout patterns, interaction patterns, terminology

## Investigate Problem

Investigate a bug, performance issue, or unexpected behavior — and get concrete solution proposals.

### Usage

```bash
/review:investigate                            # Start interactive problem gathering
/review:investigate login fails after timeout  # Investigate a specific bug
/review:investigate slow /users endpoint       # Investigate performance issue
```

### What it does

1. Clarifies the problem (symptoms, location, history)
2. Investigates the codebase — traces root cause and finds related patterns
3. Checks external docs/issues if libraries are involved
4. Proposes 2-3 concrete solutions with effort/risk assessment
5. Optionally implements the chosen solution

## Installation

```bash
npx skills add ikatsuba/skills/review
```

The CLI will prompt to pick which review skills to install. For a single skill, use `npx skills add ikatsuba/skills --skill <name>`.
