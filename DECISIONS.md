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

## DEC-003: Pull requests are the team-scale freeze boundary

- **Date:** 2026-08-22
- **Status:** Accepted
- **Decision:** Name pull requests explicitly in the operating model: with
  more than one committer, a PR pinned at its head SHA is the frozen
  boundary, the judge reviews that SHA, and the human merge — enforced by
  branch protection with required review — is the freeze. The local flow
  (uncommitted tree, saved diff, freeze commit) remains the solo default.
- **Rationale:** The contract said the human is final merge authority, but
  the lifecycle only showed a local freeze commit, implying direct pushes
  to main — the very thing `TASKS.md` forbids for agents and branch
  protection forbids for teams. The PR is where the operating model stops
  being documentation and becomes machine-enforced.
- **Alternatives considered:** Leaving PRs as one unremarked option among
  the handoff boundaries (team readers would have to derive the mapping
  themselves); mandating PRs in all modes (adds ceremony the solo flow
  does not need).
- **Consequences:** `AGENTS.md` lists pull requests as a handoff boundary;
  `docs/OPERATING_MODEL.md` maps the lifecycle onto a PR and requires
  review at a pinned head SHA, never a moving branch.

## Template

## DEC-XXX: Title

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded | Rejected
- **Decision:** What was decided?
- **Rationale:** Why?
- **Alternatives considered:** What else was considered?
- **Consequences:** What changes because of this?
- **Related runs:** `agent-runs/YYYY-MM-DD-short-task/`
