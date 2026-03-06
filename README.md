# Skills

> A collection of skills for Claude Code, Codex, Cursor and OpenCode to supercharge your specification-driven development workflow!

## Quick Start

```bash
npx skills add ikatsuba/skills
```

That's it! You're ready to go.

---

## Installation Options

### Install specific skills

Pick only what you need:

```bash
npx skills add ikatsuba/skills --skill spec:plan
npx skills add ikatsuba/skills --skill spec:research
npx skills add ikatsuba/skills --skill spec:design
npx skills add ikatsuba/skills --skill spec:breakdown
npx skills add ikatsuba/skills --skill spec:implement
npx skills add ikatsuba/skills --skill spec:test-plan
npx skills add ikatsuba/skills --skill spec:test
npx skills add ikatsuba/skills --skill git:commit
npx skills add ikatsuba/skills --skill git:amend
npx skills add ikatsuba/skills --skill git:changelog
npx skills add ikatsuba/skills --skill review:diff
npx skills add ikatsuba/skills --skill review:ux
npx skills add ikatsuba/skills --skill agent:design
npx skills add ikatsuba/skills --skill agent:eval
npx skills add ikatsuba/skills --skill agent:secure
npx skills add ikatsuba/skills --skill agent:review
npx skills add ikatsuba/skills --skill agent:prompt
npx skills add ikatsuba/skills --skill agent:tools
npx skills add ikatsuba/skills --skill agent:memory
npx skills add ikatsuba/skills --skill agent:workflow
npx skills add ikatsuba/skills --skill agent:rag
npx skills add ikatsuba/skills --skill agent:multi
npx skills add ikatsuba/skills --skill agent:context
npx skills add ikatsuba/skills --skill project:vision
npx skills add ikatsuba/skills --skill project:decompose
npx skills add ikatsuba/skills --skill project:status
npx skills add ikatsuba/skills --skill dev:create-skill
```

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

### Project Orchestration

| Skill | Description |
|-------|-------------|
| `project:vision` | Define system goals, stakeholders, constraints, shared decisions |
| `project:decompose` | Break into specs with dependency graph and execution order |
| `project:status` | Dashboard showing progress across all specs |

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

### Git

| Skill | Description |
|-------|-------------|
| `git:commit` | Smart commit with Conventional Commits |
| `git:amend` | Amend last commit |
| `git:changelog` | Generate human-readable changelogs for product, marketing, and support teams |

### Code Review

| Skill | Description |
|-------|-------------|
| `review:diff` | Diff review with structured feedback before committing |
| `review:ux` | Detailed UX review — user flows, edge cases, and UI consistency |

### AI Agent Design

| Skill | Description |
|-------|-------------|
| `agent:design` | Comprehensive agent system design — orchestrates research across all areas |
| `agent:eval` | Evaluation system — failure modes, metrics, eval test suite |
| `agent:secure` | Security audit — lethal trifecta, sandboxing, access control, guardrails |
| `agent:review` | Full pattern review — scores all patterns with maturity assessment |
| `agent:prompt` | Prompt engineering — model selection, system prompt, few-shot examples |
| `agent:tools` | Tool design — schemas, MCP strategy, third-party integrations |
| `agent:memory` | Memory architecture — working memory, semantic recall, processors |
| `agent:workflow` | Workflow design — graph primitives, suspend/resume, streaming |
| `agent:rag` | RAG pipeline — chunking, embedding, vector DB, retrieval tuning |
| `agent:multi` | Multi-agent systems — org design, supervision, control flow |
| `agent:context` | Context engineering — parallelization, failure modes, compression |

---

## Workflow

These skills support a complete specification-driven development workflow:

### Phase 0: Project Planning

For large systems with multiple specs:

1. **`/project:vision <name>`** — Creates `.projects/<name>/vision.md`
2. **`/project:decompose <name>`** — Creates `.projects/<name>/specs.md`
3. **`/project:status <name>`** — Dashboard across all specs (use anytime)

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
/review:diff                # Auto-detect changes to review
/review:diff staged         # Review staged changes only
/review:diff branch         # Review all branch changes vs main
/review:diff src/auth/      # Review specific directory
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
/git:changelog last week           # Changes from the past 7 days
/git:changelog since 2024-01-01    # All changes since a date
/git:changelog v1.0.0..v1.1.0      # Changes between releases
```

### Agent Design

Design AI agent systems from scratch or review existing ones:

```bash
/agent:design my-agent             # Full design with parallel research sub-agents
/agent:secure my-agent             # Security audit (lethal trifecta, guardrails)
/agent:eval my-agent               # Evaluation system (failure modes, test suite)
/agent:review my-agent             # Score against all patterns (0-66 points)
```

Or dive into a single area:

```bash
/agent:prompt                      # Prompt engineering and model selection
/agent:tools                       # Tool schemas, MCP, integrations
/agent:memory                      # Memory layers and processors
/agent:workflow                    # Workflow graph, streaming, observability
/agent:rag                         # RAG pipeline or alternatives
/agent:multi                       # Multi-agent organization and control flow
/agent:context                     # Context engineering and failure prevention
```

---

## Documents Structure

```
.projects/
└── <project-name>/
    ├── vision.md           # System goals, constraints, shared decisions
    └── specs.md            # Spec list, dependency graph, execution order

.specs/
└── <spec-name>/
    ├── requirements.md     # User stories and acceptance criteria
    ├── research.md         # Research findings and chosen solutions
    ├── design.md           # Architecture, components, interfaces
    ├── tasks.md            # Implementation plan with checkboxes
    ├── test-plan.md        # Manual test plan with test cases
    ├── agent-design.md     # AI agent system design (from agent:design)
    ├── agent-eval.md       # Agent evaluation system (from agent:eval)
    └── agent-security.md   # Agent security audit (from agent:secure)
```

---

## License

MIT
