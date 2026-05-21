# D1 — Architecture & Capability Design

**Dimension:** Architecture & Capability Design.
**Sources:** Patterns P1, P2, P3 + Factor F10.
**Criteria:** 4 (D1.1–D1.4).

This dimension judges whether the agent's scope and shape were *designed* —
capabilities deliberately bounded, architecture grown from simplicity, the
dynamic-vs-static choice made consciously, and the resulting agent kept small.

---

## D1.1 — Capabilities whiteboarded & bounded

**Maps to:** P1 (Whiteboard Agent Capabilities).

**What good looks like:** Before building, the team enumerated exactly what the
agent should and should not do. There is an explicit capability list, named
non-goals / out-of-scope items, and the inputs, outputs, and decision boundaries
are written down. The agent's purpose is one sentence anyone can repeat.

**Anchors:**
- **0** — No capability definition. Scope is implicit or "whatever the LLM does".
- **1** — A vague mission statement exists, but no enumerated capabilities or non-goals.
- **2** — Capabilities are listed; non-goals are partial or boundaries are fuzzy.
- **3** — Capabilities, non-goals, inputs/outputs, and decision boundaries are all
  explicitly documented and current.

**N/A condition:** Never N/A — every agent has a scope.

**Evidence to look for:** a design doc / `agent-design.md` "Capabilities" or
"Scope" section, a non-goals list, requirements docs, system-prompt preamble that
states the bounded mission.

---

## D1.2 — Architecture evolves from simple

**Maps to:** P2 (Evolve Your Agent Architecture).

**What good looks like:** The architecture started as the simplest thing that
worked (a single prompt, a linear chain) and complexity was added only where
evidence demanded it. There is a visible rationale for each escalation in
complexity — multi-step, subagents, dynamic routing were *earned*, not assumed.

**Anchors:**
- **0** — Architecture jumped straight to maximum complexity (multi-agent, dynamic
  routing) with no simpler baseline considered.
- **1** — Some awareness of simplicity, but complexity is mostly unjustified.
- **2** — Architecture is reasonably proportionate; most complexity is justified.
- **3** — Clear evolution story: simple baseline, complexity added incrementally
  with documented rationale (and ideally evidence) for each step.

**N/A condition:** Never N/A.

**Evidence to look for:** design-doc "Architecture" / "Evolution" notes, ADRs,
git history showing incremental growth, commit messages, a rationale for
introducing subagents or routing.

---

## D1.3 — Dynamic vs static agent choice

**Maps to:** P3 (Dynamic Agents). **This is the single scoring home of P3** —
D4.4 cross-references this finding but does not re-score it.

**What good looks like:** The team consciously chose between a *static* workflow
(fixed, predetermined steps) and a *dynamic* agent (the LLM decides the next step
at runtime), and the choice fits the problem. Static is preferred when the path is
predictable; dynamic is reserved for genuinely open-ended tasks. The choice is
documented with its trade-offs (reliability vs flexibility, cost, debuggability).

**Anchors:**
- **0** — No conscious choice. Dynamic LLM-decides-everything by default, or a
  rigid workflow forced onto an open-ended problem.
- **1** — A choice was made but is poorly matched to the problem, or undocumented.
- **2** — Reasonable choice; trade-offs partially considered.
- **3** — Deliberate, well-matched choice with documented trade-offs; static and
  dynamic portions are separated where the task is mixed.

**N/A condition:** Never N/A.

**Evidence to look for:** design-doc section on agent type / control style, routing
code, a planner module, comments distinguishing fixed steps from LLM-chosen steps.

---

## D1.4 — Small, focused, single-purpose agents

**Maps to:** F10 (Small focused agents).

**What good looks like:** Each agent is small — roughly 3–10 reasoning steps — with
a single clear purpose and a contained blast radius. Large jobs are decomposed into
several focused agents rather than one sprawling generalist. Smaller agents are
easier to test, evaluate, and keep reliable as LLMs improve.

**Anchors:**
- **0** — One monolithic agent does everything; unbounded step counts; huge blast
  radius.
- **1** — Some decomposition, but agents are still broad or overlap heavily.
- **2** — Mostly focused agents; one or two are still doing too much.
- **3** — Every agent is small, single-purpose, and bounded in steps; decomposition
  is clean and blast radius is contained.

**N/A condition:** Never N/A.

**Evidence to look for:** number and size of agent definitions, step/turn limits,
how a multi-part job is split, per-agent responsibility comments.

> **Merge guard:** D1.1 and D1.2 score the *process* (whiteboarding, evolving from
> simple). D1.4 scores the *result* (size and blast radius). A team can whiteboard
> well yet still ship one bloated agent — score D1.4 on what was actually built,
> independently of D1.1/D1.2.
