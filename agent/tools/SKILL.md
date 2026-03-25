---
name: agent:tools
description: Tool Design - guides through agent tool architecture, MCP integration, third-party tool selection, and tool schema design
argument-hint: ["description or path"]
---

# Tool Design

Guides the user through designing tools for AI agents. Based on "Principles of Building AI Agents" (Bhagwat & Gienow, 2025), Chapters 6, 10-11: Tool Calling, Third-Party Tools, and MCP.

## When to use

Use this skill when the user needs to:
- Design the tool set for an AI agent
- Decompose complex operations into reusable tools
- Write tool schemas with clear descriptions
- Decide between custom tools, third-party integrations, and MCP
- Plan MCP server or client integration

## Instructions

### Step 1: Understand the Agent's Needs

Use the `AskUserQuestion` tool to gather context:
1. What tasks does the agent perform? (list all actions)
2. What external systems does it interact with? (APIs, databases, services)
3. What data does it need to access? (user data, documents, web)
4. Is this agent part of a multi-agent system? (tools may be shared)
5. Is there an existing agent design? (check `.specs/<spec-name>/`)

Read any existing spec documents before proceeding.

### Step 2: Decompose into Operations

Apply the principle: **Think like an analyst — decompose into clear, reusable operations.**

Guide the user through decomposition:

1. **List all actions** the agent needs to perform
2. **Group by data source** — operations on the same data/API belong together
3. **Separate read from write** — reading data and modifying data should be different tools
4. **Make tools atomic** — each tool does ONE thing well
5. **Name semantically** — `searchProducts`, `getOrderStatus`, not `doStuff` or `handleRequest`

**Common mistake:** Trying to build one tool that does everything. If a human analyst would follow specific queries/operations, encode each as a separate tool.

Use `AskUserQuestion` to iterate on the tool list with the user.

Output:

```markdown
## Tool Inventory

| # | Tool Name | Type | Description | Input | Output |
|---|-----------|------|-------------|-------|--------|
| 1 | [searchProducts] | Read | [Search product catalog by query] | [query: string, limit?: number] | [Product[]] |
| 2 | [getOrderStatus] | Read | [Get order details by ID] | [orderId: string] | [Order] |
| 3 | [updateInventory] | Write | [Update stock count for a product] | [productId: string, quantity: number] | [success: boolean] |
```

### Step 3: Design Tool Schemas

For each tool, write a detailed schema. **Tool design is the most important step in building an agent.**

**Schema guidelines:**
- **Description:** Both what the tool does AND when to call it
- **Parameters:** Typed, with descriptions and constraints
- **Required vs optional:** Mark clearly
- **Examples:** Include example inputs in descriptions

```markdown
## Tool Schemas

### Tool: searchProducts

**Description:** Search the product catalog by keyword query. Call this tool when the user asks about products, product availability, or wants recommendations. Returns up to `limit` products sorted by relevance.

**When to call:** User mentions products, asks "do you have", wants to browse or compare items.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | string | Yes | Search keywords (e.g., "red running shoes size 10") |
| limit | number | No | Max results to return (default: 5, max: 20) |
| category | string | No | Filter by category slug (e.g., "shoes", "electronics") |

**Returns:**
```json
{
  "products": [
    { "id": "string", "name": "string", "price": "number", "inStock": "boolean" }
  ],
  "totalCount": "number"
}
```

**Error cases:**
- Empty query → return empty results, do not error
- Invalid category → return empty results with suggestion
```

Repeat for each tool.

### Step 4: Third-Party Integrations

Identify which tools need third-party services. Use `AskUserQuestion` to explore:

```markdown
## Integration Map

### Web & Search
| Need | Options | Recommendation |
|------|---------|----------------|
| Web scraping | Exa, Browserbase, Playwright | [Recommendation based on use case] |
| Web search | Tavily, Exa, SerpAPI | [Recommendation] |
| Browser automation | Stagehand (JS), Browser Use (Python) | [Recommendation] |

### Business Systems
| Need | Options | Recommendation |
|------|---------|----------------|
| Email | Gmail API, SendGrid, Resend | [Recommendation] |
| Calendar | Google Calendar, Outlook | [Recommendation] |
| CRM | Salesforce, HubSpot | [Recommendation] |
| Project management | Jira, Linear, GitHub Issues | [Recommendation] |

### Data & Storage
| Need | Options | Recommendation |
|------|---------|----------------|
| Vector search | Pinecone, pgvector, Chroma | [Recommendation] |
| Document storage | S3, GCS, Supabase | [Recommendation] |
| Database | Postgres, Supabase, PlanetScale | [Recommendation] |
```

**Principle:** Use an "agentic iPaaS" (Composio, Pipedream) to avoid months of integration work when you need many integrations.

### Step 5: MCP Strategy

Determine if MCP (Model Context Protocol) applies. MCP = "USB-C port for AI applications."

Use `AskUserQuestion`:

**Build an MCP Client when:**
- Your roadmap includes many third-party integrations
- You want to use community-built MCP servers
- You're building a platform that other agents connect to

**Build an MCP Server when:**
- You're building a tool that other agents should use
- You want to expose your API to the AI ecosystem
- You have a data source that multiple agents need

**Skip MCP when:**
- You only need a few custom tools
- Your tools are tightly coupled to your agent logic
- You're prototyping and speed matters more than standards

```markdown
## MCP Strategy

**Decision:** [Build MCP Client / Build MCP Server / Skip MCP / Both]

### MCP Servers to Use
| Server | Purpose | Source |
|--------|---------|--------|
| [Server name] | [What it provides] | [Community / Custom] |

### MCP Server to Build
| Endpoint | Tools Exposed | Auth |
|----------|--------------|------|
| [/your-service] | [tool1, tool2] | [OAuth / API key] |

### MCP Considerations
- **Discovery:** No centralized registry yet — document your servers clearly
- **Quality:** Vet community servers before production use
- **Configuration:** Each server has its own config schema — test integration thoroughly
```

### Step 6: Tool Performance Guidelines

```markdown
## Tool Performance

### Response Time Targets
| Tool Type | Target | Fallback |
|-----------|--------|----------|
| Read (cache hit) | < 200ms | Return stale data |
| Read (cache miss) | < 1s | Show loading state |
| Write | < 2s | Optimistic response |
| Search | < 3s | Partial results |

### Error Handling
- All tools MUST return structured errors (not throw exceptions)
- Include error code, message, and suggested action
- Agent should retry transient errors (429, 503) with backoff
- Agent should NOT retry client errors (400, 404)

### Token Efficiency
- Tool outputs should be concise — large payloads waste context
- Paginate large result sets (return top N, offer "more" action)
- Summarize verbose API responses before returning to agent
```

### Step 7: Summarize and Offer Next Steps

Present all findings to the user as a structured summary in the conversation. Do NOT write to `.specs/` — this skill works directly.

Use `AskUserQuestion` to offer:
1. **Implement tools** — scaffold tool code based on the schemas designed above
2. **Build MCP server** — generate MCP server code if recommended
3. **Comprehensive design** — run `agent:design` to cover all areas with a spec

## Arguments

- `$ARGUMENTS` (`$0`) - Optional description of the agent or path to existing tool code

Examples:
- `agent:tools customer-support chatbot` — design tools for a support chatbot
- `agent:tools src/agents/tools/` — review and improve existing tool implementations
- `agent:tools` — start fresh
