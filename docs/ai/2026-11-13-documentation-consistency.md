# 2026-11-13 — README documentation consistency

- **CLI Tool**: Codex CLI `0.169.0` (verified from the session runtime metadata).
- **Models**: `gpt-6-luna` for the initial review and README edits; `gpt-6.1-sol` for provenance completion and commit preparation (verified from turn metadata).
- **Authorship**: AI-assisted documentation under Fred's direction.
- **Commit**: The commit containing this record also contains the README corrections; use `git log -- docs/ai/2026-11-13-documentation-consistency.md` to locate it.
- **Transcript**: Retained privately by the author.

## Guiding prompts

> Examine the Tamlinux repos. We have a couple private ones and several public ones. Look for any inconsistencies in the READMEs, ROADMAPs, and other documents that we should fix. Make a plan for doing that.

> Implement the plan.

> commit

> Fix the problem that this message indicates:
>
> I did not commit the ecosystem README change. The required provenance guide referenced by the skill was missing at the expected path, and public commits require verified provenance records and trailers. That change remains uncommitted in ecosystem-fred-tamlinux.

## Changes and verification

- Describe the Omarchy patch directory as historical, consistent with the recorded retirement, and identify Hyprland/Quickshell as the current desktop with Sway planned for later.
- Add this session record and index it in the provenance overview and archive.
- Documentation only; reviewed the diff and checked provenance for private identifiers and broken relative links. No runtime tests were needed.
