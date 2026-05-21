# D6 — Evaluation & Observability

**Dimension:** Evaluation & Observability.
**Sources:** Patterns P10–P17 (no factors).
**Criteria:** 8 (D6.1–D6.8).

This dimension judges the agent's evaluation system — the discipline of knowing
what "good" means, measuring it, and improving against it.

**Eval taxonomy primer (shared across D6 criteria):**

- **Failure modes** — *why* outputs go wrong. Common categories: Data Quality
  (wrong/incomplete/ambiguous input), Reasoning Failure (correct data, wrong
  conclusion), Rule Misapplication (domain rule applied incorrectly), Tool Failure
  (API timeout / bad response), Context Failure (lost track of a constraint),
  Output Format (right answer, wrong shape).
- **Business metrics** — accuracy metrics (false-positive/negative rate, F1),
  domain-specific outcome metrics, human-team baseline, and one **north-star**
  metric.
- **Eval data sources** — synthetic (LLM-generated, fastest), internal user data,
  SME golden answers (highest quality), production data (most realistic).
- **Scoring** — prefer binary (pass/fail) or categorical (good/fair/poor); avoid
  numerical 1–10 scales — LLMs judge categorically better than numerically.
- **The improvement cycle** — SME review → PM prioritization (metrics × failure
  modes) → engineering experiments on failure-mode datasets → validation against
  past production data.

---

## D6.1 — Failure modes enumerated

**Maps to:** P10 (List Failure Modes).

**What good looks like:** A documented failure-mode taxonomy — each mode has an ID,
category, description, and severity. It covers the common categories above plus
domain-specific modes. The team knows *why* the agent fails, not just *that* it does.

**Anchors:**
- **0** — No failure-mode list; failures are anecdotal.
- **1** — A few failure modes noted informally; no taxonomy or severity.
- **2** — A real taxonomy exists; coverage of domain-specific modes is partial.
- **3** — Comprehensive, categorized, severity-rated taxonomy covering common and
  domain-specific modes; kept current.

**N/A condition:** Never N/A.
**Evidence to look for:** an `agent-eval.md` failure-mode table, a taxonomy doc,
failure categories in tests or issue labels.

---

## D6.2 — Critical business metrics defined

**Maps to:** P11 (List Critical Business Metrics).

**What good looks like:** Metrics connect agent performance to business value —
accuracy metrics, domain-specific outcome metrics, a human-team baseline, and a
single named **north-star** metric with current value and target.

**Anchors:**
- **0** — No metrics; "it seems to work" is the bar.
- **1** — Some accuracy metrics; no north star, no business linkage.
- **2** — A solid metric set including domain metrics; north star or targets partial.
- **3** — Full metric set with a named north star, baseline, and targets; metrics
  tie clearly to business value.

**N/A condition:** Never N/A.
**Evidence to look for:** a metrics section, a north-star definition, baseline vs
target tables, dashboards.

---

## D6.3 — Failure modes ↔ metrics cross-referenced

**Maps to:** P12 (Cross-Reference Failure Modes and Metrics).

**What good looks like:** A matrix maps which failure modes drive which metrics, so
improvement work is prioritized by metric impact. Failure modes and metrics are not
two disconnected lists.

**Anchors:**
- **0** — Failure modes and metrics exist (if at all) as unconnected lists.
- **1** — Some informal linkage; no systematic matrix.
- **2** — A cross-reference matrix exists; prioritization is partial.
- **3** — Complete failure-mode → metric-impact matrix driving a documented
  prioritization (P0/P1/P2).

**N/A condition:** N/A only if D6.1 and D6.2 are both effectively absent (nothing to
cross-reference) — state this.
**Evidence to look for:** an impact matrix, priority rankings tied to metrics, a
documented improvement cycle.

---

## D6.4 — Iterating against evals

**Maps to:** P13 (Iterate Against Your Evals).

**What good looks like:** Evals drive development — changes are validated against
the eval suite, regressions block merges, and there is a defined improvement loop.
Evals are run routinely, not written once and abandoned.

**Anchors:**
- **0** — Evals (if any) never run; changes ship on vibes.
- **1** — Evals run occasionally, manually; no regression policy.
- **2** — Evals run regularly; a regression policy exists but is loosely enforced.
- **3** — Evals are the development loop — run on every change, enforced regression
  gates, paired-improvement discipline.

**N/A condition:** N/A only if no eval suite exists at all (then D6.5 captures it).
**Evidence to look for:** CI eval jobs, a regression policy, eval-driven change
history, merge gates.

---

## D6.5 — Eval test suite exists

**Maps to:** P14 (Create an Eval Test Suite).

**What good looks like:** A real eval test suite — test cases with `id`, `input`,
`expected_output`, `failure_modes`, `metadata`; defined evaluation criteria with
weights; binary/categorical scoring; ideally CI-integrated.

**Anchors:**
- **0** — No eval suite.
- **1** — A handful of ad hoc test cases; no structure or criteria.
- **2** — A structured suite with criteria; coverage of failure modes is partial,
  or not CI-integrated.
- **3** — Comprehensive structured suite — cases tied to failure modes, weighted
  criteria, binary/categorical scoring, CI-integrated.

**N/A condition:** Never N/A.
**Evidence to look for:** an `evals/` directory, test-case files, an eval runner,
evaluation-criteria config, CI eval workflow.

---

## D6.6 — SMEs label data

**Maps to:** P15 (Have SMEs Label Data).

**What good looks like:** Subject-matter experts review and label agent outputs
against a defined schema (Pass/Partial/Fail + failure-mode tags + free-text), with
2+ annotators for inter-rater reliability and a calibration cadence. Labels feed
back into the eval suite.

**Anchors:**
- **0** — No SME involvement; correctness is judged by engineers or not at all.
- **1** — Occasional informal SME spot-checks; no schema.
- **2** — SME labeling with a schema; single annotator or no reliability tracking.
- **3** — Structured SME labeling — defined schema, 2+ annotators, inter-rater
  reliability tracked, calibration cadence; labels feed the eval suite.

**N/A condition:** Never N/A.
**Evidence to look for:** a labeling schema, an annotation workflow/tool, annotator
roles, inter-rater (Kappa) tracking, labeled datasets.

---

## D6.7 — Datasets from production data

**Maps to:** P16 (Create Datasets from Production Data).

**What good looks like:** Eval datasets are built from real production interactions
(not only synthetic data), stored in a versioned dataset store, and re-versioned
when new failure modes appear or distribution shifts.

**Anchors:**
- **0** — No production-derived datasets; only synthetic or none.
- **1** — Some production examples collected ad hoc; not versioned.
- **2** — Production data feeds datasets; versioning is partial.
- **3** — Production interactions systematically curated into versioned datasets,
  re-versioned on new failure modes / distribution shift.

**N/A condition:** N/A for a pre-launch agent with no production traffic yet —
state this explicitly.
**Evidence to look for:** a dataset store, production-log → dataset pipeline,
dataset version history, distribution-shift checks.

---

## D6.8 — Production data evaluated live

**Maps to:** P17 (Evaluate Production Data).

**What good looks like:** Production responses are evaluated live — observability
captures input/output/tool-calls/latency/tokens/model version; an LLM-as-judge (or
equivalent) scores a sampled share of production traffic; a feedback loop turns
findings into new test cases.

**Anchors:**
- **0** — No production observability or live evaluation.
- **1** — Basic logging exists; no live scoring.
- **2** — Production responses are sampled and scored; the feedback loop is partial.
- **3** — Full live-eval pipeline — rich observability, sampled LLM-as-judge
  scoring, closed feedback loop into the eval suite.

**N/A condition:** N/A for a pre-launch agent with no production traffic yet —
state this explicitly.
**Evidence to look for:** observability tooling (LangSmith/Braintrust/custom),
an LLM-as-judge eval prompt, sampling config, a production → eval feedback loop.
