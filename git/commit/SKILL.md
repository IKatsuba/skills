---
name: git:commit
description: Smart Commit - stages all changes and creates a conventional commit
---

# Smart Commit

Stages everything and commits. No questions asked.

## Arguments

- `<args>` - Optional. Full message (`"docs: update readme"`) or type hint (`fix`, `feat(auth)`)
- If a full message is provided in quotes, use it directly — skip analysis

## Instructions

1. Run `git add -A`
2. Run `git diff --cached --stat` — if nothing staged, tell the user and stop
3. Run `git diff --cached` (first 200 lines if large)
4. Determine the commit message in Conventional Commits format:
   - **Type**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `style`, `revert`
   - **Scope**: main directory or module affected (omit if widespread)
   - **Description**: imperative mood, lowercase, no period, max 72 chars
   - If args provided a type or scope, use those
5. Run `git commit -m "<message>"`

## Constraints

- Do NOT ask questions — just commit
- Do NOT run tests, lint, type-check, or any validation
- Do NOT explore the codebase beyond the diff
- Do NOT run `git status`, `git log`, or any extra git commands
- Do NOT add `Co-Authored-By`, `Signed-off-by`, or any trailers
- Total tool calls: 3 (`git add`, `git diff --cached`, `git commit`)
