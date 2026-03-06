---
name: agent:eval
description: Agent Evaluation System - designs failure modes, metrics, eval test suites, SME labeling, and production data evaluation pipelines
---

# Agent Evaluation System

Guides the user through building a comprehensive evaluation system for their AI agent. Applies patterns 10-17 from "Patterns for Building AI Agents" (Bhagwat & Gienow, 2025): failure mode taxonomy, business metrics, cross-referencing, iterating against evals, test suites, SME labeling, production datasets, and live evaluation.

## When to use

Use this skill when the user needs to:
- Define what "good" looks like for an AI agent
- Create a failure mode taxonomy
- Set up business metrics for agent performance
- Build an evaluation test suite
- Design SME labeling workflows
- Plan production data evaluation pipelines

## Instructions

### Step 1: Understand the Agent

Use the `AskUserQuestion` tool to gather context:
1. What does the agent do? (domain, tasks, outputs)
2. Who are the end users?
3. What are the consequences of wrong outputs? (low = inconvenience, high = financial/legal/safety)
4. Is there an existing agent design? (check `.specs/<spec-name>/`)
5. Do you have existing test data or production logs?

Read any existing spec documents before proceeding.

### Step 2: List Failure Modes (Pattern 10)

Build a classification of failure reasons. LLM outputs are nondeterministic — you need to understand not just WHAT fails, but WHY.

Use `AskUserQuestion` to explore failure categories with the user. Start with these common categories and adapt to the domain:

| Category | Description | Example |
|---|---|---|
| **Data Quality** | Agent received wrong, incomplete, or ambiguous input | Missing fields, contradictory data |
| **Reasoning Failure** | Agent had correct data but drew wrong conclusions | Incorrect logic chain, hallucinated facts |
| **Rule Misapplication** | Agent misapplied domain-specific rules or policies | Wrong insurance code, incorrect legal precedent |
| **Tool Failure** | External tool/API call failed or returned unexpected results | Timeout, wrong API response format |
| **Context Failure** | Agent lost track of important context | Forgot earlier constraint, ignored user correction |
| **Output Format** | Correct answer but wrong format or structure | Missing required fields, wrong data types |

Ask the user to identify domain-specific failure modes.

Output:

```markdown
## Failure Mode Taxonomy

| ID | Category | Failure Mode | Description | Severity |
|----|----------|-------------|-------------|----------|
| F1 | Reasoning | [Name] | [Description] | Critical / High / Medium / Low |
| F2 | Data Quality | [Name] | [Description] | Critical / High / Medium / Low |
| F3 | [Domain] | [Name] | [Description] | Critical / High / Medium / Low |
```

### Step 3: List Critical Business Metrics (Pattern 11)

Define metrics that connect agent performance to business value. Use `AskUserQuestion` to identify metrics in three categories:

**1. Accuracy metrics (baseline):**
- False positive rate
- False negative rate
- Overall accuracy / F1 score

**2. Domain-specific outcome metrics:**
- What domain-specific outcomes matter? (e.g., missed critical terms in legal, dollar loss in finance, resolution time in support)

**3. Human team metrics:**
- How does the equivalent human team perform?
- What is the target agent performance vs. human baseline?

Ask the user to identify the **north star metric** — the single most important metric.

Output:

```markdown
## Business Metrics

### North Star Metric
**[Metric name]:** [Description and why it matters most]
**Current baseline:** [Human performance or current agent performance]
**Target:** [Goal]

### Accuracy Metrics
| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| False positive rate | [X%] | [Y%] | [How measured] |
| False negative rate | [X%] | [Y%] | [How measured] |
| Overall accuracy | [X%] | [Y%] | [How measured] |

### Domain-Specific Metrics
| Metric | Current | Target | Business Impact |
|--------|---------|--------|----------------|
| [Metric 1] | [X] | [Y] | [Why it matters] |
| [Metric 2] | [X] | [Y] | [Why it matters] |
```

### Step 4: Cross-Reference Failure Modes and Metrics (Pattern 12)

Map which failure modes drive which metrics. This turns metrics into actionable improvement work.

```markdown
## Failure Mode → Metric Impact Matrix

| Failure Mode | North Star Impact | Other Metrics Affected | Priority |
|---|---|---|---|
| F1: [Name] | HIGH — directly causes [metric] regression | [Other metrics] | P0 |
| F2: [Name] | MEDIUM — contributes to [metric] | [Other metrics] | P1 |
| F3: [Name] | LOW — rare but severe | [Other metrics] | P2 |
```

**Define the improvement cycle:**

```markdown
## Improvement Cycle

1. **SME Review** — Domain experts review agent outputs, classify failure modes
2. **PM Prioritization** — Cross-reference metrics + failure modes, set next target
   - Current: [X%] → Next target: [Y%]
3. **Engineering** — Experiment with fixes using failure-mode-specific datasets
4. **Validation** — Test against past production data, decide go/no-go
```

### Step 5: Design Eval Test Suite (Pattern 13-14)

Help the user build an evaluation test suite.

Use `AskUserQuestion` to determine data sources:
1. **Synthetic data** — Use LLM to generate test cases (fastest to start)
2. **Internal user data** — Real data from internal testing
3. **SME golden answers** — Expert-created input/output pairs (highest quality)
4. **Production data** — Real user interactions (most realistic, available later)

**Test suite structure:**

```markdown
## Eval Test Suite

### Suite Metadata
- **Total test cases:** [N]
- **Data sources:** [Synthetic / Internal / SME / Production]
- **Evaluation method:** [LLM-as-judge / Exact match / Human review]
- **CI integration:** [Yes/No — run on every code change]

### Evaluation Criteria
| Criterion | Weight | Scoring | Description |
|-----------|--------|---------|-------------|
| Accuracy | 40% | Binary (pass/fail) | Factually correct output |
| Completeness | 25% | Binary | All required information present |
| Relevance | 20% | Binary | Focused on the user's actual question |
| Format | 15% | Binary | Correct structure and data types |

### Regression Policy
- **Merge blocker:** Any change that reduces overall accuracy below [X%]
- **Review required:** Any change that regresses accuracy by > [Y%]
- **Paired improvements:** If a regression in one area is necessary, pair with offsetting improvements elsewhere

### Test Case Template
| Field | Description |
|-------|-------------|
| `id` | Unique test case identifier |
| `input` | The user input / agent prompt |
| `expected_output` | The correct or ideal response |
| `failure_modes` | Which failure modes this tests (F1, F2, ...) |
| `metadata` | Source, date added, domain category |
```

**Scoring recommendation:** Use binary (pass/fail) or categorical (good/fair/poor) scoring. Avoid numerical scales (1-10) — LLMs are better at categorical than numerical judgment.

### Step 6: SME Labeling Plan (Pattern 15)

Design how subject matter experts will validate agent outputs.

Use `AskUserQuestion` to understand:
1. Who are the domain experts? (role, availability)
2. What tools will they use for labeling? (custom UI, spreadsheet, observability tool)
3. How many annotators per data point? (recommend 2+ for inter-rater reliability)

```markdown
## SME Labeling Plan

### Annotators
| Role | Count | Domain | Availability |
|------|-------|--------|-------------|
| [Role 1] | [N] | [Domain area] | [Hours/week] |

### Labeling Schema
Each review includes:
1. **Overall grade:** Pass / Partial / Fail
2. **Category tags:** [List of failure mode IDs that apply]
3. **Subjective feedback:** Free-text explanation (optional)

### Labeling Workflow
1. Agent generates output → logged to observability tool
2. Automated flags trigger review (guardrail violations, CI failures, low-confidence outputs)
3. Random sampling of unflagged outputs ([X%] sample rate)
4. SME reviews full trace: user input → tool calls → reasoning → output
5. SME labels using schema above
6. Labels feed back into eval test suite

### Inter-Rater Reliability
- Metric: Cohen's Kappa / Fleiss' Kappa
- Target: > 0.7 (substantial agreement)
- Calibration: Weekly sync to align on edge cases
```

### Step 7: Production Data Pipeline (Patterns 16-17)

Design how production data flows into the evaluation system.

```markdown
## Production Data Pipeline

### Data Collection
- **Observability tool:** [Tool name — e.g., LangSmith, Braintrust, custom]
- **Logged fields:** Input, output, tool calls, latency, token usage, model version
- **Storage:** [Where datasets are stored — not JSONL files, use versioned store]

### Live Evaluation
- **Method:** LLM-as-judge with defined evaluation prompt
- **Scoring:** [Binary / Categorical] — strongly recommended over numerical
- **Sampling:** Evaluate [X%] of production responses
- **Frequency:** [Real-time / Hourly / Daily batch]

### Evaluation Prompt Template
```
You are evaluating an AI agent's response.

**User input:** {input}
**Agent output:** {output}
**Expected behavior:** {criteria}

Grade the response as PASS or FAIL.
Explain your reasoning in one sentence.
```

### Dataset Versioning
- Version datasets when: new failure modes discovered, distribution shift detected
- Store: inputs, expected outputs, metadata (source, date, failure mode tags)
- Review cadence: [Weekly / Monthly] — check if synthetic data still matches production reality

### Feedback Loop
Production data → SME review → New test cases → Eval suite update → CI regression check
```

### Step 8: Generate Eval Document

Compile all outputs into `.specs/<spec-name>/agent-eval.md`.

### Step 9: Offer Next Steps

Use `AskUserQuestion` to offer:
1. **Create initial test cases** — generate synthetic eval data based on the failure modes
2. **Proceed to security audit** — run `agent:secure`
3. **Full review** — run `agent:review`

## Arguments

- `<args>` - Optional spec name
  - `<spec-name>` — reads existing agent design from `.specs/<spec-name>/`

Examples:
- `agent:eval customer-support` — design eval system for the customer-support agent
- `agent:eval` — start fresh, will ask for details
