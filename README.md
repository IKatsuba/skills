# Skills

A collection of skills for Claude Code to streamline specification-driven development workflow.

## Installation

```bash
npx add-skill ikatsuba/skills
```

### Install specific skills

```bash
npx add-skill ikatsuba/skills --skill spec:requirements
npx add-skill ikatsuba/skills --skill spec:design
npx add-skill ikatsuba/skills --skill spec:tasks
```

### Global installation

```bash
npx add-skill ikatsuba/skills -g
```

### List available skills

```bash
npx add-skill ikatsuba/skills --list
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `spec:requirements` | Create Requirements Document - generates a structured requirements document based on the task context |
| `spec:design` | Create Design Document - generates a technical design document based on the requirements |
| `spec:tasks` | Create Tasks Document - generates an implementation plan with tracked tasks |

## Workflow

These skills support a specification-driven development workflow:

1. **`/spec:requirements <name>`** - Create requirements document in `.specs/<name>/requirements.md`
2. **`/spec:design <name>`** - Create design document in `.specs/<name>/design.md`
3. **`/spec:tasks <name>`** - Create tasks document in `.specs/<name>/tasks.md`

## Documents Structure

```
.specs/
└── <spec-name>/
    ├── requirements.md   # User stories and acceptance criteria
    ├── design.md         # Architecture, components, interfaces
    └── tasks.md          # Implementation plan with checkboxes
```

## License

MIT
