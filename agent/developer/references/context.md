# Context Engineering

How context flows through an agent and how to keep the context window healthy.

## Parallelization rules

**Default: prefer sequential single-threaded execution.** Only parallelize when subtasks are truly independent.

**Parallelize ONLY when:**
- Subtasks have zero data dependencies on each other.
- Outputs do not need to be compatible or merged.
- Each subtask operates on different data.

**Keep sequential when:**
- Later steps depend on earlier results.
- Outputs must be compatible (e.g. code that works together).
- Context from one step informs the next.

For parallel branches, define an explicit merge point and a compatibility check verifying the outputs work together.

## Context-sharing strategies

For multi-agent systems, decide per agent boundary how much context flows:

1. **Full trace sharing** — subagents see the complete history (user request, prior research, all decisions).
   - Pro: better decisions with the full picture.
   - Con: larger context, higher cost, potential distraction.
2. **Minimal instruction** — subagents get only the task and essential parameters.
   - Pro: focused, cheaper, faster.
   - Con: may miss important context, produce incompatible outputs.
3. **Summary handoff** — subagents get a summary of the prior agent's output, not its intermediate steps.

Map each boundary: From → To, strategy, what is shared, what is excluded.

## Five context failure modes

| Failure mode | Description | Risk | Mitigation |
|---|---|---|---|
| **Context Poisoning** | A hallucination enters context and is then repeatedly referenced | HIGH if the agent self-references | Validate facts before adding to context; use structured outputs |
| **Context Distraction** | Context so long the model ignores its training knowledge | MEDIUM for long sessions | Cap context length; summarize old turns |
| **Context Confusion** | Irrelevant context degrades response quality | MEDIUM if using RAG | Filter retrieval results; relevance scoring |
| **Context Clash** | New info conflicts with earlier info in the prompt | HIGH for evolving data | Timestamp context; prefer the latest; use explicit override markers |
| **Context Rot** | At ~100K tokens the model cannot distinguish important from noise | HIGH for long tasks | Compress before 100K; use hierarchical summarization |

## Compression strategy

**When to compress:**
- At every step (aggressive — for very long tasks).
- At X% of the context window (e.g. 80%, 95%).
- At agent-agent boundaries (during handoff).
- After token-heavy tool calls (search, code analysis).

**How to compress:**
- **Prune oldest** — drop earliest turns, keep recent.
- **Hierarchical summarization** — summarize old turns, keep recent verbatim.
- **Recursive summarization** — chunk → summarize → combine → summarize again.
- **Selective retention** — identify critical decisions/facts and never compress them.

**Critical rule:** identify information that MUST NOT be compressed — user's original request and constraints, key architectural decisions, active error context — and mark it as protected.

## Error-feedback loop

Design how the agent handles and learns from errors:

1. Agent attempts an action → it fails.
2. Error message + the failing code/input + relevant context → fed back to the agent.
3. Agent diagnoses the issue → generates a fix.
4. Agent retries with the fix.
5. On repeated failure → escalate (HITL or a different strategy).

**Retry policy:** set a max retries per action and an escalation threshold.

**Error → context pipeline** — per error type, define what context to add and the retry strategy:
- API timeout → error message + request params → retry with backoff.
- Validation error → error + input + schema → fix input, retry.
- Code execution failure → error + code + stack trace → diagnose, fix, retry.
- Rate limit → error + timing info → wait and retry.

**Proactive error prevention:** if certain errors are common, bake them into the system prompt so the agent avoids them preemptively.

**Escalation path:** 1st failure — retry with error context; 2nd failure — try an alternative approach; 3rd failure — escalate to a human / log for review.
