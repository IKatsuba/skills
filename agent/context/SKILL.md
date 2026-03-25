---
name: agent:context
description: Context Engineering - designs agent context strategy covering parallelization, context sharing, failure modes, compression, and error feedback
argument-hint: ["description or path"]
---

# Context Engineering

Guides the user through designing a context engineering strategy for their AI agent. Applies patterns 5-9 from "Patterns for Building AI Agents" (Bhagwat & Gienow, 2025): careful parallelization, context sharing between subagents, avoiding context failure modes, context compression, and feeding errors back into context.

## When to use

Use this skill when the user needs to:
- Design how context flows through an agent or multi-agent system
- Decide whether to parallelize agent workflows
- Prevent context window issues (poisoning, distraction, rot)
- Set up context compression strategy
- Build error recovery loops

## Instructions

### Step 1: Understand the Agent System

Use the `AskUserQuestion` tool to gather context:
1. Is this a single agent or multi-agent system?
2. What is the typical task length? (short = few turns, long = dozens of turns)
3. What tools does the agent call? (some tools return large payloads)
4. What model and context window size are you using?
5. Is there an existing agent design? (check `.specs/<spec-name>/agent-design.md`)

If an agent design document exists, read it first.

### Step 2: Parallelization Strategy (Pattern 5)

Analyze the agent's workflow and determine what can run in parallel vs. what must be sequential.

**Default rule: prefer sequential single-threaded execution.** Only parallelize when subtasks are truly independent.

Use `AskUserQuestion` to walk through each workflow:

**Parallelize ONLY when:**
- Subtasks have zero data dependencies on each other
- Outputs don't need to be compatible or merged
- Each subtask operates on different data

**Keep sequential when:**
- Later steps depend on earlier results
- Outputs must be compatible (e.g., code that works together)
- Context from one step informs the next

Output a workflow diagram:

```markdown
## Workflow: [Name]

### Sequential (shared context)
1. [Step 1] → feeds into →
2. [Step 2] → feeds into →
3. [Step 3]

### Parallel (independent)
- [Task A] ← independent → [Task B]
  - Merge point: [Where results combine]
  - Compatibility check: [How to verify outputs work together]
```

### Step 3: Context Sharing Strategy (Pattern 6)

For multi-agent systems, define how context flows between agents.

**Two approaches:**
1. **Full trace sharing** — subagents see the complete history (user request, prior research, all decisions)
   - Pro: better decisions with full picture
   - Con: larger context, higher cost, potential distraction
2. **Minimal instruction** — subagents get only the task and essential parameters
   - Pro: focused, cheaper, faster
   - Con: may miss important context, produce incompatible outputs

Use `AskUserQuestion` to decide per agent boundary:

```markdown
## Context Sharing Map

| From → To | Strategy | What is shared | What is excluded |
|-----------|----------|---------------|-----------------|
| Router → Specialist A | Minimal | User query, intent classification | Prior conversation history |
| Coordinator → Worker 1 | Full trace | Full plan, all prior outputs | Raw tool outputs (summarized) |
| Worker 1 → Worker 2 | Summary | Worker 1 output summary | Worker 1 intermediate steps |
```

### Step 4: Context Failure Mode Prevention (Pattern 7)

Audit the agent design for five context failure modes:

| Failure Mode | Description | Risk Level | Mitigation |
|---|---|---|---|
| **Context Poisoning** | Hallucination enters context and gets repeatedly referenced | HIGH if agent self-references | Validate facts before adding to context; use structured outputs |
| **Context Distraction** | Context so long the model ignores training knowledge | MEDIUM for long sessions | Cap context length; summarize old turns |
| **Context Confusion** | Irrelevant context degrades response quality | MEDIUM if using RAG | Filter retrieval results; relevance scoring |
| **Context Clash** | New info conflicts with earlier info in prompt | HIGH for evolving data | Timestamp context; prefer latest; explicit override markers |
| **Context Rot** | At ~100K tokens, model can't distinguish important from noise | HIGH for long tasks | Compress before 100K; use hierarchical summarization |

Use `AskUserQuestion` to assess each risk for the specific agent.

Output a risk matrix:

```markdown
## Context Failure Risk Matrix

| Failure Mode | Risk | Likelihood | Mitigation Strategy |
|---|---|---|---|
| Poisoning | HIGH | [Low/Med/High] | [Specific mitigation] |
| Distraction | MEDIUM | [Low/Med/High] | [Specific mitigation] |
| Confusion | MEDIUM | [Low/Med/High] | [Specific mitigation] |
| Clash | HIGH | [Low/Med/High] | [Specific mitigation] |
| Rot | HIGH | [Low/Med/High] | [Specific mitigation] |
```

### Step 5: Compression Strategy (Pattern 8)

Design when and how to compress context. Use `AskUserQuestion` to determine the right approach:

**When to compress:**
- At every step (aggressive — for very long tasks)
- At X% of context window (e.g., 80%, 95%)
- At agent-agent boundaries (during hand-off)
- After token-heavy tool calls (search, code analysis)

**How to compress:**
- **Prune oldest** — drop earliest turns, keep recent
- **Hierarchical summarization** — summarize old turns, keep recent verbatim
- **Recursive summarization** — chunk → summarize → combine → summarize again
- **Selective retention** — identify critical decisions/facts and never compress those

**Critical rule:** Identify information that MUST NOT be compressed (key decisions, user constraints, error context) and mark it as protected.

Output a compression plan:

```markdown
## Compression Strategy

**Trigger:** Compress at [X%] of context window ([N] tokens)
**Method:** [Hierarchical summarization / Prune oldest / etc.]

### Protected Context (never compress)
- User's original request and constraints
- Key architectural decisions
- Active error context
- [Domain-specific critical info]

### Compression Rules
1. Tool call outputs older than [N] turns → summarize to key findings
2. Intermediate reasoning older than [N] turns → drop
3. Agent-to-agent hand-offs → compress to decision summary
```

### Step 6: Error Feedback Loop (Pattern 9)

Design how the agent handles and learns from errors.

**Error feedback loop:**
1. Agent attempts action → fails
2. Error message + failing code/input + relevant context → fed back to agent
3. Agent diagnoses issue → generates fix
4. Agent retries with fix
5. If repeated failure → escalate (HITL or different strategy)

Use `AskUserQuestion` to identify common error scenarios for the domain.

**Proactive error patterns:** If certain errors are common, bake them into the system prompt so the agent avoids them preemptively.

Output an error handling plan:

```markdown
## Error Feedback Strategy

### Retry Policy
- Max retries per action: [N]
- Escalation after: [N] failures

### Error → Context Pipeline
| Error Type | Context Added | Retry Strategy |
|---|---|---|
| API timeout | Error message + request params | Retry with backoff |
| Validation error | Error + input + schema | Fix input, retry |
| Code execution failure | Error + code + stack trace | Diagnose, fix, retry |
| Rate limit | Error + timing info | Wait and retry |

### Proactive Error Prevention
Add to system prompt:
- [Common error 1] — [How to avoid]
- [Common error 2] — [How to avoid]

### Escalation Path
1. 1st failure: Retry with error context
2. 2nd failure: Try alternative approach
3. 3rd failure: Escalate to human / log for review
```

### Step 7: Summarize and Offer Next Steps

Present all findings to the user as a structured summary in the conversation. Do NOT write to `.specs/` — this skill works directly.

Use `AskUserQuestion` to offer:
1. **Implement changes** — apply context optimizations to existing agent code
2. **Fix failure modes** — address the highest-risk context issues found
3. **Comprehensive design** — run `agent:design` to cover all areas with a spec

## Arguments

- `$ARGUMENTS` (`$0`) - Optional description of the agent or path to existing code

Examples:
- `agent:context support chatbot with long conversations` — optimize context for a chatbot
- `agent:context src/agents/researcher.ts` — review context strategy in existing agent
- `agent:context` — start fresh
