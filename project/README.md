# Project Skills

Project-level orchestration for managing large systems composed of multiple specifications.

## When to use

Use project skills when building a system that spans multiple specs — a SaaS product, a platform with many modules, or any project where you need to coordinate work across multiple feature specifications.

## Skills

| Skill | Description |
|-------|-------------|
| `project:init` | Initialize the project — goals, stakeholders, constraints, shared decisions |
| `project:plan` | Break into specs with dependencies and execution order |
| `project:status` | Dashboard showing progress across all specs |

## Workflow

```
project:init          Define the overall system
       |
project:plan          Break into specs with dependency graph
       |
  spec:requirements   Start planning individual specs
  spec:research       (standard spec pipeline per spec)
  spec:design
  spec:tasks
  spec:implement
  spec:test-plan
  spec:test
       |
project:status        Track progress across all specs
```

## Documents

```
.projects/
└── <project-name>/
    ├── vision.md       # System goals, constraints, shared decisions
    └── plan.md         # Spec list, dependency graph, execution order
```
