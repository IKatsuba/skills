# Parallel Execution Strategy

## Analyze Subtask Dependencies

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

## Parallel Execution with Concurrent Subagents

Use this strategy when the dependency analysis yields **PARALLEL**.

1. **Mark all parallel subtasks as in-progress** — update each checkbox to `[-]` in tasks.md
2. **Launch all subagents in a single message** — use multiple Task tool calls (one per subtask) in the same response, each with `subagent_type: "general-purpose"`:
   - Provide the full subtask description, file paths, and requirements
   - Include relevant context from the spec (requirements.md, design.md)
   - Instruct each subagent: implement the subtask but do NOT commit
   - Include the **Subagent Rules** from the main skill
   - Include in the subagent prompt: `You are an **Engineer** implementing a specific subtask. Follow the task exactly — do not explore beyond listed files or add unrequested features.`
3. **Wait for all subagents to complete**
4. **Verify results** — run the **Verification Checklist** for each subagent
5. **Mark all subtasks as `[x]`** in tasks.md
6. **Commit all changes together** — stage all files from the parallel batch and use `git:commit` skill once for the group

**Constraints:**
- Maximum 3 parallel subagents at a time to avoid resource contention
- If a major task has more than 3 independent subtasks, batch them in groups of 3
- If any subagent fails, stop and fall back to sequential execution for remaining subtasks
- Subagents must NOT commit — only you commit after verifying all results
