---
name: spec:research
description: Research & Brainstorm - explores ideas and alternatives before creating requirements
---

# Research & Brainstorm

Helps explore and refine a raw idea before formalizing it into requirements. This is the first step in the specification pipeline — brainstorming approaches, analyzing tradeoffs, and building shared understanding.

## When to use

Use this skill when the user needs to:
- Explore a raw idea before writing requirements
- Compare different approaches to solving a problem
- Understand codebase constraints that affect a feature
- Brainstorm alternatives and evaluate tradeoffs
- Build clarity on scope and direction

## Instructions

### Step 1: Understand the Raw Idea

Ask the user to describe their idea in their own words:
1. What problem are you trying to solve?
2. Who is this for? (users, developers, both?)
3. What does success look like?
4. Any initial thoughts on how it might work?

Keep it conversational — the goal is to extract the core intent, not formal requirements yet.

### Step 2: Explore the Codebase

Use the `Task` tool with `subagent_type=Explore` to understand relevant context:

1. **Patterns agent** — find similar features or patterns in the codebase that could inform the approach
2. **Constraints agent** — identify technical constraints, dependencies, and architectural boundaries

Launch both agents in parallel. Look for:
- Existing code that does something similar
- Architectural patterns to follow or avoid
- Integration points that will be affected
- Technical debt or limitations to consider

### Step 3: Generate Alternatives

Based on the idea and codebase analysis, propose 2-4 different approaches:

```markdown
## Approach A: [Name]

**How it works:** [Brief description]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Effort:** [Low / Medium / High]

**Risk:** [Low / Medium / High]
```

For each approach, consider:
- Implementation complexity
- Impact on existing code
- User experience implications
- Maintenance burden
- Scalability and performance

### Step 4: Research Best Practices (if needed)

If the idea involves unfamiliar technology or patterns:

1. Use `resolve-library-id` and `query-docs` to fetch documentation for relevant libraries
2. Use `WebSearch` to find best practices and common pitfalls
3. Share relevant findings with the user

### Step 5: Discuss and Refine

Engage in a dialogue with the user:
- Ask clarifying questions about priorities
- Challenge assumptions (respectfully)
- Highlight tradeoffs they might not have considered
- Help narrow down to 1-2 promising approaches

### Step 6: Summarize Direction

Once alignment is reached, create a summary document at `.specs/<spec-name>/research.md`:

```markdown
# Research: [Feature Name]

## Problem Statement

[What problem are we solving and why it matters]

## Explored Approaches

### Approach A: [Name] (Selected / Rejected)
[Brief summary and why it was selected or rejected]

### Approach B: [Name] (Selected / Rejected)
[Brief summary and why it was selected or rejected]

## Chosen Direction

[Description of the chosen approach]

### Key Decisions

1. [Decision 1] — [Rationale]
2. [Decision 2] — [Rationale]
3. [Decision 3] — [Rationale]

### Open Questions

- [ ] [Question that needs to be resolved during requirements/design]
- [ ] [Another open question]

## Codebase Insights

- [Relevant pattern or constraint discovered]
- [Another insight]

## Next Steps

Ready for `spec:requirements <spec-name>` to formalize these ideas into requirements.
```

### Step 7: Confirm with User

Present the summary and ask:
1. Does this capture our discussion accurately?
2. Any changes before we move to requirements?
3. Would you like to proceed with `spec:requirements` now?

## Arguments

- `<args>` - Optional spec name and/or idea description
  - `user-auth` - Just the spec name (will ask about the idea)
  - `user-auth add social login` - Spec name and brief idea
  - `add social login to the app` - Just the idea (will ask for spec name)

Examples:
- `spec:research` - Start from scratch, will ask questions
- `spec:research notifications` - Research ideas for a notifications feature
- `spec:research api-v2 redesign the REST API` - Research with context provided

## Tips for Effective Brainstorming

1. **No bad ideas early on** — explore freely before narrowing down
2. **Visualize when helpful** — sketch diagrams or flowcharts
3. **Question assumptions** — "Why does it need to work this way?"
4. **Consider the user** — how will this feel to use?
5. **Think about edges** — what happens in error cases, empty states?
6. **Keep scope in check** — is this one feature or three?
