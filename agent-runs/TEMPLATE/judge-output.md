# Judge Output — <boundary name> — YYYY-MM-DD

- **Boundary:** <frozen diff / uncommitted working tree on top of
  `<commit>`; how it was dispatched.>
- **Verdict: Ship | Ship with known issues | No ship.**

<Independent verification — never trust the implementer summary alone:>

- **Gates reproduced:** <re-run every gate yourself; record results.>
- **Requirements verified:** <per XX-nn: the live probe or test you ran,
  not just "test exists". Prefer probing the real artifact.>
- **Invariants held:** <the proofs for each hard invariant.>
- **Deviations adjudicated:** <each declared deviation: in whose favor
  and why. Undeclared deviations found are findings.>
- **Judge-process notes:** <your own probe errors, honestly recorded,
  and how they resolved — a probe failure is not an implementation
  failure until verified directly.>
