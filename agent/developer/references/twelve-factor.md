# Twelve-Factor Agents

Based on humanlayer/12-factor-agents (CC BY-SA 4.0).

Twelve principles for building reliable, production-grade agents. Each factor below states what it means and how to apply it while building.

## 1. Natural Language to Tool Calls

The core agent move is converting a natural-language request into a structured tool-call payload (typically JSON). Treat NL→structured-call as a discrete, testable transformation. Define the target schema first, then prompt the model to emit it; validate the JSON before acting.

## 2. Own your prompts

Prompts are first-class code, not a config string buried inside a framework. Keep prompt text in your repo where it can be reviewed, diffed, versioned, and tested. Avoid frameworks that hide the actual prompt behind abstractions — if you cannot see the exact tokens sent to the model, you cannot debug them.

## 3. Own your context window

Do not just append to the default message array and hope. Build the context window deliberately: custom serialization of state, explicit token budgeting, and your own choices about what to include, summarize, or drop. The context window is your highest-leverage surface — control it directly.

## 4. Tools are just structured outputs

A "tool call" is nothing more than JSON the LLM emits. The model does not execute anything — deterministic code reads that JSON and decides what to do. Keep the LLM's job (produce structured output) separate from execution (your code). This makes tool calls easy to log, test, and gate.

## 5. Unify execution state and business state

Keep execution state (current step, retry counts, pending calls) together with business state (the actual domain data) in one place. Minimize state that lives outside the context window. A single unified state object is easier to serialize, inspect, and resume than scattered state across systems.

## 6. Launch / Pause / Resume with simple APIs

An agent must be launchable, pausable, and resumable through simple APIs. Design these entry points from the start: a launch call that starts a run, a pause that persists state, a resume that picks up exactly where it stopped. This is what makes long-running and human-gated workflows possible.

## 7. Contact humans with tool calls

Reaching a human is just another tool call — not a special branch in your code. Model "ask a human", "request approval", or "escalate" as tools the agent can invoke. The agent emits the call; your infrastructure routes it to a person and returns their answer like any other tool result.

## 8. Own your control flow

Build your own agent loop instead of delegating it to a framework's opaque runner. Owning the loop lets you interrupt for tool calls and human input, insert checks between steps, and resume cleanly. You decide when to call the model, when to execute tools, and when to stop.

## 9. Compact errors into context window

When a tool fails, put a compact error summary into the context window so the agent can diagnose and self-heal on the next turn. Do not dump raw stack traces — distill the error to what is actionable. Cap retries so a failing agent does not loop forever; escalate after the cap.

## 10. Small, focused agents

Prefer small agents that each handle roughly 3-10 steps over one giant do-everything agent. Small scope keeps the context window manageable, makes behavior predictable, and makes each agent easy to test. Compose small agents rather than growing one large one.

## 11. Trigger from anywhere

Let agents be triggered from wherever users already are — Slack, email, webhooks, cron, CI events — not only a dedicated chat UI. Decouple the trigger source from the agent core so the same agent can be invoked through many channels. Meet users where they are.

## 12. Make your agent a stateless reducer

Model the agent as a pure function: `(state, event) → new state`. Given the same state and event, it produces the same result. Statelessness makes agents trivially testable, replayable, and horizontally scalable — all durable state lives in the passed-in state object, not inside the process.
