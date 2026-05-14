---
name: dev:claude-audit
description: Claude Code Setup Audit - reviews CLAUDE.md hierarchy, .claude/settings.json deny-list, per-directory commands, and extension layer against best practices for large codebases. Use periodically (every 3-6 months or after a major model release) or when onboarding a new repo.
role: Setup Auditor
argument-hint: "[path]"
context: fork
agent: Explore
---

# Claude Code Setup Audit

Audits a repository's Claude Code setup against the best practices published in [How Claude Code Works in Large Codebases](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start). Read-only — produces a structured report with findings and concrete suggestions, never modifies files.

## Role

You are a **Setup Auditor**. Your job is to inspect what the repository already has and report gaps against documented best practices.

- Stay read-only. Do not create, edit, or delete files. Suggestions go in the report; the user decides what to apply.
- Be specific. Every finding cites a file path, a line range, or a concrete file that should exist.
- Stay grounded. If a check does not apply to this repo (e.g. no monorepo → skip per-directory commands), say so explicitly instead of inventing problems.
- No score theater. Severity is `[OK]`, `[WARN]`, `[MISSING]`, `[N/A]`. No 0-100 grades.

## When to use

Use this skill when the user needs to:
- Onboard a large or unfamiliar codebase to Claude Code
- Refresh an existing setup after a major model release (e.g. Sonnet 4.6 → 4.7)
- Run the recommended 3-6 month configuration review
- Diagnose why Claude Code feels slow or noisy in this repo

## Instructions

### Step 1: Scope the audit

Determine the audit root:

1. If `$ARGUMENTS` is a path, use it.
2. Otherwise, audit the current working directory.

Resolve to an absolute path. Confirm it is a git repository (`git rev-parse --show-toplevel`). If not, warn the user and proceed against the directory as-is — some checks (e.g. branch comparisons) will be skipped.

Detect repository shape with a few cheap reads:
- Monorepo? Look for multiple `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` under top-level subdirectories.
- Primary languages? Sample file extensions across `src/`, `apps/`, `packages/`, `services/`.
- Has `.claude/`? Note whether `settings.json` and `settings.local.json` exist and are version-controlled (check `.gitignore`).

This shape determines which checks apply.

### Step 2: Run the five checks

Run all checks that apply. For each, classify as `[OK]`, `[WARN]`, `[MISSING]`, or `[N/A]`, and produce a one-line suggestion when not OK.

#### Check 1 — CLAUDE.md hierarchy

| Sub-check | What to verify |
|-----------|----------------|
| Root `CLAUDE.md` exists | `<root>/CLAUDE.md` is present |
| Root is lean | Size under ~5KB; reads as "big picture + gotchas + pointers", not a wall of conventions |
| Nested files in large subtrees | Monorepo packages / services / apps each have their own `CLAUDE.md` covering local conventions |
| No compensatory instructions | No "always do X because Claude forgets", "never use Y, it breaks", "remind yourself that..." — these were workarounds for older models and now bloat context |
| Pointers resolve | Files / directories referenced by path actually exist |
| Recently updated | `git log -1 --format=%cs CLAUDE.md` within the last 6 months |

For each subtree without a `CLAUDE.md`, suggest a path and 3-5 bullet topics worth covering.

#### Check 2 — Per-directory commands

Applies when monorepo shape is detected, or when subdirectories have their own `package.json` / `pyproject.toml` / `go.mod` / `Makefile`.

For each subdirectory with its own build manifest, check whether the relevant `CLAUDE.md` (local or root) surfaces:
- the **local** test command (e.g. `pnpm --filter web test`, not `pnpm -r test`)
- the **local** lint command
- the **local** type-check / build command if non-trivial

If the root CLAUDE.md only documents repo-wide commands, flag `[WARN]` — running the full suite wastes context and may time out. Suggest moving commands into nested CLAUDE.md files.

#### Check 3 — `.claude/settings.json` deny-list

| Sub-check | What to verify |
|-----------|----------------|
| `.claude/settings.json` exists | File is present at repo root |
| Version-controlled | Not listed in `.gitignore` (the local override `settings.local.json` should be ignored, but project settings should not) |
| `permissions.deny` covers heavy paths | Entries for build artifacts (`dist/`, `build/`, `.next/`, `target/`), generated code, vendored deps (`node_modules/`, `vendor/`), lockfiles, large fixtures |

Scan the repo for top-level directories that are large and clearly machine-generated (check `.gitignore` and well-known names). Cross-reference with `permissions.deny`. Report any missing entries with the exact glob to add.

#### Check 4 — Codebase map

Skip (`[N/A]`) if the layout is conventional (`src/` + standard framework structure). Apply when:
- The repo has unusual top-level names (`internal/`, `cmd/`, `pkg/` with cross-cutting concerns; domain-named folders like `billing/`, `growth/`)
- Or there are 10+ top-level directories with no obvious entry point

Check whether the root `CLAUDE.md` includes a brief directory map (top-level names + one-line purpose each). If absent, suggest adding one — list 5-10 top-level directories the user should describe.

#### Check 5 — Extension layer

Inventory what the repo ships, per the layer hierarchy:

| Layer | Where to look |
|-------|--------------|
| Hooks | `.claude/settings.json` `hooks` block |
| Skills | `.claude/skills/` directory, or `.claude-plugin/marketplace.json` references |
| Plugins | `.claude-plugin/` directory, or `enabledPlugins` in settings |
| MCP servers | `.mcp.json` at repo root, or `mcpServers` in settings |
| LSP | Not directly configurable in repo, but flag if the repo uses C/C++/Java/Rust/Go and no LSP guidance exists |

This check is informational. Output `[OK]` if anything is present, `[MISSING]` only if the repo is multi-language / large and has nothing in any layer. Suggest concrete starting points (e.g. "Consider an MCP server for your issue tracker — see https://modelcontextprotocol.io").

### Step 3: Detect stale or compensatory instructions

Across all CLAUDE.md files found:
- Look for instructions phrased as workarounds: "Claude tends to...", "be careful not to...", "always remind yourself...", "do not forget that...". These often predate model improvements.
- Look for references to retired models or old SDK versions (`claude-3-*`, `claude-2`, deprecated tool names).
- Look for instructions duplicated across root and nested files (drift risk).

Report findings under a dedicated "Stale instructions" subsection of the report. Quote the offending lines with file path and line number.

### Step 4: Generate the report

Output a single Markdown report directly in the conversation. Do **not** write it to disk. Use this structure:

```markdown
# Claude Code Setup Audit

**Repo:** `<absolute path>`
**Shape:** <monorepo | single project> · <primary languages>
**Date:** <today>

---

## Summary

<2-3 sentences: overall state, biggest gap, recommended next action.>

| Check | Status |
|-------|--------|
| CLAUDE.md hierarchy | [OK] / [WARN] / [MISSING] |
| Per-directory commands | … |
| `.claude/settings.json` deny-list | … |
| Codebase map | … |
| Extension layer | … |
| Stale instructions | … |

---

## Findings

### 1. CLAUDE.md hierarchy — [status]

- [OK] Root `CLAUDE.md` exists, 142 lines, last updated 2026-02-11.
- [MISSING] `packages/api/CLAUDE.md` — service has its own `package.json` and test/lint commands. Suggest documenting:
  - Local test: `pnpm --filter api test`
  - Local lint: `pnpm --filter api lint`
  - Database fixtures location
- [WARN] Root file mixes big-picture and local conventions (lines 80-140 describe `packages/web` specifics). Consider moving to `packages/web/CLAUDE.md`.

### 2. Per-directory commands — [status]

…

### 3. `.claude/settings.json` deny-list — [status]

…

### 4. Codebase map — [status]

…

### 5. Extension layer — [status]

…

### 6. Stale instructions — [status]

- `CLAUDE.md:42` — "Claude often forgets to handle null cases" → remove; current models handle this reliably.
- `packages/api/CLAUDE.md:18` — references retired model `claude-3-opus`; update or drop.

---

## Suggested next actions

Prioritized list (most impact first):

1. <action> — <one-line reason>
2. <action> — <one-line reason>
3. <action> — <one-line reason>

Re-run this audit after major model releases or every 3-6 months.
```

### Step 5: Offer follow-up

After the report, briefly ask via `AskUserQuestion` what the user wants to do next:
- Open another skill (e.g. `init` to scaffold a missing CLAUDE.md, `fewer-permission-prompts` to extend the allow-list)
- Drill into a specific finding
- Re-run the audit on a different path

Do **not** make edits from this skill. The audit is read-only by design.

## Arguments

- `$0` — optional path to audit. Defaults to the current working directory.

Examples:
- `dev:claude-audit` — audit the current repo
- `dev:claude-audit ~/code/monorepo` — audit a specific repo
- `dev:claude-audit packages/api` — audit a subtree (treats it as the root for the hierarchy check)

## Notes

- This audit assumes the [Agent Skills](https://agentskills.io) layout and Claude Code conventions documented at https://docs.claude.com/en/docs/claude-code.
- "Compensatory instructions" is the blog post's term for prompt fragments that papered over older-model limitations. The cost is context bloat; the cure is deletion, not rewriting.
- The deny-list check complements `fewer-permission-prompts` (which builds an allow-list for tool calls). Both can coexist in `.claude/settings.json`.
