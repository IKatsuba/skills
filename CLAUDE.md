# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skills repository providing specification-driven development tools. It contains no build tools or package managers—just skill definitions that guide users through creating technical specifications.

## Installation

Skills are installed via the `npx add-skill` command:
- All skills: `npx add-skill ikatsuba/skills`
- Individual: `npx add-skill ikatsuba/skills/spec:requirements`

## Repository Structure

```
spec/                       - Specification-driven development skills
  research/SKILL.md         - Technical research after requirements
  requirements/SKILL.md     - Requirements document generation skill
  design/SKILL.md           - Technical design document generation skill
  tasks/SKILL.md            - Implementation task breakdown skill
  do-all/SKILL.md           - Execute all tasks from specification
  do-next/SKILL.md          - Execute next pending task
  do-task/SKILL.md          - Execute specific task by number
  review/SKILL.md           - Review spec documents for quality and consistency
  test-plan/SKILL.md        - Generate manual test plan from specification
  test-next/SKILL.md        - Execute next pending test case
  test-all/SKILL.md         - Execute all pending test cases
  test-task/SKILL.md        - Execute specific test case by number
git/                        - Git workflow skills
  commit/SKILL.md           - Smart commit with Conventional Commits
  amend/SKILL.md            - Amend last commit
utils/                      - Utility skills
  changelog/SKILL.md        - Human-readable changelog generation
review/                     - Code review skills
  local/SKILL.md            - Local code review before commit
  ux/SKILL.md               - UX review for user experience quality
dev/                        - Development and meta skills
  skill/SKILL.md            - Skill creation helper (meta-skill)
```

**Important**: All skills MUST be placed in a category folder (e.g., `spec/`, `utils/`), never in the repository root. When creating new skills, either add them to an existing category or create a new category folder.

## Workflow Architecture

The skills implement a four-stage specification pipeline where each stage builds on the previous:

1. **`spec:requirements`** → Creates `.specs/<name>/requirements.md`
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

4. **`spec:tasks`** → Creates `.specs/<name>/tasks.md`
   - Reads requirements, research, and design documents
   - Generates hierarchical task breakdown with file paths and requirement references

### Specification Review

Can be invoked at **any stage** of the pipeline to validate quality of existing documents:

5. **`spec:review [spec-name] [document]`** → Reviews spec documents
   - Can review any combination: requirements, research, design, tasks
   - Validates completeness, testability, and clarity of each document
   - Cross-checks consistency between whatever documents exist
   - Verifies alignment with the actual codebase
   - Produces a structured report with severity levels and a coverage matrix

### Task Execution Skills

After creating a tasks document, use these skills to execute the implementation:

6. **`spec:do-all`** → Executes all pending tasks
   - Runs tasks sequentially from the tasks document
   - Marks each task complete as it finishes
   - Handles checkpoints and verification

7. **`spec:do-next`** → Executes the next pending task
   - Finds and runs the first incomplete task
   - Ideal for incremental implementation with review

8. **`spec:do-task <number>`** → Executes a specific task
   - Runs a task by its number (e.g., "1.2", "3")
   - Allows out-of-order or re-execution of tasks

All specification documents are stored in `.specs/<spec-name>/` directories using kebab-case naming.

### Manual Testing Skills

After implementation is complete, use these skills to generate and execute a manual test plan:

9. **`spec:test-plan`** → Creates `.specs/<name>/test-plan.md`
   - Reads all spec documents to generate test scenarios
   - Each test case traces back to requirements via `_Requirements: X.X_`
   - Checkbox states: `[ ]` pending, `[-]` in progress, `[x]` passed, `[!]` failed, `[s]` skipped
   - Includes Summary section with pass/fail/skip counters

10. **`spec:test-next`** → Executes the next pending test
    - Finds the first incomplete test case and presents it
    - User performs the test and reports result (passed/failed/skipped)
    - Updates test-plan.md and commits after each test

11. **`spec:test-all`** → Walks through all pending tests
    - Presents each test sequentially, waits for user result
    - Commits after each test, shows final summary when done
    - User can stop at any time

12. **`spec:test-task <number>`** → Executes a specific test
    - Runs a test by its number (e.g., "1.2", "2")
    - Useful for re-testing failed tests after fixes

### Utility Skills

13. **`utils:changelog [period]`** → Generates human-readable changelog
   - Analyzes git history for a specified time period
   - Creates changelog suitable for non-technical teams (product, marketing, support)
   - Transforms technical commits into user-facing benefit descriptions
   - Supports relative periods (`last week`), dates (`since 2024-01-01`), and tags (`v1.0.0..v1.1.0`)

### Git Skills

14. **`git:commit`** → Creates a conventional commit
   - Analyzes staged changes to auto-detect commit type
   - Asks user to choose type when ambiguous
   - Follows Conventional Commits specification

15. **`git:amend`** → Modifies the last commit
   - Adds staged changes to the previous commit
   - Updates commit message while keeping format
   - Warns if commit was already pushed

### Review Skills

16. **`review:local [scope]`** → Performs local code review
    - Analyzes changes for bugs, security issues, and code quality
    - Auto-detects scope (staged, unstaged, last commit)
    - Generates structured summary report with severity levels

17. **`review:ux [spec-name|path|branch]`** → Performs UX review
    - Analyzes user flows for efficiency and unnecessary navigation hops
    - Checks UI consistency with existing app patterns
    - Validates edge case handling (empty states, errors, loading)
    - Generates structured report with UX-specific severity levels

### Development Skills

18. **`dev:skill [category/name]`** → Creates a new skill definition
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
- `spec:requirements` (not `requirements`)
- `spec:do-all` (not `do-all`)
- `utils:changelog` (not `changelog`)

This ensures skills are properly namespaced and avoids naming conflicts.
