---
name: spec:test-task
description: Execute Specific Test - runs a specific test case by number from the test plan
---

# Execute Specific Test

Executes a specific test case by its number from a specification's test plan document. This skill allows targeted execution of any test, useful for re-testing failed tests or running tests out of order.

## When to use

Use this skill when the user needs to:
- Re-test a specific failed test case
- Run a particular test out of order
- Verify a fix for a previously failed test

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/test-plan.md` | Manual test plan with test cases |

## Instructions

### Step 1: Parse Arguments

The `<args>` should contain:
- Test number (required) - e.g., "1.2", "2.1"
- Spec name (optional) - e.g., "user-auth"

Format examples:
- `spec:test-task 1.2` - Execute test 1.2 from the current/only spec
- `spec:test-task user-auth 2.1` - Execute test 2.1 from the user-auth spec
- `spec:test-task 3` - Execute all tests in scenario group 3

### Step 2: Locate and Read Test Plan

1. If spec name provided, look in `.specs/<spec-name>/test-plan.md`
2. If no spec name, check if there's only one spec in `.specs/`
3. If multiple specs exist without a name specified, list them and use the `AskUserQuestion` tool to let the user choose
4. Read and parse `test-plan.md`

### Step 3: Find the Specified Test

1. Search for the test matching the provided number
2. If test number is a scenario group (e.g., "2"), include all test cases in that group (2.1, 2.2, etc.)
3. If test not found, list available tests and ask for correction

### Step 4: Execute a Single Test Case

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

### Step 5: Execute a Scenario Group

If the test number points to a **scenario group** (e.g., "2") with multiple test cases:

For each test case in the group, in order:
1. Follow the single test case flow from Step 4
2. After each test case, use the `AskUserQuestion` tool to ask: "Continue to next test in this group?" with options "Continue", "Stop here"
3. After all test cases in the group complete, show a group summary

### Step 6: Report Completion

After completing the test(s):
1. Show the result (passed/failed/skipped)
2. Note if this was a re-test of a previously completed test
3. Show the updated Summary section

## Error Handling

- If `test-plan.md` does not exist, inform the user and suggest running `spec:test-plan` first
- If the specified test number does not exist, list available tests and use the `AskUserQuestion` tool to let the user pick

## Arguments

- `<args>` - Test number and optionally spec name
  - Format: `[spec-name] <test-number>`
  - Test number: "1", "1.2", etc.
  - Spec name: kebab-case identifier

Examples:
- `1.2` - Test 1.2 from the default/only spec
- `user-auth 3.1` - Test 3.1 from user-auth spec
- `payment-flow 2` - All tests in group 2 from payment-flow spec
