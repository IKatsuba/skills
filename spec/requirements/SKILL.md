---
name: spec:requirements
description: Create Requirements Document - generates a structured requirements document, asking clarifying questions about ambiguities before proceeding
---

# Create Requirements Document

This is the first step in the specification pipeline. Creates a requirements document based on the task context and project. The user provides a spec name and task description, and this command gathers context, asks targeted clarifying questions, and generates a structured requirements document.

## When to use

Use this skill when the user needs to:
- Create a new feature specification
- Document requirements for a task
- Generate a structured requirements document for planning

## Instructions

### Step 1: Gather Information

If the user hasn't provided sufficient context, ask them:
1. What is the name for this specification? (used for folder name, e.g., "user-authentication", "payment-integration")
2. What is the main goal or purpose of this feature/task?
3. What are the key user stories or use cases?
4. Are there any specific technical constraints or requirements?

After gathering initial context, ask targeted clarifying questions about:
- **Ambiguities** — anything unclear or open to interpretation in the description
- **Edge cases** — boundary conditions, error scenarios, empty states
- **Priorities** — which aspects are most important, what can be deferred
- **Scope boundaries** — what is explicitly out of scope

Do not proceed to codebase analysis until these questions are answered.

### Step 2: Analyze the Codebase

Before writing requirements:
1. Explore the relevant parts of the codebase to understand existing patterns
2. Identify related services, components, or modules
3. Note any dependencies or integrations that will be affected

### Step 3: Create the Requirements Document

Create the document at `.specs/<spec-name>/requirements.md` with this structure:

```markdown
# Requirements Document

## Introduction

[Brief description of what this feature/task aims to achieve and why it's needed]

## Glossary

[Define key terms used throughout the document, formatted as:]
- **Term**: Definition

## Requirements

### Requirement 1: [Requirement Name]

**User Story:** As a [role], I want [feature] so that [benefit].

#### Acceptance Criteria

1. THE [Component] SHALL [action/behavior]
2. WHEN [condition] THEN [Component] SHALL [action/behavior]
3. THE [Component] SHALL NOT [prohibited action]

[Continue with additional requirements following the same pattern]

## Superseded Behaviors

[If this feature modifies or removes existing functionality, list each change explicitly. If the feature is entirely new, omit this section.]

- [Old behavior] → REMOVED / REPLACED BY Requirement X.X
```

### Writing Guidelines

1. **Use SHALL for mandatory requirements** - "THE system SHALL..."
2. **Use WHEN-THEN for conditional behavior** - "WHEN user clicks submit THEN system SHALL..."
3. **Use SHALL NOT for prohibitions** - "THE system SHALL NOT expose..."
4. **Be specific and testable** - Each criterion should be verifiable
5. **Reference existing code patterns** - Align with project conventions
6. **Keep requirements atomic** - One requirement per item
7. **Prioritize user experience** - Every user flow must feel natural. When related entities exist (e.g., category and subcategory), requirements MUST include inline/contextual creation — the user should never be forced to navigate away from the current page to create a dependent entity and then return. For example, if a form needs a parent entity that doesn't exist yet, there must be a way to create it on the spot (inline dialog, quick-add in dropdown, etc.).
8. **Document intentional behavior changes** - When the feature modifies or removes existing behavior, add a "Superseded Behaviors" section that explicitly lists what is being replaced or removed. This prevents the implementer from accidentally restoring old behavior (e.g., re-adding removed undo functionality to make old tests pass). Format:
   ```
   ### Superseded Behaviors
   - [Old behavior description] → REMOVED / REPLACED BY [new behavior or requirement reference]
   ```

### Step 4: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. A summary of the requirements
3. Ask if they want to make any changes
4. Suggest proceeding with `spec:research <spec-name>` to investigate implementation approaches

## Arguments

This skill accepts an optional argument:
- `<args>` - Can include the spec name and/or description. Parse it to extract:
  - Spec name (kebab-case, e.g., "user-auth" or "payment-flow")
  - Task description or context

If `<args>` is provided, use it to determine the spec name and context. If not sufficient, ask the user for clarification.
