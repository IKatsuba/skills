# D2 — Control Flow & State

**Dimension:** Control Flow & State.
**Sources:** Factors F5, F6, F8, F11, F12 (no patterns).
**Criteria:** 5 (D2.1–D2.5).

This dimension exists *specifically* because the 12 factors were merged in. Control
flow, state unification, and triggering are the genuine gap in the 22 patterns —
D2 closes it. It judges whether the agent owns its execution loop, unifies its
state, is built as a pure reducer, exposes launch/pause/resume APIs, and can be
triggered from anywhere.

**Design-only note:** several D2 criteria are about a *running mechanism*. In a
design-only audit, score on the quality of the *design* of the mechanism; if the
design is silent on a criterion, return `N/A` rather than guessing an
implementation score.

---

## D2.1 — Explicit control flow / own the loop

**Maps to:** F8 (Own your control flow).

**What good looks like:** The agent's loop is explicit code the team owns — a
visible `while`/state-machine that decides "call the model → run a tool → check
exit". The loop can be interrupted and resumed; it is not buried inside an opaque
framework `.run()` call. Loop exit conditions (max steps, done signal) are explicit.

**Anchors:**
- **0** — Control flow is a black-box framework call; the team cannot see or modify
  the loop; no explicit exit conditions.
- **1** — A loop exists but is implicit or tangled; exit conditions are ad hoc.
- **2** — An explicit, owned loop with clear exit conditions; interruption is
  awkward but possible.
- **3** — Fully owned, explicit loop — readable state machine, clean
  interrupt/resume, explicit step limits and exit signals.

**N/A condition:** N/A only in a design-only audit where no loop design is described.

**Evidence to look for:** an agent loop / runner module, a state-machine
definition, `maxSteps`/`maxTurns` constants, framework-vs-custom loop code.

---

## D2.2 — Unified execution + business state

**Maps to:** F5 (Unify execution state and business state).

**What good looks like:** Execution state (current step, retry count, pending tool
calls) and business state (the domain data the agent is working on) live in **one**
serializable object, not split across two stores that can drift. The whole agent
state can be snapshotted and rehydrated as a unit.

**Anchors:**
- **0** — Execution and business state are scattered across globals, framework
  internals, and DB rows with no unified representation.
- **1** — A partial state object exists, but key execution state lives elsewhere.
- **2** — Mostly unified state; minor leakage of state outside the object.
- **3** — A single, serializable state object holds both execution and business
  state; it is the one source of truth.

**N/A condition:** N/A only in a design-only audit with no state model described.

**Evidence to look for:** a state / context type definition, a serialization
schema, how a run is persisted, whether step/retry counters live with domain data.

---

## D2.3 — Stateless reducer design

**Maps to:** F12 (Stateless reducer).

**What good looks like:** The agent is structured as a pure function
`(state, event) → new state` — a reducer. Given the same state and event it
produces the same next state; side effects are pushed to the edges. This makes
runs reproducible, testable, and replayable.

**Anchors:**
- **0** — Agent step logic is full of hidden mutation and side effects; runs are
  not reproducible.
- **1** — Some functional structure, but state mutation and side effects are
  intermixed with step logic.
- **2** — Largely reducer-shaped; a few side effects leak into the core transition.
- **3** — Core transition is a clean pure `(state, event) → state` reducer; side
  effects isolated at the boundary; steps are replayable.

**N/A condition:** N/A only in a design-only audit with no transition model described.

**Evidence to look for:** a reducer / `step()` / `transition()` function, purity of
the core step, where I/O and side effects are performed, replay or time-travel
tests.

---

## D2.4 — Launch / pause / resume APIs

**Maps to:** F6 (Launch/Pause/Resume with simple APIs).

**What good looks like:** The agent exposes simple APIs to **launch** a run,
**pause** it (e.g. while awaiting a human or a long tool), and **resume** it later
from saved state. Pausing does not lose progress; resuming continues exactly where
it stopped. Long-running and human-gated workflows depend on this.

**Anchors:**
- **0** — No pause/resume. A run is one uninterruptible call; interruption loses
  all progress.
- **1** — Launch exists; pause/resume is hacked or only partially works.
- **2** — Launch/pause/resume all exist; resume is slightly lossy or awkward.
- **3** — Clean launch/pause/resume APIs; pause persists full state; resume is
  exact and lossless.

**N/A condition:** N/A in a design-only audit, OR for a genuinely synchronous
single-shot agent where pause/resume is provably out of scope (state this).

**Evidence to look for:** `launch`/`start`, `pause`/`suspend`, `resume` API
surfaces, a run-store, checkpoint persistence, webhook-callback resume handlers.

---

## D2.5 — Triggerable from anywhere

**Maps to:** F11 (Trigger from anywhere).

**What good looks like:** The agent can be initiated from multiple entry points —
Slack, email, webhook, cron, API call, UI — not just one hard-coded caller. The
core agent is decoupled from any single trigger, so new entry points are cheap to
add. Humans and systems can both reach it where they already are.

**Anchors:**
- **0** — Exactly one hard-coded entry point; the agent and its trigger are fused.
- **1** — One main entry point; adding another would require core changes.
- **2** — A couple of entry points; the trigger layer is mostly decoupled.
- **3** — Trigger-agnostic core with a thin adapter layer; multiple live triggers
  (e.g. Slack + webhook + cron) and new ones are trivial to add.

**N/A condition:** N/A only in a design-only audit with no trigger/entry-point
design described.

**Evidence to look for:** webhook handlers, Slack/email integrations, cron/schedule
config, an API route that starts a run, an adapter/entry-point layer separate from
the agent core.
