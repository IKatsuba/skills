# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skills repository providing specification-driven development tools. It contains no build tools or package managers—just skill definitions that guide users through creating technical specifications.

## Installation

Skills are installed via the `npx skills add` command:
- All skills: `npx skills add ikatsuba/skills`
- Individual: `npx skills add ikatsuba/skills/spec:plan`

## Repository Structure

```
spec/                       - Specification-driven development skills
  plan/SKILL.md             - Plan requirements (step 1)
  research/SKILL.md         - Technical research (step 2)
  design/SKILL.md           - Technical design (step 3)
  breakdown/SKILL.md        - Task breakdown (step 4)
  implement/SKILL.md        - Implement tasks: all, next, or specific (step 5)
  review/SKILL.md           - Review spec documents (any stage)
  test-plan/SKILL.md        - Generate manual test plan (step 6)
  test/SKILL.md             - Execute tests: all, next, or specific (step 7)
git/                        - Git workflow skills
  commit/SKILL.md           - Smart commit with Conventional Commits
  amend/SKILL.md            - Amend last commit
  changelog/SKILL.md        - Human-readable changelog generation
review/                     - Code review skills
  diff/SKILL.md             - Diff review before commit
  ux/SKILL.md               - UX review for user experience quality
  investigate/SKILL.md      - Analyze a problem and propose actionable solutions
project/                    - Project-level orchestration skills
  vision/SKILL.md           - Define system goals, stakeholders, shared decisions
  decompose/SKILL.md        - Break into specs with dependencies and execution order
  status/SKILL.md           - Dashboard showing progress across all specs
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
```

**Important**: All skills MUST be placed in a category folder (e.g., `spec/`, `git/`), never in the repository root. When creating new skills, either add them to an existing category or create a new category folder.

## Workflow Architecture

### Project Orchestration

For large systems composed of multiple specs, the project skills provide a higher-level orchestration layer:

1. **`project:vision [name]`** → Creates `.projects/<name>/vision.md`
   - Defines system goals, stakeholders, technical constraints
   - Establishes shared architectural decisions that apply to all specs
   - Produces a system boundary diagram (Mermaid)

2. **`project:decompose [name]`** → Creates `.projects/<name>/specs.md`
   - Breaks the vision into individual specs with clear boundaries
   - Defines dependencies between specs and execution order
   - Identifies shared interfaces consumed by multiple specs
   - Produces a dependency graph (Mermaid) and phased execution plan

3. **`project:status [name]`** → Displays progress dashboard (no file output)
   - Scans all spec directories to detect stage and completion
   - Shows blocked specs and ready-to-start specs
   - Suggests the next action based on current state

Project documents are stored in `.projects/<project-name>/` directories using kebab-case naming.

When a project exists, `spec:plan` automatically reads the project context (vision, spec boundaries, shared decisions) to pre-seed requirements gathering.

### Specification Pipeline

The skills implement a seven-step specification pipeline where each step builds on the previous:

1. **`spec:plan`** → Creates `.specs/<name>/requirements.md`
   - Gathers user stories, constraints, acceptance criteria
   - Asks clarifying questions about ambiguities, edge cases, and priorities
   - Uses SHALL/WHEN-THEN format for testable requirements

2. **`spec:research`** → Creates `.specs/<name>/research.md`
   - Investigates codebase and explores solution alternatives based on requirements
   - Generates 2-4 variants per problem area with pros/cons/effort/risk
   - User selects a variant per problem area (marked CHOSEN/Rejected)

3. **`spec:design`** → Creates `.specs/<name>/design.md`
   - Reads requirements and chosen research solutions
   - Produces architecture diagrams (Mermaid), TypeScript interfaces, test strategy

4. **`spec:breakdown`** → Creates `.specs/<name>/tasks.md`
   - Reads requirements, research, and design documents
   - Generates hierarchical task breakdown with file paths and requirement references

5. **`spec:implement [spec] [all|next|N]`** → Executes tasks from the tasks document
   - `spec:implement <spec>` — execute all pending tasks
   - `spec:implement <spec> next` — execute the next pending task
   - `spec:implement <spec> <N>` — execute a specific task by number (e.g., "1.2", "3")
   - Supports parallel subtask execution when safe
   - Handles checkpoints and verification

6. **`spec:test-plan`** → Creates `.specs/<name>/test-plan.md`
   - Reads all spec documents to generate test scenarios
   - Each test case traces back to requirements via `_Requirements: X.X_`
   - Checkbox states: `[ ]` pending, `[-]` in progress, `[x]` passed, `[!]` failed, `[s]` skipped
   - Includes Summary section with pass/fail/skip counters

7. **`spec:test [spec] [all|next|N]`** → Walks through test cases from the test plan
   - `spec:test <spec>` — walk through all pending tests
   - `spec:test <spec> next` — execute the next pending test
   - `spec:test <spec> <N>` — execute a specific test by number
   - User performs tests and reports results (passed/failed/skipped)
   - Commits after each test

### Specification Review

Can be invoked at **any stage** of the pipeline to validate quality of existing documents:

**`spec:review [spec-name] [document]`** → Reviews spec documents
- Can review any combination: requirements, research, design, tasks
- Validates completeness, testability, and clarity of each document
- Cross-checks consistency between whatever documents exist
- Verifies alignment with the actual codebase
- Produces a structured report with severity levels and a coverage matrix

All specification documents are stored in `.specs/<spec-name>/` directories using kebab-case naming.

### Git Skills

8. **`git:commit`** → Creates a conventional commit
   - Analyzes staged changes to auto-detect commit type
   - Asks user to choose type when ambiguous
   - Follows Conventional Commits specification

9. **`git:amend`** → Modifies the last commit
   - Adds staged changes to the previous commit
   - Updates commit message while keeping format
   - Warns if commit was already pushed

10. **`git:changelog [period]`** → Generates human-readable changelog
    - Analyzes git history for a specified time period
    - Creates changelog suitable for non-technical teams (product, marketing, support)
    - Transforms technical commits into user-facing benefit descriptions
    - Supports relative periods (`last week`), dates (`since 2024-01-01`), and tags (`v1.0.0..v1.1.0`)

### Review Skills

11. **`review:diff [scope]`** → Performs diff review
    - Analyzes changes for bugs, security issues, and code quality
    - Auto-detects scope (staged, unstaged, last commit)
    - Generates structured summary report with severity levels

12. **`review:ux [spec-name|path|branch]`** → Performs UX review
    - Analyzes user flows for efficiency and unnecessary navigation hops
    - Checks UI consistency with existing app patterns
    - Validates edge case handling (empty states, errors, loading)
    - Generates structured report with UX-specific severity levels

### Agent Skills

Based on "Patterns for Building AI Agents" and "Principles of Building AI Agents" (Bhagwat & Gienow, 2025).

Two tiers: **spec skills** produce design documents in `.specs/`, **action skills** work directly without files.

#### Spec Skills (produce `.specs/` documents)

13. **`agent:design [spec-name]`** → Comprehensive agent system design (orchestrator)
    - Gathers requirements, launches parallel research sub-agents
    - Each sub-agent applies methodology from the action skills below
    - Compiles all findings into a unified `.specs/<name>/agent-design.md`
    - Covers: architecture, prompts, tools, memory, workflows, RAG, multi-agent, context

14. **`agent:eval [spec-name]`** → Evaluation system design
    - Failure mode taxonomy, business metrics, cross-referencing
    - Eval test suite with CI integration, SME labeling workflow
    - Production data pipeline with LLM-as-judge
    - Outputs `.specs/<name>/agent-eval.md`

15. **`agent:secure [spec-name|path]`** → Security audit
    - Lethal trifecta analysis, sandbox assessment
    - Granular access control review, input/output guardrails
    - Outputs `.specs/<name>/agent-security.md`

16. **`agent:review [spec-name|path]`** → Full pattern review
    - Scores all patterns on a 0-3 scale, maturity assessment
    - Top 5 prioritized recommendations
    - Points to specific action skills for weak areas

#### Action Skills (work directly, no `.specs/` output)

Used standalone for focused work or invoked by `agent:design` as research phases.

17. **`agent:prompt`** → Prompt engineering
    - Model selection (start expensive, optimize later), system prompt architecture
    - Few-shot example design, production checklist (quality, cost, latency)

18. **`agent:tools`** → Tool design
    - Decompose into atomic operations (think like an analyst)
    - Tool schemas with "when to call," MCP client/server strategy, third-party integrations

19. **`agent:memory`** → Memory architecture
    - Three-layer model: conversation window, working memory, semantic recall
    - Memory processors (TokenLimiter, ToolCallFilter), dynamic configuration per user tier

20. **`agent:workflow`** → Workflow design
    - Four primitives: branching, chaining, merging, conditions
    - Suspend/resume for HITL, streaming strategy, OpenTelemetry observability

21. **`agent:rag`** → RAG pipeline
    - Decision tree: full context → agentic tools → RAG pipeline
    - Chunking, embedding, vector DB selection, retrieval tuning, reranking

22. **`agent:multi`** → Multi-agent systems
    - Organizational design (roles as job titles), supervision patterns
    - Control flow, agent-as-tool and workflow-as-tool composition, A2A protocol

23. **`agent:context`** → Context engineering
    - Parallelization analysis, context sharing between subagents
    - Five failure modes (poisoning, distraction, confusion, clash, rot), compression, error feedback

### Development Skills

24. **`dev:create-skill [category/name]`** → Creates a new skill definition
    - Scaffolds a SKILL.md with proper structure and conventions
    - Ensures consistency across all skills in the repository
    - Updates CLAUDE.md with the new skill entry

## Key Patterns

- **Interactive questions**: Skills MUST use the `AskUserQuestion` tool for all user interactions — never output questions as plain text. Provide meaningful options to reduce user typing.
- **Codebase awareness**: Skills analyze existing patterns before generating content
- **Traceability**: Each task references the requirements it fulfills (`_Requirements: X.X_`)
- **Verification checkpoints**: Tasks include milestone verification steps
- **Checkbox format**: Tasks use `[ ]` (pending), `[-]` (in progress), `[x]` (complete). Test plans extend this with `[!]` (failed) and `[s]` (skipped)

## Creating & Modifying Skills

Each skill is defined entirely in its `SKILL.md` file. These files contain:
- Skill metadata (frontmatter with `name` and `description`)
- Step-by-step instructions for Claude Code
- Output format specifications and examples
- Guidelines for handling edge cases

### Skill Naming Convention

The `name` field in SKILL.md frontmatter MUST include the category prefix:

```yaml
---
name: category:skill-name
description: Short description of the skill
---
```

Examples:
- `spec:plan` (not `plan`)
- `spec:implement` (not `implement`)
- `git:changelog` (not `changelog`)

This ensures skills are properly namespaced and avoids naming conflicts.
