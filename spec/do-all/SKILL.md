---
name: spec:do-all
description: Execute All Tasks - runs all pending tasks from the tasks document sequentially
---

# Execute All Tasks

Executes all pending tasks from a specification's tasks document. This skill reads the tasks.md file and implements each task in order, marking them as complete.

## When to use

Use this skill when the user needs to:
- Implement an entire feature based on the tasks document
- Execute all remaining tasks from a specification
- Complete the full implementation plan

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

### Step 2: Parse Tasks

1. Identify all tasks and subtasks using checkbox markers:
   - `[ ]` - Pending task (to be executed)
   - `[-]` - In progress task (continue execution)
   - `[x]` - Completed task (skip)
2. Build a task list with:
   - Task number (e.g., "1.1", "2.3")
   - Task description
   - File paths mentioned
   - Requirements references
3. Determine execution order based on task numbering

### Step 3: Execute Tasks Using Subagents

**IMPORTANT:** Each **subtask** is executed as a separate subagent and committed independently. Do NOT group subtasks of a major task into a single agent or a single commit.

For each major task, iterate over its subtasks. For each pending subtask:

1. **Mark subtask as in-progress** - Update the subtask checkbox to `[-]` in tasks.md
2. **Launch subagent** - Use the Task tool with `subagent_type: "general-purpose"` to execute the subtask:
   - Provide the full subtask description, file paths, and requirements
   - Include relevant context from the spec (requirements.md, design.md)
   - The subagent will implement the subtask autonomously
3. **Wait for completion** - Let the subagent complete its work
4. **Verify result** - Review the subagent's output for success
5. **Mark subtask as complete** - Update the subtask checkbox to `[x]` in tasks.md
6. **Commit the changes** - Use the `git:commit` skill to commit (see Committing Changes section)
7. **Proceed to next subtask**

After all subtasks of a major task are complete, mark the major task as `[x]` in tasks.md and commit this change using the `git:commit` skill.

Example Task tool call for a subtask:
```
Task tool:
  subagent_type: "general-purpose"
  description: "Execute task 1.2"
  prompt: |
    Execute subtask 1.2 from the specification.

    Task: [Subtask description from tasks.md]
    Files to modify: [file paths]
    Requirements: [requirement references]

    Context from design.md: [relevant design context]

    Implement this subtask following the project patterns.
```

**When NOT to use subagent:**
- Simple one-line changes
- Checkpoint/verification tasks (handle these directly)
- Tasks that require user interaction

### Step 4: Handle Checkpoints

When encountering a checkpoint task:
1. Run any verification commands specified
2. Ensure tests pass if mentioned
3. Summarize progress to the user
4. Continue to next task unless there are failures

### Step 5: Final Summary

After completing all tasks:
1. Summarize what was implemented
2. List any issues encountered
3. Suggest next steps (e.g., testing, review)

## Committing Changes

After completing each **subtask**, commit using the `git:commit` skill:

1. Stage the changed files related to the subtask
2. Invoke the `git:commit` skill — it will analyze staged changes, determine the commit type, and create a properly formatted Conventional Commits message

Skip committing if:
- The user explicitly asked not to commit
- The subtask only modified the tasks.md file (checkpoint tasks)

## Error Handling

- If a task fails, mark it as `[-]` and report the issue
- Ask the user how to proceed (skip, retry, abort)
- Do not proceed with dependent tasks if a prerequisite fails

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
