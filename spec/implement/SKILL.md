---
name: spec:implement
description: Implement Tasks - executes tasks from the tasks document using subagents. Use when ready to start coding a feature.
role: Senior Engineer
argument-hint: <spec-name> [all|next|N|gA]
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
| `$0` | All | Execute all pending tasks across all groups |
| `$0 next` | Next | Execute the next pending task |
| `$0 $1` (task number) | Specific | Execute task N (e.g., "1.2", "3") |
| `$0 gA` / `$0 groupA` / `$0 group A` | Group | Execute every pending task in group A and stop |

- `$0` = spec name (e.g., "user-auth")
- `$1` = mode — `next`, a task number (e.g., "2.1", "3"), or a group identifier (`gA`, `groupB`, or the literal `group` followed by `$2 = A`). If omitted, defaults to all.

A **group** is a `### Group X:` section in `tasks.md`. Groups are designed so each one can land on `main` independently without breaking anything (see `spec:tasks` group strategy). Group mode is the recommended way to ship work one PR at a time.

If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose. If a group identifier is given but the document has no groups (legacy spec), inform the user and offer to fall back to "all" or cancel.

Examples:
- `/spec:implement user-auth` — execute all pending tasks for user-auth
- `/spec:implement user-auth next` — execute the next pending task
- `/spec:implement user-auth 2.1` — execute task 2.1
- `/spec:implement user-auth 3` — execute major task 3 and all its subtasks
- `/spec:implement user-auth gA` — execute every pending task in Group A and stop
- `/spec:implement user-auth group B` — same as `gB`

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/requirements.md` | Requirements and acceptance criteria |
| `.specs/<spec-name>/research.md` | Variant catalogue per problem area (no decisions — see design.md) |
| `.specs/<spec-name>/design.md` | Technical design and architecture |
| `.specs/<spec-name>/tasks.md` | Implementation tasks with checkboxes |

**Always read all four files** to understand the full context before executing tasks.

## Instructions

### Step 0: Check Prerequisites

Prerequisites are checked by **file existence**, not by an approval status. There is no approval step in this pipeline.

| Prerequisite | Path | Requirement |
|---|---|---|
| tasks | `.specs/<spec-name>/tasks.md` | required |
| test-plan | `.specs/<spec-name>/test-plan.md` | recommended |

- **Required prerequisite missing** (`tasks.md` does not exist): Display: "Cannot proceed: `tasks.md` does not exist. Run `spec:tasks <spec-name>` first." Use `AskUserQuestion` with options: "Run spec:tasks now", "Cancel".
- **Recommended prerequisite missing** (`test-plan.md` does not exist): Display: "Warning: `test-plan.md` does not exist. Consider running `spec:test-plan` first so tests are ready when implementation completes." Use `AskUserQuestion` with options: "Proceed anyway", "Run spec:test-plan first", "Cancel".
- **Prerequisites satisfied**: Proceed silently to Step 1.

### Step 1: Locate and Read Specification Documents

1. Look in `.specs/<spec-name>/`
2. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be built
   - `research.md` - understand the variant menu the design picked from (decisions and rationale live in design.md's Decisions table)
   - `design.md` - understand how it should be built
   - `tasks.md` - get the list of tasks to execute

### Step 2: Determine Execution Mode

Based on `$0`, `$1`, and `$2`, follow one of:
- **All mode** → go to "Execute All Tasks"
- **Next mode** → go to "Execute Next Task"
- **Specific mode** (numeric `$1`) → go to "Execute Specific Task"
- **Group mode** (`$1` matches `g<letter>` / `group<letter>` / `group` + `$2`) → go to "Execute Group"

### Task Kinds

`tasks.md` may tag tasks with kinds. Handle each appropriately — never silently execute a task whose kind says a human must do it.

| Kind (title prefix) | Behaviour |
|---|---|
| _(no tag)_ | Implementation task. Run via subagent as normal. |
| `Infra — …` | Implementation task that touches Terraform / cloud configs. Run via subagent, but the subagent does NOT run `terraform apply` or any cloud-mutating CLI — it only writes the config files and prints the exact apply command for the user. |
| `External — …` | Action a human must perform in a third-party console (Google Cloud, Vercel, Stripe, etc.). Do NOT execute. Display the steps to the user, ask via `AskUserQuestion`: "I've done it", "Skip for now", "Cancel". Mark `[x]` only after the user confirms. |
| `⚠️ Cutover — …` | A production cutover. Do NOT execute autonomously even in `all` mode. Display the change, the validation steps, and the revert procedure; ask via `AskUserQuestion`: "Apply now (I'll do the env flip / merge in another window)", "Skip for now", "Cancel". Mark `[x]` only after the user confirms it has shipped and validation passed. |
| `Soak` (italic paragraph between groups) | Not a task. When you encounter it during `all` mode, stop and tell the user the soak window has begun, list the metrics to monitor, and exit. The user re-invokes `spec:implement` once the soak completes. |
| `Checkpoint` | Run verification commands, report results, mark `[x]` only if all pass. |

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
4. If `tasks.md` defines groups, list the groups in order and the commit hashes that fall inside each — this gives the user a ready-made map for splitting the work into PRs.
5. Remind the user that no PR was opened.
6. Suggest next steps (e.g., `spec:test-plan` to create a test plan, `spec:review` to review)

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

## Execute Group

Group mode runs every pending task inside a single `### Group X:` section, then stops — even if later groups have pending work. The intent is "produce one mergeable changeset, hand it to the user, let them PR it manually".

### Find the Specified Group

1. Parse the group identifier from `$1` / `$2` (strip the `g` or `group` prefix; uppercase the letter).
2. Locate the matching `### Group <letter>:` heading in `tasks.md`. If no heading matches, list the available group IDs from the document and use `AskUserQuestion` to ask the user to pick one or cancel.
3. If `tasks.md` has no `### Group` sections at all, the spec was authored before groups existed. Inform the user, then use `AskUserQuestion` with options "Run all tasks instead", "Cancel and regroup with `spec:tasks`".

### Check Group Dependencies

Read the **Shippable Groups** table at the top of `tasks.md`:

1. Identify the groups this group **depends on**.
2. For each dependency, confirm every task inside it is `[x]`. If any are pending, warn the user — merging this group alone may not be safe.
3. Use `AskUserQuestion` with options "Run prerequisite groups first", "Proceed anyway (I'll merge them together)", "Cancel".

### Execute the Group's Major Tasks

Walk every pending major task inside the group, in document order:

1. Apply the same flow as "Execute All Tasks → Execute Major Tasks Sequentially" — including the rule that **major tasks always execute sequentially**.
2. For each major task, run the dependency analysis on its subtasks (parallel vs sequential) per [parallel-execution.md](parallel-execution.md).
3. Run the group's checkpoint task(s) as part of the walk.
4. **Do not cross the group boundary.** When the next pending task is the first major task of the *next* group, stop.

### Report Completion (Group Mode)

After the group's last task is `[x]`:

1. State that Group `<letter>` is complete.
2. List the commits produced during this run (use `git log` to gather hashes since the group started).
3. Restate the group's blast radius from the table — `safe`, `gated`, or `coupled-to-X`.
4. Tell the user that no PR was opened (the skill never opens PRs) and that the commits are ready to be pushed/PRed manually when they choose.
5. Show what remains: how many groups still have pending work, and which group is next.
6. Use `AskUserQuestion` with options "Continue with next group", "Stop here", "Review changes first".

---

## Committing Changes

This skill **never** runs `git push`, `gh pr create`, or any other remote/PR command — even in group mode. Producing one PR per group is the user's job; this skill only produces commits. If the user explicitly asks for a PR, point them at `git:commit` plus their normal PR workflow.

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

**Quick summary:** Minor deviations → log and continue. Moderate → pause and ask user. Major → STOP, append a `## Deviations` note to `design.md`, escalate.

## Error Handling

- If a task fails, keep it marked as `[-]`
- If a parallel subagent fails, fall back to sequential for the remaining subtasks
- Use the `AskUserQuestion` tool to ask how to proceed, with options like "Skip this task", "Retry", "Abort execution"
- Do not proceed with dependent tasks if a prerequisite fails
