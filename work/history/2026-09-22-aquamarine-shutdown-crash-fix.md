# Session: 2026-09-22 — Aquamarine shutdown crash fix (0.15.0-2.2)

- **Tool**: Codex API (CLI version not applicable)
- **Model**: GPT-6
- **Transcript**: Not found — details unverified. API conversation; no local Codex rollout transcript recorded.
- **Participants**: Fred, Codex
- **Fork patchset commit**: `1cda9c3` (cherry-picked from `704dbe9`)

## Guiding Prompts

> Can you trace the aquamarine function and see if you can find the source of the segfault? Any bug reports or PRs online that might be applicable?

> Can we fix the Aquamarine bug on this system?

## Decisions and Verification

- The 2026-09-22 Hyprland core showed a null connector at `CDRMBackend::flushAsyncCommitEvents()` in Aquamarine 0.15.0. Upstream [issue #383](https://github.com/hyprwm/aquamarine/issues/383) independently reports the exact stack and proposed one-line guard.
- Added that guard as a second fork patch, retaining the existing KMS disconnect fix from PR #395. Exported both patches into the Arch package recipe and built `aquamarine` and `aquamarine-debug` 0.15.0-2.2 with `makepkg`.
- The installed library's disassembly skips null connector entries before dereferencing them; the KMS disable string remains. The pacman hook reports `patched`, and `omarchy-fred-ecosystem verify aquamarine` passes.
- A live Hyprland shutdown has not been used as a test; the new library is loaded when a new graphical session starts.
