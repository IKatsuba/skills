# Tool Design

How to design the tool set for an agent. Tool design is the most important step in building an agent.

## Decomposition

Principle: **think like an analyst — decompose into clear, reusable operations.**

1. **List all actions** the agent needs to perform.
2. **Group by data source** — operations on the same data/API belong together.
3. **Separate read from write** — reading and modifying data should be different tools.
4. **Make tools atomic** — each tool does ONE thing well.
5. **Name semantically** — `searchProducts`, `getOrderStatus`; never `doStuff` or `handleRequest`.

Common mistake: building one tool that does everything. If a human analyst would follow specific queries/operations, encode each as a separate tool.

## Tool schema template

For each tool, write a detailed schema:

- **Description** — both what the tool does AND when to call it.
- **When to call** — concrete trigger phrasing (e.g. "User mentions products, asks 'do you have'").
- **Parameters** — typed, with descriptions and constraints; mark required vs optional clearly; include example values in descriptions.
- **Returns** — the output shape (JSON schema).
- **Error cases** — how the tool behaves on bad input (e.g. empty query → empty results, do not error).

A tool inventory captures: number, name, type (Read/Write), description, input, output.

## Integration map — third-party services

| Need | Options |
|------|---------|
| Web scraping | Exa, Browserbase, Playwright |
| Web search | Tavily, Exa, SerpAPI |
| Browser automation | Stagehand (JS), Browser Use (Python) |
| Email | Gmail API, SendGrid, Resend |
| Calendar | Google Calendar, Outlook |
| CRM | Salesforce, HubSpot |
| Project management | Jira, Linear, GitHub Issues |
| Vector search | Pinecone, pgvector, Chroma |
| Document storage | S3, GCS, Supabase |
| Database | Postgres, Supabase, PlanetScale |

Principle: when many integrations are needed, use an "agentic iPaaS" (Composio, Pipedream) to avoid months of integration work.

## MCP decision tree

MCP (Model Context Protocol) is the "USB-C port for AI applications."

**Build an MCP Client when:**
- The roadmap includes many third-party integrations.
- You want to use community-built MCP servers.
- You are building a platform that other agents connect to.

**Build an MCP Server when:**
- You are building a tool that other agents should use.
- You want to expose your API to the AI ecosystem.
- You have a data source multiple agents need.

**Skip MCP when:**
- You only need a few custom tools.
- Tools are tightly coupled to your agent logic.
- You are prototyping and speed matters more than standards.

MCP considerations: there is no centralized registry yet — document your servers clearly. Vet community servers before production use. Each server has its own config schema — test integration thoroughly.

## Performance targets

| Tool type | Target | Fallback |
|-----------|--------|----------|
| Read (cache hit) | < 200ms | Return stale data |
| Read (cache miss) | < 1s | Show loading state |
| Write | < 2s | Optimistic response |
| Search | < 3s | Partial results |

## Error shape

- All tools MUST return structured errors — never throw exceptions.
- Include an error code, a message, and a suggested action.
- The agent should retry transient errors (429, 503) with backoff.
- The agent should NOT retry client errors (400, 404).

## Token efficiency

- Tool outputs should be concise — large payloads waste context.
- Paginate large result sets (return top N, offer a "more" action).
- Summarize verbose API responses before returning them to the agent.
