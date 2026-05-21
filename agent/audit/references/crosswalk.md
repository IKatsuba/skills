# Framework Crosswalk

The audit merges two frameworks into one deduplicated model:

- **The 22 patterns** — *"Patterns for Building AI Agents"* (Bhagwat & Gienow, 2025).
- **The 12 factors** — [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents),
  licensed CC BY-SA 4.0.

The merged model has **7 dimensions** and **35 scored criteria**. Each dimension is
owned by exactly one analysis subagent, and each criterion is scored exactly once.

## Dimension model

| Dim | Dimension | Patterns | Factors | # criteria |
|-----|-----------|----------|---------|------------|
| D1 | Architecture & Capability Design | P1, P2, P3 | F10 | 4 |
| D2 | Control Flow & State | — | F5, F6, F8, F11, F12 | 5 |
| D3 | Context Engineering | P5, P6, P7, P8 | F3 | 5 |
| D4 | Tools & Interface Design | (P3 cross-ref) | F1, F2, F4 | 4 |
| D5 | Human-in-the-Loop & Reliability | P4, P9 | F7, F9 | 4 |
| D6 | Evaluation & Observability | P10–P17 | — | 8 |
| D7 | Security | P18–P22 | — | 5 |
| | **Total** | | | **35** |

D2 exists purely because the 12 factors were added. Control flow, unified state, and
triggering are the genuine gap in the 22 patterns — D2 closes it.

## The 35 criteria

| ID | Name | Patterns | Factors |
|----|------|----------|---------|
| D1.1 | Capabilities whiteboarded & bounded | P1 | — |
| D1.2 | Architecture evolves from simple | P2 | — |
| D1.3 | Dynamic vs static agent choice | P3 | — |
| D1.4 | Small, focused, single-purpose agents | — | F10 |
| D2.1 | Explicit control flow / own the loop | — | F8 |
| D2.2 | Unified execution + business state | — | F5 |
| D2.3 | Stateless reducer design | — | F12 |
| D2.4 | Launch / pause / resume APIs | — | F6 |
| D2.5 | Triggerable from anywhere | — | F11 |
| D3.1 | Parallelization done safely | P5 | — |
| D3.2 | Context shared between subagents | P6 | — |
| D3.3 | Context failure modes avoided | P7 | — |
| D3.4 | Context compressed / compacted | P8 | — |
| D3.5 | Context window deliberately owned | — | F3 |
| D4.1 | NL → structured tool calls | — | F1 |
| D4.2 | Prompts owned / versioned / first-class | — | F2 |
| D4.3 | Tools are structured outputs / schemas | — | F4 |
| D4.4 | Tool-surface health — scoped tool-set | P3 (cross-ref) | — |
| D5.1 | Human-in-the-loop checkpoints | P4 | F7 |
| D5.2 | Errors fed & compacted into context | P9 | F9 |
| D5.4 | Graceful degradation / fallback paths | P4 (escalation) | F7 |
| D5.5 | Error-context hygiene at scale | P9 | F9 |
| D6.1 | Failure modes enumerated | P10 | — |
| D6.2 | Critical business metrics defined | P11 | — |
| D6.3 | Failure modes ↔ metrics cross-referenced | P12 | — |
| D6.4 | Iterating against evals | P13 | — |
| D6.5 | Eval test suite exists | P14 | — |
| D6.6 | SMEs label data | P15 | — |
| D6.7 | Datasets from production data | P16 | — |
| D6.8 | Production data evaluated live | P17 | — |
| D7.1 | Lethal trifecta prevented | P18 | — |
| D7.2 | Code execution sandboxed | P19 | — |
| D7.3 | Granular access control | P20 | — |
| D7.4 | Input / output guardrails | P21 | — |
| D7.5 | Future-readiness / adversarial outlook | P22 | — |

> **Note on D5 numbering:** there is intentionally **no D5.3**. The retry-discipline
> concern is folded into D5.2's rubric (errors + capped retries are scored together),
> not separately scored. D5 has 4 criteria: D5.1, D5.2, D5.4, D5.5.

## Pattern reference (22)

P1 Whiteboard Agent Capabilities · P2 Evolve Your Agent Architecture ·
P3 Dynamic Agents · P4 Human-in-the-Loop · P5 Parallelize Carefully ·
P6 Share Context Between Subagents · P7 Avoid Context Failure Modes ·
P8 Compress Context · P9 Feed Errors Into Context · P10 List Failure Modes ·
P11 List Critical Business Metrics · P12 Cross-Reference Failure Modes and Metrics ·
P13 Iterate Against Your Evals · P14 Create an Eval Test Suite ·
P15 Have SMEs Label Data · P16 Create Datasets from Production Data ·
P17 Evaluate Production Data · P18 Prevent the Lethal Trifecta ·
P19 Sandbox Code Execution · P20 Granular Agent Access Control ·
P21 Agent Guardrails · P22 What's Next.

## Factor reference (12)

F1 Natural Language to Tool Calls · F2 Own your prompts ·
F3 Own your context window · F4 Tools are structured outputs ·
F5 Unify execution state and business state ·
F6 Launch/Pause/Resume with simple APIs ·
F7 Contact humans with tool calls · F8 Own your control flow ·
F9 Compact errors into context window · F10 Small focused agents ·
F11 Trigger from anywhere · F12 Stateless reducer.

## N/A rules

- A criterion is `N/A` only when its rubric's stated N/A condition is met
  (e.g. D7.2 is N/A if the agent provably executes no code).
- `N/A` is excluded from **both** numerator and denominator — it does not count
  for or against the score.
- **Design-only audits:** D2 and D4 criteria that cannot be evidenced by design
  documents alone (e.g. an actual pause/resume API, a real tool schema) may return
  `N/A`. Do not infer an implementation score from intent stated in a design doc.

## Overlap-merge notes (scored once — never double-counted)

No-double-counting is **structural**: each subagent receives only its own
dimension's criteria, so a concept owned by one criterion cannot be re-scored by
another. The four explicit merges:

1. **D5.1 = P4 ≈ F7** (human-in-the-loop). One criterion. Its rubric checks *both*
   that approval gates exist *and* that human contact is modeled as a tool call
   that pauses/resumes cleanly. Do not also score "contact humans" anywhere else.

2. **D5.2 = P9 ≈ F9** (errors into context). One criterion. Its rubric checks *both*
   that errors loop back to the model *and* that they are compacted/summarized with
   retry limits. The retry-discipline concern lives here — there is no separate D5.3.

3. **D3.5 = F3 ≈ intent of P7 + P8.** F3 ("own your context window") is scored as the
   *owns-the-window discipline* — custom serialization, explicit token budgeting.
   **Merge guard:** do not also credit F3 under P8 (D3.4 scores compaction;
   D3.5 scores deliberate ownership of the whole window). Score each on its own
   evidence.

4. **D1.4 = F10 ≈ scoping result of P1 / P2.** Kept distinct on purpose:
   D1.1 and D1.2 score the *process* (whiteboarding, evolving from simple).
   D1.4 scores the *result* (agent size, step count, blast radius). A team can
   whiteboard well (high D1.1) yet still ship one bloated agent (low D1.4).

5. **D4.4 cross-references P3 but does not re-score it.** P3 (dynamic vs static
   agent choice) is scored once, at **D1.3**. D4.4 reads D1.3's finding to judge
   tool-surface health (is the tool-set scoped to what the agent actually needs?),
   but assigns its own independent score for the tool surface.
