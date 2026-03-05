# Skills

> A collection of skills for Claude Code, Codex, Cursor and OpenCode to supercharge your specification-driven development workflow!

## Quick Start

```bash
npx add-skill ikatsuba/skills
```

That's it! You're ready to go.

---

## Installation Options

### Install specific skills

Pick only what you need:

```bash
npx add-skill ikatsuba/skills --skill spec:plan
npx add-skill ikatsuba/skills --skill spec:research
npx add-skill ikatsuba/skills --skill spec:design
npx add-skill ikatsuba/skills --skill spec:breakdown
npx add-skill ikatsuba/skills --skill spec:implement
npx add-skill ikatsuba/skills --skill spec:test-plan
npx add-skill ikatsuba/skills --skill spec:test
npx add-skill ikatsuba/skills --skill utils:changelog
npx add-skill ikatsuba/skills --skill review:local
npx add-skill ikatsuba/skills --skill review:ux
```

### Global installation

Want skills everywhere? Go global:

```bash
npx add-skill ikatsuba/skills -g
```

### Browse available skills

```bash
npx add-skill ikatsuba/skills --list
```

---

## Available Skills

### Specification Pipeline

| Skill | Description |
|-------|-------------|
| `spec:plan` | Plan requirements — user stories, acceptance criteria |
| `spec:research` | Technical research — solution alternatives with pros/cons |
| `spec:design` | Technical design — architecture diagrams, interfaces |
| `spec:breakdown` | Task breakdown — implementation plan with checkboxes |
| `spec:implement` | Implement tasks — execute all, next, or specific task |
| `spec:review` | Review — validate documents for quality and consistency |
| `spec:test-plan` | Test plan — generate manual test scenarios |
| `spec:test` | Execute tests — walk through all, next, or specific test |

### Utility

| Skill | Description |
|-------|-------------|
| `utils:changelog` | Generate human-readable changelogs for product, marketing, and support teams |

### Code Review

| Skill | Description |
|-------|-------------|
| `review:local` | Perform local code review with structured feedback before committing |
| `review:ux` | Detailed UX review — user flows, edge cases, and UI consistency |

---

## Workflow

These skills support a complete specification-driven development workflow:

### Phase 1: Specification

Build your blueprint:

1. **`/spec:plan <name>`** — Creates `.specs/<name>/requirements.md`
2. **`/spec:research <name>`** — Creates `.specs/<name>/research.md`
3. **`/spec:design <name>`** — Creates `.specs/<name>/design.md`
4. **`/spec:breakdown <name>`** — Creates `.specs/<name>/tasks.md`

### Phase 2: Implementation

Let the magic happen:

5. **`/spec:implement <name>`** — Execute all tasks automatically
6. **`/spec:implement <name> next`** — Execute tasks one at a time with review
7. **`/spec:implement <name> <N>`** — Execute a specific task by number

### Phase 3: Testing

Verify your implementation:

8. **`/spec:test-plan <name>`** — Generate manual test plan
9. **`/spec:test <name>`** — Walk through all pending tests
10. **`/spec:test <name> next`** — Execute one test at a time
11. **`/spec:test <name> <N>`** — Execute a specific test by number

### Code Review

Review your code before committing:

```bash
/review:local                # Auto-detect changes to review
/review:local staged         # Review staged changes only
/review:local branch         # Review all branch changes vs main
/review:local src/auth/      # Review specific directory
```

### UX Review

Review the user experience of a feature:

```bash
/review:ux user-auth         # UX review based on spec documents
/review:ux src/pages/settings/  # UX review of specific files
/review:ux branch            # UX review of all UI changes on branch
```

### Changelog Generation

Keep your stakeholders in the loop:

```bash
/utils:changelog last week           # Changes from the past 7 days
/utils:changelog since 2024-01-01    # All changes since a date
/utils:changelog v1.0.0..v1.1.0      # Changes between releases
```

---

## Documents Structure

```
.specs/
└── <spec-name>/
    ├── requirements.md   # User stories and acceptance criteria
    ├── research.md       # Research findings and chosen solutions
    ├── design.md         # Architecture, components, interfaces
    ├── tasks.md          # Implementation plan with checkboxes
    └── test-plan.md      # Manual test plan with test cases
```

---

## License

MIT
