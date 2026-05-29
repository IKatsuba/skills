# Design Deviation Protocol

During implementation, a subagent or the implementer may discover that the design is incorrect, incomplete, or impractical. Follow this protocol instead of silently diverging.

## Detection

A design deviation exists when:
- A file path, API, or interface in the design does not match the actual codebase
- The designed approach is technically impossible or produces errors
- A requirement cannot be met with the designed solution
- A subtask requires changes not described in the design

## Severity Levels

| Severity | Definition | Action |
|----------|-----------|--------|
| **Minor** | Detail differs but outcome is identical (e.g., file name) | Log deviation in tasks.md under the subtask, continue |
| **Moderate** | Approach changes but requirements are still met | Pause. Use `AskUserQuestion`: "Approve deviation and continue" / "Update design first" / "Cancel task" |
| **Major** | Requirements may not be met or architecture changes significantly | STOP. Append a `## Deviations` note to `design.md` describing what the design says vs. reality. Use `AskUserQuestion`: "Re-run spec:design" / "Run review:investigate" / "Handle manually" |

## Logging Deviations

For minor and approved moderate deviations, add a note to `tasks.md`:
```
- [x] 2.1 Create user model
  - _Deviation: Used `src/models/user.model.ts` instead of `src/models/user.ts` per project naming convention_
```

For major deviations, append a `## Deviations` section to `design.md` recording what the design specified, what reality required, and the date. Bump the `updated` date in frontmatter. Do NOT continue implementation on the affected area until the design is corrected (re-run `spec:design`) and the user confirms.

```markdown
## Deviations

- 2026-05-29 — Design specified a synchronous `UserService.create()`, but the ORM only exposes an async API. Switched to async; design needs to reflect this before further work on the user module.
```
