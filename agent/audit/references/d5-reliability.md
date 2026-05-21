# D5 — Human-in-the-Loop & Reliability

**Dimension:** Human-in-the-Loop & Reliability.
**Sources:** Patterns P4, P9 + Factors F7, F9 — all four merged.
**Criteria:** 4 (D5.1, D5.2, D5.4, D5.5).

This dimension judges how the agent involves humans at the right moments and how it
behaves when things go wrong — error feedback, graceful degradation, and
error-context hygiene over long runs.

> **There is intentionally no D5.3.** The retry-discipline concern is folded into
> D5.2's rubric (errors *and* capped retries are scored together). D5 has exactly
> four criteria.

> **Merge guards (this whole dimension carries them):**
> - **D5.1 = P4 ≈ F7.** One criterion. Score *both* approval gates *and* human
>   contact as a tool call. Do not score "contact humans" elsewhere.
> - **D5.2 = P9 ≈ F9.** One criterion. Score *both* errors looping back to the
>   model *and* compaction with retry limits.

---

## D5.1 — Human-in-the-loop checkpoints

**Maps to:** P4 (Human-in-the-Loop) ≈ F7 (Contact humans with tool calls) — merged.

**What good looks like:** High-stakes or irreversible actions pause for human
approval before executing. Crucially, contacting a human is modeled as **just
another tool call** — the agent calls e.g. `request_human_approval(...)`, the run
**pauses** cleanly, and **resumes** when the human responds. The agent is not
forced to be synchronous or to block a thread while waiting.

**Anchors:**
- **0** — No human checkpoints; the agent executes every action, including
  irreversible ones, autonomously.
- **1** — Some approval exists, but ad hoc — a hard-coded blocking prompt, no clean
  pause/resume; or checkpoints are missing on genuinely high-stakes actions.
- **2** — Approval gates cover the right actions; human contact is reasonably
  modeled but pause/resume is slightly awkward.
- **3** — Checkpoints gate exactly the high-stakes actions; human contact is a
  proper tool call; the run pauses and resumes cleanly around the human.

**N/A condition:** N/A only for an agent whose every action is provably low-stakes
and reversible (state this) — rare; justify it.

**Evidence to look for:** approval-gate logic, a `request_human_*` / `ask_human`
tool, pause/resume around human input, an escalation policy, which actions are
gated.

---

## D5.2 — Errors fed & compacted into context

**Maps to:** P9 (Feed Errors Into Context) ≈ F9 (Compact errors into context) —
merged. **Retry discipline lives here** (the absent D5.3).

**What good looks like:** When a tool call or step fails, the error is fed **back
into the model's context** so it can adapt and self-heal — not swallowed silently
or surfaced only to a human. The error is **compacted** — a concise summary, not a
raw 500-line stack trace — and retries are **capped**: after N failed attempts the
agent stops looping and escalates rather than burning context on the same error.

**Anchors:**
- **0** — Errors are swallowed or crash the run; nothing goes back to the model; no
  retry limit (or infinite retry loops).
- **1** — Errors reach the model but raw and unbounded; retries uncapped or absent.
- **2** — Errors are fed back and retries are capped; error messages are only
  loosely compacted.
- **3** — Errors are compacted into concise, actionable context; retries are capped
  with escalation on exhaustion; the agent demonstrably self-heals from transient
  failures.

**N/A condition:** Never N/A — every agent encounters errors.

**Evidence to look for:** try/catch that re-injects errors into the prompt, error
summarization, a retry counter / `maxRetries`, escalation-on-exhaustion logic,
error-into-context formatting.

---

## D5.4 — Graceful degradation / fallback paths

**Maps to:** the escalation aspect of P4 / F7.

**What good looks like:** When the agent cannot complete a task — a tool is down, a
guardrail blocks, retries are exhausted, confidence is low — it degrades
gracefully: a defined fallback path, a safe partial result, or a clean escalation
to a human or a simpler deterministic flow. It never fails silently and never
fabricates a result to appear successful.

**Anchors:**
- **0** — No fallback. Failure means a crash, a hang, or a fabricated/wrong answer
  presented as success.
- **1** — Some failures are handled, but many paths have no defined fallback.
- **2** — Most failure paths degrade gracefully; one or two gaps remain.
- **3** — Every significant failure path has a defined fallback — safe partial
  result, clean human escalation, or deterministic backup flow; failure is always
  explicit.

**N/A condition:** Never N/A.

**Evidence to look for:** fallback branches, default-safe responses, escalation
handlers, "if tool unavailable" paths, partial-result handling, circuit breakers.

---

## D5.5 — Error-context hygiene at scale

**Maps to:** P9 / F9 applied over **long-running** agents.

**What good looks like:** Over a long run with many failures, error context stays
hygienic — old/resolved errors are pruned, repeated errors are deduplicated, and
accumulated failure noise does not poison or crowd out the context. The agent does
not carry a growing pile of stale stack traces that degrade later reasoning.

**Anchors:**
- **0** — Errors accumulate unbounded; resolved errors stay in context forever;
  long runs drown in failure noise.
- **1** — Some pruning, but error context still grows noticeably over a long run.
- **2** — Error context is mostly kept clean; resolved errors are usually dropped;
  minor dedup gaps.
- **3** — Disciplined error-context hygiene — resolved errors pruned, repeats
  deduplicated, failure noise bounded; long runs stay clean.

**N/A condition:** N/A for a provably short single-shot agent that cannot
accumulate errors over time (state this).

**Evidence to look for:** error-pruning logic, dedup of repeated errors, how
resolved errors leave context, long-run context-size management, error-log
trimming.
