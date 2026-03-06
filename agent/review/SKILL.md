---
name: agent:review
description: Agent Pattern Review - validates an AI agent against all 22 patterns from "Patterns for Building AI Agents" with a scored checklist and recommendations
---

# Agent Pattern Review

Reviews an existing AI agent (or agent design) against all 22 patterns from "Patterns for Building AI Agents" (Bhagwat & Gienow, 2025). Produces a scored checklist with specific recommendations for improvement.

## When to use

Use this skill when the user needs to:
- Validate an existing agent against industry best practices
- Get a comprehensive health check of an agent system
- Identify the highest-impact improvements
- Prepare for production readiness

## Instructions

### Step 1: Gather Agent Information

Use the `AskUserQuestion` tool to understand what to review:
1. Is there a spec? (check `.specs/<spec-name>/`)
2. Is there agent code to analyze? (path to source)
3. Is this a design review (documents only) or implementation review (code + documents)?

Read all available materials:
- Spec documents: `agent-design.md`, `context-engineering.md`, `agent-eval.md`, `agent-security.md`
- Source code: agent definitions, tool implementations, prompt templates
- Configuration: model settings, guardrail configs, access policies

### Step 2: Score All 22 Patterns

For each pattern, assess the current state. Use this scoring:
- **N/A** — Not applicable to this agent
- **0 - Not Started** — Pattern not addressed
- **1 - Basic** — Partially addressed, significant gaps
- **2 - Good** — Mostly addressed, minor gaps
- **3 - Excellent** — Fully addressed, follows best practices

Evaluate using parallel sub-agents (`subagent_type: "Explore"`) where code analysis is needed.

### Step 3: Generate Review Report

```markdown
# Agent Pattern Review: [System Name]

**Date:** [Date]
**Scope:** [Design / Implementation / Both]
**Overall Score:** [X / 66] ([Y%])

---

## Part I: Configure Your Agents ([X/12])

| # | Pattern | Score | Evidence | Recommendation |
|---|---------|-------|----------|----------------|
| 1 | Whiteboard Agent Capabilities | [0-3] | [What exists] | [What to improve] |
| 2 | Evolve Your Agent Architecture | [0-3] | [What exists] | [What to improve] |
| 3 | Dynamic Agents | [0-3] | [What exists] | [What to improve] |
| 4 | Human-in-the-Loop | [0-3] | [What exists] | [What to improve] |

## Part II: Engineer Agent Context ([X/15])

| # | Pattern | Score | Evidence | Recommendation |
|---|---------|-------|----------|----------------|
| 5 | Parallelize Carefully | [0-3] | [What exists] | [What to improve] |
| 6 | Share Context Between Subagents | [0-3] | [What exists] | [What to improve] |
| 7 | Avoid Context Failure Modes | [0-3] | [What exists] | [What to improve] |
| 8 | Compress Context | [0-3] | [What exists] | [What to improve] |
| 9 | Feed Errors Into Context | [0-3] | [What exists] | [What to improve] |

## Part III: Evaluate Agent Responses ([X/24])

| # | Pattern | Score | Evidence | Recommendation |
|---|---------|-------|----------|----------------|
| 10 | List Failure Modes | [0-3] | [What exists] | [What to improve] |
| 11 | List Critical Business Metrics | [0-3] | [What exists] | [What to improve] |
| 12 | Cross-Reference Failure Modes and Metrics | [0-3] | [What exists] | [What to improve] |
| 13 | Iterate Against Your Evals | [0-3] | [What exists] | [What to improve] |
| 14 | Create an Eval Test Suite | [0-3] | [What exists] | [What to improve] |
| 15 | Have SMEs Label Data | [0-3] | [What exists] | [What to improve] |
| 16 | Create Datasets from Production Data | [0-3] | [What exists] | [What to improve] |
| 17 | Evaluate Production Data | [0-3] | [What exists] | [What to improve] |

## Part IV: Secure Your Agents ([X/12])

| # | Pattern | Score | Evidence | Recommendation |
|---|---------|-------|----------|----------------|
| 18 | Prevent the Lethal Trifecta | [0-3] | [What exists] | [What to improve] |
| 19 | Sandbox Code Execution | [0-3] | [What exists] | [What to improve] |
| 20 | Granular Agent Access Control | [0-3] | [What exists] | [What to improve] |
| 21 | Agent Guardrails | [0-3] | [What exists] | [What to improve] |

## Part V: Future-Readiness ([X/3])

| # | Pattern | Score | Evidence | Recommendation |
|---|---------|-------|----------|----------------|
| 22 | What's Next (Simulations, Learning, Synthetic Evals) | [0-3] | [What exists] | [What to improve] |

---

## Score Summary

| Part | Score | Max | Percentage |
|------|-------|-----|-----------|
| I. Configure | [X] | 12 | [Y%] |
| II. Context | [X] | 15 | [Y%] |
| III. Evaluate | [X] | 24 | [Y%] |
| IV. Secure | [X] | 12 | [Y%] |
| V. Future | [X] | 3 | [Y%] |
| **Total** | **[X]** | **66** | **[Y%]** |

---

## Top 5 Recommendations

Ranked by impact and effort:

| # | Recommendation | Pattern | Impact | Effort | Priority |
|---|---------------|---------|--------|--------|----------|
| 1 | [Recommendation] | [Pattern #] | High | Low | P0 |
| 2 | [Recommendation] | [Pattern #] | High | Medium | P0 |
| 3 | [Recommendation] | [Pattern #] | Medium | Low | P1 |
| 4 | [Recommendation] | [Pattern #] | Medium | Medium | P1 |
| 5 | [Recommendation] | [Pattern #] | Medium | High | P2 |

---

## Maturity Assessment

| Level | Score Range | Description |
|-------|-----------|-------------|
| **Prototype** | 0-20% | Agent works but lacks production safeguards |
| **MVP** | 21-45% | Core patterns in place, gaps in eval and security |
| **Production-Ready** | 46-70% | Solid foundation, iterating on quality |
| **Mature** | 71-90% | Comprehensive coverage, continuous improvement |
| **Best-in-Class** | 91-100% | Industry-leading agent practices |

**Current maturity: [Level]**
```

### Step 4: Offer Next Steps

Use `AskUserQuestion` to offer targeted actions based on the weakest areas:
1. **Run `agent:design`** — if Part I scored low
2. **Run `agent:context`** — if Part II scored low
3. **Run `agent:eval`** — if Part III scored low
4. **Run `agent:secure`** — if Part IV scored low

## Arguments

- `<args>` - Optional spec name or path to agent code
  - `<spec-name>` — reviews agent from `.specs/<spec-name>/`
  - `<path>` — reviews agent code at the given path

Examples:
- `agent:review customer-support` — review the customer-support agent
- `agent:review src/agents/` — review agent code in the given directory
- `agent:review` — will ask what to review
