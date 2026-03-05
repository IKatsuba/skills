# Specification Skills

Skills for specification-driven development workflow.

## Workflow

### Phase 1: Specification

1. **`/spec:plan <name>`** — Creates `.specs/<name>/requirements.md`
2. **`/spec:research <name>`** — Creates `.specs/<name>/research.md`
3. **`/spec:design <name>`** — Creates `.specs/<name>/design.md`
4. **`/spec:breakdown <name>`** — Creates `.specs/<name>/tasks.md`

### Phase 2: Implementation

5. **`/spec:implement <name>`** — Execute all tasks automatically
6. **`/spec:implement <name> next`** — Execute tasks one at a time with review
7. **`/spec:implement <name> <N>`** — Execute a specific task by number

### Phase 3: Testing

8. **`/spec:test-plan <name>`** — Creates `.specs/<name>/test-plan.md`
9. **`/spec:test <name>`** — Walk through all pending tests
10. **`/spec:test <name> next`** — Execute one test at a time
11. **`/spec:test <name> <N>`** — Execute a specific test by number

### Review (any stage)

**`/spec:review <name>`** — Validate spec documents for quality and consistency

## Available Skills

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

## Output Structure

```
.specs/
└── <spec-name>/
    ├── requirements.md   # User stories and acceptance criteria
    ├── research.md       # Research findings and chosen solutions
    ├── design.md         # Architecture, components, interfaces
    ├── tasks.md          # Implementation plan with checkboxes
    └── test-plan.md      # Manual test plan with test cases
```

## Installation

```bash
# All spec skills
npx add-skill ikatsuba/skills/spec

# Individual skills
npx add-skill ikatsuba/skills --skill spec:plan
npx add-skill ikatsuba/skills --skill spec:research
npx add-skill ikatsuba/skills --skill spec:design
npx add-skill ikatsuba/skills --skill spec:breakdown
npx add-skill ikatsuba/skills --skill spec:implement
npx add-skill ikatsuba/skills --skill spec:review
npx add-skill ikatsuba/skills --skill spec:test-plan
npx add-skill ikatsuba/skills --skill spec:test
```
