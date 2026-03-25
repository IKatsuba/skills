---
name: project:init
description: Project Init - defines the overall system goals, stakeholders, constraints, and shared architectural decisions. Use when starting a new multi-spec project.
argument-hint: <project-name> ["description"]
---

# Project Init

Initializes a new project by defining its purpose, stakeholders, goals, technical constraints, and shared architectural decisions. This is the entry point for building a large system composed of multiple specifications.

## When to use

Use this skill when the user needs to:
- Start a new large-scale project (SaaS, platform, multi-module app)
- Define shared technical decisions before breaking work into specs
- Document system-level goals and constraints that span multiple features

## Instructions

### Step 1: Gather Information

Use the `AskUserQuestion` tool to gather:

1. **Project name** — kebab-case identifier (e.g., "my-saas", "trading-platform")
2. **What is this system?** — Brief description of what it does
3. **Who uses it?** — Key stakeholders and user roles
4. **What technology stack?** — Languages, frameworks, databases, infrastructure
5. **Any hard constraints?** — Budget, timeline, compliance, platform limitations

**Always use the `AskUserQuestion` tool** for these questions — never output them as plain text. Provide meaningful options where possible to reduce user typing.

### Step 2: Analyze the Codebase

If this is not a greenfield project:
1. Explore the existing codebase to understand current architecture
2. Identify established patterns, conventions, and technology choices
3. Note existing modules or services that will be part of the system

### Step 3: Clarify Scope

Use the `AskUserQuestion` tool to ask targeted follow-up questions about:
- **Non-goals** — What is explicitly out of scope for this system?
- **Shared architectural decisions** — Database strategy, authentication approach, API style, deployment model
- **Success criteria** — How will you know the project is complete?
- **System boundary** — What are the major modules or areas of the system?

Do not proceed to document generation until these are answered.

### Step 4: Create the Vision Document

Create the document at `.projects/<project-name>/vision.md` with this structure:

```markdown
# Project Vision: [Name]

## Problem Statement

[What problem does this system solve? Who has this problem? Why does it matter?]

## Stakeholders

| Role | Needs | Priority |
|------|-------|----------|
| [End user] | [What they need from the system] | [High/Med/Low] |
| [Admin] | [What they need] | [High/Med/Low] |

## Goals

1. [Goal 1 — specific and measurable]
2. [Goal 2 — specific and measurable]

## Non-Goals

- [What this system explicitly does NOT do]
- [Scope boundary that might be assumed but is excluded]

## Technical Constraints

- [Technology stack decisions that apply to ALL specs]
- [Infrastructure constraints]
- [Performance, scalability, or compliance requirements]

## Shared Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| [e.g., PostgreSQL for all persistent data] | [Why this choice] |
| [e.g., Next.js App Router] | [Why this choice] |
| [e.g., tRPC for internal API layer] | [Why this choice] |

## System Boundary

[Mermaid diagram showing the major modules/areas of the system and their relationships]

## Success Criteria

- [How do we know the project is done?]
- [Key metrics or milestones]
```

### Writing Guidelines

1. **Be specific** — "Fast response times" is bad; "API responses under 200ms at p95" is good
2. **Make goals measurable** — Each goal should have a way to verify it's achieved
3. **Non-goals are critical** — Explicitly excluding scope prevents creep later
4. **Shared decisions save time** — Every spec inherits these; be deliberate
5. **System boundary diagram** — Use Mermaid to show major modules and their relationships; keep it high-level

### Step 5: Confirm with User

After creating the document, present:
1. The location of the created file
2. A summary of the vision
3. Use the `AskUserQuestion` tool to ask if they want to make changes or proceed, with options like "Looks good, proceed to plan", "I want to make changes", "Review vision first"

Suggest running `project:plan <project-name>` as the next step.

## Arguments

This skill accepts an optional argument:
- `<args>` - Can include the project name and/or description. Parse it to extract:
  - Project name (kebab-case, e.g., "my-saas" or "trading-platform")
  - System description or context

If `<args>` is provided, use it to determine the project name and context. If not sufficient, ask the user for clarification.
