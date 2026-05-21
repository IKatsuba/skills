# Report Template

The orchestrator renders the audit report from this skeleton. Replace every
`[bracketed]` placeholder. Write the rendered report to
`.specs/<spec-name>/agent-audit.md` when a spec name and a `.specs/` directory
exist; otherwise emit it to stdout.

````markdown
# Agent Audit: [System Name]

**Date:** [YYYY-MM-DD]
**Scope:** [design-only | implementation] - [spec name or code path]
**Overall Score:** [X] / [Y] ([Z]%)
**Maturity:** [Band]    <!-- if capped, write: MVP (capped) -->
**Security Risk:** [Low | Medium | High | Critical]
**Lethal Trifecta:** [SAFE | AT RISK | VULNERABLE]

<!-- Include the next line ONLY when the security gate fired: -->
> **Maturity capped - unresolved Critical security finding.**

---

## Executive Summary

[3-6 sentences: the agent's overall state, its strongest dimension, its weakest
dimension, the headline security finding, and the single most important next step.]

---

## Dimension Scorecard

| Dim | Dimension | Score | Max | % | Band |
|-----|-----------|-------|-----|---|------|
| D1 | Architecture & Capability Design | [x] | [m] | [p]% | [band] |
| D2 | Control Flow & State | [x] | [m] | [p]% | [band] |
| D3 | Context Engineering | [x] | [m] | [p]% | [band] |
| D4 | Tools & Interface Design | [x] | [m] | [p]% | [band] |
| D5 | Human-in-the-Loop & Reliability | [x] | [m] | [p]% | [band] |
| D6 | Evaluation & Observability | [x] | [m] | [p]% | [band] |
| D7 | Security | [x] | [m] | [p]% | [band] |
| | **Total** | **[X]** | **[Y]** | **[Z]%** | **[Maturity]** |

---

## D1 - Architecture & Capability Design

[2-sentence dimension summary.]

| ID | Criterion | Score | Evidence | Recommendation |
|----|-----------|-------|----------|----------------|
| D1.1 | Capabilities whiteboarded & bounded | [s] | [evidence] | [rec] |
| D1.2 | Architecture evolves from simple | [s] | [evidence] | [rec] |
| D1.3 | Dynamic vs static agent choice | [s] | [evidence] | [rec] |
| D1.4 | Small, focused, single-purpose agents | [s] | [evidence] | [rec] |

## D2 - Control Flow & State

[2-sentence dimension summary.]

| ID | Criterion | Score | Evidence | Recommendation |
|----|-----------|-------|----------|----------------|
| D2.1 | Explicit control flow / own the loop | [s] | [evidence] | [rec] |
| D2.2 | Unified execution + business state | [s] | [evidence] | [rec] |
| D2.3 | Stateless reducer design | [s] | [evidence] | [rec] |
| D2.4 | Launch / pause / resume APIs | [s] | [evidence] | [rec] |
| D2.5 | Triggerable from anywhere | [s] | [evidence] | [rec] |

## D3 - Context Engineering

[2-sentence dimension summary.]

| ID | Criterion | Score | Evidence | Recommendation |
|----|-----------|-------|----------|----------------|
| D3.1 | Parallelization done safely | [s] | [evidence] | [rec] |
| D3.2 | Context shared between subagents | [s] | [evidence] | [rec] |
| D3.3 | Context failure modes avoided | [s] | [evidence] | [rec] |
| D3.4 | Context compressed / compacted | [s] | [evidence] | [rec] |
| D3.5 | Context window deliberately owned | [s] | [evidence] | [rec] |

## D4 - Tools & Interface Design

[2-sentence dimension summary.]

| ID | Criterion | Score | Evidence | Recommendation |
|----|-----------|-------|----------|----------------|
| D4.1 | NL -> structured tool calls | [s] | [evidence] | [rec] |
| D4.2 | Prompts owned / versioned / first-class | [s] | [evidence] | [rec] |
| D4.3 | Tools are structured outputs / schemas | [s] | [evidence] | [rec] |
| D4.4 | Tool-surface health - scoped tool-set | [s] | [evidence] | [rec] |

## D5 - Human-in-the-Loop & Reliability

[2-sentence dimension summary.]

| ID | Criterion | Score | Evidence | Recommendation |
|----|-----------|-------|----------|----------------|
| D5.1 | Human-in-the-loop checkpoints | [s] | [evidence] | [rec] |
| D5.2 | Errors fed & compacted into context | [s] | [evidence] | [rec] |
| D5.4 | Graceful degradation / fallback paths | [s] | [evidence] | [rec] |
| D5.5 | Error-context hygiene at scale | [s] | [evidence] | [rec] |

<!-- D5 has no D5.3 by design - retry discipline is folded into D5.2. -->

## D6 - Evaluation & Observability

[2-sentence dimension summary.]

| ID | Criterion | Score | Evidence | Recommendation |
|----|-----------|-------|----------|----------------|
| D6.1 | Failure modes enumerated | [s] | [evidence] | [rec] |
| D6.2 | Critical business metrics defined | [s] | [evidence] | [rec] |
| D6.3 | Failure modes <-> metrics cross-referenced | [s] | [evidence] | [rec] |
| D6.4 | Iterating against evals | [s] | [evidence] | [rec] |
| D6.5 | Eval test suite exists | [s] | [evidence] | [rec] |
| D6.6 | SMEs label data | [s] | [evidence] | [rec] |
| D6.7 | Datasets from production data | [s] | [evidence] | [rec] |
| D6.8 | Production data evaluated live | [s] | [evidence] | [rec] |

## D7 - Security

[2-sentence dimension summary.]

| ID | Criterion | Score | Evidence | Recommendation |
|----|-----------|-------|----------|----------------|
| D7.1 | Lethal trifecta prevented | [s] | [evidence] | [rec] |
| D7.2 | Code execution sandboxed | [s] | [evidence] | [rec] |
| D7.3 | Granular access control | [s] | [evidence] | [rec] |
| D7.4 | Input / output guardrails | [s] | [evidence] | [rec] |
| D7.5 | Future-readiness / adversarial outlook | [s] | [evidence] | [rec] |

### Lethal Trifecta Analysis

**Leg 1 - Private Data Access:** [present? what data] - Risk: [None/Low/Medium/High]
**Leg 2 - Untrusted Content Exposure:** [present? what input] - Risk: [None/Low/Medium/High]
**Leg 3 - Exfiltration Capability:** [present? what channel] - Risk: [None/Low/Medium/High]

**Trifecta Status:** [SAFE | AT RISK | VULNERABLE]
[If VULNERABLE - which leg is cheapest to remove and how.]

### Sandbox Assessment

[Does the agent execute code? If yes: isolation, network policy, filesystem,
resource limits, credential exposure. If no: state "N/A - no code execution".]

| Threat | Risk | Mitigation |
|--------|------|-----------|
| Secret exfiltration | [risk] | [mitigation] |
| Environment destruction | [risk] | [mitigation] |
| Resource abuse | [risk] | [mitigation] |

### Access Control Review

[Authentication: own identity, OAuth, scoped/short-lived credentials.
Authorization: least-privilege per tool. Permission modes: planning vs execution.
Just-in-time access.]

| Tool / Action | Current Access | Recommended Access | Justification |
|---|---|---|---|
| [tool] | [current] | [recommended] | [why] |

### Guardrails

**Input guardrails** (before the LLM): [prompt-injection, jailbreak, PII, off-topic].
**Output guardrails** (before user/tools): [data leakage, hallucination, toxicity,
format validation, action validation].

| Guard | Layer | Present? | Action on Trigger |
|-------|-------|----------|-------------------|
| [guard] | input/output | [yes/no] | [action] |

---

## Framework Coverage Crosswalk

Each criterion with its score, so coverage of both source frameworks is visible.

| ID | Criterion | Patterns | Factors | Score |
|----|-----------|----------|---------|-------|
| D1.1 | Capabilities whiteboarded & bounded | P1 | - | [s] |
| D1.2 | Architecture evolves from simple | P2 | - | [s] |
| D1.3 | Dynamic vs static agent choice | P3 | - | [s] |
| D1.4 | Small, focused, single-purpose agents | - | F10 | [s] |
| D2.1 | Explicit control flow / own the loop | - | F8 | [s] |
| D2.2 | Unified execution + business state | - | F5 | [s] |
| D2.3 | Stateless reducer design | - | F12 | [s] |
| D2.4 | Launch / pause / resume APIs | - | F6 | [s] |
| D2.5 | Triggerable from anywhere | - | F11 | [s] |
| D3.1 | Parallelization done safely | P5 | - | [s] |
| D3.2 | Context shared between subagents | P6 | - | [s] |
| D3.3 | Context failure modes avoided | P7 | - | [s] |
| D3.4 | Context compressed / compacted | P8 | - | [s] |
| D3.5 | Context window deliberately owned | - | F3 | [s] |
| D4.1 | NL -> structured tool calls | - | F1 | [s] |
| D4.2 | Prompts owned / versioned / first-class | - | F2 | [s] |
| D4.3 | Tools are structured outputs / schemas | - | F4 | [s] |
| D4.4 | Tool-surface health - scoped tool-set | P3 (xref) | - | [s] |
| D5.1 | Human-in-the-loop checkpoints | P4 | F7 | [s] |
| D5.2 | Errors fed & compacted into context | P9 | F9 | [s] |
| D5.4 | Graceful degradation / fallback paths | P4 | F7 | [s] |
| D5.5 | Error-context hygiene at scale | P9 | F9 | [s] |
| D6.1 | Failure modes enumerated | P10 | - | [s] |
| D6.2 | Critical business metrics defined | P11 | - | [s] |
| D6.3 | Failure modes <-> metrics cross-referenced | P12 | - | [s] |
| D6.4 | Iterating against evals | P13 | - | [s] |
| D6.5 | Eval test suite exists | P14 | - | [s] |
| D6.6 | SMEs label data | P15 | - | [s] |
| D6.7 | Datasets from production data | P16 | - | [s] |
| D6.8 | Production data evaluated live | P17 | - | [s] |
| D7.1 | Lethal trifecta prevented | P18 | - | [s] |
| D7.2 | Code execution sandboxed | P19 | - | [s] |
| D7.3 | Granular access control | P20 | - | [s] |
| D7.4 | Input / output guardrails | P21 | - | [s] |
| D7.5 | Future-readiness / adversarial outlook | P22 | - | [s] |

---

## Top Recommendations

Ranked by impact and effort.

| # | Recommendation | Criterion | Impact | Effort | Priority |
|---|----------------|-----------|--------|--------|----------|
| 1 | [recommendation] | [Dx.y] | High | Low | P0 |
| 2 | [recommendation] | [Dx.y] | High | Medium | P0 |
| 3 | [recommendation] | [Dx.y] | Medium | Low | P1 |
| 4 | [recommendation] | [Dx.y] | Medium | Medium | P1 |
| 5 | [recommendation] | [Dx.y] | Medium | High | P2 |

---

## Priority Security Actions

| # | Action | Criterion | Severity | Effort |
|---|--------|-----------|----------|--------|
| 1 | [action] | [D7.y] | Critical | [Low/Med/High] |
| 2 | [action] | [D7.y] | High | [Low/Med/High] |

[If D7 surfaced no Critical/High findings, state: "No priority security actions -
D7 findings are Medium or below."]

---

## Maturity Assessment

**Current maturity: [Band]** ([Z]%)
<!-- If capped: "Current maturity: MVP (capped) - true score [Z]%." -->

| Band | Range | Description |
|------|-------|-------------|
| Prototype | 0-20% | Agent works but lacks production safeguards. |
| MVP | 21-45% | Core patterns in place; gaps in eval and security. |
| Production-Ready | 46-70% | Solid foundation; iterating on quality. |
| Mature | 71-90% | Comprehensive coverage; continuous improvement. |
| Best-in-Class | 91-100% | Industry-leading agent practices. |

[1-3 sentences: what would move the agent to the next band, and - if capped -
exactly what must be resolved to lift the cap.]
````
