---
name: spec:do-task
description: Execute Specific Task - runs a task by its number from the tasks document
---

# Execute Specific Task

Executes a specific task by its number from a specification's tasks document. This skill allows targeted execution of any task in the plan.

## When to use

Use this skill when the user needs to:
- Execute a specific task out of order
- Re-run a previously completed task
- Jump to a particular task in the implementation plan

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/requirements.md` | Requirements and acceptance criteria |
| `.specs/<spec-name>/research.md` | Research findings and chosen solutions |
| `.specs/<spec-name>/design.md` | Technical design and architecture |
| `.specs/<spec-name>/tasks.md` | Implementation tasks with checkboxes |

**Always read all four files** to understand the full context before executing tasks.

## Instructions

### Step 1: Parse Arguments

The `<args>` should contain:
- Task number (required) - e.g., "1", "1.2", "3.1"
- Spec name (optional) - e.g., "user-auth"

Format examples:
- `spec:do-task 1.2` - Execute task 1.2 from the current/only spec
- `spec:do-task user-auth 2.1` - Execute task 2.1 from the user-auth spec
- `spec:do-task 3` - Execute major task 3 (and all its subtasks)

### Step 2: Locate and Read Specification Documents

1. If spec name provided, look in `.specs/<spec-name>/`
2. If no spec name, check if there's only one spec in `.specs/`
3. If multiple specs exist without a name specified, list them and ask user to choose
4. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built
   - `research.md` - understand chosen solutions and their rationale
   - `design.md` - understand how it should be built
   - `tasks.md` - get the list of tasks to execute

### Step 3: Find the Specified Task

1. Search for the task matching the provided number
2. If task number is a major task (e.g., "2"), include all subtasks (2.1, 2.2, etc.)
3. If task not found, list available tasks and ask for correction

### Step 4: Execute a Single Subtask

If the task number points to a **single subtask** (e.g., "1.2"):

1. **Mark subtask as in-progress** - Update the subtask checkbox to `[-]` in tasks.md
2. **Show task info** - Display to the user:
   - Subtask number and description
   - Files to create/modify
   - Requirements being addressed
   - Current status (pending/in-progress/completed)
3. **Launch subagent** - Use the Task tool with `subagent_type: "general-purpose"` to execute the subtask:
   - Provide the full subtask description, file paths, and requirements
   - Include relevant context from the spec (requirements.md, design.md)
   - Include these rules in the prompt:
     - Implement directly. Do NOT explore the codebase beyond the files listed in the task.
     - If you need to understand an existing pattern, read ONLY the specific file — do not launch broad searches.
     - If tests fail because behavior was intentionally changed, update the tests to match the new behavior. NEVER re-add removed functionality to make old tests pass.
     - For new fields/entities, ensure they appear in ALL layers: schema, query/mutation, API response type, frontend type, and UI rendering.
4. **Verify result** - After the subagent completes:
   - Confirm every file listed in the subtask was actually modified (`git diff --stat`)
   - If the subtask adds a new field, spot-check it appears in all required layers (schema → query → type → UI)
   - If verification fails, fix directly or re-run the subagent with specific corrections
5. **Mark subtask as complete** - Update the subtask checkbox to `[x]` in tasks.md only after verification passes
6. **Commit the changes** - Use the `git:commit` skill to commit (see Committing Changes section)
7. If all subtasks of the parent major task are now complete, mark the major task as `[x]` in tasks.md and commit this change using the `git:commit` skill

### Step 5: Execute a Major Task with Subtasks

If the task number points to a **major task** (e.g., "2") that has subtasks:

#### Step 5a: Analyze Subtask Dependencies

Before executing subtasks, analyze whether they can run in parallel. Check each subtask pair for conflicts:

**Subtasks are DEPENDENT (must run sequentially) when ANY of the following is true:**
- They modify the same file
- One creates a file/module/export that another imports or uses
- One generates types, schemas, or configs consumed by another
- They have an explicit ordering requirement in the task description
- One subtask's output is another's input (e.g., "create API" → "write tests for API")
- They modify related parts of the same system (e.g., both touch the same database table schema)

**Subtasks are INDEPENDENT (can run in parallel) when ALL of the following are true:**
- They touch completely different files
- No data or import dependencies between them
- No shared state (database tables, config files, global state)
- Each is self-contained and can be verified independently

**When in doubt, choose sequential execution.** The quality of the implementation is more important than speed.

Produce a short dependency verdict before proceeding:

```
Major Task 2 — dependency analysis:
  2.1 Create user model (files: src/models/user.ts)
  2.2 Create auth middleware (files: src/middleware/auth.ts) — depends on 2.1 (imports User type)
  2.3 Add login route (files: src/routes/login.ts) — depends on 2.1, 2.2
  Verdict: SEQUENTIAL — chain of dependencies
```

#### Step 5b: Parallel Execution with Concurrent Subagents

Use this strategy when the dependency analysis yields **PARALLEL**.

1. **Mark all parallel subtasks as in-progress** — update each checkbox to `[-]` in tasks.md
2. **Launch all subagents in a single message** — use multiple Task tool calls (one per subtask) in the same response, each with `subagent_type: "general-purpose"`:
   - Provide the full subtask description, file paths, and requirements
   - Include relevant context from the spec (requirements.md, design.md)
   - Instruct each subagent: implement the subtask but do NOT commit
   - Include these rules in each prompt:
     - Implement directly. Do NOT explore the codebase beyond the files listed in the task.
     - If you need to understand an existing pattern, read ONLY the specific file — do not launch broad searches.
     - If tests fail because behavior was intentionally changed, update the tests. NEVER re-add removed functionality.
     - For new fields/entities, ensure they appear in ALL layers: schema, query/mutation, API response type, frontend type, and UI rendering.
3. **Wait for all subagents to complete**
4. **Verify results** — for each subagent, confirm every file listed in the subtask was modified and new fields appear in all required layers
5. **Mark all subtasks as `[x]`** in tasks.md
6. **Commit all changes together** — single commit for the batch using `git:commit` skill

**Constraints:**
- Maximum 3 parallel subagents at a time
- If more than 3 independent subtasks, batch them in groups of 3
- If any subagent fails, fall back to sequential for remaining subtasks
- Subagents must NOT commit — only you commit after verification

#### Step 5c: Sequential Execution with Subagents

Use this strategy when the dependency analysis yields **SEQUENTIAL**, or as a fallback.

For each subtask, follow the single subtask execution flow from Step 4 (separate subagent + separate commit per subtask).

After all subtasks complete, mark the major task as `[x]` in tasks.md and commit using `git:commit` skill.

### Step 6: Report Completion

After completing the task:
1. Summarize what was implemented
2. Note if this was a re-execution of a completed task
3. Note whether parallel or sequential strategy was used
4. Show related tasks that might need attention

## Committing Changes

### After sequential subtask execution

Commit each subtask individually using the `git:commit` skill:

1. Stage the changed files related to the subtask
2. Check if `tasks.md` is tracked by git (run `git check-ignore .specs/<spec-name>/tasks.md`). If it is NOT ignored, also stage `tasks.md` in the same commit so the task progress is captured
3. Invoke the `git:commit` skill

### After parallel subtask execution

Commit ALL subtasks from the parallel batch together as a single commit:

1. Stage all changed files from all completed parallel subtasks
2. Include `tasks.md` if tracked
3. Invoke the `git:commit` skill

### Skip committing if:
- The user explicitly asked not to commit
- The subtask only modified the tasks.md file (checkpoint tasks)

## Warning on Dependencies

If the specified task depends on incomplete prerequisite tasks:
1. Warn the user about missing dependencies
2. List the prerequisite tasks
3. Ask if they want to:
   - Execute prerequisites first
   - Proceed anyway
   - Cancel

## Error Handling

- If the task fails, keep it marked as `[-]`
- If a parallel subagent fails, fall back to sequential for remaining subtasks
- Report the issue to the user
- Suggest fixes or ask for guidance

## Arguments

- `<args>` - Task number and optionally spec name
  - Format: `[spec-name] <task-number>`
  - Task number: "1", "1.2", "2.3.1", etc.
  - Spec name: kebab-case identifier

Examples:
- `1.2` - Task 1.2 from the default/only spec
- `user-auth 3.1` - Task 3.1 from user-auth spec
- `payment-flow 2` - All of task 2 from payment-flow spec
