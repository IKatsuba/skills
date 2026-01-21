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
npx add-skill ikatsuba/skills --skill spec:do-all
npx add-skill ikatsuba/skills --skill spec:do-next
npx add-skill ikatsuba/skills --skill spec:do-task
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

### Specification Creation

| Skill | Description |
|-------|-------------|
| `spec:requirements` | Create Requirements Document - generates a structured requirements document based on the task context |
| `spec:design` | Create Design Document - generates a technical design document based on the requirements |
| `spec:tasks` | Create Tasks Document - generates an implementation plan with tracked tasks |

### Task Execution

| Skill | Description |
|-------|-------------|
| `spec:do-all` | Execute All Tasks - runs all pending tasks from the tasks document sequentially using subagents |
| `spec:do-next` | Execute Next Task - runs the next pending task from the tasks document |
| `spec:do-task` | Execute Specific Task - runs a task by its number (e.g., `spec:do-task 1.2`) |

## Workflow

These skills support a specification-driven development workflow:

### Phase 1: Specification

1. **`/spec:requirements <name>`** - Create requirements document in `.specs/<name>/requirements.md`
2. **`/spec:design <name>`** - Create design document in `.specs/<name>/design.md`
3. **`/spec:tasks <name>`** - Create tasks document in `.specs/<name>/tasks.md`

### Phase 2: Implementation

4. **`/spec:do-all <name>`** - Execute all tasks automatically
5. **`/spec:do-next <name>`** - Execute tasks one at a time with review
6. **`/spec:do-task <name> <number>`** - Execute a specific task (e.g., `/spec:do-task user-auth 1.2`)

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
