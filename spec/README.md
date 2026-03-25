# Specification Skills

Skills for specification-driven development workflow with phase gating and role-based specialists.

## Pipeline

Each phase must be approved (`spec:approve`) before the next can begin.

```
spec:requirements → spec:research → spec:design → spec:tasks    → spec:implement
                                                → spec:test-plan → spec:test
```

### Phase 1: Specification

1. **`/spec:requirements <name>`** — Creates `.specs/<name>/requirements.md` [Product Analyst]
2. **`/spec:research <name>`** — Creates `.specs/<name>/research.md` [Technical Researcher]
3. **`/spec:design <name>`** — Creates `.specs/<name>/design.md` [Software Architect]
4. **`/spec:tasks <name>`** — Creates `.specs/<name>/tasks.md` [Technical Lead]
5. **`/spec:test-plan <name>`** — Creates `.specs/<name>/test-plan.md` [QA Engineer]

### Phase 2: Implementation

6. **`/spec:implement <name>`** — Execute all tasks automatically [Senior Engineer]
7. **`/spec:implement <name> next`** — Execute tasks one at a time with review
8. **`/spec:implement <name> <N>`** — Execute a specific task by number

### Phase 3: Testing

9. **`/spec:test <name>`** — Walk through all pending tests [QA Engineer]
10. **`/spec:test <name> next`** — Execute one test at a time
11. **`/spec:test <name> <N>`** — Execute a specific test by number

### Pipeline Management

- **`/spec:approve <name> <document>`** — Approve phase gate, unblock downstream
- **`/spec:status <name>`** — Pipeline dashboard with blockers and next action
- **`/spec:review <name>`** — Quality review at any stage [Staff Engineer]

## Available Skills

| Skill | Role | Description |
|-------|------|-------------|
| `spec:requirements` | Product Analyst | Requirements analysis — user stories, acceptance criteria |
| `spec:research` | Technical Researcher | Solution alternatives with evidence-based tradeoffs |
| `spec:design` | Software Architect | Architecture diagrams, interfaces, data flow |
| `spec:tasks` | Technical Lead | Task breakdown — implementation plan with checkboxes |
| `spec:implement` | Senior Engineer | Execute tasks with subagent orchestration |
| `spec:test-plan` | QA Engineer | Generate manual test scenarios from requirements |
| `spec:test` | QA Engineer | Walk through tests, collect results |
| `spec:review` | Staff Engineer | Validate documents for quality and consistency |
| `spec:approve` | — | Approve phase gate |
| `spec:status` | — | Pipeline dashboard |

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

Every document includes frontmatter: `status: DRAFT | IN_REVIEW | APPROVED | SUPERSEDED`

## Installation

```bash
# All spec skills
npx skills add ikatsuba/skills/spec

# Individual skills
npx skills add ikatsuba/skills --skill spec:requirements
npx skills add ikatsuba/skills --skill spec:research
npx skills add ikatsuba/skills --skill spec:design
npx skills add ikatsuba/skills --skill spec:tasks
npx skills add ikatsuba/skills --skill spec:implement
npx skills add ikatsuba/skills --skill spec:review
npx skills add ikatsuba/skills --skill spec:test-plan
npx skills add ikatsuba/skills --skill spec:test
npx skills add ikatsuba/skills --skill spec:approve
npx skills add ikatsuba/skills --skill spec:status
```
