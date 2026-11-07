# Session: 2026-11-07 — Retire `omarchy` from the ecosystem registry (D231, K51)

- **CLI tool:** OpenCode (`opencode`) `2.2.5`
- **Model:** `beam-free` (variant: high)
- **Transcript:** Retained privately by the author.
- **Scope:** `ecosystem.json`, `ECOSYSTEM.md`, `/var/cache/local-patches`, `~/pkgs/omarchy`.

## User direction

Fred's guiding prompts, verbatim:

> Implement the approved Tamlinux 0.6.16 plan (Decision D231). (excerpt)

## Decisions and implementation

- Retired `omarchy` in the registry via `bin/tam-ecosystem retire omarchy` and re-rendered `ECOSYSTEM.md`.
- Removed `omarchy` from `/var/cache/local-patches` (`repo-remove`) and deleted `~/pkgs/omarchy`.
- Verified the registry with `bin/tam-ecosystem verify` (all checks pass).