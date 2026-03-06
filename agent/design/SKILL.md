---
name: agent:design
description: Design AI Agent - comprehensive agent system design that orchestrates research sub-agents across all areas and produces a unified design document
---

# Design AI Agent

The main orchestrator skill for designing AI agent systems. Gathers requirements, launches parallel research sub-agents to investigate each area (prompts, tools, memory, workflows, RAG, multi-agent, context engineering), and compiles findings into a unified design document.

Based on "Patterns for Building AI Agents" and "Principles of Building AI Agents" (Bhagwat & Gienow, 2025).

## When to use

Use this skill when the user needs to:
- Design a new AI agent or multi-agent system from scratch
- Create a comprehensive design covering all aspects of an agent system
- Get a structured design document for implementation planning

For focused work on a single area, use the standalone skills directly:
`agent:prompt`, `agent:tools`, `agent:memory`, `agent:workflow`, `agent:rag`, `agent:multi`, `agent:context`

## Instructions

### Step 1: Understand the Domain

Use the `AskUserQuestion` tool to gather context:
1. What problem domain will the agent operate in?
2. Who are the end users?
3. What systems/APIs/data sources will the agent interact with?
4. What is the risk tolerance? (low = heavy HITL, high = autonomous)
5. What is the scale? (prototype, internal tool, production SaaS)

Do not proceed until the domain is clear.

### Step 2: Whiteboard Agent Capabilities

Guide the user through a capability mapping exercise:

1. **Brainstorm** — Use `AskUserQuestion` to list everything the agent should do
2. **Group** — Cluster by data sources, "job title," or business process step
3. **Divide** — Identify natural boundaries (departments, task types, data access)
4. **Assign** — Map capability groups to distinct agent roles
5. **Prioritize** — Rank by business impact

### Step 3: Choose Architecture

Apply the evolutionary principle: **start simple, split when needed.**

Use `AskUserQuestion` to select:

| Architecture | When to use |
|---|---|
| **Single Agent** | < 5 tools, one domain, simple workflow |
| **Router + Specialists** | Multiple domains, user intent varies |
| **Coordinator + Workers** | Multi-step workflows, tasks depend on each other |
| **Pipeline** | Sequential processing stages |

Generate a Mermaid architecture diagram.

### Step 4: Determine Research Scope

Use `AskUserQuestion` to ask which areas need investigation. Present as multi-select:

| Area | Skill | When relevant |
|------|-------|---------------|
| Prompt engineering | `agent:prompt` | Always — every agent needs prompts |
| Tool design | `agent:tools` | Agent calls APIs, databases, or external services |
| Memory architecture | `agent:memory` | Agent needs to remember across turns or sessions |
| Workflow design | `agent:workflow` | Complex multi-step processes with branching |
| RAG pipeline | `agent:rag` | Agent needs to search documents or knowledge bases |
| Multi-agent | `agent:multi` | System has multiple collaborating agents |
| Context engineering | `agent:context` | Long tasks, large context, or multi-agent context sharing |

### Step 5: Launch Research Sub-Agents

For each selected area, launch a parallel `Agent` sub-agent. Use a **single message with multiple Agent tool calls** to run them in parallel.

Each sub-agent should:
- Analyze the codebase (if there is existing code)
- Apply the frameworks from the corresponding skill
- Return a structured summary of findings and recommendations

**Sub-agent prompts should include:**

#### Prompt Research Agent
> Analyze what this agent system needs for prompts. Apply frameworks from agent:prompt methodology:
> - Recommend model and provider (start expensive, optimize later)
> - Draft system prompt architecture (identity, context, instructions, examples)
> - Suggest few-shot example strategy (zero/single/few-shot)
> - Production checklist (quality, cost, latency)
> Return a structured section for the design document.

#### Tool Research Agent
> Analyze what tools this agent needs. Apply frameworks from agent:tools methodology:
> - Decompose operations (think like an analyst — one tool per operation)
> - Design tool schemas with descriptions and "when to call"
> - Identify third-party integrations needed
> - Recommend MCP strategy (client/server/skip)
> Return a structured section for the design document.

#### Memory Research Agent
> Analyze memory requirements. Apply frameworks from agent:memory methodology:
> - Determine which layers needed: conversation window, working memory, semantic recall
> - Design working memory schema if needed
> - Configure semantic recall settings (topK, embedding model, vector DB)
> - Recommend memory processors (TokenLimiter, ToolCallFilter)
> Return a structured section for the design document.

#### Workflow Research Agent
> Analyze workflow requirements. Apply frameworks from agent:workflow methodology:
> - Map process to workflow primitives (branch, chain, merge, condition)
> - Identify suspend/resume points for HITL
> - Design streaming strategy for UX
> - Plan observability (OpenTelemetry spans)
> Return a structured section for the design document.

#### RAG Research Agent
> Analyze RAG requirements. Apply frameworks from agent:rag methodology:
> - Apply RAG decision tree: is RAG even needed? (full context → tools → RAG)
> - If yes: recommend chunking strategy, embedding model, vector DB
> - Configure retrieval (topK, reranking, hybrid queries)
> Return a structured section for the design document.

#### Multi-Agent Research Agent
> Analyze multi-agent requirements. Apply frameworks from agent:multi methodology:
> - Design agent organization (roles, expertise, supervision)
> - Choose supervision pattern (agent supervisor, workflow orchestrator, hybrid)
> - Define control flow and communication patterns
> - Plan composition (agents as tools, workflows as tools)
> Return a structured section for the design document.

#### Context Research Agent
> Analyze context engineering needs. Apply frameworks from agent:context methodology:
> - Assess parallelization: sequential vs. parallel workflow
> - Design context sharing between agents
> - Identify context failure mode risks (poisoning, distraction, rot, clash, confusion)
> - Plan compression strategy and error feedback loops
> Return a structured section for the design document.

### Step 6: Human-in-the-Loop Design

After research completes, determine HITL checkpoints:

**Three HITL modes:**
1. **In-the-loop** — Agent pauses for human approval (irreversible actions)
2. **Post-processing** — Human reviews draft before finalization (content, code)
3. **Deferred** — Agent continues, collects feedback asynchronously (long workflows)

**Decision framework:**
- Action irreversible? → HITL required
- Legal/regulatory risk? → HITL required
- Cost of error high? → HITL required
- Domain well-defined with clear rules? → Can be autonomous

### Step 7: Dynamic Configuration

Identify runtime signals that change agent behavior:
- User tiers (free/pro/enterprise) → model, tools, retrieval depth
- User roles (admin/viewer) → available actions
- Environment (dev/staging/production) → safety constraints

### Step 8: Compile Design Document

Compile all research findings and decisions into `.specs/<spec-name>/agent-design.md`:

```markdown
# Agent Design: [System Name]

## Overview
[Brief description of the agent system and its purpose]

## Agent Capability Map
[From Step 2 — agents, capabilities, tools, data sources]

## Architecture
[From Step 3 — architecture type, Mermaid diagram]

## Prompt Strategy
[From prompt research agent — model selection, system prompt, few-shot]

## Tool Design
[From tool research agent — tool inventory, schemas, integrations, MCP]

## Memory Architecture
[From memory research agent — layers, working memory, semantic recall]

## Workflow Design
[From workflow research agent — graph, suspend/resume, streaming, observability]

## RAG Pipeline
[From RAG research agent — decision, chunking, embedding, retrieval]

## Multi-Agent Design
[From multi-agent research agent — org, supervision, control flow, composition]

## Context Engineering
[From context research agent — parallelization, sharing, failure modes, compression]

## Human-in-the-Loop
[From Step 6 — HITL map with modes and triggers]

## Dynamic Configuration
[From Step 7 — configuration matrix]

## Implementation Priority
1. [First agent to build — highest priority]
2. [Second agent — add when first is stable]
3. [Additional agents — split when needed]

## Evolution Plan
- **Phase 1:** [Starting point]
- **Phase 2:** [Growth trigger and expansion]
- **Phase 3:** [Maturity target]
```

### Step 9: Offer Next Steps

Use `AskUserQuestion` to offer:
1. **Deep dive** — run a standalone skill for any area that needs more detail (e.g., `agent:tools` for detailed schema design)
2. **Security audit** — run `agent:secure` to check for vulnerabilities
3. **Eval system** — run `agent:eval` to set up evaluation
4. **Full review** — run `agent:review` to validate against all patterns

## Arguments

- `<args>` - Optional spec name and/or description of the agent system
  - `<spec-name>` — name for the specification (kebab-case)
  - Free text — description of the agent's purpose

Examples:
- `agent:design customer-support` — design a customer support agent
- `agent:design multi-agent code review system` — design a code review system
