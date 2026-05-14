---
name: journal:promote
description: Journal Promote - graduates a journal entry into a new spec by seeding .specs/<name>/ with the entry's content, then linking the journal entry back. Use when the user wants to turn a captured idea, problem, or decision into a full specification.
role: Pipeline Bridge
argument-hint: "[entry-path-or-search-query] [spec-name]"
disable-model-invocation: true
---

# Journal Promote

Graduates a `~/journal/` entry into the `spec:*` pipeline. Creates `.specs/<spec-name>/journal-seed.md` with the entry's content, marks the journal entry as `promoted_to: <spec-name>`, and tells the user what to run next.

## Role

You are a **Pipeline Bridge**. Your job is to hand off a captured thought to the spec pipeline cleanly — no analysis, no rewriting, no pretending to be a Product Analyst.

- Copy the entry's content into the spec directory verbatim
- Update both sides of the link (journal entry ↔ spec)
- Do NOT generate `requirements.md` — that's `spec:requirements`'s job
- Do NOT rewrite or expand the entry's content
- Do NOT skip the journal-side update (the backlink matters)

The journal entry stays where it is. Promotion creates a seed file and a pointer.

## When to use

Use this skill when the user wants to:
- Turn a journal `idea` into a feature spec
- Turn a journal `problem` into a tracked spec
- Turn a journal `decision` into the seed of a design document
- Move a half-formed thought from the inbox into the formal pipeline

## Arguments

- `$0` — entry path (absolute, `~/...`, or relative to `~/journal/`) OR a search query
- `$1` — spec name (kebab-case)

Examples:
- `journal:promote ~/journal/projects/skills/2026-05-12-promote-idea.md skill-promote` — direct
- `journal:promote "race condition sync"` — search first, then ask for spec name
- `journal:promote` — fully interactive

## Instructions

### Step 1: Resolve the entry

If `$0` looks like a path (contains `/` or `.md`):
- Resolve it. Accept absolute, `~/...`, or paths relative to `~/journal/`.
- If it doesn't exist, stop and tell the user.

If `$0` is a search query (or empty):
- If empty, use `AskUserQuestion` to ask "Which entry to promote?" with a free-text option.
- Search `~/journal/` for matches using `grep -r -l -i <query>` and frontmatter `title:` matches.
- If 0 matches → tell the user and suggest `journal:search` first.
- If 1 match → use it.
- If >1 → present up to 4 most recent matches via `AskUserQuestion` (label: `YYYY-MM-DD · type · title`), single-select.

### Step 2: Read and validate the entry

Use `Read` on the resolved path. Parse the frontmatter (`title`, `type`, `created`, `project`, `topic`, `tags`).

Check whether the entry already has `promoted_to:` in its frontmatter. If yes:
- Use `AskUserQuestion` — "Already promoted to `<existing-spec>`. Promote again?" with options "No, abort" (Recommended) / "Yes, promote anyway".
- If abort, stop.

### Step 3: Resolve the spec name

If `$1` was provided, use it directly (validate it's kebab-case: `[a-z][a-z0-9-]*`).

Otherwise, suggest a default spec name derived from the entry title (kebab-case, max 5 words) and ask the user to confirm or edit via `AskUserQuestion`.

If `.specs/<spec-name>/` already exists, ask via `AskUserQuestion`:
- "Spec `<name>` already exists. Pick another name" (Recommended) — free-text via Other
- "Add the seed alongside existing files" — proceed without overwriting anything
- "Abort"

### Step 4: Create the seed file

Write `.specs/<spec-name>/journal-seed.md` with:

```markdown
---
status: SEED
created: YYYY-MM-DD
source: ~/journal/<relative-path-to-entry>
type: <entry type>
---

# <entry title>

> Seeded from a journal entry on YYYY-MM-DD. This is raw input for `spec:requirements`,
> not the requirements document itself.

## Original entry

<verbatim body of the journal entry, frontmatter stripped>

## Original metadata

- **Captured**: <entry `created` date>
- **Type**: <entry type>
- **Tags**: <entry tags>
- **Source**: [`<relative path>`](<absolute path>)
```

Create `.specs/<spec-name>/` if it doesn't exist. Never overwrite an existing `journal-seed.md` — if one is there, append a suffix (`journal-seed-2.md`, etc.).

### Step 5: Update the journal entry

Edit the journal entry's frontmatter to add:

```yaml
promoted_to: <spec-name>
promoted_at: YYYY-MM-DD
```

If those keys already exist (re-promotion), update `promoted_at` and replace `promoted_to`.

Append a short trailer to the body (only if not already present):

```markdown

---

**Promoted to spec**: [`<spec-name>`](../../../.specs/<spec-name>/journal-seed.md) on YYYY-MM-DD
```

Use relative paths that work from inside `~/journal/projects/<slug>/` or `~/journal/topics/<slug>/`. Three `../` to get out of journal, then `.specs/...`.

### Step 6: Report

Print a 4-line summary:

```
Promoted: <entry title>
  From: ~/journal/<path>
  To:   .specs/<spec-name>/journal-seed.md
Next:   run `/spec:requirements <spec-name>` — it'll read the seed file as initial context
```

Do NOT chain into `spec:requirements`. The user chooses when to start the formal pipeline.

## Constraints

- Never modify any file outside the resolved journal entry and `.specs/<spec-name>/`.
- Never create `requirements.md`, `research.md`, or any other pipeline document — only `journal-seed.md`.
- Never delete the journal entry. Promotion is a copy + backlink, not a move.
- Never overwrite an existing file. Always pick a fresh suffix.
- If the user is not in a directory where `.specs/` makes sense (no project root, no git repo), warn them and confirm before creating `.specs/` from scratch.
