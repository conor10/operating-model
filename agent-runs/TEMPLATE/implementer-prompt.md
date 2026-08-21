# Implementer Prompt — <boundary name>

You are the implementer for this repo (read `AGENTS.md` first — it is
binding). <One-paragraph context: what this boundary delivers and why.>

## Hard invariants (violating any of these is a failed boundary)

- <Things that must provably not change — pinned artifacts, hashes,
  protected files. Give the implementer the proof command where possible.>

## Requirements (stable IDs — reference from tests as `# verifies: XX-nn`)

- **XX-01 — <Name>.** <Testable requirement.>
- **XX-02 — <Name>.** <Testable requirement.>

## Out of scope

<Explicit non-goals; files/areas not to touch; decisions already made
elsewhere (do not edit `DECISIONS.md`).>

## Quality gates (all must pass; record outcomes)

<The project's real commands — tests, typecheck, lint, format, smoke —
plus any boundary-specific proof (determinism probes, regeneration
checks). If this boundary adds `# verifies:` markers, regenerate
`docs/TRACEABILITY.md` and keep its staleness guard green.>

## Deliverables

Working tree only — do not commit; the operator commits after judge
review. Write `implementer-summary.md` in this run directory: what was
built, the requirement→test map (every XX-nn), gate outcomes, and any
declared deviations with reasons. Deviations from this prompt are
acceptable only if declared there.
