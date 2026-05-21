# D3 — Context Engineering

**Dimension:** Context Engineering.
**Sources:** Patterns P5, P6, P7, P8 + Factor F3.
**Criteria:** 5 (D3.1–D3.5).

This dimension judges how the agent manages the contents of its context window —
parallel work done safely, context shared between subagents, failure modes
avoided, context compressed, and the window owned deliberately.

---

## D3.1 — Parallelization done safely

**Maps to:** P5 (Parallelize Carefully).

**What good looks like:** Subagents or tool calls run in parallel **only** when
their tasks are genuinely independent — read-only fan-out, non-overlapping writes.
Work with shared mutable state or ordering dependencies stays sequential. Parallel
results are merged deterministically, and there is no race or write conflict.

**Anchors:**
- **0** — Either no parallelism where it would obviously help, or reckless
  parallelism over interdependent tasks causing races / conflicting writes.
- **1** — Some parallelism, but independence is assumed rather than verified.
- **2** — Parallelism is mostly applied to independent work; merge logic is sound.
- **3** — Parallel vs sequential is a deliberate, justified choice per task;
  independence is verified; merges are deterministic and conflict-free.

**N/A condition:** N/A if the agent is strictly single-threaded with no subagents
or concurrent tool calls (state this).

**Evidence to look for:** `Promise.all` / fan-out code, subagent dispatch, parallel
tool-call handling, write-target analysis, result-merge logic.

---

## D3.2 — Context shared between subagents

**Maps to:** P6 (Share Context Between Subagents).

**What good looks like:** When work is split across subagents, each receives the
context it needs — relevant prior findings, shared constraints, the parent's goal —
via an explicit, structured hand-off. Subagents are not flying blind, nor are they
dumped the entire unfiltered transcript.

**Anchors:**
- **0** — Subagents get no shared context, or get the whole raw history with no
  curation.
- **1** — Context is passed, but ad hoc and often missing what the subagent needs.
- **2** — A structured hand-off exists; occasionally over- or under-shares.
- **3** — Deliberate, curated context hand-off — each subagent gets exactly the
  relevant slice, in a structured envelope.

**N/A condition:** N/A if the agent uses no subagents (state this).

**Evidence to look for:** subagent prompt construction, a hand-off / envelope
schema, how parent state is sliced for children, shared-context objects.

---

## D3.3 — Context failure modes avoided

**Maps to:** P7 (Avoid Context Failure Modes).

**What good looks like:** The agent actively guards against the known context
failure modes — **poisoning** (a hallucination or bad fact persisting in context),
**distraction** (irrelevant content crowding out the task), **confusion** (too many
tools/options muddying decisions), and **clash** (contradictory information in
context). There are mechanisms to detect or prevent each.

**Anchors:**
- **0** — No awareness of context failure modes; context grows unmanaged.
- **1** — Vague awareness; maybe a token cap, but no targeted mitigation.
- **2** — Two or three failure modes are actively mitigated.
- **3** — All four failure modes are explicitly considered, with concrete
  mitigations (validation of facts, relevance filtering, tool scoping, conflict
  resolution).

**N/A condition:** Never N/A.

**Evidence to look for:** context pruning/filtering logic, fact-validation steps,
relevance scoring, tool-set scoping, conflict-resolution or precedence rules,
design-doc notes on context risks.

---

## D3.4 — Context compressed / compacted

**Maps to:** P8 (Compress Context).

**What good looks like:** As a run grows, the agent compacts context — summarizing
older turns, dropping stale tool output, keeping a running condensed state — so the
window holds signal, not raw history. Compaction is triggered by a threshold and
preserves the information needed to continue.

**Anchors:**
- **0** — No compaction; context grows until it overflows or degrades.
- **1** — Crude truncation (drop oldest) with no summarization.
- **2** — Summarization-based compaction exists; triggering or fidelity is rough.
- **3** — Deliberate compaction strategy — threshold-triggered, summarizes while
  preserving decision-critical state, validated to not lose key facts.

**N/A condition:** N/A only for a provably short single-shot agent whose context
cannot approach the window limit (state this).

**Evidence to look for:** summarization calls, a compaction/condense function, a
token-threshold trigger, running-summary state, "compact"/"summarize" logic.

---

## D3.5 — Context window deliberately owned

**Maps to:** F3 (Own your context window).

**What good looks like:** The team builds the context window itself rather than
delegating it to a framework — custom serialization of state into the prompt,
explicit token budgeting per section (system / history / tools / task), and a
conscious decision about what occupies the window at each step. The window is
treated as a designed artifact.

**Anchors:**
- **0** — Context assembly is entirely framework-default; no token budgeting; the
  team cannot say what is in the window.
- **1** — Some custom assembly, but no explicit budgeting or section ownership.
- **2** — Custom serialization with rough token budgeting; mostly owned.
- **3** — Fully owned window — custom serialization, explicit per-section token
  budget, deliberate decisions about window contents at each step.

**N/A condition:** Never N/A.

**Evidence to look for:** custom prompt-assembly code, a token-budget config,
per-section context construction, serialization functions for state-into-prompt.

> **Merge guard:** D3.5 (F3) is the *owns-the-window discipline* — serialization
> and budgeting. D3.4 (P8) is *compaction*. They share intent but are scored
> separately on separate evidence. **Do not credit F3 under P8:** good compaction
> alone does not earn D3.5, and a budgeted window without compaction does not earn
> D3.4. Score each on its own evidence.
