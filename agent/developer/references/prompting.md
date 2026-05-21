# Prompt Engineering & Model Selection

How to pick a model and write production prompts for an agent.

## Model selection

Principle: **start expensive, optimize later.** Build with the most capable model, prove the task is solvable, then move down to cheaper models where quality holds.

| Factor | Small / Fast | Medium | Large / Capable |
|--------|-------------|--------|-----------------|
| **Use case** | Classification, routing, simple extraction | Conversation, summarization, tool calling | Complex reasoning, code gen, multi-step planning |
| **Latency** | < 500ms | 1-3s | 3-10s |
| **Cost** | $0.25-1/M tokens | $3-5/M tokens | $15-75/M tokens |
| **Examples** | Haiku, GPT-4o-mini, Gemini Flash | Sonnet, GPT-4o, Gemini Pro | Opus, o1/o3, Gemini Ultra |

Key principles:

- **Start hosted** — use cloud APIs (Anthropic, OpenAI, Google) even if you plan to self-host open-source models later.
- **Use model routing** — abstract the provider so a model can be swapped without rewriting code.
- **Consider context windows** — if the task needs large input (codebases, long documents), pick models with large context windows.
- **Reasoning models** — best for complex analysis but need lots of context upfront (many-shot prompting); without good context they go off the rails.

Output a recommendation with a **primary** model, a **fallback** (cheaper / lower-stakes), and a chosen **context window** size.

## Prompt architecture — five layers

Every production prompt is composed of these layers, in order:

1. **System prompt** — agent identity, role, tone, constraints, persona. Shapes behavior boundaries and tone; usually does not improve accuracy on its own.
2. **Context block** — data the agent needs: retrieved documents (RAG), user profile / session state, tool descriptions and schemas. Structure it with XML-like tags: `<context>`, `<user_data>`, `<documents>`.
3. **Task instructions** — step-by-step instructions, output-format specification, edge-case handling.
4. **Examples (few-shot)** — input/output pairs showing desired behavior.
5. **User input** — the actual user message / query.

## Seed-crystal bootstrapping

When starting a prompt from scratch:

1. Describe the agent's purpose in 2-3 sentences.
2. Ask the target LLM to generate a v1 system prompt from that description.
3. Refine iteratively against real inputs.

## Formatting principles

- CAPITALIZATION adds weight to important words — use sparingly.
- XML-like tags help models parse structure: `<task>`, `<context>`, `<constraints>`, `<examples>`.
- Be extremely specific — production prompts are long and detailed.
- Include what the agent should NOT do — explicit prohibitions prevent common failure modes.

## Few-shot examples

- Zero-shot: no examples — simplest, least control.
- Single-shot: one example — establishes format.
- Few-shot: 3-5 examples — most control, highest quality. This is the sweet spot.

Guidelines for writing examples:

- Cover the most common case first.
- Include at least one edge case / boundary condition.
- Show the exact output format expected.
- If the agent handles errors, include an error-path example.
- More examples = more control but higher token cost.

## Production checklist

**Quality**
- System prompt clearly defines agent identity and boundaries.
- At least 3 few-shot examples covering common + edge cases.
- Output format is unambiguous (JSON schema, structured template).
- Prohibitions prevent known failure modes.
- Formatting uses XML tags for structure.

**Cost**
- Prompt tokens minimized — no redundant instructions.
- Examples concise but representative.
- Context filtered to what is relevant — not dumping everything.
- Smaller model used for simple subtasks.

**Latency**
- Streaming enabled for user-facing responses.
- Long prompts cached where supported.
- Model size matches latency requirements.

**Robustness**
- Tested with adversarial inputs.
- Tested with empty / minimal input.
- Tested with very long input (near context limit).
- Output format holds across temperature settings.
