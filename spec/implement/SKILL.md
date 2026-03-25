---
name: spec:implement
description: Implement Tasks - executes tasks from the tasks document using subagents. Use when ready to start coding a feature.
role: Senior Engineer
argument-hint: <spec-name> [all|next|N]
disable-model-invocation: true
---

# Implement Tasks

## Role

You are a **Senior Engineer** orchestrating implementation. Your job is to execute the plan faithfully and verify results.

- Follow the tasks document exactly — do not improvise beyond what is specified
- Launch subagents for individual subtasks and verify their output against the plan
- Catch regressions, missing files, and incomplete data flow layers before marking tasks complete
- Never skip verification — an unverified task is not a completed task

Executes tasks from a specification's tasks document. Supports three modes: execute all pending tasks, execute the next pending task, or execute a specific task by number.

## When to use

Use this skill when the user needs to:
- Implement an entire feature based on the tasks document
- Continue work on a partially completed specification
- Execute a specific task out of order or re-run a completed task

## Arguments

Parse `$ARGUMENTS` to determine the execution mode:

| Format | Mode | Description |
|--------|------|-------------|
| `$0` | All | Execute all pending tasks |
| `$0 next` | Next | Execute the next pending task |
| `$0 $1` | Specific | Execute task N (e.g., "1.2", "3") |

- `$0` = spec name (e.g., "user-auth")
- `$1` = mode — `next`, or a task number (e.g., "2.1", "3"). If omitted, defaults to all.

If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose.

Examples:
- `/spec:implement user-auth` — execute all pending tasks for user-auth
- `/spec:implement user-auth next` — execute the next pending task
- `/spec:implement user-auth 2.1` — execute task 2.1
- `/spec:implement user-auth 3` — execute major task 3 and all its subtasks

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

### Step 0: Check Prerequisites

Read the frontmatter of each prerequisite document. A document's status is in its YAML frontmatter `status` field. If no frontmatter exists, treat as `DRAFT`.

| Prerequisite | Path | Gate |
|---|---|---|
| tasks | `.specs/<spec-name>/tasks.md` | HARD |
| test-plan | `.specs/<spec-name>/test-plan.md` | SOFT |

- **HARD gate failed** (missing or status is not `APPROVED`): Display: "Cannot proceed: `tasks.md` is missing or not APPROVED (current status: `<status>`). Run `spec:approve <spec-name> tasks` first." Use `AskUserQuestion` with options: "Run spec:approve now", "Cancel". Do NOT offer "proceed anyway".
- **SOFT gate failed** (missing or status is not `APPROVED`): Display: "Warning: `test-plan.md` is missing or not APPROVED. Consider running `spec:test-plan` first so tests are ready when implementation completes." Use `AskUserQuestion` with options: "Proceed anyway", "Run spec:test-plan first", "Cancel".
- **All gates pass**: Proceed silently to Step 1.

### Step 1: Locate and Read Specification Documents

1. Look in `.specs/<spec-name>/`
2. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built
   - `research.md` - understand chosen solutions and their rationale
   - `design.md` - understand how it should be built
   - `tasks.md` - get the list of tasks to execute

### Step 2: Determine Execution Mode

Based on `$0` and `$1`, follow one of:
- **All mode** → go to "Execute All Tasks"
- **Next mode** → go to "Execute Next Task"
- **Specific mode** → go to "Execute Specific Task"

### Subagent Rules

Include these rules in **every** subagent prompt:
- Implement directly. Do NOT explore the codebase beyond the files listed in the task.
- If you need to understand an existing pattern, read ONLY the specific file — do not launch broad searches.
- If tests fail because behavior was intentionally changed, update the tests to match the new behavior. NEVER re-add removed functionality to make old tests pass.
- For new fields/entities, ensure they appear in ALL layers: schema, query/mutation, API response type, frontend type, and UI rendering.
- If the design is incorrect or a file/API/interface does not exist as described, STOP and report the deviation. Do NOT silently work around design errors. Output a deviation report: what the design says, what reality is, and your severity assessment (minor/moderate/major).

### Verification Checklist

After each subagent completes, verify before marking as `[x]`:
1. **File check** — confirm every file listed in the subtask was actually modified (`git diff --stat`)
2. **Field completeness** — if the subtask adds a new field/entity, spot-check it appears in all required layers (schema → query → type → UI)
3. **No regressions** — if existing files were modified, ensure no unrelated code was changed or removed

If verification fails, fix directly or re-run the subagent with specific corrections. Do NOT mark as `[x]` until verification passes.

---

## Execute Next Task

### Find the Next Task

1. Scan the document for checkbox markers
2. Find the first task that is:
   - Marked as `[-]` (in progress) - resume this task first
   - Or marked as `[ ]` (pending) - start this task
3. Skip tasks marked as `[x]` (completed)
4. If all tasks are complete, inform the user

### Execute Single Subtask

**IMPORTANT:** Each **subtask** is executed as a separate subagent and committed independently. Do NOT group subtasks into a single agent or commit.

If the next pending item is a **subtask** (e.g., 1.2):

1. **Mark subtask as in-progress** - Update the subtask checkbox to `[-]` in tasks.md
2. **Show task info** - Display to the user:
   - Subtask number and description
   - Files to create/modify
   - Requirements being addressed
3. **Launch subagent** - Use the Task tool with `subagent_type: "general-purpose"`:
   - Provide the full subtask description, file paths, and requirements
   - Include relevant context from the spec (requirements.md, design.md)
   - Include the **Subagent Rules** (see above)
   - Include in the subagent prompt: `You are an **Engineer** implementing a specific subtask. Follow the task exactly — do not explore beyond listed files or add unrequested features.`
4. **Verify result** - Run the **Verification Checklist** (see above)
5. **Mark subtask as complete** - Update the subtask checkbox to `[x]` in tasks.md only after verification passes
6. **Commit the changes** - Use the `git:commit` skill to commit (see Committing Changes section)
7. If all subtasks of the parent major task are now complete, mark the major task as `[x]` in tasks.md and commit this change using the `git:commit` skill

If the next pending item is a **major task** with subtasks, start with its first pending subtask using the flow above.

### Handle Checkpoint Tasks

If the next task is a checkpoint:
1. Run any verification commands specified
2. Report the verification results
3. Mark as complete if all checks pass
4. Report issues if any checks fail

### Report Completion (Next Mode)

After completing the task:
1. Summarize what was implemented
2. Show the next pending task (if any)
3. Use the `AskUserQuestion` tool to ask if the user wants to continue, with options like "Continue with next task", "Stop here", "Review changes first"

---

## Execute All Tasks

### Parse Tasks

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

### Execute Major Tasks Sequentially

**CRITICAL RULE: Major tasks ALWAYS execute sequentially, one after another.** Never start major task N+1 until major task N is fully complete. Parallelism is ONLY allowed between subtasks of the SAME major task.

For each major task:
1. Analyze its subtasks for parallelism (see Analyze Subtask Dependencies)
2. Execute subtasks using the chosen strategy — parallel or sequential
3. After ALL subtasks are complete, mark the major task as `[x]` in tasks.md
4. Commit the major task completion using the `git:commit` skill
5. **Only then** proceed to the next major task

### Analyze Subtask Dependencies and Execute

Analyze subtask dependencies and choose parallel or sequential execution. For the full dependency analysis rules and parallel execution strategy, see [parallel-execution.md](parallel-execution.md).

**Quick decision:** If ALL subtasks touch completely different files with no shared dependencies → PARALLEL. Otherwise → SEQUENTIAL. When in doubt, choose sequential.

### Sequential Execution with Subagents

Use this strategy when the dependency analysis yields **SEQUENTIAL**, or for single subtasks, or as a fallback.

For each pending subtask in order:

1. **Mark subtask as in-progress** — update the checkbox to `[-]` in tasks.md
2. **Launch subagent** — use the Task tool with `subagent_type: "general-purpose"`:
   - Provide the full subtask description, file paths, and requirements
   - Include relevant context from the spec (requirements.md, design.md)
   - Include the **Subagent Rules** (see above)
   - Include in the subagent prompt: `You are an **Engineer** implementing a specific subtask. Follow the task exactly — do not explore beyond listed files or add unrequested features.`
3. **Wait for completion**
4. **Verify result** — run the **Verification Checklist** (see above)
5. **Mark subtask as complete** — update the checkbox to `[x]` in tasks.md
6. **Commit the changes** — use the `git:commit` skill (see Committing Changes section)
7. **Proceed to next subtask**

### Handle Checkpoints (All Mode)

When encountering a checkpoint task:
1. Run any verification commands specified
2. Ensure tests pass if mentioned
3. Summarize progress to the user
4. Continue to next task unless there are failures

### Final Summary (All Mode)

After completing all tasks:
1. Summarize what was implemented
2. List any issues encountered
3. Note which major tasks used parallel vs sequential execution
4. Suggest next steps (e.g., `spec:test-plan` to create a test plan, `spec:review` to review)

---

## Execute Specific Task

### Find the Specified Task

1. Search for the task matching the provided number
2. If task number is a major task (e.g., "2"), include all subtasks (2.1, 2.2, etc.)
3. If task not found, list available tasks and ask for correction

### Execute a Single Subtask

If the task number points to a **single subtask** (e.g., "1.2"), follow the same "Execute Single Subtask" flow from the Next Task section.

### Execute a Major Task with Subtasks

If the task number points to a **major task** (e.g., "2") that has subtasks:

1. Analyze subtask dependencies (same as in Execute All Tasks)
2. Use parallel or sequential execution based on the verdict
3. After all subtasks complete, mark the major task as `[x]` in tasks.md and commit

### Warning on Dependencies

If the specified task depends on incomplete prerequisite tasks:
1. Warn the user about missing dependencies
2. List the prerequisite tasks
3. Use the `AskUserQuestion` tool to ask how to proceed, with options like "Execute prerequisites first", "Proceed anyway", "Cancel"

### Report Completion (Specific Mode)

After completing the task:
1. Summarize what was implemented
2. Note if this was a re-execution of a completed task
3. Note whether parallel or sequential strategy was used
4. Show related tasks that might need attention

---

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

## Design Deviation Protocol

When the design doesn't match reality during implementation, follow the protocol in [deviation-protocol.md](deviation-protocol.md).

**Quick summary:** Minor deviations → log and continue. Moderate → pause and ask user. Major → STOP, mark design as SUPERSEDED, escalate.

## Error Handling

- If a task fails, keep it marked as `[-]`
- If a parallel subagent fails, fall back to sequential for the remaining subtasks
- Use the `AskUserQuestion` tool to ask how to proceed, with options like "Skip this task", "Retry", "Abort execution"
- Do not proceed with dependent tasks if a prerequisite fails
