---
name: agent:secure
description: Agent Security Audit - analyzes agent for lethal trifecta, sandboxing, access control, and guardrails
argument-hint: [spec-name|path]
---

# Agent Security Audit

Performs a security audit of an AI agent system. Applies patterns 18-21 from "Patterns for Building AI Agents" (Bhagwat & Gienow, 2025): preventing the lethal trifecta, sandboxing code execution, granular access control, and input/output guardrails.

## When to use

Use this skill when the user needs to:
- Audit an existing agent for security vulnerabilities
- Design security controls for a new agent
- Prevent prompt injection and data exfiltration
- Set up sandboxing for code execution
- Design access control and guardrails

## Instructions

### Step 1: Understand the Agent

Use the `AskUserQuestion` tool to gather context:
1. What does the agent do?
2. Does it access private/sensitive data? (user data, internal docs, credentials)
3. Does it process untrusted input? (public content, user uploads, external APIs)
4. Can it communicate externally? (send emails, create PRs, call APIs, write files)
5. Does it execute code? (run scripts, shell commands, code generation)
6. What authentication/authorization exists today?

Read any existing spec documents (`.specs/<spec-name>/`) before proceeding.

### Step 2: Lethal Trifecta Analysis (Pattern 18)

The "lethal trifecta" (coined by Simon Willison) is the combination of:
1. **Access to private data** — agent can read sensitive information
2. **Exposure to untrusted content** — agent processes external/user-generated input
3. **Exfiltration capability** — agent can send data outside the system

**When all three are present, prompt injection attacks become possible:** malicious instructions hidden in external content trick the agent into accessing private data and sending it to an attacker.

Analyze the agent:

```markdown
## Lethal Trifecta Analysis

### Leg 1: Private Data Access
- [ ] Reads user PII
- [ ] Accesses internal documents
- [ ] Has database read access
- [ ] Can read credentials/secrets
- [ ] Accesses private repositories
**Risk level:** [None / Low / Medium / High]

### Leg 2: Untrusted Content Exposure
- [ ] Processes user-generated content
- [ ] Reads public web pages
- [ ] Parses uploaded files
- [ ] Ingests third-party API responses
- [ ] Reads public issues/tickets/comments
**Risk level:** [None / Low / Medium / High]

### Leg 3: Exfiltration Capability
- [ ] Can send emails
- [ ] Can create PRs/issues
- [ ] Can call external APIs
- [ ] Can write to public endpoints
- [ ] Can modify shared state
**Risk level:** [None / Low / Medium / High]

### Trifecta Status: [SAFE / AT RISK / VULNERABLE]
```

**If all three legs are present:** The agent is VULNERABLE. Recommend removing at least one leg:
- **Easiest: remove exfiltration** — constrain agent actions after processing untrusted input
- **Alternative: isolate data access** — use separate agents for private data vs. untrusted content
- **Alternative: sanitize input** — add middleware to intercept and clean untrusted content before it reaches the LLM

Use `AskUserQuestion` to recommend and confirm the mitigation approach.

### Step 3: Sandbox Assessment (Pattern 19)

If the agent executes code, audit the sandbox:

```markdown
## Code Execution Sandbox

### Current State
- [ ] Code runs in isolated container
- [ ] Network access restricted
- [ ] File system access restricted
- [ ] Resource limits set (CPU, memory, time)
- [ ] No access to production credentials
- [ ] No access to host file system

### Threats
| Threat | Risk | Mitigation |
|--------|------|-----------|
| Secret exfiltration | [Risk] | [Mitigation] |
| Environment deletion | [Risk] | [Mitigation] |
| Resource abuse (crypto mining) | [Risk] | [Mitigation] |
| Accidental resource hogging | [Risk] | [Mitigation] |

### Recommendations
- **Runtime:** [Docker / E2B / Daytona / other]
  - Note: Docker has 10-20s cold starts; consider agentic runtimes for sub-second startup
- **Resource limits:** CPU: [X], Memory: [X], Timeout: [X]
- **Network policy:** [Allow-list specific endpoints / Block all / etc.]
```

If the agent does NOT execute code, note this and skip to Step 4.

### Step 4: Access Control Review (Pattern 20)

Agents need MORE granular access control than humans because they are:
- **Infinitely diligent** — security by obscurity doesn't work
- **Ephemeral** — sessions are short-lived, credentials need scoping
- **Unpredictable** — LLM behavior is nondeterministic

```markdown
## Access Control Review

### Authentication
- [ ] Agent has its own identity (not using a shared service account)
- [ ] OAuth flow implemented for user-delegated access
- [ ] Credentials are scoped to specific operations
- [ ] Credentials are short-lived / rotated

### Authorization
| Tool/Action | Current Access | Recommended Access | Justification |
|---|---|---|---|
| [Database read] | [Full access] | [Read-only, filtered by user] | [Least privilege] |
| [API call X] | [Admin] | [Scoped to operation] | [Least privilege] |
| [File write] | [Unrestricted] | [Specific directory only] | [Blast radius reduction] |

### Permission Modes
- [ ] **Planning mode** — agent has reduced permissions during reasoning
  - Restrict: UPDATE, DELETE, external API calls
  - Allow: SELECT, read-only operations
- [ ] **Execution mode** — elevated permissions only for confirmed actions
  - Requires: explicit user approval or automated policy check

### Just-in-Time Access
- [ ] Credentials granted per-task, not per-session
- [ ] Access scoped to specific user context
- [ ] Unused permissions revoked after task completion
```

### Step 5: Guardrails Design (Pattern 21)

Design input and output guardrails — live, low-latency checks that prevent harm in real-time.

```markdown
## Guardrails

### Input Guardrails
Intercept incoming inputs BEFORE they reach the LLM.

| Guard | Description | Action on Trigger |
|-------|-------------|-------------------|
| Prompt Injection | Detect attempts to override system instructions | Block + return default message |
| Jailbreak Detection | Detect attempts to bypass safety constraints | Block + log + alert |
| PII Detection | Detect sensitive personal information in input | Redact or block |
| Off-Topic | Detect requests outside agent's domain | Redirect to appropriate handler |
| On-Brand | Ensure input aligns with acceptable use | Block inappropriate content |

### Output Guardrails
Screen generated output BEFORE it reaches the user or tools.

| Guard | Description | Action on Trigger |
|-------|-------------|-------------------|
| Data Leakage | Detect private data in output | Redact + log |
| Hallucination Check | Verify factual claims against source data | Flag for review |
| Toxicity | Detect harmful, biased, or inappropriate content | Block + regenerate |
| Format Validation | Ensure output matches expected schema | Retry with format instructions |
| Action Validation | Verify tool calls are within authorized scope | Block unauthorized actions |

### Implementation Notes
- Guardrails must be LOW LATENCY — they run on every request
- Use specialized lightweight models or rule-based systems for speed
- Log all guardrail triggers for monitoring and tuning
- Guardrails complement evals — evals are after-the-fact, guardrails are real-time
```

Use `AskUserQuestion` to prioritize which guardrails to implement first based on the agent's risk profile.

### Step 6: Generate Security Report

Compile all outputs into `.specs/<spec-name>/agent-security.md`:

```markdown
# Agent Security Audit: [System Name]

## Executive Summary
**Overall Risk:** [Low / Medium / High / Critical]
**Lethal Trifecta:** [SAFE / AT RISK / VULNERABLE]
**Immediate Actions Required:** [Count]

## Lethal Trifecta Analysis
[From Step 2]

## Sandbox Assessment
[From Step 3]

## Access Control
[From Step 4]

## Guardrails
[From Step 5]

## Priority Actions
| # | Action | Severity | Effort |
|---|--------|----------|--------|
| 1 | [Action] | Critical | [Low/Med/High] |
| 2 | [Action] | High | [Low/Med/High] |
```

### Step 7: Offer Next Steps

Use `AskUserQuestion` to offer:
1. **Implement top-priority fix** — start with the highest-severity action item
2. **Full review** — run `agent:review` to validate against all 22 patterns
3. **Re-audit** — run `agent:secure` again after implementing fixes

## Arguments

- `$ARGUMENTS` (`$0`) - Optional spec name or path to agent code
  - `<spec-name>` — reads existing agent design from `.specs/<spec-name>/`
  - `<path>` — analyzes agent code at the given path

Examples:
- `agent:secure customer-support` — audit the customer-support agent
- `agent:secure src/agents/` — audit agent code in the given directory
