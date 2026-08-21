# Planner / Architect Prompt

Mode: planner/architect only. Do not edit files.

Follow `AGENTS.md` and the project operating model.

Task:

```text
<paste task here>
```

Produce:

1. Problem framing
2. Assumptions
3. Open questions or blockers
4. Proposed approach
5. Files/modules likely to change
6. Acceptance criteria as stable requirement IDs (`XX-nn`) — these become
   the dispatch prompt's requirements and the tests' `# verifies:` markers
7. Verification plan
8. Risks and tradeoffs
9. Explicit non-goals

Decisions the plan embeds are recorded in `DECISIONS.md` on approval,
before any dispatch. Domain questions the plan cannot resolve go to
`SME-REVIEW.md` with an interim default — never decided silently.

If the task is unsafe, vague, or too broad, push back and propose a smaller slice.
