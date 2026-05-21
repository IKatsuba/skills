# RAG Pipeline Design

How to design a Retrieval-Augmented Generation pipeline — and how to decide whether you need one.

## Do you actually need RAG?

Principle: **start simple, check quality, get complex.**

Recommended progression — try each before moving on:
1. Load the entire corpus into a large context window (Gemini 2M, Claude 200K).
2. Write functions that query the dataset and give them to the agent as tools (agentic RAG).
3. Only if 1 and 2 fail on quality, build a traditional RAG pipeline.

### Decision tree

**Corpus size:**
- < 200 pages → try full context loading first.
- 200-10,000 pages → consider agentic RAG (tools that query data) OR traditional RAG.
- > 10,000 pages → a traditional RAG pipeline is likely needed.

**Query pattern:**
- Factual lookup ("What is X?") → RAG works well.
- Analytical ("Compare X and Y across documents") → agentic RAG may be better.
- Conversational ("Tell me about...") → either works.

**Data structure:**
- Highly structured (tables, databases) → use tools/APIs, not RAG.
- Semi-structured (markdown, HTML) → RAG with format-specific chunking.
- Unstructured (PDFs, free text) → traditional RAG.

## Chunking matrix

| Strategy | Best for | Description |
|----------|----------|-------------|
| Recursive | General text | Splits by paragraph, then sentence, then character |
| Token-aware | LLM optimization | Splits by token count, respects model limits |
| Format-specific | Markdown/HTML/JSON | Uses document structure (headers, tags, keys) |
| Semantic | High quality needs | Uses an LLM to identify natural topic boundaries |

Parameters: chunk size 256-1024 tokens (smaller = more precise, larger = more context); overlap 50-200 tokens (prevents losing context at boundaries); metadata = title, source, date, section, page (enables filtered retrieval).

Document-specific rules: markdown → split on `##` headers, keep header as metadata; PDFs → page-based with overlap; code → function/class-level chunks; chat logs → message groups of N turns.

## Embedding matrix

| Model | Dimensions | Quality | Cost | Speed |
|-------|-----------|---------|------|-------|
| OpenAI text-embedding-3-large | 3072 | High | $0.13/M tokens | Fast |
| OpenAI text-embedding-3-small | 1536 | Good | $0.02/M tokens | Fast |
| Voyage voyage-3 | 1024 | High | $0.06/M tokens | Fast |
| Cohere embed-v3 | 1024 | High | $0.10/M tokens | Fast |
| Local (e5-large, BGE) | 1024 | Good | Free (compute) | Varies |

Indexing: similarity metric = cosine (most common); index type = HNSW (default, good speed/accuracy balance).

## Vector database matrix

Principle: **prevent infra sprawl — vector DB choice is mostly commoditized.**

| Option | When to choose | Pros | Cons |
|--------|---------------|------|------|
| **pgvector** (Postgres extension) | Already using Postgres | No new infra, familiar SQL, metadata filtering | May need tuning at scale |
| **Pinecone** (managed) | New project, want simplicity | Fully managed, fast, scalable | Additional service + cost |
| **Chroma** (open-source) | Local dev, small scale | Free, easy setup | Self-host in production |
| **Cloud-native** (Cloudflare, DataStax) | Already on that cloud | Integrated billing, low latency | Vendor lock-in |

## Retrieval tuning

Query strategy: topK 3-10 (chunks to retrieve); similarityThreshold 0.7-0.9 (min relevance); reranking yes/no (post-retrieval quality boost).

**Hybrid queries** — combine vector similarity with metadata filters: date range, category, source, user-access permission.

**Reranking** — use when quality matters more than latency: retrieve topK × 3 candidates, rerank with a cross-encoder, return topK. Models: Cohere Rerank, bge-reranker, cross-encoder/ms-marco. More expensive per query but runs only on candidates.

**Query transformation** — HyDE (generate a hypothetical answer, use it as the search query); multi-query (generate variations, merge results); step-back (abstract the query to a higher level, then search).

## Pipeline architecture

**Ingestion:** Load documents → Chunk → Enrich metadata (source, date, category, section) → Embed → Upsert into vector DB. Schedule: on change / nightly / manual.

**Query:** Receive query → Transform (optional) → Embed query with the same model as ingestion → Search vector DB (topK, metadata filters) → Rerank (optional) → Inject top chunks into LLM context as `<retrieved_documents>` → Generate response with source attribution.

## Quality checklist

**Retrieval:** relevant documents consistently in top-K; metadata filters working; no duplicate chunks; chunk size balances precision vs. context.

**Generation:** responses grounded in retrieved documents; accurate source attribution; agent says "I don't know" when no relevant chunks found; no hallucination beyond retrieved context.

**Operational:** ingestion runs on schedule; new documents available within SLA; vector DB latency within target; embedding costs within budget.
