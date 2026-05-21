# D7 — Security

**Dimension:** Security.
**Sources:** Patterns P18–P22 (no factors).
**Criteria:** 5 (D7.1–D7.5).

This dimension audits the agent's security posture, covering the lethal trifecta,
sandboxing, access control, and guardrails. **D7 additionally returns two
qualitative outputs** that feed the security override gate (see `scoring.md`):

- `risk_level`: `Low` | `Medium` | `High` | `Critical`
- `trifecta_status`: `SAFE` | `AT RISK` | `VULNERABLE`

**Security override:** if `trifecta_status` is `VULNERABLE`, or any D7 criterion is
scored at a level this rubric flags as **Critical**, the displayed overall maturity
is capped at MVP. Each criterion below states what counts as a Critical finding.

---

## D7.1 — Lethal trifecta prevented

**Maps to:** P18 (Prevent the Lethal Trifecta).

The **lethal trifecta** (Simon Willison) is the co-occurrence of three legs:
1. **Private data access** — the agent can read sensitive information (PII,
   internal docs, DB rows, credentials, private repos).
2. **Untrusted content exposure** — the agent ingests external/user-generated input
   (user content, public web pages, uploaded files, third-party API responses,
   public issues/comments).
3. **Exfiltration capability** — the agent can send data outside the system (email,
   PRs/issues, external API calls, public endpoints, shared-state writes).

When **all three** are present, prompt-injection attacks become possible: malicious
instructions hidden in untrusted content trick the agent into reading private data
and sending it to an attacker.

**Determine `trifecta_status`:**
- `SAFE` — at most one leg present, or two legs robustly isolated from each other.
- `AT RISK` — two legs present and not cleanly isolated.
- `VULNERABLE` — **all three legs present** with no mitigation.

**What good looks like:** At least one leg is deliberately removed or isolated.
Preferred mitigations: remove exfiltration (constrain actions after untrusted
input); isolate data access (separate agents for private data vs untrusted
content); sanitize input (middleware that cleans untrusted content before the LLM).

**Anchors:**
- **0 — Critical** — all three legs present, no mitigation (`VULNERABLE`).
- **1** — all three legs present but a partial mitigation exists; or two legs with
  weak isolation (`AT RISK`).
- **2** — a leg is removed or strongly isolated; residual risk is minor (`SAFE`/`AT RISK`).
- **3** — trifecta provably broken — a leg is absent by design, or strong isolation
  with sanitization; `SAFE`.

**Critical-finding rule:** a score of **0 here is a Critical finding** and triggers
the maturity cap.

**N/A condition:** Never N/A.
**Evidence to look for:** what data the agent reads, what untrusted input it
ingests, what outbound channels it has, any isolation/sanitization middleware.

---

## D7.2 — Code execution sandboxed

**Maps to:** P19 (Sandbox Code Execution).

**What good looks like:** If the agent executes code, it runs in an isolated
sandbox — isolated container, restricted/blocked network, restricted filesystem,
CPU/memory/time limits, no production credentials, no host-filesystem access.
Threats to assess: secret exfiltration, environment destruction, resource abuse
(crypto mining), accidental resource hogging.

**Anchors:**
- **0 — Critical (if code execution exists)** — generated code runs unsandboxed
  with host/credential/network access.
- **1** — minimal isolation; significant gaps (e.g. network open, no resource limits).
- **2** — solid sandbox; one or two gaps remain.
- **3** — robust sandbox — isolation, network policy, filesystem limits, resource
  limits, no production credentials.

**Critical-finding rule:** a score of **0 here is a Critical finding** (unsandboxed
code execution) and triggers the maturity cap.

**N/A condition:** N/A if the agent provably executes **no** code (no shell, no eval,
no code-gen-and-run) — state this explicitly.
**Evidence to look for:** container/Dockerfile config, runtime choice (Docker / E2B
/ Daytona), network policy, resource limits, credential scoping in the sandbox.

---

## D7.3 — Granular access control

**Maps to:** P20 (Granular Agent Access Control).

Agents need **more** granular access control than humans — they are infinitely
diligent (security-by-obscurity fails), ephemeral (credentials must be scoped), and
unpredictable (LLM behavior is nondeterministic).

**What good looks like:** The agent has its own identity (not a shared service
account); credentials are scoped and short-lived; tools follow least privilege;
there are distinct **planning-mode** (read-only) and **execution-mode** (elevated,
gated) permissions; access is just-in-time (per-task, not per-session) and revoked
after use.

**Anchors:**
- **0** — broad standing credentials, shared service account, no least privilege.
- **1** — some scoping, but over-broad permissions and no mode separation.
- **2** — least privilege mostly applied; own identity; mode separation partial.
- **3** — own identity, scoped short-lived credentials, least privilege per tool,
  planning/execution mode separation, just-in-time access.

**Critical-finding rule:** treat as a **Critical finding** if the agent holds
standing admin/production credentials with no scoping AND can act autonomously.

**N/A condition:** Never N/A.
**Evidence to look for:** IAM/role config, credential scoping & TTLs, the agent's
identity, planning-vs-execution permission code, JIT-access logic.

---

## D7.4 — Input / output guardrails

**Maps to:** P21 (Agent Guardrails).

Guardrails are live, low-latency checks that prevent harm in real time (they
complement evals, which are after-the-fact).

**Input guardrails** (before the LLM): prompt-injection detection, jailbreak
detection, PII detection, off-topic detection, on-brand/acceptable-use checks.
**Output guardrails** (before user/tools): data-leakage detection, hallucination
checks, toxicity detection, format/schema validation, action validation (tool calls
within authorized scope).

**What good looks like:** Both input and output guardrails exist, run on every
request, are low-latency (lightweight models or rules), and log all triggers for
monitoring and tuning.

**Anchors:**
- **0** — no guardrails; raw input reaches the LLM and raw output reaches users/tools.
- **1** — a guardrail or two on one side only; gaps on the highest-risk checks.
- **2** — input and output guardrails both present; coverage of key risks partial.
- **3** — comprehensive input + output guardrails, low-latency, logged and tuned.

**Critical-finding rule:** treat as a **Critical finding** if the agent processes
untrusted input AND can take consequential actions AND has **no** input guardrails
(no injection/jailbreak defense at all).

**N/A condition:** Never N/A.
**Evidence to look for:** input/output guard middleware, injection/jailbreak
detectors, PII redaction, schema validation, action-scope checks, guardrail logs.

---

## D7.5 — Future-readiness / adversarial outlook

**Maps to:** P22 (What's Next).

**What good looks like:** The team has a forward-looking security posture — it
tracks emerging agent threats (new injection vectors, multi-agent collusion, model
updates changing behavior), revisits the threat model periodically, and plans for
adversarial testing / red-teaming and synthetic adversarial evals. Security is
treated as ongoing, not a one-time checkbox.

**Anchors:**
- **0** — no forward-looking security thinking; threat model (if any) is static and
  stale.
- **1** — some awareness of evolving threats; no plan or cadence.
- **2** — a revisited threat model and some adversarial testing; not yet systematic.
- **3** — active adversarial outlook — periodic threat-model review, red-teaming /
  adversarial evals planned or running, monitoring of emerging agent threats.

**Critical-finding rule:** never a Critical finding on its own — D7.5 is a maturity
signal, not an exploitable gap.

**N/A condition:** Never N/A.
**Evidence to look for:** a threat-model doc with a review cadence, red-team plans,
adversarial/synthetic eval cases, notes on emerging-threat monitoring.
