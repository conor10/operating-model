# Implementer Prompt

Mode: implement.

Follow `AGENTS.md`.

Use the approved planner output as guidance, not as infallible truth. Inspect relevant files before editing. Keep changes scoped. Do not overwrite unrelated changes.

Task:

```text
<paste approved task and planner output here>
```

Before editing:

1. Check git status.
2. Read relevant files.
3. State any assumption that materially affects implementation.

After editing:

1. Run relevant verification (judge commits nothing for you — leave the
   working tree uncommitted unless the dispatch says otherwise).
2. Write the summary into the run directory: changed files, the
   requirement→test map (every `XX-nn` with its `# verifies:` marker),
   gate outcomes by real exit status, and **declared deviations** — any
   departure from the dispatch prompt, with reasons. Undeclared
   deviations are findings; declared ones get adjudicated, often in your
   favor.
4. Note deviations from the plan.
5. Note remaining risks or blocked verification.

Do not commit unless explicitly asked.
