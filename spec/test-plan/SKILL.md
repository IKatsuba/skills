---
name: spec:test-plan
description: Generate Test Plan - creates a manual test plan document from specification documents
---

# Generate Test Plan

Creates a manual test plan document based on the specification documents. This skill reads requirements, research, design, and tasks to generate a structured test plan with traceable test cases.

## When to use

Use this skill when the user needs to:
- Create a manual test plan after implementation is complete
- Generate test scenarios from existing specification documents
- Establish a structured testing phase for a feature

## Specification Files Structure

All specification documents are located in `.specs/<spec-name>/` directory:

| File | Description |
|------|-------------|
| `.specs/<spec-name>/requirements.md` | Requirements and acceptance criteria |
| `.specs/<spec-name>/research.md` | Research findings and chosen solutions |
| `.specs/<spec-name>/design.md` | Technical design and architecture |
| `.specs/<spec-name>/tasks.md` | Implementation tasks with checkboxes |

**Read all available files** to understand the full context before generating the test plan.

## Instructions

### Step 1: Locate and Read Specification Documents

1. If `<args>` contains a spec name, look in `.specs/<spec-name>/`
2. If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose
3. Read and parse all specification documents:
   - `requirements.md` - understand what needs to be tested
   - `research.md` - understand chosen solutions and edge cases
   - `design.md` - understand architecture and integration points
   - `tasks.md` - understand what was implemented

### Step 2: Analyze for Test Coverage

Before writing the test plan:
1. Extract all testable requirements from `requirements.md` (SHALL/WHEN-THEN statements)
2. Identify user flows and feature areas from the design
3. Note edge cases, error states, and boundary conditions from research
4. Review tasks to understand which components were built and how they connect
5. Group related test cases by feature area or user flow

### Step 3: Create the Test Plan Document

Create the document at `.specs/<spec-name>/test-plan.md` with this structure:

```markdown
# Manual Test Plan: [Feature Name]

## Overview
[What is being tested, scope, and goals of this test plan]

## Prerequisites
- [Environment setup needed]
- [Test data or accounts required]
- [Access or permissions needed]
- [Dependencies that must be running]

## Test Scenarios

- [ ] 1. [Scenario Group Name]
  - [ ] 1.1 [Test Case Name]
    - **Preconditions:** [Required state before testing]
    - **Steps:**
      1. [Action to perform]
      2. [Next action]
      3. [Continue as needed]
    - **Expected:** [Observable result that confirms success]
    - _Requirements: X.X_

  - [ ] 1.2 [Test Case Name]
    - **Preconditions:** [Required state]
    - **Steps:**
      1. [Action]
    - **Expected:** [Result]
    - _Requirements: X.X_

- [ ] 2. [Another Scenario Group]
  - [ ] 2.1 [Test Case]
    - **Preconditions:** [State]
    - **Steps:**
      1. [Action]
    - **Expected:** [Result]
    - _Requirements: X.X_

## Summary
- Total: N tests
- Passed: 0
- Failed: 0
- Skipped: 0
```

### Test Plan Guidelines

1. **Trace every requirement** - Each testable requirement from `requirements.md` must be covered by at least one test case via `_Requirements: X.X_`
2. **Group by feature area** - Organize scenario groups by user flow or feature area, not by requirement number
3. **Include edge cases** - Add test cases for error states, boundary conditions, empty states, and invalid inputs
4. **Be specific in steps** - Each step should be a concrete action the tester can perform without ambiguity
5. **Be specific in expected results** - Describe exactly what the tester should observe, not vague outcomes
6. **Include preconditions** - State any setup needed before running the test case
7. **Order logically** - Start with happy paths, then edge cases, then error scenarios within each group

### Checkbox States

- `[ ]` - Pending (not tested)
- `[-]` - In progress (currently being tested)
- `[x]` - Passed
- `[!]` - Failed

### Step 4: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. A summary of the test plan structure
3. Total number of test scenarios and test cases
4. Coverage: which requirements are covered
5. Use the `AskUserQuestion` tool to ask if they want to make changes or start testing, with options like "Looks good, start testing", "I want to make changes", "Review test plan first"

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
