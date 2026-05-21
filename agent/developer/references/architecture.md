# Agent Architecture

How to choose and evolve the overall shape of an agent system. Read this first when starting a new agent.

## Evolutionary principle

**Start simple, split when needed.** Begin with the smallest architecture that could work and add structure only when a concrete limitation forces it. Do not design a multi-agent system on day one.

## Capability mapping

Before choosing an architecture, whiteboard what the agent must do:

1. **Brainstorm** — list everything the agent should be able to do, with no filtering.
2. **Group** — cluster capabilities by data source, by "job title," or by business-process step.
3. **Divide** — find natural boundaries: departments, task types, data-access scopes.
4. **Assign** — map each capability group to a distinct agent role.
5. **Prioritize** — rank groups by business impact; the highest-impact group is what you build first.

## Architecture selection matrix

| Architecture | When to use | Shape |
|---|---|---|
| **Single Agent** | < 5 tools, one domain, simple linear workflow, one user persona | One LLM loop with a tool set |
| **Router + Specialists** | Multiple distinct domains, user intent varies | A classifier routes each request to a specialist agent |
| **Coordinator + Workers** | Multi-step workflows, tasks depend on each other | A manager plans and dispatches to worker agents, then synthesizes |
| **Pipeline** | Sequential processing stages with fixed order | Deterministic stages, each transforms the previous output |

Performance degrades past ~15 tools on one agent — that is a concrete trigger to split into Router + Specialists or Coordinator + Workers. Separate creative tasks from analytical tasks; separate parts that need different models or permissions.

## Human-in-the-loop (HITL) framework

Three HITL modes:

1. **In-the-loop** — agent pauses for human approval before acting. Use for irreversible actions.
2. **Post-processing** — human reviews a draft before it is finalized. Use for content and code.
3. **Deferred** — agent continues; humans give feedback asynchronously. Use for long workflows.

Decision rules — require HITL when ANY of these hold:

- The action is irreversible.
- There is legal or regulatory risk.
- The cost of an error is high.

The agent can be autonomous when the domain is well-defined with clear rules and errors are cheap and reversible.

## Dynamic configuration signals

Identify runtime signals that should change agent behavior, and wire them into config rather than hard-coding one behavior:

- **User tier** (free / pro / enterprise) → model size, available tools, retrieval depth.
- **User role** (admin / editor / viewer) → which actions are permitted.
- **Environment** (dev / staging / production) → strictness of safety constraints and guardrails.

## Evolution plan

Plan the agent in phases so growth is intentional:

- **Phase 1** — the minimal single-agent starting point that delivers the top-priority capability.
- **Phase 2** — the growth trigger (e.g. tool count, new domain) and the first split.
- **Phase 3** — the mature target architecture.

## Implementation priority

Build the highest-business-impact agent first. Add the second agent only once the first is stable. Split further only when a real limitation appears — never preemptively.
