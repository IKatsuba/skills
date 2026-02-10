---
name: git:commit
description: Smart Commit - creates a conventional commit with auto-detected or user-selected type
---

# Smart Commit

Creates a conventional commit. Fast, no extras.

## Arguments

- `<args>` - Optional. Commit type (`fix`), type+scope (`feat(auth)`), or full message (`"docs: update readme"`)
- If a full message is provided in quotes, skip analysis and use it directly

## Instructions

### Step 1: Check staged changes

Run `git diff --cached --stat`.

- If nothing is staged, run `git add -A` and re-check.
- If still nothing, tell the user and stop.

### Step 2: Analyze the diff

Run `git diff --cached` (read only the first 200 lines if the diff is large).

From the diff, determine:
- **Type**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `style`, `revert`
- **Scope**: main directory or module affected (omit if widespread)
- **Description**: imperative mood, lowercase, no period, max 72 chars

If the user provided a type or scope in args, use those instead of detecting.

If the type is ambiguous, ask the user to pick using `AskUserQuestion`.

### Step 3: Present the message

Show the proposed commit message and ask for approval using `AskUserQuestion`:

```
feat(auth): add password reset flow
```

Options: "Commit", "Edit message"

If the user wants to edit, let them provide a new message and commit with that.

### Step 4: Commit

Run `git commit -m "<message>"`. Done.

## Constraints

- Do NOT run tests, lint, type-check, or any validation commands.
- Do NOT explore the codebase beyond the diff.
- Do NOT run `git status`, `git log`, or any extra git commands.
- Do NOT add `Co-Authored-By`, `Signed-off-by`, or any trailers.
- Total tool calls: aim for 3-4 (diff stat, diff, ask, commit).
