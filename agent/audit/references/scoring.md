# Scoring

## Per-criterion scale (0–3)

Each of the 35 criteria is scored on this scale:

| Score | Label | Meaning |
|-------|-------|---------|
| `N/A` | Not Applicable | The criterion's stated N/A condition is met. Excluded from numerator **and** denominator. |
| `0` | Not Started | The criterion is not addressed at all. No evidence found. |
| `1` | Basic | Partially addressed; significant gaps remain. |
| `2` | Good | Mostly addressed; only minor gaps. |
| `3` | Excellent | Fully addressed; follows best practice. |

**Evidence rule:** any score above `0` must be backed by a concrete artifact — a
file path, code signature, or doc section. Absence of evidence is `0`, not a guess.
Each `d*.md` rubric gives explicit 0/1/2/3 anchor descriptions per criterion;
use those anchors, not intuition.

## N/A handling

- Use `N/A` **only** when the criterion's rubric explicitly permits it.
- `N/A` criteria are dropped from the count entirely. They neither raise nor lower
  any score.
- **Design-only audits:** D2 and D4 criteria that an implementation would evidence
  (a live pause/resume API, a real JSON tool schema) may be `N/A` when only design
  docs exist. Stated *intent* in a design doc is not implementation evidence — but
  a design doc that thoroughly *designs* the mechanism can still earn 1–3 on
  criteria that are about design quality (e.g. D1.1, D1.2, D6.1).

## Dimension roll-up

For each dimension:

```
dimension_score   = Σ (scores of non-N/A criteria)
dimension_max     = 3 × (count of non-N/A criteria)
dimension_percent = round(100 × dimension_score / dimension_max)
```

If every criterion in a dimension is `N/A`, report the dimension as `N/A` and
exclude it from the overall roll-up.

## Overall roll-up

```
overall_score   = Σ dimension_score   (across all 7 dimensions)
overall_max     = Σ dimension_max     (across all 7 dimensions)
overall_percent = round(100 × overall_score / overall_max)
```

Report the overall result as `X / Y (Z%)` where:
- `X` = overall_score
- `Y` = overall_max — the **post-N/A** maximum (the theoretical ceiling is
  `105 = 35 × 3`; `Y` is lower whenever any criterion is N/A)
- `Z` = overall_percent

## Maturity bands

Map `overall_percent` to a maturity band:

| Band | Range | Description |
|------|-------|-------------|
| **Prototype** | 0–20% | Agent works but lacks production safeguards. |
| **MVP** | 21–45% | Core patterns in place; gaps in eval and security. |
| **Production-Ready** | 46–70% | Solid foundation; iterating on quality. |
| **Mature** | 71–90% | Comprehensive coverage; continuous improvement. |
| **Best-in-Class** | 91–100% | Industry-leading agent practices. |

## Security override gate

D7 produces two qualitative outputs in addition to its numeric score:

- **Security Risk verdict:** `Low` / `Medium` / `High` / `Critical`.
- **Lethal Trifecta Status:** `SAFE` / `AT RISK` / `VULNERABLE`.

**The gate:** if either of the following is true —
- `Lethal Trifecta Status = VULNERABLE`, or
- any D7 criterion scored at a level its rubric flags as **Critical**

— then the **displayed** maturity band is **capped at MVP**, regardless of the
computed percent. The report must:
- still show the true `overall_percent` and `overall_score / overall_max`,
- display the band as `MVP (capped)` rather than the band the percent would imply,
- carry the banner:
  `Maturity capped — unresolved Critical security finding.`

The cap is a safety mechanism: an agent cannot be called "Mature" or
"Production-Ready" while it is exploitable. Removing the Critical finding (or
breaking a leg of the trifecta) lifts the cap on the next audit.
