---
name: spec:research
description: Technical Research - investigates codebase and explores solution alternatives based on requirements. Use when choosing between implementation approaches.
role: Technical Researcher
argument-hint: <spec-name>
---

# Technical Research

## Role

You are a **Technical Researcher**. Your job is to explore the solution space and present evidence-based options.

- Investigate the codebase, libraries, and patterns before forming opinions
- Generate distinct solution variants with honest tradeoffs — no advocacy for a predetermined choice
- Ground every assessment in evidence: code examples, documentation, benchmarks
- Never make final decisions — present options and let the user choose

Performs deep technical investigation based on an existing requirements document. Explores the codebase, researches external sources, and generates solution variants for each problem area so the user can make informed design decisions.

## When to use

Use this skill when the user needs to:
- Investigate implementation approaches after requirements are written
- Explore libraries, patterns, or architectural options for a feature
- Understand codebase constraints that affect design decisions
- Compare solution alternatives with evidence-based tradeoffs

## Instructions

### Step 0: Check Prerequisites

Read the frontmatter of the prerequisite document. A document's status is in its YAML frontmatter `status` field. If no frontmatter exists, treat as `DRAFT`.

| Prerequisite | Path | Gate |
|---|---|---|
| requirements | `.specs/<spec-name>/requirements.md` | HARD |

- **HARD gate failed** (missing or status is not `APPROVED`): Display: "Cannot proceed: `requirements.md` is missing or not APPROVED (current status: `<status>`). Run `spec:approve <spec-name> requirements` first." Use `AskUserQuestion` with options: "Run spec:approve now", "Cancel". Do NOT offer "proceed anyway".
- **All gates pass**: Proceed silently to Step 1.

### Step 1: Read Requirements

1. If `<args>` contains a spec name, look for requirements at `.specs/<spec-name>/requirements.md`
2. If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose
3. Read and analyze the requirements document
4. Identify **distinct problem areas** — groups of related requirements that need separate technical investigation (e.g., "authentication mechanism", "data storage", "notification delivery")
5. Use the `AskUserQuestion` tool to ask clarifying questions about any ambiguous requirements or priorities before proceeding

### Step 2: Explore Codebase

Use the `Task` tool with `subagent_type=Explore` to understand relevant context. Launch **parallel agents** for each problem area:

1. **Patterns Analyst** — you are a Patterns Analyst exploring the codebase. Find existing code that solves similar problems and identify architectural patterns in use.
2. **Constraints Analyst** — you are a Constraints Analyst. Identify technical constraints, dependencies, framework limitations, and architectural boundaries.

Look for:
- Existing solutions that can be extended or reused
- Architectural patterns to follow (or consciously deviate from)
- Integration points and APIs that will be affected
- Technical debt or limitations that constrain options

### Step 3: Research External Sources

For each problem area, gather evidence from external sources. Launch these **in parallel** with each other (and in parallel with Step 2 where possible):

1. **Context7 MCP server** — use `resolve-library-id` and `query-docs` to fetch up-to-date documentation for relevant libraries and frameworks
2. **Web search** — use `WebSearch` to find best practices, architectural recommendations, and known pitfalls
3. **Web fetch** — use `WebFetch` to retrieve specific API docs, specs, or references mentioned in the requirements

### Step 4: Generate Solution Variants

For **each problem area**, propose 2-4 solution variants:

```markdown
### Problem Area: [Name]

_Related requirements: X.X, X.X_

#### Variant A: [Name]

**How it works:** [Brief description]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Effort:** [Low / Medium / High]
**Risk:** [Low / Medium / High]
**Codebase fit:** [How well it aligns with existing patterns]
```

For each variant, consider:
- Implementation complexity and effort
- Impact on existing code
- Alignment with codebase patterns and conventions
- Maintenance burden
- Scalability and performance
- Evidence from documentation and best practices

### Step 5: Discuss and Select

Present the variants to the user and use the `AskUserQuestion` tool for each problem area to let the user **pick one variant**:
- Explain tradeoffs clearly before asking
- Highlight which variant best fits the existing codebase (mark it as "(Recommended)" in the options)
- Use the `AskUserQuestion` tool with variant names as options — one question per problem area
- Note any constraints or dependencies between choices across problem areas

### Step 6: Write research.md

Once the user has selected variants, create the document at `.specs/<spec-name>/research.md`.

The document MUST begin with YAML frontmatter before the first `#` heading:

```yaml
---
status: DRAFT
created: <today's date YYYY-MM-DD>
updated: <today's date YYYY-MM-DD>
---
```

```markdown
# Research: [Feature Name]

## Problem Statement

[What problem are we solving and why it matters]

## Problem Areas

### 1. [Problem Area Name]

_Related requirements: X.X, X.X_

#### Variant A: [Name] — CHOSEN

**How it works:** [Description]

**Pros:** [list]
**Cons:** [list]
**Effort:** [Low/Medium/High] | **Risk:** [Low/Medium/High]

**Why chosen:** [Rationale based on discussion]

#### Variant B: [Name] — Rejected

**How it works:** [Description]

**Pros:** [list]
**Cons:** [list]
**Effort:** [Low/Medium/High] | **Risk:** [Low/Medium/High]

**Why rejected:** [Reason]

### 2. [Next Problem Area]

[Same structure]

## Summary

| Problem Area | Chosen Variant | Effort | Risk |
|-------------|---------------|--------|------|
| [Area 1]    | [Variant name] | [L/M/H] | [L/M/H] |
| [Area 2]    | [Variant name] | [L/M/H] | [L/M/H] |

## Codebase Insights

- [Relevant pattern or constraint discovered]
- [Another insight]

## Open Questions

- [ ] [Question that needs to be resolved during design]
- [ ] [Another open question]

## Next Steps

Ready for `spec:design <spec-name>` to create the technical design based on these chosen solutions.
```

### Step 7: Confirm with User

Present the summary and use the `AskUserQuestion` tool to confirm, with options like "Looks good, proceed to design", "I want to make changes", "Review research first"

## Arguments

- `<args>` - Spec name (required — `requirements.md` must already exist)
  - `user-auth` - Research for the user-auth specification
  - `payment-flow` - Research for the payment-flow specification

Examples:
- `spec:research user-auth` - Research implementation approaches for user-auth
- `spec:research api-v2` - Research solutions for the api-v2 specification

## Research Guidelines

1. **Ground in evidence** — back variant assessments with documentation, codebase examples, or benchmarks
2. **Respect existing patterns** — prefer solutions that align with the codebase unless there's a strong reason to deviate
3. **Keep variants distinct** — each variant should represent a meaningfully different approach, not minor variations
4. **Be honest about unknowns** — flag areas where more investigation is needed as open questions
5. **Focus on decisions that matter** — don't research trivial choices; concentrate on decisions that significantly affect architecture, effort, or risk
