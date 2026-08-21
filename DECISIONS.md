# Decision Log

Record non-trivial decisions here. Keep entries concise and useful for future humans.

## DEC-001: Adopt lightweight agent operating model

- **Date:** YYYY-MM-DD
- **Status:** Accepted
- **Decision:** Use `AGENTS.md`, `STATUS.md`, `DECISIONS.md`, reusable prompts, and optional agent-run records as the project operating layer.
- **Rationale:** The project should be easy for humans and agents to understand without reverse-engineering prior chats.
- **Alternatives considered:** No operating layer; heavyweight multi-agent process from day one.
- **Consequences:** New work should respect the repo contract and record durable decisions.

## DEC-002: Operating model v2 — practices from the first production use

- **Date:** 2026-08-05
- **Status:** Accepted
- **Decision:** Fold the practices proven during the operating model's first
  sustained production use (a real project run with the
  planner → implementer → judge → freeze loop for ~20 boundaries) into the
  template: requirement-ID traceability with a generated matrix and
  staleness guard; the boundary lifecycle with human freeze; the
  declared-deviation protocol; judge independent-reproduction practice;
  the task register (`TASKS.md`) and domain-question register
  (`SME-REVIEW.md`); and hardened working rules (real-exit-code commit
  gating, model-visible = versioned configuration, additive formats with
  tolerant readers, immutable published artifacts, history never
  rewritten).
- **Rationale:** Each practice earned its place by catching or preventing
  a real defect; a fresh project should start with them rather than
  rediscover them.
- **Alternatives considered:** Keeping the template minimal and importing
  practices per-project (loses them exactly when a project starts);
  linking out to the source project (couples the template to one repo's
  history).
- **Consequences:** New projects copy these files as the starting
  contract; the template stays small by folding lessons into existing
  files rather than adding process documents.

## Template

## DEC-XXX: Title

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded | Rejected
- **Decision:** What was decided?
- **Rationale:** Why?
- **Alternatives considered:** What else was considered?
- **Consequences:** What changes because of this?
- **Related runs:** `agent-runs/YYYY-MM-DD-short-task/`
