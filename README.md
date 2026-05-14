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
npx skills add ikatsuba/skills --skill spec:requirements
npx skills add ikatsuba/skills --skill spec:research
npx skills add ikatsuba/skills --skill spec:design
npx skills add ikatsuba/skills --skill spec:tasks
npx skills add ikatsuba/skills --skill spec:implement
npx skills add ikatsuba/skills --skill spec:test-plan
npx skills add ikatsuba/skills --skill spec:test
npx skills add ikatsuba/skills --skill spec:approve
npx skills add ikatsuba/skills --skill spec:status
npx skills add ikatsuba/skills --skill spec:review
npx skills add ikatsuba/skills --skill git:commit
npx skills add ikatsuba/skills --skill git:amend
npx skills add ikatsuba/skills --skill git:changelog
npx skills add ikatsuba/skills --skill review:diff
npx skills add ikatsuba/skills --skill review:ux
npx skills add ikatsuba/skills --skill review:investigate
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
npx skills add ikatsuba/skills --skill project:init
npx skills add ikatsuba/skills --skill project:plan
npx skills add ikatsuba/skills --skill project:status
npx skills add ikatsuba/skills --skill dev:create-skill
npx skills add ikatsuba/skills --skill dev:claude-audit
npx skills add ikatsuba/skills --skill journal:capture
npx skills add ikatsuba/skills --skill journal:search
npx skills add ikatsuba/skills --skill journal:promote
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

### Specification Pipeline

| Skill | Role | Description |
|-------|------|-------------|
| `spec:requirements` | Product Analyst | Requirements analysis — user stories, acceptance criteria |
| `spec:research` | Technical Researcher | Solution alternatives with pros/cons and evidence |
| `spec:design` | Software Architect | Architecture diagrams, interfaces, data flow |
| `spec:tasks` | Technical Lead | Task breakdown — implementation plan with checkboxes |
| `spec:implement` | Senior Engineer | Execute tasks — all, next, or specific task |
| `spec:test-plan` | QA Engineer | Generate manual test scenarios |
| `spec:test` | QA Engineer | Execute tests — all, next, or specific test |
| `spec:review` | Staff Engineer | Validate documents for quality and consistency |
| `spec:approve` | — | Approve phase gate, unblock downstream skills |
| `spec:status` | — | Per-spec pipeline dashboard |

### Project Orchestration

| Skill | Description |
|-------|-------------|
| `project:init` | Define system goals, stakeholders, constraints, shared decisions |
| `project:plan` | Break into specs with dependency graph and execution order |
| `project:status` | Dashboard showing progress across all specs |

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
| `review:investigate` | Analyze a problem and propose actionable solutions |

### Journal

| Skill | Description |
|-------|-------------|
| `journal:capture` | Capture a thought, problem, edge case, or decision into `~/journal` with auto-indexed README files |
| `journal:search` | Search journal entries by query, type, project, topic, tag, or date range |
| `journal:promote` | Graduate a journal entry into `.specs/<name>/journal-seed.md` to feed the spec pipeline |

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

These skills support a complete specification-driven development workflow with **phase gating** — each phase must be approved before the next can begin.

### Phase 0: Project Planning

For large systems with multiple specs:

1. **`/project:init <name>`** — Creates `.projects/<name>/vision.md`
2. **`/project:plan <name>`** — Creates `.projects/<name>/plan.md`
3. **`/project:status <name>`** — Dashboard across all specs (use anytime)

### Phase 1: Specification

Build your blueprint. Each step requires approval before the next:

```
/spec:requirements <name>        → requirements.md (DRAFT)
/spec:approve <name> requirements → APPROVED ✓
/spec:research <name>            → research.md (DRAFT)
/spec:approve <name> research    → APPROVED ✓
/spec:design <name>              → design.md (DRAFT)
/spec:approve <name> design      → APPROVED ✓
/spec:tasks <name>               → tasks.md (DRAFT)
/spec:test-plan <name>           → test-plan.md (DRAFT)
/spec:approve <name> tasks
/spec:approve <name> test-plan
```

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
/spec:review <name>              → Quality review at any stage
/spec:approve <name> <document>  → Approve a phase to unblock the next
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

### Agent Design

```bash
/agent:design my-agent             # Full design with parallel research sub-agents
/agent:secure my-agent             # Security audit (lethal trifecta, guardrails)
/agent:eval my-agent               # Evaluation system (failure modes, test suite)
/agent:review my-agent             # Score against all patterns (0-66 points)
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
    ├── agent-design.md     # AI agent system design (from agent:design)
    ├── agent-eval.md       # Agent evaluation system (from agent:eval)
    └── agent-security.md   # Agent security audit (from agent:secure)
```

Every spec document includes YAML frontmatter with status tracking:

```yaml
---
status: DRAFT | IN_REVIEW | APPROVED | SUPERSEDED
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

---

## License

MIT
