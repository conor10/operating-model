# Agent Operating Model

A reference operating model for agentic engineering — workflow, decision capture, and stakeholder collaboration for teams building with agents. Read more [here](https://conorsvensson.com/writing/why-you-need-an-operating-model-for-agentic-engineering/).

The default operating model is:

1. **Planner / Architect**: Claude, Fable, or another high-reasoning model plans the work.
2. **Implementer**: Codex / GPT edits code in the primary workspace.
3. **Judge / Reviewer**: Claude, Fable, or another independent model reviews the frozen diff.
4. **Human**: accepts direction, resolves tradeoffs, and decides whether to merge or deploy.

The template is deliberately small. `AGENTS.md` is the portable project contract. Deeper process belongs in `docs/OPERATING_MODEL.md`, and reusable role prompts live in `prompts/`.

## What's in the box

- `AGENTS.md` — the binding contract (modes, rules, gates)
- `STATUS.md` / `DECISIONS.md` / `ROADMAP.md` — state and decision docs
- `TASKS.md` — agent-readable task register (per-person assignments; optional)
- `SME-REVIEW.md` — domain-question register with interim defaults (optional;
  recreated on first need per the `AGENTS.md` rule)
- `prompts/` — planner / implementer / reviewer / advisory role prompts
- `agent-runs/TEMPLATE/` — run-record skeletons: manifest, dispatch
  prompt (stable requirement IDs), implementer summary, judge output
- `tools/traceability.py` — generates `docs/TRACEABILITY.md` from
  requirement IDs and `# verifies:` test markers (wire its staleness test
  once the project has a suite)
- `docs/OPERATING_MODEL.md` — roles plus the boundary lifecycle
  (plan → decisions → dispatch → implement → judge re-check → human freeze)

## Practices baked in (learned the expensive way)

- Acceptance criteria are **stable requirement IDs**; tests carry
  `# verifies:` markers; the traceability matrix is generated, never
  hand-edited, and guarded against staleness.
- Implementers **declare deviations** instead of hiding them; judges
  adjudicate explicitly — a plausible deviation is often the prompt's error.
- Judges **reproduce gates and probe real artifacts** rather than
  trusting summaries, and record their own probe errors honestly.
- Commits are gated on **real exit codes** (never `command | tail`
  pipelines), and the human freeze commit carries implementation and run
  record together.
- Anything a model sees — prompts, schemas, and the mechanism delivering
  them — is **versioned configuration**, never an unpinned implementation
  choice.
- Formats evolve **additively with tolerant readers**; parsers fail
  closed; published artifacts are immutable (a change is a new version);
  history is never rewritten.
- Domain questions get **registered with interim defaults**, not decided
  silently by whichever agent hit them first.

## Quick Start

Copy this operating model into a new project root:

```bash
cp -R ~/code/conor10/operating-model/. /path/to/new-project/
```

Then customize:

1. Update `README.md` with the actual project overview and setup commands.
2. Update `AGENTS.md` with project-specific rules, commands, quality gates, and security constraints.
3. Update `STATUS.md` with the current phase and next step.
4. Record important tradeoffs in `DECISIONS.md`.
5. Keep reusable prompts in `prompts/`; keep task-specific run logs in `agent-runs/`.
6. Trim to fit: `TASKS.md` (multi-person delegation) and `SME-REVIEW.md`
   (domain-expert questions) are optional — delete them if they don't apply
   yet. The rule in `AGENTS.md` recreates the domain-question register the
   first time a question actually arises.

For Claude Code compatibility, this template includes `CLAUDE.md` that imports `AGENTS.md`.

## Primary Workspace Recommendation

Use **Codex app** as the primary implementation workspace:

- one working tree owns file edits
- tests and verification happen where the code changes
- Codex can use native subagents for bounded Codex-on-Codex exploration or review
- final integration stays in one place

Use Claude/Fable as planner and judge around that workspace.

```text
Claude/Fable planner -> Codex implementer -> frozen diff/commit -> Claude/Fable judge -> Codex fixes -> human merge
```

## Copy/Paste Workflow

Use this first. It is lower ceremony than orchestration tooling and exposes where the process needs automation.

### 1. Planner / Architect

Open Claude/Fable and paste `prompts/planner.md` plus the task.

Expected output:

- assumptions
- proposed approach
- likely files/modules
- acceptance criteria
- verification plan
- risks and open questions

Do not allow planner edits.

### 2. Codex Implementer

Open the project in Codex app. Paste the planner output plus `prompts/implementer.md`.

Codex should:

- inspect relevant files
- make scoped edits
- run verification
- report changed files, test evidence, deviations, and risks

### 3. Freeze Review Boundary

Prefer a commit or branch. A saved diff is fine for local review:

```bash
mkdir -p agent-runs/$(date +%F)-short-task-name
git diff > agent-runs/$(date +%F)-short-task-name/final.diff
```

### 4. Judge / Reviewer

Open Claude/Fable and paste:

- original request
- planner output
- Codex implementation summary
- test evidence
- frozen diff or commit
- `prompts/reviewer.md`

The judge is read-only. Findings should be severity-ranked with file/line references.

### 5. Fix Accepted Findings

Bring accepted findings back to Codex. Codex fixes, reruns verification, and summarizes.

### 6. Human Decision

The human decides whether the change is ready to merge, needs another review, or should be re-scoped.

## ACPx Workflow

Use ACPx when you want less copy/paste and more repeatable cross-agent sessions.

ACPx is useful for:

- running planner/judge sessions outside the Codex app
- comparing model reviews
- queueing prompts against named sessions
- keeping the implementation workspace separate from the review workspace

Recommended pattern:

```bash
# Planner session, read-only
acpx fable -s plan-short-task "Use the repo AGENTS.md and prompts/planner.md. Plan this task. Do not edit files."

# Codex app implements in the primary workspace.

# Freeze boundary
git diff > agent-runs/2026-07-09-short-task/final.diff

# Judge session, read-only
acpx fable -s judge-short-task "Use prompts/reviewer.md. Review agent-runs/2026-07-09-short-task/final.diff. Do not edit files."
```

If your ACPx command names differ, keep the same boundary: planner and judge are read-only; Codex owns edits.

For safer review isolation, review from a separate worktree:

```bash
git worktree add ../project-review HEAD
```

Then point the reviewer at that worktree or a saved diff.

## What To Track

Use two histories:

- `DECISIONS.md`: durable decisions and why they were made.
- `agent-runs/`: meaningful agent prompts, outputs, reviews, and summaries.

Do not log every casual chat. Track runs that affected code, architecture, process, or direction.

## When To Add More Process

Start small. Add ceremony only when needed:

- Add `docs/ARCHITECTURE.md` when people cannot quickly understand the system shape.
- Add `docs/RUNBOOK.md` when deploy/support/runtime steps matter.
- Add `docs/decisions/` ADR files when `DECISIONS.md` gets too long.
- Add stricter phase gates when multiple agents or humans are working in parallel.

## References

- AGENTS.md: https://agents.md/
- ACPx: https://github.com/openclaw/acpx
- codex-first skill: https://github.com/steipete/agent-scripts/blob/main/skills/codex-first/SKILL.md
- agent-skills: https://github.com/addyosmani/agent-skills

## About

Maintained by Conor Svensson. I work with a small number of teams putting agentic engineering to work in regulated industries. Learn more [here](https://conorsvensson.com/advisory/).
