# Evidence Rule — no invention, cite sources

This rule governs every factual claim about anything **external to this codebase**:
a library, framework, language, runtime, API, protocol, CLI tool, cloud service,
version number, default value, rate limit, pricing, or "best practice".

The failure mode this prevents: stating something from model memory as if it were
verified. Training data is stale and frequently wrong about current APIs, defaults,
and version-specific behaviour. **Do not guess. Fetch, then write.**

## Mandatory tool use

Before writing any external claim, retrieve it from a live source:

1. **Library / framework / SDK / API docs → context7 MCP.** Use `resolve-library-id`
   to find the library, then `query-docs` to pull current documentation. Prefer this
   over web search for anything that has official docs — even libraries you think you
   know. Your memory of an API may not reflect recent changes.
2. **Everything else → `WebSearch` + `WebFetch`.** Best practices, architectural
   recommendations, known pitfalls, benchmarks, comparisons, release notes, changelogs.
   `WebSearch` to find the authoritative page, `WebFetch` to read it.
3. **Codebase facts → read the actual files.** Never assert that a file, function,
   type, or pattern exists without having read it.

## The guardrail

- **No source → no claim.** If you cannot back a statement with a fetched source (or
  a file you read), do not state it as fact. Write `needs investigation` instead and
  move on. An honest gap is useful; a confident fabrication is a landmine.
- **Cite specifically.** Vague "according to the docs" is not a citation. Give the
  exact URL (or library + doc section from context7) and what it said.
- **Date-stamp.** Record the date you fetched each source — external facts rot.
- **Distinguish verified from inferred.** If you reason beyond what a source states,
  label it as inference, not as documented fact.

## Sources section (required output)

Every variant / problem area / external assertion carries its evidence inline and
contributes to a `Sources` list:

```markdown
**Evidence:** Next.js App Router caches `fetch` by default; opt out with
`cache: 'no-store'`. [next-caching] Verified against current docs.

...

## Sources
- [next-caching] https://nextjs.org/docs/app/building-your-application/caching — fetched 2026-05-29 (context7: /vercel/next.js)
- [pg-pool] https://node-postgres.com/apis/pool — fetched 2026-05-29
```

Anything tagged `needs investigation` must NOT appear in the Sources list — it is an
open question, not a finding.

## For subagents

When delegating research to a subagent, include this rule verbatim in its prompt and
require it to:
- use context7 / `WebSearch` / `WebFetch` for every external claim,
- return a `Sources` list with URLs and fetch dates,
- mark anything it could not verify as `needs investigation`.

A subagent result that asserts external facts with no citations is **rejected** — send
it back to re-investigate with sources, or downgrade its unsourced claims to
`needs investigation` before using them.
