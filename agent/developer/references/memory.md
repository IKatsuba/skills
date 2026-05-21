# Memory Architecture

How an agent remembers information across turns and sessions.

## Three-layer memory model

### Layer 1: Conversation window (short-term)
Recent messages kept verbatim in the context window.
- **Scope:** current session only.
- **Implementation:** last N messages (sliding window).
- **Tuning:** `lastMessages` — how many recent turns to keep.

### Layer 2: Working memory (persistent state)
Long-term facts about the user or task, always included in context.
- **Scope:** across sessions.
- **Implementation:** key-value store or structured profile.
- **Examples:** user name, preferences, subscription tier, language, past decisions.
- **Tuning:** keep small — this is injected into every request.

### Layer 3: Semantic recall (long-term, on-demand)
Past conversations and knowledge retrieved by relevance.
- **Scope:** across sessions.
- **Implementation:** RAG over past conversations / documents.
- **Tuning:** `topK` (number of results), `messageRange` (context around each match).
- **When to use:** the user references past interactions ("remember when...").

## Agent type → layer matrix

| Agent type | Layer 1 | Layer 2 | Layer 3 |
|-----------|---------|---------|---------|
| One-shot tool (e.g. code formatter) | Minimal | No | No |
| Chatbot (no memory) | Yes | No | No |
| Personal assistant | Yes | Yes | Yes |
| Support agent | Yes | Yes (ticket context) | Maybe (past tickets) |
| Research agent | Yes | No | Yes (past research) |

## Working memory schema

When the agent needs persistent state, define what it stores:

**User profile** — fields with type, source, and update trigger. Examples:
- `name` — string — user input — on first mention.
- `language` — string — user input / detection — on change.
- `tier` — enum (free/pro/enterprise) — auth system — on login.
- `preferences` — object — accumulated from conversations — continuously.

**Task state** — fields tracking the active task:
- `currentGoal` — what the user is trying to achieve.
- `completedSteps` — what has been done.
- `pendingActions` — what needs to happen next.

**Injection strategy:** working memory is serialized into the system prompt inside `<working_memory>` tags. Enforce a token budget — keep it concise.

## Semantic recall configuration

**What to store:** full transcripts, agent-generated summaries, selective tool-call results, user-provided documents, decision rationale.

**Retrieval settings:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| topK | 3-10 | Number of past messages/chunks to retrieve |
| messageRange | 1-5 | Messages of context around each match |
| similarityThreshold | 0.7-0.9 | Minimum relevance score to include |
| embedding model | — | Matches quality needs |

**Storage options:** pgvector (no new infra, familiar SQL), Pinecone (managed, fast, scalable), Chroma (open-source, local-dev friendly).

**When to recall:** the user references past interactions ("last time", "as before"); the agent needs historical context; or retrieval runs automatically every turn.

## Memory processors

### TokenLimiter
Prevents exceeding the context window by removing oldest messages.
- **Trigger:** total tokens > X% of context window.
- **Strategy:** remove oldest messages first.
- **Protected:** system prompt, working memory, last N messages.

### ToolCallFilter
Removes verbose tool-call results from history to save tokens.
- **When to use:** the agent calls tools that return large payloads (search, code analysis).
- **Strategy:** keep the tool-call intent, drop the raw response; OR summarize the response.
- **Tradeoff:** agent always calls tools fresh (no cached results) vs. seeing past tool outputs.

### SummaryProcessor (optional)
Periodically summarizes older conversation turns.
- **Trigger:** conversation exceeds N turns.
- **Strategy:** summarize turns 1..N-K into a paragraph, keep last K turns verbatim.
- **Protected:** key decisions, user corrections, error context.

## Dynamic memory configuration

Adjust memory depth by runtime signal:

| User signal | Memory adjustment |
|------------|-------------------|
| Free tier | topK=3, no semantic recall, basic working memory |
| Pro tier | topK=10, full semantic recall, rich working memory |
| Enterprise | topK=20, full recall, extended working memory with org context |
| New user | No working memory yet, rely on conversation window |
| Returning user | Load working memory, enable semantic recall |
