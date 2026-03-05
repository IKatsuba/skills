# Review Skills

Code and UX review skills for quality assurance before committing or releasing.

## Available Skills

| Skill | Description |
|-------|-------------|
| `review:diff` | Diff review with structured feedback before committing |
| `review:ux` | Detailed UX review — user flows, edge cases, and UI consistency |

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

## Installation

```bash
# All review skills
npx add-skill ikatsuba/skills/review

# Individual skills
npx add-skill ikatsuba/skills --skill review:diff
npx add-skill ikatsuba/skills --skill review:ux
```
