---
name: agent:developer
description: Designs and builds AI agents. Use when working on agent architecture, prompts, model selection, tool design, MCP, memory, context engineering, RAG, graph workflows, multi-agent systems, evaluation, or production reliability.
---

# Agent Developer

A reference skill for designing and building AI agents. It carries no deep knowledge itself — it routes you to focused reference files, each loaded only when you need it.

Based on "Patterns for Building AI Agents" and "Principles of Building AI Agents" (Bhagwat & Gienow, 2025), plus the twelve-factor-agents methodology.

## How to use this skill

**Starting a new agent?** Read [references/architecture.md](references/architecture.md) first. It walks you through capability mapping and choosing an architecture (Single Agent, Router + Specialists, Coordinator + Workers, or Pipeline). The architecture decision determines which other references matter.

**Working on an existing agent?** Jump straight to the topic section below that matches the subsystem you are touching, and read its reference file.

Each reference file is dense, agent-readable knowledge meant to be consulted *while* building — frameworks, decision trees, matrices, and checklists.

## Architecture

Choosing the overall shape of the agent system: how many agents, how they relate, and how the design evolves.

- **Architecture & evolution**: Capability mapping, the architecture selection matrix, the human-in-the-loop framework, and dynamic-configuration signals. Read [references/architecture.md](references/architecture.md)

## Prompting & model selection

The model you pick and the prompt you write are the foundation of every agent.

- **Prompts & models**: Model-selection matrix, the five prompt-architecture layers, seed-crystal bootstrapping, few-shot guidelines, and the production checklist. Read [references/prompting.md](references/prompting.md)

## Tools

How the agent acts on the world. Tool design is the single most important step in building an agent.

- **Tool design**: Operation decomposition, the tool-schema template, the third-party integration map, the MCP decision tree, performance targets, and the structured error shape. Read [references/tools.md](references/tools.md)

## Memory

How the agent remembers across turns and sessions.

- **Memory architecture**: The three-layer memory model, the agent-type-to-layer matrix, the working-memory schema, semantic-recall configuration, and memory processors. Read [references/memory.md](references/memory.md)

## Context engineering

How context flows through the agent and how to keep the context window healthy.

- **Context strategy**: Parallelization rules, context-sharing strategies, the five context failure modes, compression strategy, and the error-feedback loop. Read [references/context.md](references/context.md)

## Workflows

When pure agentic looping is too unpredictable, give the agent explicit structure.

- **Graph workflows**: The four workflow primitives, suspend/resume, streaming, OpenTelemetry tracing, and workflow composition. Read [references/workflows.md](references/workflows.md)

## RAG

When the agent needs to retrieve knowledge from a corpus — and how to decide whether RAG is even the right tool.

- **RAG pipeline**: The RAG decision tree, chunking / embedding / vector-DB matrices, retrieval tuning, the pipeline architecture, and the quality checklist. Read [references/rag.md](references/rag.md)

## Multi-agent systems

When one agent is not enough and the work needs a team of collaborating agents.

- **Multi-agent design**: Single-vs-multi criteria, supervision patterns, organizational design, control flow, the A2A protocol, and failure handling. Read [references/multi-agent.md](references/multi-agent.md)

## Evaluation

Define what "good" looks like and measure it continuously.

- **Eval system**: The failure-mode taxonomy, business metrics, eval-suite structure, SME labeling, and the production-data pipeline. Read [references/evaluation.md](references/evaluation.md)

## Production reliability

Cross-cutting principles for making an agent reliable, debuggable, and operable in production.

- **Twelve-factor agents**: The twelve factors — natural-language-to-tool-calls, owning your prompts and context window, treating tools as structured outputs, unified state, launch/pause/resume, human contact as tool calls, owning control flow, compacting errors, small focused agents, triggering from anywhere, and the stateless-reducer model. Read [references/twelve-factor.md](references/twelve-factor.md)
