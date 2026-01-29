---
name: spec:do-next
description: Execute Next Task - runs the next pending task from the tasks document
---

# Execute Next Task

Executes the next pending task from a specification's tasks document. This skill finds the first incomplete task and implements it.

## When to use

Use this skill when the user needs to:
- Implement one task at a time with review between tasks
- Continue work on a partially completed specification
- Execute tasks incrementally with manual control

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/requirements.md` | Requirements and acceptance criteria |
| `.specs/<spec-name>/design.md` | Technical design and architecture |
| `.specs/<spec-name>/tasks.md` | Implementation tasks with checkboxes |

**Always read all three files** to understand the full context before executing tasks.

## Instructions

### Step 1: Locate and Read Specification Documents

1. If `<args>` contains a spec name, look in `.specs/<spec-name>/`
2. If no spec name provided, list available specs in `.specs/` and ask user to choose
3. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built
   - `design.md` - understand how it should be built
   - `tasks.md` - get the list of tasks to execute

### Step 2: Find the Next Task

1. Scan the document for checkbox markers
2. Find the first task that is:
   - Marked as `[-]` (in progress) - resume this task first
   - Or marked as `[ ]` (pending) - start this task
3. Skip tasks marked as `[x]` (completed)
4. If all tasks are complete, inform the user

### Step 3: Execute the Task

**IMPORTANT:** Each **subtask** is executed as a separate subagent and committed independently. Do NOT group subtasks into a single agent or commit.

If the next pending item is a **subtask** (e.g., 1.2):

1. **Mark subtask as in-progress** - Update the subtask checkbox to `[-]` in tasks.md
2. **Show task info** - Display to the user:
   - Subtask number and description
   - Files to create/modify
   - Requirements being addressed
3. **Launch subagent** - Use the Task tool with `subagent_type: "general-purpose"` to execute the subtask:
   - Provide the full subtask description, file paths, and requirements
   - Include relevant context from the spec (requirements.md, design.md)
4. **Verify result** - Review the subagent's output for success
5. **Mark subtask as complete** - Update the subtask checkbox to `[x]` in tasks.md
6. **Commit the changes** - Use the `git:commit` skill to commit (see Committing Changes section)
7. If all subtasks of the parent major task are now complete, mark the major task as `[x]` in tasks.md and commit this change using the `git:commit` skill

If the next pending item is a **major task** with subtasks, start with its first pending subtask using the flow above.

### Step 4: Handle Checkpoint Tasks

If the next task is a checkpoint:
1. Run any verification commands specified
2. Report the verification results
3. Mark as complete if all checks pass
4. Report issues if any checks fail

### Step 5: Report Completion

After completing the task:
1. Summarize what was implemented
2. Show the next pending task (if any)
3. Ask if the user wants to continue with the next task

## Committing Changes

After completing each **subtask**, commit using the `git:commit` skill:

1. Stage the changed files related to the subtask
2. Invoke the `git:commit` skill — it will analyze staged changes, determine the commit type, and create a properly formatted Conventional Commits message

Skip committing if:
- The user explicitly asked not to commit
- The subtask only modified the tasks.md file (checkpoint tasks)

## Error Handling

- If the task fails, keep it marked as `[-]`
- Report the issue to the user
- Suggest fixes or ask for guidance

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
