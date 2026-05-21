# Graph-Based Workflows

How to give an agent structure when pure agentic looping is too unpredictable.

**Key principle:** use workflows when agents are too unpredictable for the task. Workflows define explicit branching, parallel execution, checkpoints, and tracing.

## Four primitives

### 1. Chaining (sequential)
Steps run one after another; each step has access to the previous step's output.
- Use when: step B depends on step A's result.
- Example: Extract data → Validate → Transform → Store.

### 2. Branching (parallel)
Multiple steps run simultaneously on the same input.
- Use when: independent analyses of the same data.
- Example: Analyze sentiment + Extract entities + Classify topic, all in parallel.

### 3. Merging (convergence)
Combine results from multiple branches into a single output.
- Use when: parallel branches need to produce a unified result.
- Example: combine sentiment + entities + topic into one report.

### 4. Conditions (decision points)
Route to different steps based on intermediate results.
- Use when: different inputs require different processing paths.
- Example: if intent = "complaint" → escalation flow; else → standard flow.

## Step design rules

- Each step does ONE thing — no more than one LLM call per step.
- Input/output at each step should be meaningful and inspectable.
- Name steps clearly — names appear in traces.

## Suspend / resume

Identify where the workflow must pause for external input. For each suspension point define: the trigger, what state to persist, the resume signal, and a timeout.

Common suspension points:
- Human approval needed → persist full workflow state + pending action → resume on approve/reject → 24h timeout.
- External API callback → persist request ID + workflow state → resume on webhook → 1h timeout.
- User clarification → persist conversation history + ambiguous input → resume on user response → 30min timeout.

**Persistence:** store workflow state in a database / Redis / durable execution engine; state must be JSON-serializable; expire suspended workflows after their timeout.

**Key principle:** do NOT keep running processes alive for long waits. Persist state, shut down, resume when the signal arrives.

## Streaming

Users want to see progress, not a blank screen. Streaming makes agents feel faster and more reliable.

What to stream:
- **Step start** — step name + description, when each step begins.
- **LLM tokens** — token-by-token, during generation.
- **Tool call** — tool name + status, during tool execution.
- **Progress** — percentage or step count, between steps.
- **Custom data** — partial results, previews, when available.

Implementation: SSE or WebSocket; the frontend shows step-by-step progress, auto-scrolls, and displays tool calls. Push partial results even if the function is not done.

## OTel tracing

Use OpenTelemetry — the industry standard. Structure: Traces → Spans (a tree of nested operations, like a flame chart).

What to trace:

| Span | Attributes | Purpose |
|------|-----------|---------|
| Workflow run | workflow_id, user_id, start_time, status | Top-level trace |
| Each step | step_name, duration, status, input/output tokens | Step-level detail |
| LLM call | model, prompt_tokens, completion_tokens, latency | Cost and performance |
| Tool call | tool_name, input, output, duration, status | Tool reliability |
| Guardrail | guard_name, triggered, action_taken | Security monitoring |

Dashboards: per-run view (every step, duration, JSON input/output inspector); aggregate view (success rate, avg latency, cost per run, error rate); eval view (score per run, score over time, regression detection).

Tooling: LangSmith / Braintrust / custom for trace + eval dashboards; Grafana / Datadog for infra metrics; PagerDuty / OpsGenie for alerting on failure spikes.

## Composition

**Workflows as tools** — complex tasks become workflows; workflows become tools for agents. The agent decides WHICH workflow to run; the workflow ensures HOW it executes (structured, reliable).

**Agents as workflow steps** — agent calls become individual steps in a larger workflow. The workflow orchestrates the sequence; the agent handles the unstructured reasoning within a step.
