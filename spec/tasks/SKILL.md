---
name: spec:tasks
description: Create Tasks Document - generates an implementation plan with tracked tasks based on requirements and design documents
---

# Create Tasks Document

Creates a tasks document based on the requirements and design documents. This command reads both documents and generates an implementation plan with tracked tasks.

## When to use

Use this skill when the user needs to:
- Create an implementation plan from existing requirements and design
- Generate a task breakdown for development work
- Plan the order of implementation with dependencies

## Instructions

### Step 1: Locate Documents

1. If `<args>` contains a spec name, look for:
   - Requirements at `.specs/<spec-name>/requirements.md`
   - Design at `.specs/<spec-name>/design.md`
2. If no spec name provided, list available specs in `.specs/` and ask user to choose
3. Read and analyze both documents

### Step 2: Analyze the Design

Before creating tasks:
1. Review the architecture and components from the design
2. Identify dependencies between components
3. Determine the optimal order of implementation
4. Note checkpoints for verification

### Step 3: Verify Against the Codebase

Do not blindly trust the documents — cross-check key assumptions against the real codebase:

1. **Check existing code** — verify that files, modules, and APIs mentioned in the design actually exist and match the described structure
2. **Validate assumptions** — if the design references specific patterns, frameworks, or utilities, confirm they are present and used as described
3. **Detect drift** — if the codebase has changed since the documents were written, note discrepancies and adjust tasks accordingly
4. **Identify missing context** — look for related code, tests, or configs that the documents may have overlooked but that the tasks should account for

If you find significant discrepancies between the documents and the codebase, mention them in the **Notes** section of the tasks document.

### Step 4: Create the Tasks Document

Create the document at `.specs/<spec-name>/tasks.md` with this structure:

```markdown
# Implementation Plan: [Feature Name]

## Overview

[Brief description of the implementation and goals]

## Tasks

- [ ] 1. [Major Task Name]
  - [ ] 1.1 [Subtask Name]
    - [Detailed description of what to do]
    - [File to create/modify: `path/to/file.ts`]
    - [Key implementation points]
    - _Requirements: X.X, X.X_

  - [ ] 1.2 [Subtask Name]
    - [Details]
    - _Requirements: X.X_

- [ ] 2. Checkpoint - [Verification point]
  - [What to verify]
  - [Run tests for the group: `test command or path`]
  - [Run existing tests for affected files to check for regressions]

- [ ] 3. [Next Major Task]
  - [ ] 3.1 [Subtask]
    - [Details]
    - _Requirements: X.X_

[Continue with all tasks]

- [ ] N. Final checkpoint - Complete verification
  - Run the full test suite to ensure all new and existing tests pass
  - Run tests for all files affected by the implementation to check for regressions
  - Verify all requirements are met

## Notes

- [Important notes about the implementation]
- [Dependencies or constraints]
- [Any special considerations]
```

### Task Structure Guidelines

1. **Group related tasks** - Major tasks contain related subtasks
2. **Include file paths** - Specify which files to create/modify
3. **Reference requirements** - Link each task to requirements with `_Requirements: X.X_`
4. **Add test tasks per group** - Each major task group MUST end with a subtask for writing tests covering the implemented functionality. Use the test strategy from the design document to determine test types (unit, integration, e2e) and coverage expectations
5. **Add checkpoints** - Include verification points after major milestones (see Checkpoint Guidelines)
6. **Order by dependencies** - Tasks that depend on others come later
7. **Be specific** - Each subtask should be actionable and clear

### Task Types

1. **Implementation tasks** - Create or modify code
2. **Configuration tasks** - Update configs, dependencies
3. **Testing tasks** - Write unit/integration tests
4. **Cleanup tasks** - Remove old code, update references
5. **Checkpoint tasks** - Verify implementation milestones

### Checkpoint Guidelines

Every checkpoint task MUST include:
1. **Run new tests** — execute the tests written for the preceding task group
2. **Run affected tests** — execute existing tests for files that were created or modified in the group to catch regressions
3. **Verify functionality** — describe what to check manually or programmatically

### Checkbox States

- `[ ]` - Pending (not started)
- `[-]` - Pending tasks
- `[x]` - Completed

### Step 5: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. A summary of the task breakdown
3. Total number of tasks and estimated checkpoints
4. Ask if they want to make any changes

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
