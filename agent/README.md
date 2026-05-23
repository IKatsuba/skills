# Agent Skills

Skills for designing, building, and auditing AI agent systems. Based on "Patterns
for Building AI Agents" and "Principles of Building AI Agents" (Bhagwat & Gienow,
2025), plus [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents)
(CC BY-SA 4.0).

## Two Skills

| Skill | Description |
|-------|-------------|
| [`agent:developer`](developer/) | Reference skill for designing and building AI agents — a thin router into focused knowledge files (architecture, prompting, tools, memory, context, workflows, RAG, multi-agent, evaluation, twelve-factor reliability). |
| [`agent:audit`](audit/) | Audits an existing agent against a merged framework — the 22 patterns + the 12 factors + security — and emits a scored maturity report across 7 dimensions / 35 criteria. |

## `agent:developer`

A reference skill modeled on the angular-developer pattern: the `SKILL.md` carries no
deep knowledge, it routes you to one of ten `references/` files, each loaded only when
needed.

- **Starting a new agent?** Read `references/architecture.md` first — it covers
  capability mapping and choosing an architecture (Single Agent, Router + Specialists,
  Coordinator + Workers, or Pipeline). That decision determines which other references
  matter.
- **Working on an existing agent?** Jump to the topic reference for the subsystem you
  are touching: `prompting`, `tools`, `memory`, `context`, `workflows`, `rag`,
  `multi-agent`, `evaluation`, or `twelve-factor`.

Each reference is dense, agent-readable knowledge — frameworks, decision trees,
matrices, and checklists — meant to be consulted *while* building.

## `agent:audit`

Audits an agent (or an agent design) against **7 dimensions / 35 criteria** that merge
two frameworks with overlaps deduplicated:

| Dim | Dimension | Sources |
|-----|-----------|---------|
| D1 | Architecture & Capability Design | P1–P3 + F10 |
| D2 | Control Flow & State | F5, F6, F8, F11, F12 |
| D3 | Context Engineering | P5–P8 + F3 |
| D4 | Tools & Interface Design | F1, F2, F4 (+ P3) |
| D5 | Human-in-the-Loop & Reliability | P4, P9 + F7, F9 |
| D6 | Evaluation & Observability | P10–P17 |
| D7 | Security | P18–P22 |

It fans out 7 parallel subagents (one per dimension, so each criterion is scored
exactly once), rolls the scores into an overall maturity band, applies a security
override gate, and writes a report.

```bash
/agent:audit my-agent          # audit the agent specced under .specs/my-agent/
/agent:audit src/agents/       # audit agent code at a path
/agent:audit                   # ask what to audit
```

The report is written to `.specs/<spec-name>/agent-audit.md` when a spec name is
known, otherwise to stdout, always with a compact stdout digest.

## Output Structure

```
.specs/
└── <agent-name>/
    └── agent-audit.md     # Scored audit report (from agent:audit)
```

## Installation

```bash
npx skills add ikatsuba/skills/agent
```

The CLI will prompt to pick which agent skills to install. For a single skill, use `npx skills add ikatsuba/skills --skill <name>`.
