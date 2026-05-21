# D4 — Tools & Interface Design

**Dimension:** Tools & Interface Design.
**Sources:** Factors F1, F2, F4 + a cross-reference to P3 (scored at D1.3).
**Criteria:** 4 (D4.1–D4.4).

This dimension judges the agent's tool layer and prompt assets — natural language
mapped to structured tool calls, prompts owned as first-class code, tools defined
as structured schemas, and the overall tool surface kept scoped and healthy.

**Design-only note:** D4.1 and D4.3 are about a *running* tool layer. In a
design-only audit, score on the quality of the tool *design*; if the design is
silent, return `N/A` rather than guessing.

---

## D4.1 — NL → structured tool calls

**Maps to:** F1 (Natural Language to Tool Calls).

**What good looks like:** The agent reliably translates natural-language intent
into well-formed, structured tool-call JSON — correct tool name, correct argument
shape, valid types. The tool-call boundary is clean: the LLM emits structured
calls, not free text that downstream code must parse heuristically.

**Anchors:**
- **0** — No structured tool-calling; the agent emits prose that is regex-parsed,
  or tool calls are routinely malformed.
- **1** — Structured tool-calling exists but is unreliable — frequent argument
  errors, weak typing.
- **2** — Tool calls are mostly well-formed; occasional argument-shape issues.
- **3** — Reliable NL→structured-call mapping — typed arguments, validated shapes,
  the LLM emits clean structured calls consistently.

**N/A condition:** N/A in a design-only audit with no tool-calling mechanism
described, OR if the agent provably calls no tools (state this).

**Evidence to look for:** tool-call handling code, argument schemas, validation of
tool arguments, function-calling / tool-use API usage, parse-and-dispatch logic.

---

## D4.2 — Prompts owned / versioned / first-class

**Maps to:** F2 (Own your prompts).

**What good looks like:** Prompts are first-class, owned code — stored in version
control as discrete files, reviewed, diffable, and ideally tested. They are not
buried as inline string literals or hidden behind a framework's prompt
abstraction. Prompt changes go through the same rigor as code changes.

**Anchors:**
- **0** — Prompts are scattered inline string literals or framework defaults; no
  versioning, no review.
- **1** — Prompts are in files but unstructured; changes are unreviewed.
- **2** — Prompts are version-controlled files, reviewed like code; no testing.
- **3** — Prompts are first-class assets — versioned, reviewed, organized, and
  exercised by tests or evals; changes are deliberate and tracked.

**N/A condition:** Never N/A — every agent has prompts.

**Evidence to look for:** a `prompts/` directory, prompt files in version control,
prompt-change history, prompt tests, separation of prompts from logic.

---

## D4.3 — Tools are structured outputs / schemas

**Maps to:** F4 (Tools are structured outputs).

**What good looks like:** Each tool is defined by an explicit schema — typed
parameters, described fields, a defined return shape. A tool call is understood as
"just JSON the LLM emits" against that schema; the schema is the contract. Tool
definitions are declarative and machine-checkable, not implicit in handler code.

**Anchors:**
- **0** — Tools have no schemas; parameters and returns are untyped and undocumented.
- **1** — Partial schemas; some tools typed, descriptions thin or missing.
- **2** — Most tools have proper typed schemas with descriptions; returns mostly
  structured.
- **3** — Every tool has a complete, declarative schema — typed params, clear
  descriptions, defined structured return shape; schemas are the enforced contract.

**N/A condition:** N/A if the agent provably calls no tools (state this).

**Evidence to look for:** tool/function schema definitions (JSON Schema, Zod,
Pydantic), parameter type annotations, field descriptions, declared return types.

---

## D4.4 — Tool-surface health — scoped tool-set

**Maps to:** cross-references P3 (scored at D1.3) — **does not re-score P3.**

**What good looks like:** The agent is given a tool-set scoped to what it actually
needs — no grab-bag of unused or overlapping tools that bloats decisions and widens
the attack surface. Reading D1.3's dynamic-vs-static finding: a static agent needs
only its workflow's tools; a dynamic agent needs a curated, minimal set. Tools are
named clearly and do not overlap confusingly.

**Anchors:**
- **0** — Huge, unscoped tool grab-bag; many tools unused; overlapping/ambiguous
  tools confuse the model.
- **1** — Tool-set is broad and only loosely matched to need.
- **2** — Tool-set is mostly scoped; one or two redundant or unused tools remain.
- **3** — Lean, deliberately scoped tool-set — every tool is needed, names are
  distinct, no overlap; scoping matches the D1.3 agent type.

**N/A condition:** N/A if the agent provably calls no tools (state this).

**Evidence to look for:** the full tool registry/list, count of tools vs count
actually invoked, naming clarity, overlapping tools, per-agent tool scoping.

> **Cross-reference guard:** P3 (dynamic vs static) is scored **once**, at D1.3.
> D4.4 *reads* that finding to judge whether the tool surface is appropriately
> scoped, but assigns its own independent score for tool-surface health. Do not
> re-score the dynamic/static choice here.
