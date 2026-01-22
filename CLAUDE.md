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
spec:requirements/SKILL.md  - Requirements document generation skill
spec:design/SKILL.md        - Technical design document generation skill
spec:tasks/SKILL.md         - Implementation task breakdown skill
spec:do-all/SKILL.md        - Execute all tasks from specification
spec:do-next/SKILL.md       - Execute next pending task
spec:do-task/SKILL.md       - Execute specific task by number
changelog/SKILL.md          - Human-readable changelog generation
```

## Workflow Architecture

The skills implement a three-stage specification pipeline where each stage builds on the previous:

1. **`spec:requirements`** → Creates `.specs/<name>/requirements.md`
   - Gathers user stories, constraints, acceptance criteria
   - Uses SHALL/WHEN-THEN format for testable requirements

2. **`spec:design`** → Creates `.specs/<name>/design.md`
   - Reads requirements, analyzes codebase patterns
   - Produces architecture diagrams (Mermaid), TypeScript interfaces, test strategy

3. **`spec:tasks`** → Creates `.specs/<name>/tasks.md`
   - Reads both requirements and design documents
   - Generates hierarchical task breakdown with file paths and requirement references

### Task Execution Skills

After creating a tasks document, use these skills to execute the implementation:

4. **`spec:do-all`** → Executes all pending tasks
   - Runs tasks sequentially from the tasks document
   - Marks each task complete as it finishes
   - Handles checkpoints and verification

5. **`spec:do-next`** → Executes the next pending task
   - Finds and runs the first incomplete task
   - Ideal for incremental implementation with review

6. **`spec:do-task <number>`** → Executes a specific task
   - Runs a task by its number (e.g., "1.2", "3")
   - Allows out-of-order or re-execution of tasks

All specification documents are stored in `.specs/<spec-name>/` directories using kebab-case naming.

### Utility Skills

7. **`changelog [period]`** → Generates human-readable changelog
   - Analyzes git history for a specified time period
   - Creates changelog suitable for non-technical teams (product, marketing, support)
   - Transforms technical commits into user-facing benefit descriptions
   - Supports relative periods (`last week`), dates (`since 2024-01-01`), and tags (`v1.0.0..v1.1.0`)

## Key Patterns

- **Codebase awareness**: Skills analyze existing patterns before generating content
- **Traceability**: Each task references the requirements it fulfills (`_Requirements: X.X_`)
- **Verification checkpoints**: Tasks include milestone verification steps
- **Checkbox format**: Tasks use `[ ]` (pending), `[-]` (partial), `[x]` (complete)

## Modifying Skills

Each skill is defined entirely in its `SKILL.md` file. These files contain:
- Skill metadata and description
- Step-by-step instructions for Claude Code
- Output format specifications and examples
- Guidelines for handling edge cases
