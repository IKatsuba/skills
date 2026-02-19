---
name: spec:test-next
description: Execute Next Test - walks through the next pending test case from the test plan
---

# Execute Next Test

Finds and presents the next pending test case from a specification's test plan document. The user performs the test manually and reports the result.

## When to use

Use this skill when the user needs to:
- Execute one test at a time with review between tests
- Continue testing a partially completed test plan
- Work through tests incrementally with manual control

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

### Step 2: Find the Next Test

1. Scan the document for checkbox markers
2. Find the first test case that is:
   - Marked as `[-]` (in progress) - resume this test first
   - Or marked as `[ ]` (pending) - start this test
3. Skip tests marked as `[x]` (passed), `[!]` (failed), or `[s]` (skipped)
4. If all tests are complete, show the final Summary section and inform the user

### Step 3: Present the Test

1. Mark the test case as `[-]` (in progress) in `test-plan.md`
2. Display to the user:
   - Test number and name
   - Preconditions
   - Step-by-step instructions
   - Expected result
   - Requirements being verified

### Step 4: Collect Result

Use the `AskUserQuestion` tool to ask: "What was the result of this test?"

Options:
- "Passed" — test met expected result
- "Failed" — test did not meet expected result
- "Skipped" — test was not applicable or blocked

If the user selects "Failed", use the `AskUserQuestion` tool to ask: "What happened? Describe the failure." with a free-text option.

### Step 5: Update Test Plan

Based on the result:
- **Passed**: Mark the test case as `[x]` in `test-plan.md`
- **Failed**: Mark the test case as `[!]` in `test-plan.md`. Add a failure note below the test case: `    - **FAILED:** [user's failure description]`
- **Skipped**: Mark the test case as `[s]` in `test-plan.md`

If all test cases within a scenario group are now complete (all `[x]`, `[!]`, or `[s]`), mark the scenario group checkbox accordingly:
- All passed → `[x]`
- Any failed → `[!]`
- All skipped → `[s]`

### Step 6: Update Summary Counters

Update the Summary section at the bottom of `test-plan.md`:
- Recount Passed, Failed, and Skipped from the current checkbox states
- Total remains the same

### Step 7: Commit Changes

1. Stage `test-plan.md`
2. Check if `test-plan.md` is tracked by git (run `git check-ignore .specs/<spec-name>/test-plan.md`). If it is NOT ignored, invoke the `git:commit` skill
3. Skip committing if the user explicitly asked not to commit

### Step 8: Offer to Continue

Use the `AskUserQuestion` tool to ask: "Continue to next test?"

Options:
- "Continue with next test"
- "Stop here"
- "Review test plan"

If the user chooses to continue, go back to Step 2.

## Error Handling

- If `test-plan.md` does not exist, inform the user and suggest running `spec:test-plan` first
- If the test plan has no pending tests, show the Summary and inform the user

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
