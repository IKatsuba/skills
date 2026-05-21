# Agent Evaluation

How to define what "good" looks like and build an evaluation system for an agent.

## Failure-mode taxonomy

LLM outputs are nondeterministic — you need to understand not just WHAT fails, but WHY. Start from these common categories and add domain-specific ones:

| Category | Description | Example |
|---|---|---|
| **Data Quality** | Agent received wrong, incomplete, or ambiguous input | Missing fields, contradictory data |
| **Reasoning Failure** | Agent had correct data but drew wrong conclusions | Incorrect logic chain, hallucinated facts |
| **Rule Misapplication** | Agent misapplied domain-specific rules or policies | Wrong insurance code, incorrect legal precedent |
| **Tool Failure** | An external tool/API call failed or returned unexpected results | Timeout, wrong API response format |
| **Context Failure** | Agent lost track of important context | Forgot an earlier constraint, ignored a user correction |
| **Output Format** | Correct answer but wrong format or structure | Missing required fields, wrong data types |

Capture each failure mode with an ID, category, name, description, and severity (Critical / High / Medium / Low).

## Business metrics

Connect agent performance to business value across three categories:

1. **Accuracy metrics (baseline)** — false positive rate, false negative rate, overall accuracy / F1 score.
2. **Domain-specific outcome metrics** — what domain outcomes matter (missed critical terms in legal, dollar loss in finance, resolution time in support).
3. **Human team metrics** — how the equivalent human team performs; the target agent performance vs. that human baseline.

Identify the **north star metric** — the single most important metric. Record its current baseline (human or current-agent performance) and target.

## Cross-reference failure modes and metrics

Map which failure modes drive which metrics — this turns metrics into actionable work. For each failure mode record its north-star impact (HIGH/MEDIUM/LOW), other metrics affected, and a priority (P0/P1/P2).

**Improvement cycle:**
1. **SME review** — domain experts review agent outputs, classify failure modes.
2. **PM prioritization** — cross-reference metrics + failure modes, set the next target.
3. **Engineering** — experiment with fixes using failure-mode-specific datasets.
4. **Validation** — test against past production data, decide go/no-go.

## Eval test suite

Data sources, fastest-to-start first:
1. **Synthetic data** — use an LLM to generate test cases.
2. **Internal user data** — real data from internal testing.
3. **SME golden answers** — expert-created input/output pairs (highest quality).
4. **Production data** — real user interactions (most realistic, available later).

**Evaluation criteria** — weight each: e.g. Accuracy 40%, Completeness 25%, Relevance 20%, Format 15%. Each scored binary (pass/fail).

**Scoring recommendation:** use binary (pass/fail) or categorical (good/fair/poor) scoring. Avoid numerical scales (1-10) — LLMs are better at categorical than numerical judgment.

**Regression policy:** merge blocker = any change that drops overall accuracy below threshold; review required = any change that regresses accuracy by more than Y%; paired improvements = if a regression is necessary, pair it with offsetting improvements elsewhere.

**Test case template** — fields: `id`, `input`, `expected_output`, `failure_modes` (which modes this tests), `metadata` (source, date added, domain category).

## SME labeling

Subject-matter experts validate agent outputs.

**Labeling schema** — each review includes: an overall grade (Pass / Partial / Fail); category tags (failure mode IDs that apply); optional free-text subjective feedback.

**Labeling workflow:**
1. Agent generates output → logged to the observability tool.
2. Automated flags trigger review (guardrail violations, CI failures, low-confidence outputs).
3. Random sampling of unflagged outputs at a set sample rate.
4. SME reviews the full trace: user input → tool calls → reasoning → output.
5. SME labels using the schema.
6. Labels feed back into the eval test suite.

**Inter-rater reliability:** use 2+ annotators per data point; metric = Cohen's / Fleiss' Kappa; target > 0.7 (substantial agreement); weekly calibration sync to align on edge cases.

## Production-data pipeline

**Data collection:** an observability tool (LangSmith, Braintrust, custom); logged fields = input, output, tool calls, latency, token usage, model version; store datasets in a versioned store, not loose JSONL files.

**Live evaluation:** method = LLM-as-judge with a defined evaluation prompt; scoring binary/categorical; sample X% of production responses; frequency real-time / hourly / daily batch.

**Evaluation prompt** — give the judge the user input, the agent output, and the expected behavior; ask for a PASS/FAIL grade plus one sentence of reasoning.

**Dataset versioning:** version datasets when new failure modes are discovered or distribution shift is detected; store inputs, expected outputs, and metadata; review cadence weekly/monthly to check synthetic data still matches production reality.

**Feedback loop:** production data → SME review → new test cases → eval suite update → CI regression check.
