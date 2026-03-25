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
| **Major** | Requirements may not be met or architecture changes significantly | STOP. Mark `design.md` frontmatter as `status: SUPERSEDED`. Use `AskUserQuestion`: "Re-run spec:design" / "Run review:investigate" / "Handle manually" |

## Logging Deviations

For minor and approved moderate deviations, add a note to `tasks.md`:
```
- [x] 2.1 Create user model
  - _Deviation: Used `src/models/user.model.ts` instead of `src/models/user.ts` per project naming convention_
```

For major deviations, update `design.md` frontmatter to `status: SUPERSEDED` and `updated: <today>`. Do NOT continue implementation until the design is updated and re-approved.
