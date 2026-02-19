---
name: spec:test-all
description: Execute All Tests - walks through all pending test cases from the test plan sequentially
---

# Execute All Tests

Walks through all pending test cases from a specification's test plan document. Presents each test sequentially, waits for user results, and commits after each test.

## When to use

Use this skill when the user needs to:
- Run through the entire test plan in one session
- Execute all remaining tests from a partially completed plan
- Complete the full manual testing phase

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/test-plan.md` | Manual test plan with test cases |

## Instructions

### Step 1: Locate and Read Test Plan

1. If `<args>` contains a spec name, look in `.specs/<spec-name>/test-plan.md`
2. If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose
3. Read and parse `test-plan.md`
4. Show the user a summary: total tests, how many passed/failed/skipped/pending

### Step 2: Loop Through Tests

For each pending test case (in document order), repeat the following:

#### Step 2a: Find Next Test

1. Scan for the first test case marked as `[-]` (in progress) or `[ ]` (pending)
2. Skip tests marked as `[x]` (passed), `[!]` (failed), or `[s]` (skipped)
3. If no pending tests remain, go to Step 3

#### Step 2b: Present the Test

1. Mark the test case as `[-]` (in progress) in `test-plan.md`
2. Display to the user:
   - Test number and name (e.g., "Test 2.3 of 12")
   - Preconditions
   - Step-by-step instructions
   - Expected result
   - Requirements being verified

#### Step 2c: Collect Result

Use the `AskUserQuestion` tool to ask: "What was the result of this test?"

Options:
- "Passed" — test met expected result
- "Failed" — test did not meet expected result
- "Skipped" — test was not applicable or blocked
- "Stop testing" — end the session

If the user selects "Failed", use the `AskUserQuestion` tool to ask: "What happened? Describe the failure." with a free-text option.

If the user selects "Stop testing", go to Step 3.

#### Step 2d: Update Test Plan

Based on the result:
- **Passed**: Mark the test case as `[x]` in `test-plan.md`
- **Failed**: Mark the test case as `[!]` in `test-plan.md`. Add a failure note below the test case: `    - **FAILED:** [user's failure description]`
- **Skipped**: Mark the test case as `[s]` in `test-plan.md`

If all test cases within a scenario group are now complete (all `[x]`, `[!]`, or `[s]`), mark the scenario group checkbox accordingly:
- All passed → `[x]`
- Any failed → `[!]`
- All skipped → `[s]`

#### Step 2e: Update Summary Counters

Update the Summary section at the bottom of `test-plan.md`:
- Recount Passed, Failed, and Skipped from the current checkbox states
- Total remains the same

#### Step 2f: Commit Changes

1. Stage `test-plan.md`
2. Check if `test-plan.md` is tracked by git (run `git check-ignore .specs/<spec-name>/test-plan.md`). If it is NOT ignored, invoke the `git:commit` skill
3. Skip committing if the user explicitly asked not to commit

#### Step 2g: Continue Loop

Go back to Step 2a.

### Step 3: Final Summary

After all tests are complete or the user stops:
1. Read the final state of `test-plan.md`
2. Display the Summary section:
   - Total tests
   - Passed count
   - Failed count (list which tests failed)
   - Skipped count
3. If there are failures, list the failed test cases with their failure notes
4. Use the `AskUserQuestion` tool to ask: "What would you like to do next?" with options like "Re-test failed tests", "Generate failure report", "Done testing"

## Error Handling

- If `test-plan.md` does not exist, inform the user and suggest running `spec:test-plan` first
- If the test plan has no pending tests, show the Summary and inform the user

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
