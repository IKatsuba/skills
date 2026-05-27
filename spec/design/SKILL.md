---
name: spec:design
description: Technical Design - picks one variant per problem area from the research catalogue, then produces architecture diagrams, interfaces, and data flow. Decisions live here, not in research.
role: Software Architect
argument-hint: <spec-name>
---

# Create Design Document

Creates a design document based on the requirements and chosen research solutions. This command reads both `.specs/<spec-name>/requirements.md` and `.specs/<spec-name>/research.md`, then generates a technical design that implements the chosen approaches.

## Role

You are a **Software Architect**. Your job has two parts, in order:

1. **Decide.** Read the variant catalogue produced by `spec:research` and, *with the user*, pick one variant per problem area. Record the chosen variants and the rationale for each. This is where CHOSEN/Rejected lives — not in research.
2. **Deepen.** Translate the chosen variants into a buildable technical blueprint: components, interfaces, data flows, integration points, diagrams, and type definitions precise enough for an engineer to implement without guessing.

Other rules:
- Validate the design against the actual codebase, not assumptions.
- Never introduce requirements not present in the requirements document.
- If during design you discover the variant catalogue is incomplete (you'd like an option that isn't in `research.md`), pause and tell the user — they can re-run `spec:research` in extension mode rather than have you invent options here.

## When to use

Use this skill when the user needs to:
- Create a technical design document from existing requirements
- Generate architecture diagrams and component specifications
- Plan implementation details before coding

## Instructions

### Step 0: Check Prerequisites

Read the frontmatter of each prerequisite document. A document's status is in its YAML frontmatter `status` field. If no frontmatter exists, treat as `DRAFT`.

| Prerequisite | Path | Gate |
|---|---|---|
| requirements | `.specs/<spec-name>/requirements.md` | HARD |
| research | `.specs/<spec-name>/research.md` | SOFT |

- **HARD gate failed** (missing or status is not `APPROVED`): Display: "Cannot proceed: `requirements.md` is missing or not APPROVED (current status: `<status>`). Run `spec:approve <spec-name> requirements` first." Use `AskUserQuestion` with options: "Run spec:approve now", "Cancel". Do NOT offer "proceed anyway".
- **SOFT gate failed** (research.md missing or not APPROVED): Decisions are part of this skill's job, but they're much weaker without a variant catalogue. Display: "Warning: `research.md` is missing or not APPROVED. Without a variant catalogue, decisions in this skill will be made from a much narrower option space." Use `AskUserQuestion` with options: "Run spec:research first (recommended)", "Run spec:approve research", "Proceed without a catalogue".
- **All gates pass**: Proceed silently to Step 1.

### Step 1: Locate Specification Documents

1. If `$0` is provided, use it as the spec name and look in `.specs/<spec-name>/`
2. If no spec name provided, list available specs in `.specs/` and use the `AskUserQuestion` tool to let the user choose
3. Read and analyze:
   - `requirements.md` — the requirements document (required)
   - `research.md` — the variant catalogue (strongly recommended; see Step 0)

### Step 1.5: Decision Pass — Pick a Variant per Problem Area

**MANDATORY STOP — DO NOT SKIP. DO NOT choose variants yourself. You MUST ask the user.**

This is the step where CHOSEN/Rejected is decided. `spec:research` deliberately leaves the catalogue undecided; the decision lives here.

For **each** problem area in `research.md`, one at a time:

1. Summarize the variants for that area in 1–2 sentences each, with their Effort/Risk/Codebase-fit lines from the catalogue.
2. If `research.md` notes a cross-area dependency that constrains this area (because of a choice made for an earlier area), state it before asking.
3. Call `AskUserQuestion` with the variant names as options. Optionally include "None of these — re-run spec:research to widen the catalogue" as a final option.
4. Wait for the user's answer.
5. **Draft the `Why chosen` rationale yourself** from the catalogue context (the Effort/Risk/Codebase-fit lines that distinguish the chosen variant from the alternatives). Then decide whether the choice is **obvious** or **non-obvious**:
   - **Obvious** — the chosen variant is the clear winner on the catalogue's own signals (e.g., lowest Effort + lowest Risk, or strongest codebase-fit, or the only one without a noted blocker). Record your drafted rationale silently and move on. Do **not** ask the user "why".
   - **Non-obvious** — the user picked a variant that is worse on at least one explicit signal than a rejected alternative (higher Effort, higher Risk, weaker codebase-fit, or contradicts a cross-area dependency). The catalogue doesn't explain this choice, so you must ask. Call `AskUserQuestion` and **name the contradiction in the question** (e.g., "Why B over A? B is Medium Effort vs A's Low — what tips it?"). Use the user's answer as the rationale.
6. Record `{ area, chosen variant, why chosen }` in working memory before moving to the next area.

Rules:
- You MUST use `AskUserQuestion` — never output the question as plain text.
- You MUST NOT pre-select a variant, mark one as "(Recommended)", or proceed without explicit answers for every area.
- If the user picks "None of these", **stop the design skill** and tell them to run `spec:research <spec-name>` in extension mode. Do not invent a new variant in the design step.
- If `research.md` is missing (the user chose "Proceed without a catalogue" at Step 0), conduct the Decision Pass in a degraded form: prompt the user to name the chosen approach per problem area directly. Be vocal that this skips the variant-comparison benefit.

When all decisions are recorded, present a one-screen recap (`Area → Chosen Variant → Why chosen` table) and confirm via `AskUserQuestion` ("Decisions look right, proceed", "Let me revisit area X"). Only proceed to Step 2 after explicit confirmation.

### Step 2: Analyze the Codebase

Before writing the design, analyze the codebase using **parallel sub-agents** — focused on the variants that were just chosen in Step 1.5.

#### 2a. Codebase Exploration (launch in parallel)

Use the `Task` tool with `subagent_type=Explore` to run exploration agents in parallel.

**When `research.md` EXISTS** — run 2 focused validation agents scoped to the variants chosen in Step 1.5:

1. **Integration Validator** — you are an Integration Validator. Find specific files, APIs, and models that the chosen variants will touch. Verify that the integration points the chosen variants assume actually exist in the codebase as described in `research.md`.
2. **Impact Analyst** — you are an Impact Analyst. Identify the exact files and components that will need to be created or modified to implement the chosen variants. Map the full data flow.

The research catalogue already covers architecture and patterns for each variant — do NOT re-discover what is already documented. Focus narrowly on the chosen variants.

**When `research.md` is MISSING** — run 4 broad discovery agents:

1. **Architecture Scout** — you are an Architecture Scout. Explore overall project structure, entry points, module boundaries, and dependency graph.
2. **Patterns Analyst** — you are a Patterns Analyst. Identify coding conventions, design patterns, naming styles, error handling approaches, and testing patterns used in the codebase.
3. **Integration Validator** — you are an Integration Validator. Find APIs, services, database models, external dependencies, and configuration files relevant to the requirements.
4. **Impact Analyst** — you are an Impact Analyst. Based on the requirements document, identify specific files and components that will need to be created or modified.

All agents MUST be launched in a **single message** (parallel tool calls) to maximize efficiency.

#### 2b. Technology Research (launch in parallel with 2a)

Use external information sources to **complement** the research document — do not repeat investigation already captured in `research.md`. Focus on implementation-level details needed for the design:

1. **Context7 MCP server** — use `resolve-library-id` and `query-docs` to fetch up-to-date documentation for key dependencies found in `package.json`, `go.mod`, `Cargo.toml`, or equivalent manifest files. Query API references and implementation patterns relevant to the chosen variants
2. **Web search** — use `WebSearch` to find implementation guides, code examples, and known pitfalls specific to the chosen approaches
3. **Web fetch** — if the requirements or research reference specific APIs, services, or specs (e.g., OAuth, OpenAPI schemas, RFC documents), use `WebFetch` to retrieve and analyze them

Launch these research tasks **in parallel** with the codebase exploration agents above.

#### 2c. Synthesize Findings

After all parallel agents and research complete, synthesize the results into a unified understanding:
- Current architecture and where the new feature fits
- Existing patterns to follow (or consciously deviate from with justification)
- Technology constraints and best practices from documentation
- Files and components to create or modify
- Integration points and potential risks

### Step 3: Create the Design Document

Create the document at `.specs/<spec-name>/design.md` with this structure:

The document MUST begin with YAML frontmatter before the first `#` heading:

```yaml
---
status: DRAFT
created: <today's date YYYY-MM-DD>
updated: <today's date YYYY-MM-DD>
---
```

```markdown
# Design Document: [Feature Name]

## Overview

[Brief description of what will be implemented and the key changes]

### Key Changes

1. [Major change 1]
2. [Major change 2]
3. [Major change 3]

### Decisions

[Record the variants picked in Step 1.5. This is the canonical home for these choices — `research.md` only lists the menu.]

| Problem Area | Chosen Variant | Why chosen | Reference |
|-------------|----------------|------------|-----------|
| [Area 1]    | [Variant name] | [one-line rationale captured during Step 1.5] | research.md §1 |
| [Area 2]    | [Variant name] | [one-line rationale]                          | research.md §2 |

[If `research.md` was absent and decisions were made directly in Step 1.5, write the chosen approach in 1–2 sentences per area and note that no variant catalogue existed.]

## Architecture

### Component Diagram

\`\`\`mermaid
graph TB
    subgraph "Module Name"
        A[Component A]
        B[Component B]
    end

    subgraph "External"
        C[External Service]
    end

    A --> B
    B --> C
\`\`\`

### Data Flow

\`\`\`mermaid
sequenceDiagram
    participant U as User
    participant C as Component
    participant S as Service
    participant E as External

    U->>C: Action
    C->>S: Request
    S->>E: API Call
    E-->>S: Response
    S-->>C: Result
    C-->>U: Display
\`\`\`

## Components and Interfaces

### [Component/Service Name]

[Description of the component]

\`\`\`typescript
// Path: src/path/to/file.ts

interface InterfaceName {
  property: Type;
  method(param: Type): ReturnType;
}

class ClassName {
  constructor(config: ConfigType);

  methodName(param: Type): ReturnType;
}
\`\`\`

[Continue with additional components]

## Data Models

### [Model Name]

\`\`\`typescript
interface ModelName {
  // Properties with comments
  field1: string;  // Description
  field2: number;  // Description
}
\`\`\`

## Data Flow Completeness

For each new field or entity introduced by this feature, trace the full data flow to ensure nothing is missed during implementation:

| Field/Entity | Schema | Migration | Query/Mutation | API Type | Frontend Type | UI Component |
|-------------|--------|-----------|---------------|----------|--------------|-------------|
| [field1]    | `path` | `path`    | `path`        | `path`   | `path`       | `path`      |
| [field2]    | `path` | N/A       | `path`        | `path`   | `path`       | `path`      |

Any field missing from a layer in this table is a bug waiting to happen. If a layer is not applicable (e.g., no migration needed), mark it as N/A with a reason.

## Error Handling

### Error Types and Handling

| Error | User Message |
|-------|-------------|
| Network error | "Could not connect to server." |
| Invalid input | "Please check your input." |

## Testing Strategy

### Approach

[Describe the testing approach - unit tests, integration tests, etc.]

### Unit Tests

\`\`\`typescript
describe('ComponentName', () => {
  it('should [expected behavior]', () => {
    // Test example
  });
});
\`\`\`

### Edge Cases

1. [Edge case 1] - [Expected handling]
2. [Edge case 2] - [Expected handling]
```

### Writing Guidelines

1. **Include diagrams** - Use Mermaid for architecture and flow diagrams
2. **Show TypeScript interfaces** - Define all new interfaces and types
3. **Reference file paths** - Indicate where code will be located
4. **Map to requirements** - Ensure design covers all requirements
5. **Consider error cases** - Document error handling strategy
6. **Include test examples** - Show how components will be tested
7. **Align with the variants chosen in Step 1.5** — The design implements the variants picked during the Decision Pass. If you find yourself wanting to deviate from a chosen variant while writing the design, stop and revisit Step 1.5 (re-decide for that area, possibly after re-running `spec:research` to add a missing option) rather than silently designing something different.
8. **Design for natural user flows** - Every interaction flow must minimize navigation hops. When related entities are managed on different pages (e.g., categories and subcategories), the design MUST include inline creation mechanisms (modal dialogs, quick-add controls in dropdowns/selects) so the user can create a dependent entity without leaving the current context. Never design flows where the user has to go to page A, create entity X, go back to page B, and then link X — instead, provide in-context creation of X directly on page B.

### Step 4: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. A summary of the design decisions
3. Use the `AskUserQuestion` tool to ask if they want to make changes or proceed, with options like "Looks good, proceed to tasks", "I want to make changes", "Review design first"

## Arguments

- `$ARGUMENTS` - The spec name via `$0` (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
