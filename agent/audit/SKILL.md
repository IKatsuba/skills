---
name: agent:audit
description: Agent Audit - audits an existing AI agent against the 22 patterns from "Patterns for Building AI Agents" and the 12 factors of production-reliable agents, emitting a scored maturity report with a security gate. Use when reviewing, scoring, or assessing the production-readiness of an AI agent or agent design.
argument-hint: "[spec-name|path]"
---

# Agent Audit

Audits an existing AI agent — or an agent design — against a **merged framework**:
the 22 patterns from *"Patterns for Building AI Agents"* (Bhagwat & Gienow, 2025)
and the 12 factors from [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents)
(licensed CC BY-SA 4.0). It produces a scored maturity report across **7 dimensions /
35 criteria**, with an expanded security block and a security override gate.

It folds a full 22-pattern review and a dedicated security audit into one unified,
deduplicated assessment.

## When to use

Use this skill when the user needs to:
- Validate an existing agent against industry best practices
- Get a comprehensive, deduplicated health check of an agent system
- Score production-readiness against both the patterns and the 12 factors
- Identify the highest-impact improvements and priority security actions
- Prepare an agent for production

## How it works

The audit covers **7 dimensions**, each owned by exactly one analysis subagent so
that every criterion is scored exactly once (no double-counting):

| Dim | Dimension | Sources | # criteria |
|-----|-----------|---------|------------|
| D1 | Architecture & Capability Design | P1,P2,P3 + F10 | 4 |
| D2 | Control Flow & State | F5,F6,F8,F11,F12 | 5 |
| D3 | Context Engineering | P5,P6,P7,P8 + F3 | 5 |
| D4 | Tools & Interface Design | F1,F2,F4 (+ P3 cross-ref) | 4 |
| D5 | Human-in-the-Loop & Reliability | P4,P9 + F7,F9 | 4 |
| D6 | Evaluation & Observability | P10–P17 | 8 |
| D7 | Security | P18–P22 | 5 |

D2 exists specifically because the 12 factors were merged in — control flow, state
unification, and triggering are the genuine gap in the 22 patterns. Four criteria
are explicit **overlap merges** (P4≈F7, P9≈F9, F3≈intent of P7+P8, F10≈result of
P1/P2); they are scored once. See `references/crosswalk.md` for the full mapping.

## Instructions

The orchestrator **never analyzes code itself** — it gathers scope, builds an
evidence pack, dispatches 7 parallel subagents, assembles their results, applies
the security gate, and writes the report.

### Step 1: Gather Scope

Use the `AskUserQuestion` tool to determine:
1. **Spec name** — is there a spec under `.specs/<spec-name>/`? (used for output path)
2. **Code path** — is there agent source code to analyze? (path to the agent)
3. **Audit type** — *design-only* (documents only) or *implementation* (code + documents)?

If `$ARGUMENTS` is provided, use it as the spec name or path and skip the questions
it already answers (see **Arguments** below).

### Step 2: Pre-Read & Build the Evidence Pack

Before dispatching subagents, the orchestrator reads what is available and assembles
a **shared evidence pack** — a concrete inventory of file paths and locations that
every subagent receives, so they do not each re-discover the codebase.

Read / locate:
- Spec documents: everything in `.specs/<spec-name>/` (e.g. `agent-design.md`,
  `context-engineering.md`, `agent-eval.md`, `agent-security.md`, `requirements.md`,
  `design.md`, prior `agent-audit.md`).
- Source code: agent definitions, the control-flow loop, tool implementations,
  prompt templates / prompt files, guardrail configs, access policy / IAM config,
  sandbox / container config, eval suites and test data.
- Configuration: model settings, observability wiring, CI integration.

Produce the evidence pack as a structured list, e.g.:

```
EVIDENCE PACK
- Agent design doc: .specs/foo/agent-design.md
- Control-flow loop: src/agent/loop.ts
- Tool definitions: src/agent/tools/*.ts (8 files)
- Prompt templates: prompts/system.md, prompts/planner.md
- Guardrails: src/guards/ (input.ts, output.ts)
- Access policy: infra/iam/agent-role.tf
- Sandbox config: docker/agent-sandbox.Dockerfile
- Eval suite: evals/ (12 cases) + CI job .github/workflows/eval.yml
- Observability: LangSmith wiring in src/agent/trace.ts
- No code found for: triggers, pause/resume APIs   ← design-only for D2
```

If no code exists for a dimension, note it — those criteria may return `N/A`.

### Step 3: Dispatch 7 Parallel Dimension Subagents

Launch **7 subagents in parallel**, each with `subagent_type: "Explore"`, one per
dimension. Each subagent prompt is a **fixed envelope** plus the dimension rubric.

The envelope (identical for all 7):

```
ROLE: You are a Dimension Auditor for an AI-agent audit. Audit ONLY the criteria
listed below. Do not score anything outside your dimension — other criteria are
owned by other auditors. Be evidence-based and skeptical: a score above 0 requires
a concrete artifact (file, code path, doc section). Absence of evidence is a 0,
not a guess.

SCOPE CONTEXT:
- Audit type: <design-only | implementation>
- Spec: <spec-name or "none">

EVIDENCE PACK:
<paste the Step 2 evidence pack verbatim>

SCORING:
- Per criterion score one of: N/A | 0 (Not Started) | 1 (Basic) | 2 (Good) | 3 (Excellent).
- N/A only when the criterion's stated N/A condition is met. N/A is excluded from
  both numerator and denominator.
- dimension_score = sum of non-N/A scores.
- dimension_max   = 3 × (count of non-N/A criteria).
- dimension_percent = round(100 × dimension_score / dimension_max).

OUTPUT CONTRACT — return exactly this structure:
{
  "dimension": "<Dx — name>",
  "criteria": [
    { "id": "Dx.y", "name": "...", "score": <N/A|0|1|2|3>,
      "evidence": "<concrete artifact or 'no evidence found'>",
      "recommendation": "<specific next action>" },
    ...
  ],
  "dimension_score": <int>,
  "dimension_max": <int>,
  "dimension_percent": <int>,
  "summary": "<exactly 2 sentences>"
}
(D7 ALSO returns: "risk_level": <Low|Medium|High|Critical>,
 "trifecta_status": <SAFE|AT RISK|VULNERABLE>.)

RUBRIC FOR YOUR DIMENSION:
<inline the full contents of references/d<N>-*.md here>
```

Inline the matching rubric file into each subagent's prompt:

| Subagent | Rubric file |
|----------|-------------|
| D1 | `references/d1-architecture.md` |
| D2 | `references/d2-control-flow.md` |
| D3 | `references/d3-context.md` |
| D4 | `references/d4-tools.md` |
| D5 | `references/d5-reliability.md` |
| D6 | `references/d6-evaluation.md` |
| D7 | `references/d7-security.md` |

Also read `references/scoring.md` and `references/crosswalk.md` yourself so you can
roll up correctly in Step 4.

### Step 4: Roll Up & Apply the Security Gate

Collect the 7 dimension blocks and compute, per `references/scoring.md`:
- **Overall score** = Σ `dimension_score`. **Overall max** = Σ `dimension_max`
  (theoretical ceiling 105 = 35×3; lower if any criterion is N/A).
- **Overall percent** = round(100 × overall_score / overall_max).
- **Maturity band** from the percent: Prototype 0–20% / MVP 21–45% /
  Production-Ready 46–70% / Mature 71–90% / Best-in-Class 91–100%.
- **Security risk** and **Lethal Trifecta status** = the D7 subagent's
  `risk_level` and `trifecta_status`.

**Security override gate:** if `trifecta_status` is `VULNERABLE`, OR any D7
criterion scored at a level its rubric flags as Critical, the **displayed** maturity
band is **capped at MVP**. Keep the raw percent visible, but show the band as
`MVP (capped)` and add the banner:
`Maturity capped — unresolved Critical security finding.`

### Step 5: Write the Report

Render the report using `references/report-template.md`. Write it to
`.specs/<spec-name>/agent-audit.md` when a spec name is known and a `.specs/`
directory exists; otherwise emit the full report to stdout.

Either way, also print a **compact stdout digest**: overall score + maturity band,
the 7-row dimension scorecard, security risk + trifecta status, and the top 3
recommendations.

### Step 6: Offer Next Steps

Use `AskUserQuestion` to offer actions targeting the weakest dimensions:
- **Fix the top P0 recommendation** — start with the highest-impact item.
- **Address a Priority Security Action** — if D7 surfaced Critical/High findings.
- **Run `agent:developer`** — to design or strengthen the agent (architecture,
  context, control flow, tools).
- **Re-audit** — run `agent:audit` again after changes land.

## Arguments

Parse `$ARGUMENTS` (`$0`):
- `<spec-name>` — audits the agent described in `.specs/<spec-name>/`; the report
  is written to `.specs/<spec-name>/agent-audit.md`.
- `<path>` — audits agent code at the given path (implementation audit).
- empty — use `AskUserQuestion` (Step 1) to gather scope.

Examples:
- `agent:audit customer-support` — audit the agent specced under `.specs/customer-support/`
- `agent:audit src/agents/` — audit the agent code in that directory
- `agent:audit` — ask what to audit

## References

Heavy rubric content lives in `references/` (loaded on demand):
- `crosswalk.md` — the 35-criterion → patterns/factors map, dimension model,
  N/A rules, and the 4 overlap-merge notes.
- `scoring.md` — the 0–3 scale, N/A handling, roll-up formulas, maturity bands,
  and the security override gate.
- `report-template.md` — the exact markdown skeleton of the report.
- `d1-architecture.md`, `d2-control-flow.md`, `d3-context.md`, `d4-tools.md`,
  `d5-reliability.md`, `d6-evaluation.md`, `d7-security.md` — the per-dimension
  scoring rubrics inlined into each subagent.
