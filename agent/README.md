# Agent Skills

Skills for designing, reviewing, and securing AI agent systems. Based on "Patterns for Building AI Agents" and "Principles of Building AI Agents" (Bhagwat & Gienow, 2025).

## Two-Tier Architecture

### Spec Skills (produce `.specs/` documents)

| Skill | Description |
|-------|-------------|
| `agent:design` | Comprehensive agent system design — orchestrates research sub-agents, compiles unified design document |
| `agent:eval` | Evaluation system — failure modes, metrics, eval test suite, SME labeling, production data pipeline |
| `agent:secure` | Security audit — lethal trifecta, sandboxing, access control, guardrails |
| `agent:review` | Full pattern review — scores all patterns 0-3, maturity assessment, prioritized recommendations |

### Action Skills (work directly, no files)

| Skill | Description |
|-------|-------------|
| `agent:prompt` | Prompt engineering — model selection, system prompt architecture, few-shot examples |
| `agent:tools` | Tool design — operation decomposition, schemas, MCP strategy, third-party integrations |
| `agent:memory` | Memory architecture — working memory, semantic recall, memory processors |
| `agent:workflow` | Workflow design — graph primitives, suspend/resume, streaming, observability |
| `agent:rag` | RAG pipeline — decision tree, chunking, embedding, vector DB, retrieval tuning |
| `agent:multi` | Multi-agent systems — org design, supervision patterns, control flow, composition |
| `agent:context` | Context engineering — parallelization, sharing, failure modes, compression, error feedback |

## How They Work Together

`agent:design` is the main orchestrator. It launches parallel research sub-agents, each applying the methodology of the corresponding action skill:

```
/agent:design my-agent

  agent:design (orchestrator)
  ├── Gathers requirements, maps capabilities
  ├── Launches parallel research:
  │   ├── Prompt research    (agent:prompt methodology)
  │   ├── Tool research      (agent:tools methodology)
  │   ├── Memory research    (agent:memory methodology)
  │   ├── Workflow research   (agent:workflow methodology)
  │   ├── RAG research       (agent:rag methodology)
  │   ├── Multi-agent research (agent:multi methodology)
  │   └── Context research   (agent:context methodology)
  ├── Compiles findings into unified design
  └── Outputs .specs/my-agent/agent-design.md
```

Action skills can also be used **standalone** for focused work on a single area:

```
/agent:prompt              # Just work on prompts
/agent:tools               # Just design tools
/agent:rag                 # Just figure out RAG strategy
```

After design, use the validation skills:

```
/agent:review my-agent     # Score against all patterns
/agent:secure my-agent     # Security audit
/agent:eval my-agent       # Set up evaluation system
```

## Usage Examples

### Full design workflow

```bash
/agent:design my-chatbot           # Comprehensive design → .specs/my-chatbot/agent-design.md
/agent:secure my-chatbot           # Security audit → .specs/my-chatbot/agent-security.md
/agent:eval my-chatbot             # Eval system → .specs/my-chatbot/agent-eval.md
/agent:review my-chatbot           # Pattern review (scored report)
```

### Focused single-area work

```bash
/agent:prompt                      # Improve prompts for current agent
/agent:tools src/agents/support.ts # Review tool design in existing code
/agent:memory                      # Design memory architecture
/agent:rag                         # Decide if RAG is needed, design pipeline
/agent:workflow                    # Design workflow graph with streaming
/agent:multi                       # Design multi-agent system
/agent:context                     # Optimize context strategy
```

## Output Structure

```
.specs/
└── <agent-name>/
    ├── agent-design.md     # Unified design (from agent:design)
    ├── agent-eval.md       # Evaluation system (from agent:eval)
    └── agent-security.md   # Security audit (from agent:secure)
```

## Installation

```bash
# All agent skills
npx skills add ikatsuba/skills/agent

# Individual skills
npx skills add ikatsuba/skills --skill agent:design
npx skills add ikatsuba/skills --skill agent:eval
npx skills add ikatsuba/skills --skill agent:secure
npx skills add ikatsuba/skills --skill agent:review
npx skills add ikatsuba/skills --skill agent:prompt
npx skills add ikatsuba/skills --skill agent:tools
npx skills add ikatsuba/skills --skill agent:memory
npx skills add ikatsuba/skills --skill agent:workflow
npx skills add ikatsuba/skills --skill agent:rag
npx skills add ikatsuba/skills --skill agent:multi
npx skills add ikatsuba/skills --skill agent:context
```
