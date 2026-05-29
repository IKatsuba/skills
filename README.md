# Skills

> A collection of skills for Claude Code, Codex, Cursor and OpenCode to supercharge your specification-driven development workflow!

## Quick Start

```bash
npx skills add ikatsuba/skills
```

That's it! You're ready to go.

---

## Installation Options

### Install a category

Install only the group you need — the CLI will prompt to pick skills within it:

```bash
npx skills add ikatsuba/skills/spec       # Spec pipeline
npx skills add ikatsuba/skills/project    # Project orchestration
npx skills add ikatsuba/skills/git        # Git workflow
npx skills add ikatsuba/skills/review     # Code & UX review
npx skills add ikatsuba/skills/journal    # Engineering journal
npx skills add ikatsuba/skills/agent      # AI agent design & audit
npx skills add ikatsuba/skills/dev        # Development & meta skills
```

For a single skill, use `--skill <name>` (e.g. `--skill spec:requirements`).

### Global installation

Want skills everywhere? Go global:

```bash
npx skills add ikatsuba/skills -g
```

### Browse available skills

```bash
npx skills add ikatsuba/skills --list
```

---

## Available Skills

### Specification Pipeline

| Skill | Role | Description |
|-------|------|-------------|
| [`spec:requirements`](spec/requirements/) | Product Analyst | Requirements analysis — user stories, acceptance criteria |
| [`spec:research`](spec/research/) | Technical Researcher | Solution alternatives with pros/cons and evidence |
| [`spec:design`](spec/design/) | Software Architect | Architecture diagrams, interfaces, data flow |
| [`spec:tasks`](spec/tasks/) | Technical Lead | Task breakdown — implementation plan with checkboxes |
| [`spec:implement`](spec/implement/) | Senior Engineer | Execute tasks — all, next, or specific task |
| [`spec:test-plan`](spec/test-plan/) | QA Engineer | Generate manual test scenarios |
| [`spec:test`](spec/test/) | QA Engineer | Execute tests — all, next, or specific test |
| [`spec:review`](spec/review/) | Staff Engineer | Validate documents for quality and consistency (optional, any stage) |
| [`spec:status`](spec/status/) | — | Per-spec pipeline dashboard |

### Project Orchestration

| Skill | Description |
|-------|-------------|
| [`project:init`](project/init/) | Define system goals, stakeholders, constraints, shared decisions |
| [`project:plan`](project/plan/) | Break into specs with dependency graph and execution order |
| [`project:status`](project/status/) | Dashboard showing progress across all specs |

### Git

| Skill | Description |
|-------|-------------|
| [`git:commit`](git/commit/) | Smart commit with Conventional Commits |
| [`git:amend`](git/amend/) | Amend last commit |
| [`git:changelog`](git/changelog/) | Generate human-readable changelogs for product, marketing, and support teams |

### Code Review

| Skill | Description |
|-------|-------------|
| [`review:diff`](review/diff/) | Diff review with structured feedback before committing |
| [`review:ux`](review/ux/) | Detailed UX review — user flows, edge cases, and UI consistency |
| [`review:investigate`](review/investigate/) | Analyze a problem and propose actionable solutions |

### Journal

| Skill | Description |
|-------|-------------|
| [`journal:capture`](journal/capture/) | Capture a thought, problem, edge case, or decision into `~/journal` with auto-indexed README files |
| [`journal:search`](journal/search/) | Search journal entries by query, type, project, topic, tag, or date range |
| [`journal:promote`](journal/promote/) | Graduate a journal entry into `.specs/<name>/journal-seed.md` to feed the spec pipeline |

### AI Agents

| Skill | Description |
|-------|-------------|
| [`agent:developer`](agent/developer/) | Reference skill for designing and building AI agents — architecture, prompting, tools, memory, context, workflows, RAG, multi-agent, evaluation, twelve-factor reliability |
| [`agent:audit`](agent/audit/) | Audit an agent against the 22 patterns + 12 factors + security — scored maturity report across 7 dimensions |

### Development

| Skill | Description |
|-------|-------------|
| [`dev:create-skill`](dev/create-skill/) | Scaffold a new skill with proper structure (meta-skill) |
| [`dev:claude-audit`](dev/claude-audit/) | Audit a repo's Claude Code setup against best practices |

---

## Workflow

These skills support a complete specification-driven development workflow. Each phase produces a document the next phase consumes — there is no separate approval step. A phase can run as soon as its prerequisite document **exists**, and each generating skill ends by offering to chain straight into the next phase (revise / proceed / stop). Review is an optional quality check you can run at any stage.

### Phase 0: Project Planning

For large systems with multiple specs:

1. **`/project:init <name>`** — Creates `.projects/<name>/vision.md`
2. **`/project:plan <name>`** — Creates `.projects/<name>/plan.md`
3. **`/project:status <name>`** — Dashboard across all specs (use anytime)

### Phase 1: Specification

Build your blueprint. Each step produces a document and offers to chain into the next — no approval command in between:

```
/spec:requirements <name>        → requirements.md   → "proceed to research?"
/spec:research <name>            → research.md       → "proceed to design?"
/spec:design <name>              → design.md         → "proceed to tasks / test-plan?"
/spec:tasks <name>               → tasks.md          → "start implementing?"
/spec:test-plan <name>           → test-plan.md      → "start testing?"
```

You can also run any phase directly — it only needs its prerequisite document to exist.

### Phase 2: Implementation

```
/spec:implement <name>           → Execute all tasks automatically
/spec:implement <name> next      → Execute tasks one at a time
/spec:implement <name> <N>       → Execute a specific task by number
```

### Phase 3: Testing

```
/spec:test <name>                → Walk through all pending tests
/spec:test <name> next           → Execute one test at a time
/spec:test <name> <N>            → Execute a specific test by number
```

### Pipeline Management

```
/spec:status <name>              → See where a spec is in the pipeline
/spec:review <name>              → Optional quality review at any stage
```

### Code Review

```bash
/review:diff                # Auto-detect changes to review
/review:diff staged         # Review staged changes only
/review:diff branch         # Review all branch changes vs main
```

### UX Review

```bash
/review:ux user-auth         # UX review based on spec documents
/review:ux src/pages/settings/  # UX review of specific files
```

### Changelog Generation

```bash
/git:changelog last week           # Changes from the past 7 days
/git:changelog since 2024-01-01    # All changes since a date
/git:changelog v1.0.0..v1.1.0      # Changes between releases
```

### AI Agents

```bash
/agent:developer                   # Consult reference knowledge while building an agent
/agent:audit my-agent              # Score an agent against the 22 patterns + 12 factors
```

---

## Documents Structure

```
.projects/
└── <project-name>/
    ├── vision.md           # System goals, constraints, shared decisions
    └── plan.md             # Spec list, dependency graph, execution order

.specs/
└── <spec-name>/
    ├── requirements.md     # User stories and acceptance criteria
    ├── research.md         # Research findings and chosen solutions
    ├── design.md           # Architecture, components, interfaces
    ├── tasks.md            # Implementation plan with checkboxes
    ├── test-plan.md        # Manual test plan with test cases
    └── agent-audit.md      # AI agent audit report (from agent:audit)
```

Every spec document includes lightweight YAML frontmatter with timestamps. Pipeline progress is tracked by which documents exist and by task/test checkbox counts — there is no approval status:

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

---

## License

MIT
