---
name: dev:create-skill
description: Create New Skill - scaffolds a skill definition following Claude Code conventions and this repository's patterns. Use when adding a new skill.
argument-hint: <category/skill-name>
disable-model-invocation: true
---

# Create New Skill

Scaffolds a new skill definition following Claude Code's [Agent Skills](https://agentskills.io) standard and this repository's conventions.

## When to use

Use this skill when the user needs to:
- Add a new skill to this repository
- Create a Claude Code skill following best practices

## Instructions

### Step 1: Gather Information

Use the `AskUserQuestion` tool to gather:

1. **Category** — which folder?
   - `spec/` — Specification pipeline skills
   - `git/` — Git workflow skills
   - `review/` — Code review skills
   - `project/` — Project orchestration skills
   - `dev/` — Development and meta skills
   - Or a new category if none fit

2. **Skill name** — kebab-case (e.g., `validate`, `format-log`)

3. **Purpose** — what does it do, what problem does it solve?

4. **Invocation model** — who triggers it?
   - Both user and Claude (default)
   - User only (`disable-model-invocation: true`) — for actions with side effects
   - Claude only (`user-invocable: false`) — for background knowledge

5. **Arguments** — what does the user pass? (optional)

### Step 2: Analyze Existing Skills

Read 2-3 existing skills from the target category to understand:
- Writing style and level of detail
- Category-specific patterns (e.g., spec skills have `## Role`, gating, frontmatter injection)

### Step 3: Create the Skill Directory

Create `<category>/<skill-name>/SKILL.md`. A skill is a directory with `SKILL.md` as the entrypoint:

```
my-skill/
├── SKILL.md           # Main instructions (required, keep under 500 lines)
├── reference.md       # Detailed reference (optional, loaded when needed)
└── examples/          # Supporting files (optional)
```

### Step 4: Write SKILL.md

Use this template, filling in all applicable fields:

````markdown
---
name: <category>:<skill-name>
description: <Title> - <what it does>. Use when <trigger condition>.
role: <Role Title>
argument-hint: <required-arg> [optional-arg]
---

# <Title>

## Role

You are a **<Role Title>**. Your job is to <primary responsibility>.

- <Focus area 1>
- <Focus area 2>
- <Anti-pattern: what NOT to do>

<1-2 sentence description.>

## When to use

Use this skill when the user needs to:
- <Use case 1>
- <Use case 2>

## Instructions

### Step 1: <Action Name>

<Clear, imperative instructions.>

### Step N: Confirm with User

<Present results, use `AskUserQuestion` with options.>

## Arguments

Parse `$ARGUMENTS` to determine behavior:
- `$0` — first argument (e.g., spec name)
- `$1` — second argument (e.g., mode)

If `$ARGUMENTS` is empty, use `AskUserQuestion` to ask.

Examples:
- `<skill-name> <example>` — <what happens>
````

### Step 5: Apply Frontmatter

Choose the right frontmatter fields based on the skill's behavior:

| Field | When to use |
|-------|-------------|
| `name` | Always. Format: `category:skill-name` |
| `description` | Always. Include "Use when..." trigger for auto-discovery |
| `role` | For skills with a specialist persona (most spec/ skills) |
| `argument-hint` | When the skill accepts arguments |
| `disable-model-invocation` | For actions with side effects (deploy, commit, approve, implement) |
| `user-invocable` | Set `false` for background knowledge Claude shouldn't expose as a command |
| `context` | Set `fork` for read-only skills that don't need conversation history |
| `agent` | With `context: fork` — choose agent type (`Explore`, `Plan`, `general-purpose`) |
| `allowed-tools` | To restrict which tools Claude can use |
| `model` | To override the model for this skill |
| `effort` | To override effort level (`low`, `medium`, `high`, `max`) |

### Step 6: Apply Category Conventions

**For `spec/` skills**, also add:
- `## Role` section with anti-pattern prevention
- `### Step 0: Check Prerequisites` that gate by **file existence** — required prereq missing → block and offer to run its generating skill; recommended prereq missing → warn. No approval status.
- Frontmatter injection instruction (if the skill generates a document) — lightweight `created` / `updated` only, no `status` field
- A `Confirm and Chain` final step that offers to proceed straight into the next phase (revise / proceed / stop)

**For `git/` skills**: follow Conventional Commits patterns.

**For `review/` skills**: include severity levels and structured report format.

### Step 7: Write Supporting Files (if needed)

If `SKILL.md` exceeds ~300 lines, extract detailed sections into supporting files:

```markdown
## Additional resources

- For detailed execution strategy, see [strategy.md](strategy.md)
- For examples, see [examples.md](examples.md)
```

Claude loads supporting files on demand, keeping the main skill focused.

### Step 8: Update Documentation

1. Add the new skill to the repository structure in `CLAUDE.md`
2. Add to the Available Skills table in `README.md`
3. Update the category `README.md` if it exists

### Step 9: Validate Frontmatter

Before confirming, validate the new SKILL.md to catch malformed YAML, mismatched names, or `argument-hint` shapes that silently break `npx skills` and other tooling.

If this repository has `.github/scripts/validate-skills.py`, run it:

```bash
python3 .github/scripts/validate-skills.py
```

If the script isn't present (the skill is being created in a different repo), run this inline check against the new SKILL.md:

```bash
python3 - <<'PY'
import re, sys, pathlib
try:
    import yaml
except ImportError:
    sys.exit("PyYAML not available; skipping inline check. Install with: pip install pyyaml")

path = pathlib.Path("<category>/<skill-name>/SKILL.md")  # replace with actual path
text = path.read_text()
m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
assert m, "no frontmatter block"
data = yaml.safe_load(m.group(1))
assert isinstance(data, dict), "frontmatter must be a mapping"

parts = path.parts
expected = f"{parts[-3]}:{parts[-2]}"
assert data.get("name") == expected, f"name {data.get('name')!r} must equal {expected!r}"
assert data.get("description"), "description missing or empty"

hint = data.get("argument-hint")
assert hint is None or isinstance(hint, (str, list)), \
    f"argument-hint must be string or list, got {type(hint).__name__}"

print("OK")
PY
```

If validation fails, fix the SKILL.md and re-run. The most common failure is `argument-hint: [a] [b]` — YAML parses this as a one-element list with junk after, breaking tooling. Quote it: `argument-hint: "[a] [b]"`.

### Step 10: Confirm

Present to the user:
1. The path of the created files
2. A summary of the skill's purpose
3. Documentation updates made
4. Validation result
5. Use `AskUserQuestion` to ask if changes are needed

## Skill Anatomy Reference

### Required Sections

| Section | Purpose |
|---------|---------|
| Frontmatter | `name`, `description`, and configuration fields |
| Title (H1) | Matches the description title |
| When to use | Bullet points of trigger conditions |
| Instructions | Numbered steps with imperative verbs |

### Recommended Sections

| Section | Purpose |
|---------|---------|
| Role | Specialist persona with anti-patterns (required for `spec/` skills) |
| Arguments | How `$ARGUMENTS` / `$0` / `$1` are parsed |
| Error Handling | What to do when things go wrong |

### Built-in Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed by the user |
| `$0`, `$1`, `$2` | Individual arguments by position |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing this SKILL.md |

### Naming Conventions

- **Category names**: lowercase, single word (`spec`, `git`, `dev`)
- **Skill names**: kebab-case (`format-log`, `create-skill`)
- **Full name**: `category:skill-name` (`git:commit`, `spec:requirements`)
