---
name: spec:do-all
description: Execute All Tasks - runs all pending tasks from the tasks document, with parallel subtask execution when safe
---

# Execute All Tasks

Executes all pending tasks from a specification's tasks document. Major tasks run sequentially. Subtasks within a single major task can run in parallel via concurrent subagents when they are independent.

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
| `.specs/<spec-name>/research.md` | Research findings and chosen solutions |
| `.specs/<spec-name>/design.md` | Technical design and architecture |
| `.specs/<spec-name>/tasks.md` | Implementation tasks with checkboxes |

**Always read all four files** to understand the full context before executing tasks.

## Instructions

### Step 1: Locate and Read Specification Documents

1. If `<args>` contains a spec name, look in `.specs/<spec-name>/`
2. If no spec name provided, list available specs in `.specs/` and ask user to choose
3. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built
   - `research.md` - understand chosen solutions and their rationale
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

### Step 3: Execute Major Tasks Sequentially

**CRITICAL RULE: Major tasks ALWAYS execute sequentially, one after another.** Never start major task N+1 until major task N is fully complete. Parallelism is ONLY allowed between subtasks of the SAME major task.

For each major task:
1. Analyze its subtasks for parallelism (see Step 3a)
2. Execute subtasks using the chosen strategy — parallel or sequential (see Steps 3b/3c)
3. After ALL subtasks are complete, mark the major task as `[x]` in tasks.md
4. Commit the major task completion using the `git:commit` skill
5. **Only then** proceed to the next major task

### Step 3a: Analyze Subtask Dependencies

Before executing a major task's subtasks, analyze whether they can run in parallel. Check each subtask pair for conflicts:

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

Produce a short dependency verdict for the major task before proceeding:

```
Major Task 2 — dependency analysis:
  2.1 Create user model (files: src/models/user.ts)
  2.2 Create auth middleware (files: src/middleware/auth.ts) — depends on 2.1 (imports User type)
  2.3 Add login route (files: src/routes/login.ts) — depends on 2.1, 2.2
  Verdict: SEQUENTIAL — chain of dependencies
```

or

```
Major Task 3 — dependency analysis:
  3.1 Add email validation util (files: src/utils/email.ts)
  3.2 Add phone validation util (files: src/utils/phone.ts)
  3.3 Add address validation util (files: src/utils/address.ts)
  Verdict: PARALLEL — all independent, no shared files or imports
```

### Step 3b: Parallel Execution with Concurrent Subagents

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
6. **Commit all changes together** — stage all files from the parallel batch and use `git:commit` skill once for the group

**IMPORTANT constraints for parallel execution:**
- Maximum 3 parallel subagents at a time to avoid resource contention
- If a major task has more than 3 independent subtasks, batch them in groups of 3
- If any subagent fails, stop and fall back to sequential execution for remaining subtasks
- Subagents must NOT commit — only you commit after verifying all results

### Step 3c: Sequential Execution with Subagents

Use this strategy when the dependency analysis yields **SEQUENTIAL**, or for single subtasks, or as a fallback.

For each pending subtask in order:

1. **Mark subtask as in-progress** — update the checkbox to `[-]` in tasks.md
2. **Launch subagent** — use the Task tool with `subagent_type: "general-purpose"`:
   - Provide the full subtask description, file paths, and requirements
   - Include relevant context from the spec (requirements.md, design.md)
   - The subagent implements the subtask autonomously
3. **Wait for completion**
4. **Verify result** — review the subagent's output for success
5. **Mark subtask as complete** — update the checkbox to `[x]` in tasks.md
6. **Commit the changes** — use the `git:commit` skill (see Committing Changes section)
7. **Proceed to next subtask**

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

    RULES:
    - Implement directly. Do NOT explore the codebase beyond the files listed above.
    - If you need to understand an existing pattern, read ONLY the specific file — do not launch broad searches.
    - If tests fail because behavior was intentionally changed, update the tests to match the new behavior. NEVER re-add removed functionality to make old tests pass.
    - For new fields/entities, ensure they appear in ALL layers: schema, query/mutation, API response type, frontend type, and UI rendering.
```

**When NOT to use subagent:**
- Simple one-line changes
- Checkpoint/verification tasks (handle these directly)
- Tasks that require user interaction

### Step 3d: Post-Subtask Verification

After each subagent completes (whether parallel or sequential), verify before marking as `[x]`:

1. **File check** — confirm that every file listed in the subtask was actually modified (use `git diff --stat`)
2. **Field completeness** — if the subtask adds a new field or entity, spot-check that it appears in all required layers (schema → query → type → UI)
3. **No regressions** — if the subtask modified existing files, ensure no unrelated code was changed or removed

If verification fails, either fix it directly or re-run the subagent with specific correction instructions. Do NOT mark the subtask as `[x]` until verification passes.

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
3. Note which major tasks used parallel vs sequential execution
4. Suggest next steps (e.g., testing, review)

## Committing Changes

### After sequential subtask execution

Commit each subtask individually using the `git:commit` skill:

1. Stage the changed files related to the subtask
2. Check if `tasks.md` is tracked by git (run `git check-ignore .specs/<spec-name>/tasks.md`). If it is NOT ignored, also stage `tasks.md` in the same commit so the task progress is captured
3. Invoke the `git:commit` skill — it will analyze staged changes, determine the commit type, and create a properly formatted Conventional Commits message

### After parallel subtask execution

Commit ALL subtasks from the parallel batch together as a single commit:

1. Stage all changed files from all completed parallel subtasks
2. Include `tasks.md` if tracked
3. Invoke the `git:commit` skill — the commit message should reference the major task (e.g., "feat(auth): implement validation utilities (tasks 3.1-3.3)")

### Skip committing if:
- The user explicitly asked not to commit
- The subtask only modified the tasks.md file (checkpoint tasks)

## Error Handling

- If a task fails, mark it as `[-]` and report the issue
- If a parallel subagent fails, fall back to sequential for the remaining subtasks of that major task
- Ask the user how to proceed (skip, retry, abort)
- Do not proceed with dependent tasks if a prerequisite fails

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
