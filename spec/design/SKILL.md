---
name: spec:design
description: Create Design Document - generates a technical design document based on the requirements document
---

# Create Design Document

Creates a design document based on the requirements document. This command reads the requirements from `.specs/<spec-name>/requirements.md` and generates a technical design.

## When to use

Use this skill when the user needs to:
- Create a technical design document from existing requirements
- Generate architecture diagrams and component specifications
- Plan implementation details before coding

## Instructions

### Step 1: Locate Requirements

1. If `<args>` contains a spec name, look for requirements at `.specs/<spec-name>/requirements.md`
2. If no spec name provided, list available specs in `.specs/` and ask user to choose
3. Read and analyze the requirements document

### Step 2: Analyze the Codebase

Before writing the design, perform a deep analysis using **parallel sub-agents and all available information sources**. Launch the following investigations concurrently:

#### 2a. Codebase Exploration (launch in parallel)

Use the `Task` tool with `subagent_type=Explore` to run **multiple exploration agents in parallel**. Each agent should investigate a different aspect:

1. **Architecture agent** — explore overall project structure, entry points, module boundaries, and dependency graph
2. **Patterns agent** — identify coding conventions, design patterns, naming styles, error handling approaches, and testing patterns used in the codebase
3. **Integration points agent** — find APIs, services, database models, external dependencies, and configuration files relevant to the requirements
4. **Affected areas agent** — based on the requirements document, identify specific files and components that will need to be created or modified

All four agents MUST be launched in a **single message** (parallel tool calls) to maximize efficiency.

#### 2b. Technology Research (launch in parallel with 2a)

Use all available external information sources to gather context about the technologies and libraries used in the project:

1. **Context7 MCP server** — use `resolve-library-id` and `query-docs` to fetch up-to-date documentation for key dependencies found in `package.json`, `go.mod`, `Cargo.toml`, or equivalent manifest files. Query best practices, API references, and recommended patterns relevant to the design
2. **Web search** — use `WebSearch` to find current best practices, architectural recommendations, and known pitfalls for the technologies and patterns relevant to the feature being designed
3. **Web fetch** — if the requirements reference specific APIs, services, or specs (e.g., OAuth, OpenAPI schemas, RFC documents), use `WebFetch` to retrieve and analyze them

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

```markdown
# Design Document: [Feature Name]

## Overview

[Brief description of what will be implemented and the key changes]

### Key Changes

1. [Major change 1]
2. [Major change 2]
3. [Major change 3]

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
7. **Design for natural user flows** - Every interaction flow must minimize navigation hops. When related entities are managed on different pages (e.g., categories and subcategories), the design MUST include inline creation mechanisms (modal dialogs, quick-add controls in dropdowns/selects) so the user can create a dependent entity without leaving the current context. Never design flows where the user has to go to page A, create entity X, go back to page B, and then link X — instead, provide in-context creation of X directly on page B.

### Step 4: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. A summary of the design decisions
3. Ask if they want to make any changes

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
