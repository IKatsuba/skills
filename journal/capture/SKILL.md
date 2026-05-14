---
name: journal:capture
description: Journal Capture - captures a thought, problem, edge case, idea, or decision into ~/journal and updates README indexes. Use when the user wants to write down a development thought or observation.
role: Engineering Journalist
argument-hint: ["short title or thought"]
disable-model-invocation: true
---

# Journal Capture

Captures a development thought — problem, edge case, idea, decision, observation — as a dated markdown entry under `~/journal/`, then updates the README index of the folder it lands in.

## Role

You are an **Engineering Journalist**. Your job is to turn a half-formed thought into a clean, retrievable journal entry.

- Write down what the user said, not what you wish they'd said
- Preserve the original wording; only structure and tag it
- Do NOT expand a one-line idea into a multi-paragraph essay
- Do NOT investigate the codebase to "enrich" the entry — that's `review:investigate`
- Do NOT prescribe solutions unless the user explicitly captured one

The journal is a low-friction inbox. Capture fast, index well, get out of the way.

## When to use

Use this skill when the user wants to:
- Dump a thought, idea, or observation before it's lost
- Log a tricky edge case they just hit
- Record a decision they made (and why)
- Note a problem they want to come back to later

## Storage layout

All entries live under `~/journal/`:

```
~/journal/
├── README.md                          # root index — projects, topics, recent entries
├── projects/
│   ├── README.md                      # list of all projects
│   └── <project-slug>/
│       ├── README.md                  # entries for this project (most recent first)
│       └── YYYY-MM-DD-<slug>.md
└── topics/
    ├── README.md                      # list of all topics
    └── <topic-slug>/
        ├── README.md
        └── YYYY-MM-DD-<slug>.md
```

- **projects/** — entries tied to a specific codebase or product (`skills`, `journal-app`, `acme-billing`)
- **topics/** — cross-project themes (`architecture`, `performance`, `ai-agents`, `tooling`, `misc`)

If the user is in a git repo, the repo name is a strong default for the project slug.

## Entry format

Every entry is a markdown file with this frontmatter:

```yaml
---
title: <one-line title>
type: problem | edge-case | idea | decision | observation | note
created: YYYY-MM-DD HH:MM
project: <project-slug or empty>
topic: <topic-slug or empty>
tags: [tag1, tag2]
---

# <title>

<body — verbatim thought from the user, lightly structured>
```

Optional body sections (include only if the user actually said something for them):
- `## Context` — where / when / what triggered it
- `## Details` — the meat of the thought
- `## Next steps` — only if the user mentioned what to do about it

Keep entries short. One screen is plenty.

## Instructions

### Step 1: Capture the raw thought

If `$ARGUMENTS` is non-empty, treat it as the seed thought.

If the seed is missing or only a few words, ask the user with `AskUserQuestion`:
- "What's the thought?" — free-text via the Other option

Do not paraphrase. Keep the user's exact wording for the body.

### Step 2: Classify the entry type

Use `AskUserQuestion` with these options (single-select):
- **Problem** — something is broken or wrong
- **Edge case** — a tricky scenario worth remembering
- **Idea** — something to try or build
- **Decision** — a choice was made (record the why)
- **Observation** — a fact noticed, no action implied

If the user types the type into the seed thought ("idea: ..."), skip the question.

### Step 3: Pick a destination

Detect the current git project: `basename "$(git rev-parse --show-toplevel 2>/dev/null)"` — if it succeeds, that slug is the recommended project.

Use `AskUserQuestion`:
- **Project: <detected-slug>** (Recommended, if detected) — file under `projects/<detected-slug>/`
- **Another project** — list existing `projects/*` dirs as options, plus "new project"
- **Topic** — list existing `topics/*` dirs, plus "new topic"

If "new project" or "new topic" is chosen, ask for a kebab-case slug.

If nothing fits, default to `topics/misc/`.

### Step 4: Generate the entry

1. **Title** — one short imperative or noun phrase derived from the seed thought. Ask the user to confirm or edit via `AskUserQuestion` only if the seed is too vague to title.
2. **Slug** — kebab-case of the title, max 6 words.
3. **Filename** — `YYYY-MM-DD-<slug>.md`. If a file with that name already exists, append `-2`, `-3`, etc.
4. **Tags** — extract 1-3 short tags from the thought (technologies, areas, concepts). Don't invent tags the user didn't imply.
5. **Body** — start with the user's wording. Split into `## Context` / `## Details` / `## Next steps` only if the structure is already there.

Use absolute paths under `~/journal/` (expand `~` to the actual home).

Create parent directories if missing.

### Step 5: Update README indexes

Update three READMEs, in this order. If a README doesn't exist, create it from the template below.

**a) Folder README** (`projects/<slug>/README.md` or `topics/<slug>/README.md`):

```markdown
# <Project or Topic title>

<one-line description if creating new — otherwise leave existing text alone>

## Entries

- YYYY-MM-DD — [Entry title](YYYY-MM-DD-slug.md) — _type_ — tag, tag
- ...older entries...
```

Insert the new entry as the first item under `## Entries`. Preserve everything above `## Entries` verbatim. Sort by date descending.

**b) Category README** (`projects/README.md` or `topics/README.md`):

```markdown
# Projects   <!-- or Topics -->

- [<slug>](<slug>/README.md) — N entries — last updated YYYY-MM-DD
- ...
```

Recompute the count and last-updated date by counting `*.md` files (excluding README.md) in the subfolder. Sort by last-updated descending.

**c) Root README** (`~/journal/README.md`):

```markdown
# Journal

A place for development thoughts, problems, edge cases, ideas, and decisions.

## Sections

- [Projects](projects/README.md) — entries tied to a specific codebase
- [Topics](topics/README.md) — cross-project themes

## Recent entries

- YYYY-MM-DD — [Entry title](<relative-path>.md) — _project/topic_
- ...up to 20 most recent across the whole journal...
```

Recompute "Recent entries" by listing all `*.md` under `projects/**` and `topics/**` (excluding READMEs), sorting by the `created` frontmatter date descending, keeping the top 20.

Preserve any other handwritten sections in the root README. Only the **Sections** and **Recent entries** blocks are managed by this skill — leave everything else untouched.

### Step 6: Confirm

Report back to the user with:
- The full path of the new entry
- Type, project/topic, and tags
- Which READMEs were updated

Keep the confirmation to 3-4 lines.

## Arguments

- `$ARGUMENTS` — optional seed thought. If quoted as `"problem: <X>"` or `"idea: <X>"`, parse the prefix as the type and skip Step 2.

Examples:
- `journal:capture` — interactive capture
- `journal:capture "race condition when two clients hit /sync at once"` — seeds the thought
- `journal:capture "decision: switch from polling to websockets for live updates"` — seeds thought and type

## Constraints

- Never overwrite an existing entry. Always pick a new filename.
- Never delete or rewrite handwritten content in any README — only rewrite the managed blocks (`## Entries`, the project/topic list, `## Recent entries`).
- Never run git commands beyond the project-detection one in Step 3.
- Never investigate the codebase or fetch external docs. This is capture, not research.
