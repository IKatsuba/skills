---
name: agent:memory
description: Memory Architecture - designs agent memory strategy with working memory, hierarchical recall, memory processors, and context management
---

# Memory Architecture

Guides the user through designing memory for AI agents. Based on "Principles of Building AI Agents" (Bhagwat & Gienow, 2025), Chapters 7-8: Agent Memory and Dynamic Agents.

## When to use

Use this skill when the user needs to:
- Design how an agent remembers information across turns and sessions
- Choose between context window, working memory, and semantic recall
- Set up memory processors (token limiting, tool call filtering)
- Plan long-term memory and user profile storage

## Instructions

### Step 1: Understand Memory Requirements

Use the `AskUserQuestion` tool to gather context:
1. Does the agent need to remember across sessions? (ephemeral vs. persistent)
2. What user-specific information matters? (preferences, history, profile)
3. How long are typical conversations? (few turns vs. dozens)
4. Does the agent call tools with large outputs? (search results, code, documents)
5. What model and context window are you using?

Read any existing spec documents (`.specs/<spec-name>/`) before proceeding.

### Step 2: Memory Architecture Design

Present the three-layer memory model:

```markdown
## Memory Architecture

### Layer 1: Conversation Window (Short-term)
Recent messages kept verbatim in the context window.
- **Scope:** Current session only
- **Implementation:** Last N messages (sliding window)
- **Tuning:** `lastMessages` parameter — how many recent turns to keep

### Layer 2: Working Memory (Persistent state)
Long-term facts about the user or task, always included in context.
- **Scope:** Across sessions
- **Implementation:** Key-value store or structured profile
- **Examples:** User name, preferences, subscription tier, language, past decisions
- **Tuning:** Keep small — this is injected into every request

### Layer 3: Semantic Recall (Long-term, on-demand)
Past conversations and knowledge retrieved by relevance.
- **Scope:** Across sessions
- **Implementation:** RAG over past conversations / documents
- **Tuning:** `topK` (number of results), `messageRange` (context around each match)
- **When to use:** User references past interactions, asks "remember when..."
```

Use `AskUserQuestion` to determine which layers the agent needs:

| Agent Type | Layer 1 | Layer 2 | Layer 3 |
|-----------|---------|---------|---------|
| One-shot tool (e.g., code formatter) | Minimal | No | No |
| Chatbot (no memory) | Yes | No | No |
| Personal assistant | Yes | Yes | Yes |
| Support agent | Yes | Yes (ticket context) | Maybe (past tickets) |
| Research agent | Yes | No | Yes (past research) |

### Step 3: Working Memory Design

If the agent needs persistent state (Layer 2), define what it stores:

```markdown
## Working Memory Schema

### User Profile
| Field | Type | Source | Updated |
|-------|------|--------|---------|
| name | string | User input | On first mention |
| language | string | User input / detection | On change |
| tier | enum (free/pro/enterprise) | Auth system | On login |
| preferences | object | Accumulated from conversations | Continuously |

### Task State
| Field | Type | Purpose |
|-------|------|---------|
| currentGoal | string | What the user is trying to achieve |
| completedSteps | string[] | What has been done |
| pendingActions | string[] | What needs to happen next |

### Injection Strategy
Working memory is injected into the system prompt as:
<working_memory>
{serialized working memory}
</working_memory>

**Size budget:** [N] tokens max — keep concise
```

Use `AskUserQuestion` to identify the specific fields for the user's domain.

### Step 4: Semantic Recall Configuration

If the agent needs long-term recall (Layer 3), configure it:

```markdown
## Semantic Recall

### What is Stored
- [ ] Full conversation transcripts
- [ ] Agent-generated summaries of conversations
- [ ] Tool call results (selectively)
- [ ] User-provided documents
- [ ] Decision rationale

### Retrieval Settings
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| topK | [3-10] | Number of past messages/chunks to retrieve |
| messageRange | [1-5] | Messages of context around each match |
| similarityThreshold | [0.7-0.9] | Minimum relevance score to include |
| embedding model | [Model] | Matches quality needs |

### Storage
| Option | Pros | Cons |
|--------|------|------|
| pgvector (on existing Postgres) | No new infra, familiar | May need tuning for scale |
| Pinecone | Managed, fast, scalable | Additional service + cost |
| Chroma | Open-source, local dev friendly | Self-hosted in production |

### When to Recall
- User references past interactions ("last time", "remember when", "as before")
- Agent needs historical context for the current task
- Retrieval is triggered automatically on every turn (configurable)
```

### Step 5: Memory Processors

Design processors that manage context size and relevance:

```markdown
## Memory Processors

### TokenLimiter
Prevents exceeding context window by removing oldest messages.
- **Trigger:** Total tokens > [X% of context window]
- **Strategy:** Remove oldest messages first, preserve system prompt and working memory
- **Protected:** System prompt, working memory, last [N] messages

### ToolCallFilter
Removes verbose tool call results from history to save tokens.
- **When to use:** Agent calls tools that return large payloads (search, code analysis)
- **Strategy:** Keep tool call intent, remove raw response; OR summarize response
- **Tradeoff:** Agent always calls tools fresh (no cached results) vs. seeing past tool outputs

### SummaryProcessor (optional)
Periodically summarizes older conversation turns.
- **Trigger:** Conversation exceeds [N] turns
- **Strategy:** Summarize turns [1..N-K] into a paragraph, keep last K turns verbatim
- **Protected:** Key decisions, user corrections, error context
```

Use `AskUserQuestion` to select which processors are needed.

### Step 6: Dynamic Memory Configuration

If the agent adapts based on user context (Pattern 3 from Patterns book):

```markdown
## Dynamic Memory Configuration

| User Signal | Memory Adjustment |
|------------|-------------------|
| Free tier | topK=3, no semantic recall, basic working memory |
| Pro tier | topK=10, full semantic recall, rich working memory |
| Enterprise | topK=20, full recall, extended working memory with org context |
| New user | No working memory yet, rely on conversation window |
| Returning user | Load working memory, enable semantic recall |
```

### Step 7: Generate Memory Document

Compile into `.specs/<spec-name>/agent-memory.md`:

```markdown
# Memory Architecture: [Agent Name]

## Overview
[Which layers are used and why]

## Memory Architecture
[From Step 2]

## Working Memory
[From Step 3]

## Semantic Recall
[From Step 4]

## Memory Processors
[From Step 5]

## Dynamic Configuration
[From Step 6]
```

### Step 8: Offer Next Steps

Use `AskUserQuestion` to offer:
1. **Proceed to workflow design** — run `agent:workflow`
2. **Proceed to RAG pipeline** — run `agent:rag` (if using semantic recall)
3. **Proceed to context engineering** — run `agent:context`
4. **Full review** — run `agent:review`

## Arguments

- `<args>` - Optional spec name
  - `<spec-name>` — reads existing agent design from `.specs/<spec-name>/`

Examples:
- `agent:memory customer-support` — design memory for the customer-support agent
- `agent:memory` — start fresh
