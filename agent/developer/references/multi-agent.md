# Multi-Agent Systems

How to design a system of multiple collaborating agents.

## Single vs. multi-agent

**A single agent is enough when:**
- One domain, one task type.
- < 10 tools.
- Simple linear workflows.
- One user persona.

**Multi-agent is needed when:**
- Multiple distinct domains or expertise areas.
- > 15 tools — performance degrades with tool count.
- Creative tasks need separation from analytical tasks.
- Different parts of the system need different models or permissions.
- You need peer review or quality checks between steps.

If a single agent is sufficient, do not build a multi-agent system.

## Organizational design

Principle: **design multi-agent systems like organizational design.**

1. **List all roles** — if humans did this work, what job titles would they have?
2. **Group by expertise** — the same domain knowledge = the same agent.
3. **Separate creative from analytical** — generators vs. reviewers.
4. **Define supervision** — who manages whom?

An agent roster captures, per agent: role, expertise, model, tools. A typical roster: Coordinator (manager — task routing, planning), Researcher (specialist — information gathering), Writer (specialist — content generation), Reviewer (quality — review and feedback).

## Supervision patterns

**A. Agent supervisor** — a dedicated agent manages others, which are passed as tools.
- Pros: flexible, the supervisor decides strategy.
- Cons: the supervisor is an LLM — may make unpredictable routing decisions.
- Best for: open-ended tasks, research, creative work.

**B. Workflow orchestrator** — a deterministic workflow calls agents at defined steps.
- Pros: predictable, traceable, testable.
- Cons: less flexible, cannot adapt at runtime.
- Best for: business processes, pipelines, compliance-heavy domains.

**C. Hybrid** — a workflow handles the skeleton; agents handle unstructured decisions within steps.
- Pros: best of both — structure plus flexibility.
- Best for: most production systems.

## Control flow

**Planning phase** — agents should establish an approach BEFORE executing, like a PM specs features before engineering builds:
1. Coordinator receives the task.
2. Coordinator creates a plan (which agents, in what order, with what inputs).
3. Human reviews the plan (optional HITL checkpoint).
4. Coordinator dispatches to specialists.
5. Specialists execute and report back.
6. Coordinator synthesizes results.

**Communication patterns:**

| Pattern | Description | When to use |
|---------|------------|-------------|
| Sequential handoff | Agent A → B → C | Tasks have dependencies |
| Parallel dispatch | Agent A + B simultaneously | Independent subtasks |
| Review loop | Writer → Reviewer → Writer (iterate) | Quality-critical output |
| Gossip / consensus | All agents discuss until agreement | Collaborative decision-making |
| Manager decision | Supervisor collects inputs, decides | Efficiency over consensus |

## Composition

**Agents as workflow steps** — the workflow orchestrates; agents are individual steps, each with a defined autonomy level (high = decides what to do; low = follows instructions exactly).

**Workflows as agent tools** — the agent decides WHICH workflow to run; the workflow ensures HOW. Each workflow-tool needs a clear description and a "when the agent should call" trigger.

## A2A protocol

Use the Agent-to-Agent protocol only when agents cross trust boundaries or frameworks.

**Use A2A when:**
- Agents built in different frameworks need to communicate.
- Agents are maintained by different teams/organizations.
- You need standardized agent discovery and capability advertising.

**A2A vs MCP:** MCP connects Agent ↔ Tool (a USB port for peripherals); A2A connects Agent ↔ Agent (HTTP between microservices).

**A2A implementation:** discovery via a `/.well-known/agent.json` metadata file; task lifecycle submitted → working → input-required → completed / failed / canceled; communication over HTTP + JSON-RPC 2.0; streaming via SSE; standard web auth (OAuth, API keys).

Most systems do NOT need A2A — skip it if all agents live in the same codebase.

## Failure handling

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Agent timeout | Max execution time | Retry with a simplified task |
| Agent hallucination | Review agent or guardrail | Request regeneration with a stricter prompt |
| Agent loop | Max iterations counter | Break the loop, escalate to the supervisor |
| Tool failure | Error response | Feed the error to the agent for retry |
| Coordination failure | Conflicting outputs | Supervisor arbitrates or requests human input |

**Graceful degradation:** if a specialist agent fails, can the supervisor handle the task directly? If the reviewer is unavailable, can output go to human review? If the whole system is degraded, what is the minimal viable response?
