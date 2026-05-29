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
  review/SKILL.md           - Review documents (any stage, optional) [Staff Engineer]
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
agent/                      - AI agent design and audit skills
  developer/SKILL.md        - Reference skill for building AI agents (router + references/)
  audit/SKILL.md            - Unified agent audit: 22 patterns + 12 factors + security
dev/                        - Development and meta skills
  create-skill/SKILL.md     - Skill creation helper (meta-skill)
  claude-audit/SKILL.md     - Audit a repo's Claude Code setup against best practices [Setup Auditor]
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


FEATURE PIPELINE (per spec — each phase needs only its prerequisite doc to EXIST)

  spec:requirements ──→ spec:research ──→ spec:design
   (requirements.md)    (research.md)     (design.md)
                                              │
                                 ┌────────────┴────────────┐
                                 ▼                         ▼
                           spec:tasks              spec:test-plan
                           (tasks.md)              (test-plan.md)
                                 │                         │
                                 ▼                         │
                          spec:implement                   │
                                 │                         │
                                 └────────────┬────────────┘
                                              ▼
                                         spec:test

  No approval step. Each generating skill ends by offering to chain into the
  next phase (revise / proceed / stop).

CROSS-CUTTING
  spec:status    — per-spec pipeline dashboard
  spec:review    — optional quality review at any stage [Staff Engineer]
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

### Document Frontmatter

Every spec document has lightweight YAML frontmatter with timestamps only — there is no approval status. Progress is tracked by which documents exist and by task/test checkbox counts.

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### Phase Gating

Each skill checks its prerequisites by **file existence**, not by an approval status. There is no approval step.

| Skill | Required prerequisite (must exist) | Recommended (warns if missing) |
|-------|-----------------------------------|-------------------------------|
| `spec:requirements` | _(entry point)_ | — |
| `spec:research` | requirements.md | — |
| `spec:design` | requirements.md | research.md |
| `spec:tasks` | design.md | — |
| `spec:test-plan` | design.md | — |
| `spec:implement` | tasks.md | test-plan.md |
| `spec:test` | test-plan.md + all tasks `[x]` | — |

Required prerequisites block execution (skill offers to run the generating skill). Recommended prerequisites warn but allow proceeding. After producing a document, each generating skill offers to chain straight into the next phase.

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
   - Detects each spec's stage from which documents exist and checkbox progress
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
   - Produces a *catalogue* of variants — no decisions, no CHOSEN markers
   - Iterative: re-running on an existing `research.md` extends the catalogue (add variants, open new areas, drop non-starters)
   - **Evidence rule**: external claims must be fetched and cited (context7 / web), never recalled from memory; unverifiable claims are marked "needs investigation". See `spec/research/references/evidence-rule.md`.

3. **`spec:design`** → Creates `.specs/<name>/design.md`
   - Decision Pass first: picks one variant per problem area from the research catalogue (this is where CHOSEN/Rejected happens)
   - Then produces architecture diagrams (Mermaid), TypeScript interfaces, test strategy
   - Same **evidence rule** applies — validate against the real codebase and live docs, not assumptions (`spec/design/references/evidence-rule.md`)

4. **`spec:tasks`** → Creates `.specs/<name>/tasks.md`
   - Hierarchical task breakdown with file paths and requirement references

5. **`spec:implement [spec] [all|next|N|gA|team]`** → Executes tasks
   - Supports parallel subtask execution when safe
   - Includes Design Deviation Protocol for handling plan divergence
   - **Team mode** (`team`): implements shippable groups in parallel with a Claude Code agent team, gated behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`. No git worktrees — teammates share one tree and coordinate edits over messages. Falls back to standard execution when the env var is unset. See `spec/implement/references/team-mode.md`.

6. **`spec:test-plan`** → Creates `.specs/<name>/test-plan.md`
   - Test cases traced to requirements via `_Requirements: X.X_`

7. **`spec:test [spec] [all|next|N]`** → Walks through test cases

### Pipeline Management

- **`spec:status [spec]`** → Per-spec pipeline dashboard with blockers and next action
- **`spec:review [spec] [document]`** → Optional quality review at any stage

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

Based on "Patterns for Building AI Agents" / "Principles of Building AI Agents" (Bhagwat & Gienow, 2025) and [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) (CC BY-SA 4.0). Two skills:

- **`agent:developer`** → Reference skill for designing and building AI agents. A thin `SKILL.md` router into ten `references/` knowledge files (architecture, prompting, tools, memory, context, workflows, RAG, multi-agent, evaluation, twelve-factor). Consulted *while* building — produces no documents.
- **`agent:audit [spec-name|path]`** → Unified audit of an existing agent against a merged framework (22 patterns + 12 factors + security). Fans out 7 parallel dimension subagents, scores 35 criteria, applies a security gate, and writes a maturity report to `.specs/<spec-name>/agent-audit.md`. Rubric content lives in `agent/audit/references/`.

### Development Skills

- **`dev:create-skill [category/name]`** → Scaffolds a new skill with proper structure
- **`dev:claude-audit [path]`** → Audits a repo's Claude Code setup (CLAUDE.md hierarchy, deny-list, per-dir commands, extension layer) against best practices for large codebases

## Key Patterns

- **Interactive questions**: Skills MUST use the `AskUserQuestion` tool for all user interactions — never output questions as plain text. Provide meaningful options to reduce user typing.
- **Roles**: Each skill has a `role:` in frontmatter and a `## Role` section defining the specialist persona and anti-patterns to avoid.
- **Timestamps, not status**: Every generated spec document includes lightweight frontmatter with `created` / `updated`. There is no approval status — progress is tracked by which documents exist and by checkbox counts.
- **Phase gating by existence**: Skills check whether the prerequisite document exists (required → block & offer to create; recommended → warn). No approval step; each generating skill offers to chain into the next phase.
- **Evidence rule**: `spec:research` and `spec:design` must fetch and cite external facts (context7 MCP for library docs; `WebSearch`/`WebFetch` otherwise) rather than recall them from memory; unverifiable claims become "needs investigation". The rule lives in each skill's `references/evidence-rule.md` (duplicated, because skills install independently).
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
