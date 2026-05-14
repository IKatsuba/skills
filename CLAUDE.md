# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skills repository providing specification-driven development tools. It contains no build tools or package managers—just skill definitions that guide users through creating technical specifications.

## Installation

Skills are installed via the `npx skills add` command:
- All skills: `npx skills add ikatsuba/skills`
- Individual: `npx skills add ikatsuba/skills/spec:requirements`

## Repository Structure

```
spec/                       - Specification pipeline skills
  requirements/SKILL.md     - Requirements analysis (step 1) [Product Analyst]
  research/SKILL.md         - Technical research (step 2) [Technical Researcher]
  design/SKILL.md           - Technical design (step 3) [Software Architect]
  tasks/SKILL.md            - Task breakdown (step 4) [Technical Lead]
  implement/SKILL.md        - Implement tasks (step 5) [Senior Engineer]
  test-plan/SKILL.md        - Generate test plan (step 6) [QA Engineer]
  test/SKILL.md             - Execute tests (step 7) [QA Engineer]
  review/SKILL.md           - Review documents (any stage) [Staff Engineer]
  approve/SKILL.md          - Approve phase gate
  status/SKILL.md           - Per-spec pipeline dashboard
project/                    - Project-level orchestration skills
  init/SKILL.md             - Initialize project (goals, stakeholders, decisions)
  plan/SKILL.md             - Plan project (break into specs with dependencies)
  status/SKILL.md           - Dashboard showing progress across all specs
git/                        - Git workflow skills
  commit/SKILL.md           - Smart commit with Conventional Commits
  amend/SKILL.md            - Amend last commit
  changelog/SKILL.md        - Human-readable changelog generation
review/                     - Code review skills
  diff/SKILL.md             - Diff review before commit
  ux/SKILL.md               - UX review for user experience quality
  investigate/SKILL.md      - Analyze a problem and propose actionable solutions
agent/                      - AI agent design and review skills
  design/SKILL.md           - Agent architecture design (patterns 1-4)
  context/SKILL.md          - Context engineering strategy (patterns 5-9)
  eval/SKILL.md             - Evaluation system design (patterns 10-17)
  secure/SKILL.md           - Security audit (patterns 18-21)
  review/SKILL.md           - Full review checklist across all agent skills
  prompt/SKILL.md           - Prompt engineering and model selection
  tools/SKILL.md            - Tool design, MCP integration
  memory/SKILL.md           - Memory architecture (working, semantic, processors)
  workflow/SKILL.md         - Graph-based workflow design
  rag/SKILL.md              - RAG pipeline design
  multi/SKILL.md            - Multi-agent system design
dev/                        - Development and meta skills
  create-skill/SKILL.md     - Skill creation helper (meta-skill)
journal/                    - Personal engineering journal skills
  capture/SKILL.md          - Capture a thought, problem, edge case, or decision into ~/journal
  search/SKILL.md           - Search journal entries by query, type, project, topic, tag, or date
  promote/SKILL.md          - Graduate a journal entry into a .specs/<name>/ seed file
```

**Important**: All skills MUST be placed in a category folder (e.g., `spec/`, `git/`), never in the repository root. When creating new skills, either add them to an existing category or create a new category folder.

## Workflow Architecture

### Pipeline Overview

```
PROJECT LEVEL
  project:init ──→ project:plan ──→ project:status
   (vision.md)      (plan.md)        (dashboard)
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
        Feature A  Feature B  Feature C


FEATURE PIPELINE (per spec, each phase gated by APPROVED status)

  spec:requirements ──→ spec:research ──→ spec:design
   (requirements.md)    (research.md)     (design.md)
        │                    │                 │
     APPROVE              APPROVE           APPROVE
                                              │
                                 ┌────────────┴────────────┐
                                 ▼                         ▼
                           spec:tasks              spec:test-plan
                           (tasks.md)              (test-plan.md)
                                 │                         │
                              APPROVE                   APPROVE
                                 │                         │
                                 ▼                         │
                          spec:implement                   │
                                 │                         │
                                 └────────────┬────────────┘
                                              ▼
                                         spec:test

CROSS-CUTTING
  spec:approve   — promote DRAFT → APPROVED, unblock downstream
  spec:status    — per-spec pipeline dashboard
  spec:review    — quality review at any stage [Staff Engineer]
  project:status — project-wide dashboard
```

### Role System

Each pipeline skill operates as a specialist with a defined role that prevents common mistakes:

| Skill | Role | Prevents |
|-------|------|----------|
| `spec:requirements` | **Product Analyst** | Solution contamination in requirements |
| `spec:research` | **Technical Researcher** | Confirmation bias in variant analysis |
| `spec:design` | **Software Architect** | Scope creep through design |
| `spec:tasks` | **Technical Lead** | Silent design overrides in task breakdown |
| `spec:implement` | **Senior Engineer** | Creative implementation diverging from plan |
| `spec:test-plan` | **QA Engineer** | Implementation-biased testing |
| `spec:test` | **QA Engineer** | Optimistic reporting |
| `spec:review` | **Staff Engineer** | Rubber stamp reviews |

Subagents launched within skills receive micro-roles (e.g., **Engineer**, **Patterns Analyst**, **Integration Validator**) that constrain them to their specific subtask.

### Status System

Every spec document has YAML frontmatter tracking its lifecycle:

```yaml
---
status: DRAFT | IN_REVIEW | APPROVED | SUPERSEDED
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

- **DRAFT** — skill created the document
- **IN_REVIEW** — `spec:review` is reviewing (optional)
- **APPROVED** — `spec:approve` promoted, gates open for next phase
- **SUPERSEDED** — design changed during implementation

### Phase Gating

Each skill checks prerequisites before proceeding:

| Skill | Hard gate (blocks) | Soft gate (warns) |
|-------|-------------------|-------------------|
| `spec:requirements` | _(entry point)_ | — |
| `spec:research` | requirements APPROVED | — |
| `spec:design` | requirements APPROVED | research APPROVED |
| `spec:tasks` | design APPROVED | — |
| `spec:test-plan` | design APPROVED | — |
| `spec:implement` | tasks APPROVED | test-plan APPROVED |
| `spec:test` | test-plan APPROVED + all tasks `[x]` | — |

Hard gates block execution. Soft gates warn but allow proceeding.

### Project Orchestration

For large systems composed of multiple specs:

1. **`project:init [name]`** → Creates `.projects/<name>/vision.md`
   - Defines system goals, stakeholders, technical constraints
   - Establishes shared architectural decisions that apply to all specs

2. **`project:plan [name]`** → Creates `.projects/<name>/plan.md`
   - Breaks the vision into individual specs with clear boundaries
   - Defines dependencies between specs and execution order
   - Produces a dependency graph (Mermaid) and phased execution plan

3. **`project:status [name]`** → Displays progress dashboard
   - Reads frontmatter statuses from all spec documents
   - Shows blocked specs and ready-to-start specs
   - Suggests the next action based on current state

Project documents are stored in `.projects/<project-name>/` directories using kebab-case naming.

When a project exists, `spec:requirements` automatically reads the project context (vision, spec boundaries, shared decisions) to pre-seed requirements gathering.

### Specification Pipeline

1. **`spec:requirements`** → Creates `.specs/<name>/requirements.md`
   - Gathers user stories, constraints, acceptance criteria
   - Uses SHALL/WHEN-THEN format for testable requirements

2. **`spec:research`** → Creates `.specs/<name>/research.md`
   - Investigates codebase and explores 2-4 solution variants per problem area
   - User selects one variant per area (marked CHOSEN/Rejected)

3. **`spec:design`** → Creates `.specs/<name>/design.md`
   - Produces architecture diagrams (Mermaid), TypeScript interfaces, test strategy

4. **`spec:tasks`** → Creates `.specs/<name>/tasks.md`
   - Hierarchical task breakdown with file paths and requirement references

5. **`spec:implement [spec] [all|next|N]`** → Executes tasks
   - Supports parallel subtask execution when safe
   - Includes Design Deviation Protocol for handling plan divergence

6. **`spec:test-plan`** → Creates `.specs/<name>/test-plan.md`
   - Test cases traced to requirements via `_Requirements: X.X_`

7. **`spec:test [spec] [all|next|N]`** → Walks through test cases

### Pipeline Management

- **`spec:approve [spec] [document]`** → Promotes DRAFT → APPROVED, unblocks downstream
- **`spec:status [spec]`** → Per-spec pipeline dashboard with blockers and next action
- **`spec:review [spec] [document]`** → Quality review at any stage

All specification documents are stored in `.specs/<spec-name>/` directories using kebab-case naming.

### Git Skills

- **`git:commit`** → Smart conventional commit (auto-detects type)
- **`git:amend`** → Amend last commit
- **`git:changelog [period]`** → Human-readable changelog for non-technical teams

### Review Skills

- **`review:diff [scope]`** → Diff review with structured feedback
- **`review:ux [spec-name|path|branch]`** → UX review for user flows and consistency
- **`review:investigate`** → Analyze a problem and propose solutions

### Journal Skills

- **`journal:capture [seed thought]`** → Captures a thought into `~/journal/projects/<slug>/` or `~/journal/topics/<slug>/`, auto-updates README indexes at folder, category, and root levels.
- **`journal:search [query] [--filters]`** → Searches `~/journal/` by text, type, project, topic, tag, or date range. Returns ranked snippets.
- **`journal:promote [entry] [spec-name]`** → Graduates a journal entry into `.specs/<spec-name>/journal-seed.md` for `spec:requirements` to consume; backlinks the journal entry with `promoted_to:`.

### Agent Skills

Based on "Patterns for Building AI Agents" (Bhagwat & Gienow, 2025). Two tiers: **spec skills** produce documents in `.specs/`, **action skills** work directly.

#### Spec Skills

- **`agent:design [spec-name]`** → Comprehensive agent system design (orchestrator)
- **`agent:eval [spec-name]`** → Evaluation system design
- **`agent:secure [spec-name|path]`** → Security audit
- **`agent:review [spec-name|path]`** → Full pattern review (0-66 score)

#### Action Skills

- **`agent:prompt`** → Prompt engineering and model selection
- **`agent:tools`** → Tool design, MCP integration
- **`agent:memory`** → Memory architecture
- **`agent:workflow`** → Graph-based workflow design
- **`agent:rag`** → RAG pipeline design
- **`agent:multi`** → Multi-agent systems
- **`agent:context`** → Context engineering

### Development Skills

- **`dev:create-skill [category/name]`** → Scaffolds a new skill with proper structure

## Key Patterns

- **Interactive questions**: Skills MUST use the `AskUserQuestion` tool for all user interactions — never output questions as plain text. Provide meaningful options to reduce user typing.
- **Roles**: Each skill has a `role:` in frontmatter and a `## Role` section defining the specialist persona and anti-patterns to avoid.
- **Status tracking**: Every generated spec document includes frontmatter with `status`, `created`, `updated` fields.
- **Phase gating**: Skills check prerequisite document statuses before proceeding (HARD gates block, SOFT gates warn).
- **Traceability**: Each task references the requirements it fulfills (`_Requirements: X.X_`)
- **Verification checkpoints**: Tasks include milestone verification steps
- **Checkbox format**: Tasks use `[ ]` (pending), `[-]` (in progress), `[x]` (complete). Test plans extend this with `[!]` (failed) and `[s]` (skipped)
- **Design Deviation Protocol**: During implementation, deviations from design are classified as minor/moderate/major with escalation rules.
- **Arguments**: Skills use `$ARGUMENTS` / `$0`, `$1` (Claude Code built-in substitutions) instead of custom `<args>` parsing.

## Creating & Modifying Skills

Each skill is a directory with `SKILL.md` as the entrypoint. These files contain:
- Skill metadata (frontmatter with `name`, `description`, `role`, and Claude Code-specific fields)
- A `## Role` section defining the specialist persona
- Step-by-step instructions for Claude Code
- Output format specifications and examples
- Guidelines for handling edge cases

Large skills can include supporting files (keep `SKILL.md` under 500 lines):
```
my-skill/
├── SKILL.md              # Main instructions (required)
├── reference.md          # Detailed reference (loaded when needed)
└── examples.md           # Examples (loaded when needed)
```

### Skill Frontmatter

```yaml
---
name: category:skill-name
description: What it does. Use when [trigger condition].
role: Role Title
argument-hint: <required-arg> [optional-arg]
disable-model-invocation: true    # user-only (approve, implement, test)
context: fork                     # run in isolated subagent (status)
agent: Explore                    # agent type for forked context
---
```

**Key fields:**
- `argument-hint` — shown during autocomplete
- `disable-model-invocation: true` — prevents Claude from auto-invoking (use for action skills)
- `context: fork` + `agent` — runs skill in an isolated subagent (use for read-only skills)
- `$ARGUMENTS` / `$0`, `$1` — built-in argument substitution in skill content

### Naming Convention

The `name` field MUST include the category prefix:
- `spec:requirements` (not `requirements`)
- `spec:implement` (not `implement`)
- `git:changelog` (not `changelog`)

This ensures skills are properly namespaced and avoids naming conflicts.
