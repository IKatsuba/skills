---
name: spec:test
description: Execute Tests - walks through test cases from the test plan, collects results, and updates the plan. Use when verifying a feature implementation.
role: QA Engineer
argument-hint: <spec-name> [all|next|N]
disable-model-invocation: true
---

# Execute Tests

## Role

You are a **QA Engineer** executing tests. Your job is to report results accurately, not to make tests pass.

- Present each test case clearly with all context the tester needs
- Record results exactly as observed — never round a "partial pass" up to "passed"
- Capture failure details thoroughly enough to reproduce and debug
- Never modify test cases during execution — if a test is wrong, flag it and move on

Walks through test cases from a specification's test plan document. Presents each test to the user, collects results, and updates the test plan. Supports three modes: execute all pending tests, execute the next pending test, or execute a specific test by number.

## When to use

Use this skill when the user needs to:
- Run through the entire test plan in one session
- Execute one test at a time with review between tests
- Re-test a specific failed test case or run a particular test out of order

## Arguments

Parse `$ARGUMENTS` to determine the execution mode:

| Format | Mode | Description |
|--------|------|-------------|
| `$0` | All | Walk through all pending tests |
| `$0 next` | Next | Execute the next pending test |
| `$0 $1` | Specific | Execute test N (e.g., "1.2", "2") |

- `$0` = spec name (e.g., "user-auth")
- `$1` = mode — `next`, or a test number (e.g., "2.1", "3"). If omitted, defaults to all.

If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose.

Examples:
- `/spec:test user-auth` — walk through all pending tests for user-auth
- `/spec:test user-auth next` — execute the next pending test
- `/spec:test user-auth 2.1` — execute test 2.1
- `/spec:test user-auth 3` — execute all tests in scenario group 3

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/test-plan.md` | Manual test plan with test cases |

## Instructions

### Step 0: Check Prerequisites

Prerequisites are checked by **file existence**, not by an approval status. There is no approval step in this pipeline.

| Prerequisite | Path | Requirement |
|---|---|---|
| test-plan | `.specs/<spec-name>/test-plan.md` | required |

- **Required prerequisite missing** (`test-plan.md` does not exist): Display: "Cannot proceed: `test-plan.md` does not exist. Run `spec:test-plan <spec-name>` first." Use `AskUserQuestion` with options: "Run spec:test-plan now", "Cancel".

Additionally, verify that `.specs/<spec-name>/tasks.md` exists and all implementation task checkboxes are marked `[x]`. If implementation is incomplete, display: "Cannot proceed: implementation is not complete (N/M tasks done). Run `spec:implement <spec-name>` first." Use `AskUserQuestion` with options: "Run spec:implement now", "Proceed anyway", "Cancel".

- **Prerequisites satisfied**: Proceed silently to Step 1.

### Step 1: Locate and Read Test Plan

1. Look in `.specs/<spec-name>/test-plan.md`
2. Read and parse `test-plan.md`
3. If `test-plan.md` does not exist, inform the user and suggest running `spec:test-plan` first

### Step 2: Determine Execution Mode

Based on `$0` and `$1`, follow one of:
- **All mode** → go to "Execute All Tests"
- **Next mode** → go to "Execute Next Test"
- **Specific mode** → go to "Execute Specific Test"

---

## Execute Next Test

### Find the Next Test

1. Scan the document for checkbox markers
2. Find the first test case that is:
   - Marked as `[-]` (in progress) - resume this test first
   - Or marked as `[ ]` (pending) - start this test
3. Skip tests marked as `[x]` (passed), `[!]` (failed), or `[s]` (skipped)
4. If all tests are complete, show the final Summary section and inform the user

### Present the Test

1. Mark the test case as `[-]` (in progress) in `test-plan.md`
2. Display to the user:
   - Test number and name
   - Preconditions
   - Step-by-step instructions
   - Expected result
   - Requirements being verified

### Collect Result

Use the `AskUserQuestion` tool to ask: "What was the result of this test?"

Options:
- "Passed" — test met expected result
- "Failed" — test did not meet expected result
- "Skipped" — test was not applicable or blocked

If the user selects "Failed", use the `AskUserQuestion` tool to ask: "What happened? Describe the failure." with a free-text option.

### Update Test Plan

Based on the result:
- **Passed**: Mark the test case as `[x]` in `test-plan.md`
- **Failed**: Mark the test case as `[!]` in `test-plan.md`. Add a failure note below the test case: `    - **FAILED:** [user's failure description]`
- **Skipped**: Mark the test case as `[s]` in `test-plan.md`

If all test cases within a scenario group are now complete (all `[x]`, `[!]`, or `[s]`), mark the scenario group checkbox accordingly:
- All passed → `[x]`
- Any failed → `[!]`
- All skipped → `[s]`

### Update Summary Counters

Update the Summary section at the bottom of `test-plan.md`:
- Recount Passed, Failed, and Skipped from the current checkbox states
- Total remains the same

### Commit Changes

1. Stage `test-plan.md`
2. Check if `test-plan.md` is tracked by git (run `git check-ignore .specs/<spec-name>/test-plan.md`). If it is NOT ignored, invoke the `git:commit` skill
3. Skip committing if the user explicitly asked not to commit

### Offer to Continue (Next Mode)

Use the `AskUserQuestion` tool to ask: "Continue to next test?"

Options:
- "Continue with next test"
- "Stop here"
- "Review test plan"

If the user chooses to continue, go back to Find the Next Test.

---

## Execute All Tests

### Show Overview

Show the user a summary: total tests, how many passed/failed/skipped/pending.

### Loop Through Tests

For each pending test case (in document order), repeat the following:

1. **Find next** — scan for the first test case marked as `[-]` or `[ ]`. Skip `[x]`, `[!]`, `[s]`. If none remain, go to Final Summary.
2. **Present the test** — mark as `[-]` and display test details (same as Execute Next Test)
3. **Collect result** — use `AskUserQuestion` with options: "Passed", "Failed", "Skipped", "Stop testing". If "Failed", ask for failure description. If "Stop testing", go to Final Summary.
4. **Update test plan** — mark result, update scenario group if complete
5. **Update summary counters** — recount from checkbox states
6. **Commit changes** — stage and commit via `git:commit` skill
7. **Continue loop** — go back to step 1

### Final Summary

After all tests are complete or the user stops:
1. Read the final state of `test-plan.md`
2. Display the Summary section:
   - Total tests
   - Passed count
   - Failed count (list which tests failed)
   - Skipped count
3. If there are failures, list the failed test cases with their failure notes
4. Use the `AskUserQuestion` tool to ask: "What would you like to do next?" with options like "Re-test failed tests", "Generate failure report", "Done testing"

---

## Execute Specific Test

### Find the Specified Test

1. Search for the test matching the provided number
2. If test number is a scenario group (e.g., "2"), include all test cases in that group (2.1, 2.2, etc.)
3. If test not found, list available tests and ask for correction

### Execute a Single Test Case

If the test number points to a **single test case** (e.g., "1.2"):

1. **Mark as in-progress** - Update the test case checkbox to `[-]` in `test-plan.md`
2. **Show test info** - Display to the user:
   - Test number and name
   - Current status (pending/passed/failed — note if this is a re-test)
   - Preconditions
   - Step-by-step instructions
   - Expected result
   - Requirements being verified
3. **Collect result** - Use the `AskUserQuestion` tool to ask: "What was the result of this test?"
   - Options: "Passed", "Failed", "Skipped"
   - If "Failed", use the `AskUserQuestion` tool to ask for failure description
4. **Update test plan** - Based on the result:
   - **Passed**: Mark as `[x]`. If this was previously `[!]` (failed), remove the old failure note
   - **Failed**: Mark as `[!]`. Add or update failure note: `    - **FAILED:** [description]`
   - **Skipped**: Mark as `[s]`
5. **Update scenario group** - If all test cases within the group are now complete:
   - All passed → `[x]`
   - Any failed → `[!]`
   - All skipped → `[s]`
6. **Update Summary counters** - Recount Passed, Failed, and Skipped
7. **Commit changes** - Stage `test-plan.md` and invoke the `git:commit` skill (if tracked)

### Execute a Scenario Group

If the test number points to a **scenario group** (e.g., "2") with multiple test cases:

For each test case in the group, in order:
1. Follow the single test case flow from above
2. After each test case, use the `AskUserQuestion` tool to ask: "Continue to next test in this group?" with options "Continue", "Stop here"
3. After all test cases in the group complete, show a group summary

### Report Completion (Specific Mode)

After completing the test(s):
1. Show the result (passed/failed/skipped)
2. Note if this was a re-test of a previously completed test
3. Show the updated Summary section

---

## Error Handling

- If `test-plan.md` does not exist, inform the user and suggest running `spec:test-plan` first
- If the test plan has no pending tests, show the Summary and inform the user
- If the specified test number does not exist, list available tests and use the `AskUserQuestion` tool to let the user pick
