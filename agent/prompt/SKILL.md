---
name: agent:prompt
description: Prompt Engineering - guides through model selection, prompt writing, few-shot examples, and production prompt optimization
---

# Prompt Engineering

Guides the user through designing and optimizing prompts for AI agents. Based on "Principles of Building AI Agents" (Bhagwat & Gienow, 2025), Part I: Prompting a Large Language Model.

## When to use

Use this skill when the user needs to:
- Choose the right model and provider for their agent
- Write or improve system prompts and agent instructions
- Design few-shot examples for consistent output
- Optimize prompts for production (cost, quality, latency)
- Bootstrap a prompt from scratch using the seed crystal approach

## Instructions

### Step 1: Understand the Use Case

Use the `AskUserQuestion` tool to gather context:
1. What does the agent do? (task type: classification, generation, extraction, conversation, code, reasoning)
2. What is the expected input format? (free text, structured data, images, code)
3. What is the expected output format? (free text, JSON, code, decision)
4. What quality bar is needed? (prototype, internal tool, customer-facing, high-stakes)
5. What are the constraints? (latency, cost, context size)

### Step 2: Model Selection

Guide the user through model choice. Apply the principle: **start expensive, optimize later**.

Use `AskUserQuestion` to present options:

```markdown
## Model Selection Matrix

| Factor | Small/Fast | Medium | Large/Capable |
|--------|-----------|--------|---------------|
| **Use case** | Classification, routing, simple extraction | Conversation, summarization, tool calling | Complex reasoning, code gen, multi-step planning |
| **Latency** | < 500ms | 1-3s | 3-10s |
| **Cost** | $0.25-1/M tokens | $3-5/M tokens | $15-75/M tokens |
| **Examples** | Haiku, GPT-4o-mini, Gemini Flash | Sonnet, GPT-4o, Gemini Pro | Opus, o1/o3, Gemini Ultra |
```

**Key principles:**
- **Start hosted** — use cloud APIs (Anthropic, OpenAI, Google) even if you plan open-source later
- **Use model routing** — abstract the provider so you can swap models without rewriting code
- **Consider context windows** — if your use case needs large input (codebases, long documents), pick models with large context windows
- **Reasoning models** — best for complex analysis but need lots of context upfront (many-shot prompting); without good context they go off the rails

Output a recommendation:

```markdown
## Recommended Model

**Primary:** [Model] — [Why]
**Fallback:** [Model] — [For cost optimization / lower-stakes tasks]
**Context window:** [Size] — [Sufficient for X pages / Y tokens of input]
```

### Step 3: Prompt Architecture

Design the prompt structure. Every production prompt has these layers:

```markdown
## Prompt Architecture

### 1. System Prompt
[Agent identity, role, tone, constraints, persona]
- Sets characteristics and behavior boundaries
- Good for shaping tone; usually does not improve accuracy alone

### 2. Context Block
[Data the agent needs to do its job]
- Retrieved documents (RAG)
- User profile / session state
- Tool descriptions and schemas
- Use XML-like tags to structure: <context>, <user_data>, <documents>

### 3. Task Instructions
[What to do with the context]
- Step-by-step instructions
- Output format specification
- Edge case handling

### 4. Examples (Few-Shot)
[Input/output pairs showing desired behavior]
- Zero-shot: no examples (simplest, least control)
- Single-shot: one example (establishes format)
- Few-shot: 3-5 examples (most control, highest quality)

### 5. User Input
[The actual user message / query]
```

### Step 4: Write the System Prompt

Guide the user through writing each section. Use `AskUserQuestion` at each step.

**Seed Crystal Approach:** If the user is starting from scratch, offer to bootstrap:
1. Describe the agent's purpose in 2-3 sentences
2. Ask the target LLM to generate a v1 system prompt
3. Refine iteratively

**Formatting principles:**
- CAPITALIZATION adds weight to important words (use sparingly)
- XML-like tags help models parse structure: `<task>`, `<context>`, `<constraints>`, `<examples>`
- Be extremely specific — production prompts are long and detailed
- Include what the agent should NOT do (prohibitions prevent common failures)

Output a complete system prompt:

```markdown
## System Prompt

<system>
You are [role/identity].

## Your Task
[Clear description of what to do]

## Constraints
- [Constraint 1]
- [Constraint 2]
- NEVER [prohibition]

## Output Format
[Exact format specification]

## Examples

<example>
<input>[Example input]</input>
<output>[Example output]</output>
</example>

<example>
<input>[Another input]</input>
<output>[Another output]</output>
</example>
</system>
```

### Step 5: Design Few-Shot Examples

Help the user create high-quality examples. Use `AskUserQuestion` to gather real scenarios.

**Guidelines:**
- Cover the most common case first
- Include at least one edge case
- Show the exact output format you expect
- If the agent handles errors, show an error example
- 3-5 examples is the sweet spot (more = more control but higher cost)

```markdown
## Few-Shot Examples

| # | Input | Expected Output | Covers |
|---|-------|----------------|--------|
| 1 | [Common case] | [Ideal response] | Happy path |
| 2 | [Edge case] | [Correct handling] | Boundary condition |
| 3 | [Ambiguous input] | [Clarification response] | Uncertainty handling |
| 4 | [Error case] | [Graceful failure] | Error path |
```

### Step 6: Production Optimization

Review the prompt for production readiness:

```markdown
## Production Checklist

### Quality
- [ ] System prompt clearly defines agent identity and boundaries
- [ ] At least 3 few-shot examples covering common + edge cases
- [ ] Output format is unambiguous (JSON schema, structured template)
- [ ] Prohibitions prevent known failure modes
- [ ] Formatting uses XML tags for structure

### Cost
- [ ] Prompt tokens are minimized (no redundant instructions)
- [ ] Examples are concise but representative
- [ ] Context is filtered to what's relevant (not dumping everything)
- [ ] Consider using a smaller model for simple subtasks

### Latency
- [ ] Streaming is enabled for user-facing responses
- [ ] Long prompts are cached where supported
- [ ] Model size matches latency requirements

### Robustness
- [ ] Tested with adversarial inputs
- [ ] Tested with empty/minimal input
- [ ] Tested with very long input (near context limit)
- [ ] Output format holds across model temperature settings
```

### Step 7: Summarize and Offer Next Steps

Present all findings to the user as a structured summary in the conversation. Do NOT write to `.specs/` — this skill works directly.

Use `AskUserQuestion` to offer:
1. **Test the prompt** — try it with sample inputs right now
2. **Write the prompt to a file** — if the user wants to save it to their codebase
3. **Comprehensive design** — run `agent:design` to cover all areas with a spec

## Arguments

- `<args>` - Optional description of the agent or path to existing prompt file

Examples:
- `agent:prompt customer-support chatbot` — design prompts for a support chatbot
- `agent:prompt src/agents/writer.ts` — improve prompts in an existing agent file
- `agent:prompt` — start fresh
