# Operating Model

This repo uses a lightweight planner -> implementer -> judge workflow.

## Roles

### Planner / Architect

Usually Claude, Fable, or another high-reasoning model.

Responsibilities:

- clarify the problem
- identify assumptions and blockers
- propose architecture and file scope
- define acceptance criteria
- define verification plan
- flag risks and tradeoffs

Planner is read-only by default.

### Implementer / Integrator

Usually Codex / GPT in the primary implementation workspace.

Responsibilities:

- inspect relevant files
- implement the accepted plan
- adapt when the plan is wrong
- run verification
- summarize changed files, tests, deviations, and risks

Implementer owns file edits.

### Judge / Reviewer

Usually Claude, Fable, or a different high-reasoning model from the implementer.

Responsibilities:

- review a frozen diff, commit, or branch
- find bugs and missing tests
- check acceptance criteria
- check security/privacy/runtime risks
- recommend ship/no-ship

Judge is read-only by default.

### Human

Responsibilities:

- approve direction
- resolve tradeoffs
- accept or reject review findings
- decide merge and deploy

## Standard Workflow

1. Human states task and mode.
2. Planner produces plan and acceptance criteria.
3. Human approves or edits plan.
4. Implementer edits code and verifies.
5. Implementer freezes a diff, branch, or commit.
6. Judge reviews frozen boundary.
7. Implementer fixes accepted findings.
8. Human decides merge/deploy.

## Boundary Lifecycle (the proven ritual)

For each substantial unit of work ("boundary"):

1. **Plan approved** and any decisions it embeds are recorded in
   `DECISIONS.md` *before* dispatch — the implementer never edits the
   decision log.
2. **Dispatch prompt cut and committed** (`agent-runs/<run>/implementer-prompt.md`),
   with stable requirement IDs (`XX-nn`), hard invariants with proof
   commands, explicit out-of-scope, and the deliverables contract.
3. **Implementer works in the working tree and does not commit.** Tests
   carry `# verifies: XX-nn` markers; deviations from the prompt are
   declared in the summary, never silent.
4. **Judge re-check**: independently reproduce every gate, probe the real
   artifacts (not the summary), verify each requirement and invariant,
   adjudicate declared deviations, and record honest judge-process notes
   (a failed probe is judge-side until verified directly). Verdict:
   Ship / Ship with known issues / No ship.
5. **Human freeze**: one commit carrying the implementation and the run
   record together; state docs (`STATUS.md`, registers) update at freeze,
   with the suite verified green by real exit status immediately before.
6. **Anything the judge or run surfaced** that is a domain question goes
   to `SME-REVIEW.md`; process lessons go into `AGENTS.md` working rules.

## Handoff Boundaries

Use one of:

- commit hash
- branch name
- pull request
- git worktree
- saved diff under `agent-runs/.../final.diff`

Avoid reviewing a moving working tree.

## Agent Run Records

Record meaningful runs under `agent-runs/` when they affect architecture, code, process, or direction.

Each run should include:

- prompt or prompt reference
- context summary
- model output
- test evidence
- review output
- final summary

Do not store secrets or sensitive customer data.
